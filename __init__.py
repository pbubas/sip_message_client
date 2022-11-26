from core.sip_message import SipServer
import logging
from sys import stdout

logging.basicConfig(level=logging.INFO, stream=stdout)
LOG = logging.getLogger()

if __name__ == "__main__":
    sip_server = SipServer("10.0.0.15", 5060, "sipuser", "password")
    response = sip_server.message.send("+48555222111", "test message")

    if response.ok: LOG.info ('message sent successfully')
