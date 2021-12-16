Private Chatter
===================

Private Chatter aims to provide an easy-to-use and easy-to-deploy, end-to-end encrypted anonymous chat service.


## How to run
```shell
python3 chat.py
```

Then open http://localhost:9999/

Before chatting, you need to set your username and chat room. Then share the chat room and your public key.
Other people should also set usernames and share their public keys.
You should copy other people's public keys over to your Endpoint's public key area


## Features
- [x] No registration
- [x] RSA based
- [x] No raw text passed to server
- [x] Persistent RSA keys and public keys