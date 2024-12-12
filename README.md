# sip_message
sip client to send message to asterisk

# example use

```python
sip_client = SipClient("10.0.0.15", 5060, "sipuser", "password")
response = sip_client.message.send("+48555222111", "test message")
```


# command line install
```
cmd/install_command_line.sh
```

# command line usage 
```
sip_message --server=10.0.0.15 --username=sipuser --password=password --recipient=+48555222111 --message="test message"`
```

