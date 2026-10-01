"""
Main entry point for BLADE: The House of Severance.
"""

import sys
import argparse
from blade.server import run_server


def main():
    parser = argparse.ArgumentParser(description="BLADE - Terminal Psychological Horror Telnet Game")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=2323, help="Port to listen on (default: 2323)")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
