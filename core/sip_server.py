from dataclasses import dataclass


@dataclass(frozen=True)
class SipServer:
    IP : str
    port : int
    user : str
    password : str

