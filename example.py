from sip_message_client import SipClient
import logging

logging.basicConfig(level=logging.INFO)
logging = logging.getLogger()

if __name__ == "__main__":
    sip_client = SipClient("10.0.0.15", 5060, "sipuser", "password")
    response = sip_client.message.send("+48555222111", "test message")
