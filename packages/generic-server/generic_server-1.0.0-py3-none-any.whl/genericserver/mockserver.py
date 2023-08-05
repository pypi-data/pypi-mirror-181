"""The main MockServer class."""

from __future__ import absolute_import
from typing import Union

from .udpserver import UdpServer
from .tcpserver import TcpServer
from .responders import MockResponder
from .responders.reflector import Reflector
from .responders.okresponder import OkResponder
from .responders.manual import ManualResponder
from .responders.json_responder import JsonResponder


class MockServer:
    """
    Generic Server e.g. to use as a mock device in an integration test.
    """
    def __init__(self,
                 protocol: str = 'udp',
                 responder: Union[str, MockResponder] = 'reflect'):
        """
        Create a MockServer Object.

        Parameters
        ----------
        protocol:
            The protocol to use, Either 'udp' (default) or 'tcp'.
        responder:
            The responder to use. Either one of 'reflect' (default), 'ok', or
            'manual', or a MockResponder object.
        """
        server = {'udp': UdpServer,
                  'tcp': TcpServer}[protocol]

        if ".json" in responder:
            json_filename = responder
            responder = 'json'

        responders = {'reflect': Reflector,
                      'ok': OkResponder,
                      'manual': ManualResponder,
                      'json': JsonResponder}
        if responder in responders.keys():
            if responder == 'json':
                responder = responders[responder](json_filename)
            else:
                responder = responders[responder]()
        else:
            keys = str(list(responders.keys()))
            raise NotImplemented("Responder can't be any other type than string yet. Should be one of %s." % keys)
        self.server = server(responder=responder)

    def run(self):
        """
        Start the server.
        """
        self.server.run()

    def stop(self):
        """
        Stop the server.
        """
        self.server.stop()

    @property
    def is_running(self) -> bool:
        """
        Check if the server is running.

        Returns
        -------
            True if server is running, False otherwise.
        """
        return self.server.is_running
