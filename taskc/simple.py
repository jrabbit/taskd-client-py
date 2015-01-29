import ssl
import socket
import struct
import email

import transaction
import errors

c = ssl.create_default_context()
c.load_cert_chain("/home/jack/.task/jacklaxson.cert.pem", "/home/jack/.task/jacklaxson.key.pem")
c.load_verify_locations("/home/jack/.task/ca.cert.pem")
c.check_hostname = False
conn = c.wrap_socket(socket.socket(socket.AF_INET))
conn.connect(("192.168.1.110", 53589))
# print conn.getpeercert()
msg = transaction.mk_message("Public", "Jack Laxson", "f60bfcb9-b7b8-4466-b4c1-7276b8afe609")
msg['type'] = "statistics"
our_len = long(len(msg.as_string()) + 4)
size = struct.pack('>L', our_len)
# print size
conn.sendall(size+msg.as_string())
a = conn.recv(4096)
print struct.unpack('>L',a[:4])[0], "Byte Response"
resp = email.message_from_string(a[4:])
if 'code' in resp:
    print errors.Status(resp['code'])
    if int(resp['code']) >= 400:
        raise errors.Error(resp['code'])
print resp