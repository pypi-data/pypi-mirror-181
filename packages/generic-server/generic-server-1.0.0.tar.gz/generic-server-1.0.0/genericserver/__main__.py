"""Module to run MockServer."""

from .mockserver import MockServer
import argparse


def getCommandlineArguments():
    parser = argparse.ArgumentParser(description="Run a MockServer",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("protocol", help="Protocol to use. Either 'udp' (default) or 'tcp'.")
    parser.add_argument("responder", help="Responder to use. Either 'reflect', 'ok', or 'manual'.")
    return parser.parse_args()


def main():
    """
    Starts the MockServer.
    """
    args = getCommandlineArguments()
    my_server = MockServer(protocol=args.protocol, responder=args.responder)
    my_server.run()

    
