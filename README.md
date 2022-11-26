# sip_message
sip client to send message to asterisk

# example use

```python
sip_server = SipServer("10.0.0.15", 5060, "sipuser", "password")
response = sip_server.message.send("+48555222111", "test message")

if response.ok: LOG.info ('message sent successfully')
```
