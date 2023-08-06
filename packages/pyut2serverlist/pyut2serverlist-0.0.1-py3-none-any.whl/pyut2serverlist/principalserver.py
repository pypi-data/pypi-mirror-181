import socket
import struct
from hashlib import md5
from typing import List

from .connection import Connection
from .exceptions import AuthError
from .packet import Packet
from .server import Server
from .utils import pack, unpack, int_to_ip


class PrincipalServer:
    address: str
    port: int
    cd_key: bytes

    connection: Connection
    authenticated: bool

    def __init__(self, address: str, port: int, cd_key: str, timeout: float = 2.0):
        self.address = address
        self.port = port
        self.cd_key = cd_key.encode()
        self.connection = Connection(self.address, self.port, protocol=socket.SOCK_STREAM, timeout=timeout)
        self.authenticated = False

    def authenticate(self) -> None:
        challenge = self.connection.read()

        challenge_response = self.build_auth_packet(self.cd_key, unpack(challenge.body))
        self.connection.write(challenge_response)

        approval = self.connection.read()
        if unpack(approval.body) != b'APPROVED':
            # TODO Raise different error/change message when principal returns "UNKNOWN_CDKEY"
            raise AuthError('Authentication failed')

        self.connection.write(Packet.build(pack(b"0014e800000000000000000000000000")))

        verification = self.connection.read()
        if unpack(verification.body) != b'VERIFIED':
            raise AuthError('Authentication failed')

        self.authenticated = True

    def get_servers(self) -> List[Server]:
        if not self.authenticated:
            self.authenticate()

        # TODO Implement filters
        # Just get all servers with a non-empty gametype for now (should be all servers)
        query_packet = Packet.build(b'\x00\x01\tgametype\x00\x01\x00\x04')
        self.connection.write(query_packet)

        result = self.connection.read()
        num_servers, *_ = struct.unpack("<IB", result.body)

        servers = []
        for _ in range(num_servers):
            server_packet = self.connection.read()
            packed_ip, game_port, query_port = struct.unpack("<IHH", server_packet.body[:8])
            servers.append(Server(int_to_ip(packed_ip), game_port, query_port))

        return servers

    @staticmethod
    def build_auth_packet(cd_key: bytes, challenge: bytes) -> Packet:
        cd_key_hash = md5(cd_key).hexdigest()
        challenge_response_hash = md5(cd_key + challenge).hexdigest()

        # TODO Figure out meaning of additional data, see https://github.com/chc/openspy-core-v2/blob/cf248cdf01c8fb78c679d2c0c32795eb054659c5/code/utmaster/server/commands/handle_challenge.cpp#L11
        data = b"%s%s%s)\r\x00\x00\x05%s\x16\x04\x00\x00\x86\x80\x00\x00\x18\x00\x00\x00\x00" % tuple(
            map(pack, [cd_key_hash.encode(), challenge_response_hash.encode(), b"UT2K4CLIENT", b"int"]))
        return Packet.build(data)
