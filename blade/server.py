"""
Asyncio Telnet Server for Blade.
Implements RFC 854 Telnet option negotiation, line buffering, and concurrent sessions.
"""

import asyncio
import logging
import os
import signal
import sys
from typing import Set, Optional

from blade.engine import GameSession
from blade.terminal import RESET

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("blade.server")

# Telnet Command Constants (RFC 854)
IAC = b"\xff"
DONT = b"\xfe"
DO = b"\xfd"
WONT = b"\xfc"
WILL = b"\xfb"
SB = b"\xfa"
SE = b"\xf0"

OPT_ECHO = b"\x01"
OPT_SGA = b"\x03"       # Suppress Go Ahead
OPT_LINEMODE = b"\x22"  # Linemode
OPT_NAWS = b"\x1f"      # Negotiate About Window Size


class TelnetClient:
    """Manages telnet byte stream and line buffering for a connected client."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.peer = writer.get_extra_info("peername")
        self.closed = False
        self.line_buffer = bytearray()

    async def send_negotiation(self):
        """Sends initial Telnet negotiation options."""
        neg = (
            IAC + WILL + OPT_ECHO +
            IAC + WILL + OPT_SGA +
            IAC + DO + OPT_LINEMODE
        )
        self.writer.write(neg)
        await self.writer.drain()

    async def write_text(self, text: str):
        """Encodes and transmits text with CRLF line endings."""
        if self.closed or self.writer.is_closing():
            return
        try:
            normalized = text.replace("\r\n", "\n").replace("\n", "\r\n")
            self.writer.write(normalized.encode("utf-8", errors="replace"))
            await self.writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            self.closed = True

    async def read_line(self) -> Optional[str]:
        """Reads a line of input, processing backspaces and filtering Telnet IAC commands."""
        while not self.closed:
            try:
                char = await self.reader.read(1)
            except (ConnectionResetError, asyncio.CancelledError):
                self.closed = True
                return None

            if not char:
                self.closed = True
                return None

            # Check for IAC escape sequences
            if char == IAC:
                cmd = await self.reader.read(1)
                if cmd in (DO, DONT, WILL, WONT):
                    opt = await self.reader.read(1)
                    continue
                elif cmd == SB:
                    while True:
                        sub = await self.reader.read(1)
                        if not sub or sub == IAC:
                            sub2 = await self.reader.read(1)
                            if sub2 == SE:
                                break
                    continue
                else:
                    continue

            # Handle Enter (\r or \n)
            if char in (b"\r", b"\n"):
                if char == b"\r":
                    try:
                        next_char = await asyncio.wait_for(self.reader.read(1), timeout=0.01)
                        if next_char not in (b"\n", b"\0"):
                            self.line_buffer.extend(next_char)
                    except asyncio.TimeoutError:
                        pass

                self.writer.write(b"\r\n")
                await self.writer.drain()

                line = self.line_buffer.decode("utf-8", errors="replace").strip()
                self.line_buffer.clear()
                return line

            # Handle Backspace / Delete
            elif char in (b"\x08", b"\x7f"):
                if self.line_buffer:
                    self.line_buffer.pop()
                    self.writer.write(b"\x08 \x08")
                    await self.writer.drain()

            # Normal printable characters
            elif len(char) == 1 and (32 <= char[0] <= 126 or char[0] >= 160):
                self.line_buffer.extend(char)
                self.writer.write(char)
                await self.writer.drain()

        return None

    def close(self):
        self.closed = True
        try:
            self.writer.close()
        except Exception:
            pass


class BladeServer:
    """Asyncio TCP / Telnet game server."""

    def __init__(self, host: str = "0.0.0.0", port: int = 2323):
        self.host = host
        self.port = port
        self.active_sessions: Set[asyncio.Task] = set()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client = TelnetClient(reader, writer)
        peer = client.peer
        logger.info(f"New victim entered the Death House from {peer}")

        try:
            await client.send_negotiation()
            session = GameSession(writer=client.write_text, reader=client.read_line)
            await session.start()
        except (ConnectionResetError, asyncio.CancelledError):
            logger.info(f"Victim at {peer} disconnected prematurely.")
        except Exception as e:
            logger.error(f"Error handling session for {peer}: {e}", exc_info=True)
        finally:
            client.close()
            logger.info(f"Session finished for {peer}")

    async def start(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        logger.info(f"BLADE: The House of Severance is listening on {addrs}")
        logger.info(f"Connect via: telnet <host> {self.port}  or  nc <host> {self.port}")

        async with server:
            await server.serve_forever()


def run_server(host: str = "0.0.0.0", port: int = 2323):
    """Entry point to run the asyncio server."""
    port_env = os.environ.get("TELNET_PORT")
    if port_env:
        try:
            port = int(port_env)
        except ValueError:
            pass

    server = BladeServer(host=host, port=port)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("BLADE server terminated by administrator.")
