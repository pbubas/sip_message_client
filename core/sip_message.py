from dataclasses import dataclass
from .sip_server_response import SipServerResponse

import socket
import random
import string
import uuid
from hashlib import md5,sha256

@dataclass()
class SipClient:
    ip: str
    port: int
    user: str
    password: str

    def __post_init__(self):
        self.message = SipMessage(self)


class SipMessage:
    def __init__(
        self,
        sip_server: SipClient,
    ):
        self.sip_server = sip_server

    def send(self, destination_number: str, message_text: str):
        self.message_text = message_text
        self.to = destination_number 
        self.my_ip = "0.0.0.0"
        self.my_port = 5060

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sip_server_udp:
            self._set_branchid()
            self._set_tag()
            self._set_callid()
            self.counter=1

            self._build_message()
            sip_server_udp.sendto(self.request, (self.sip_server.ip, self.sip_server.port))
            response_data, address = sip_server_udp.recvfrom(1024)
            self.response = SipServerResponse.decode(response_data)
            self.my_port = self.response.header['Via']['rport']
            self.my_ip = self.response.header['Via']['received']

            self.counter+=1
            self._build_message(self.response.header['WWW-Authenticate'])
            sip_server_udp.sendto(self.request, (self.sip_server.ip, self.sip_server.port))
            response_data, address = sip_server_udp.recvfrom(1024)
            self.response = SipServerResponse.decode(response_data)
            return self.response

    def _build_message(self, www_authenticate=None):
        header = dict()
        method = f'MESSAGE sip:{self.to}@{self.sip_server.ip};transport=UDP SIP/2.0'
        header = {
            'Via': f'SIP/2.0/UDP {self.my_ip}:{self.my_port};branch={self.branchid};rport',
            'Max-Forwards': f'70',
            'To': f'<sip:{self.to}@{self.sip_server.ip};transport=UDP>',
            'From': f'<sip:{self.sip_server.user}@{self.sip_server.ip};transport=UDP>;tag={self.tag}',
            'Call-ID': f'{self.call_id}',
            'CSeq': f'{self.counter} MESSAGE',
            'Allow': 'INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE',
            'Content-Type': 'text/plain',
            'User-Agent': 'SipSmsMessage',
            'Allow-Events': 'presence, kpml, talk ',
            'Content-Length': f'{len(self.message_text)}'
        }
        if www_authenticate:
            header['Authorization'] = self._build_authorization(www_authenticate)
        request = method + '\r\n'
        request = request + '\r\n'.join(f'{k}: {v}' for k,v in header.items())
        request = request + '\r\n' + self.message_text
        self.method = method
        self.header = header
        self.request = request.encode()

    def _build_authorization(self, www_authenticate):
        nonce = www_authenticate['nonce'].strip('"')
        realm = www_authenticate['realm'].strip('"')
        algorithim = www_authenticate['Digest algorithm']
        hash1 = md5(f'{self.sip_server.user}:{realm}:{self.sip_server.password}'.encode('utf-8')).hexdigest()
        hash2 = md5(f'MESSAGE:sip:{self.sip_server.ip};transport=UDP'.encode('utf-8')).hexdigest()
        response = md5(f'{hash1}:{nonce}:{hash2}'.encode('utf-8')).hexdigest()
        return (
            f'Digest username="{self.sip_server.user}",'
            f'realm={realm},'
            f'nonce={nonce},'
            f'uri="sip:{self.sip_server.ip};transport=UDP",'
            f'response="{response}",'
            f'algorithm={algorithim}\r\n'
        )

    def _set_callid(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        call_id = ''.join(random.choice(characters) for i in range(24))
        self.call_id = call_id
        hash = sha256(str(self.call_id).encode("utf8"))
        hhash = hash.hexdigest()
        return f"{hhash[0:32]}@{self.my_ip}:{self.my_port}"

    def _set_branchid(self) -> str:
        branchid = uuid.uuid4().hex[: 25]
        self.branchid = f"z9hG4bK-{branchid}"

    def _set_tag(self):
        rand = str(random.randint(1, 4294967296)).encode("utf8")
        tag = md5(rand).hexdigest()[0:8]
        self.tag=tag