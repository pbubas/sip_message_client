#!/usr/bin/env python3
import logging
import argparse
from sip_message_client import SipClient

logger = logging.getLogger(__name__)

def send_sip_message(server, port, username, password, recipient, message):
    sip_client = SipClient(server, port, username, password)
    response = sip_client.message.send(recipient, message)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send SIP messages from the command line.")
    parser.add_argument("--server", required=True, help="SIP server address")
    parser.add_argument("--port", default=5060, type=int, help="SIP server port")
    parser.add_argument("--username", required=True, help="SIP username")
    parser.add_argument("--password", required=True, help="SIP password")
    parser.add_argument("--recipient", required=True, help="Recipient phone number")
    parser.add_argument("--message", required=True, help="Message to send")

    args = parser.parse_args()

    response = send_sip_message(args.server, args.port, args.username, args.password, args.recipient, args.message)
    logger.info(f"Response: {response}")