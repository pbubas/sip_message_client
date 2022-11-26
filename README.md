# sip_message
sip client to send message to asterisk

# example use

```python
sip_client = SipClient("10.0.0.15", 5060, "sipuser", "password")
response = sip_client.message.send("+48555222111", "test message")

if response.ok: LOG.info ('message sent successfully')
```
