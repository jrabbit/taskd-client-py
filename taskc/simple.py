import ssl
import socket
import struct

import transaction

c = ssl.create_default_context()
c.load_cert_chain("/home/jack/.task/jacklaxson.cert.pem", "/home/jack/.task/jacklaxson.key.pem")
c.load_verify_locations("/home/jack/.task/ca.cert.pem")
c.check_hostname = False
conn = c.wrap_socket(socket.socket(socket.AF_INET))
conn.connect(("192.168.1.110", 53589))
print conn.getpeercert()
msg = transaction.mk_message("Public", "Jack Laxson", "f60bfcb9-b7b8-4466-b4c1-7276b8afe609")
msg['type'] = "statistics"
our_len = long(len(msg.as_string()) + 4)
size = struct.pack('>L', our_len)
# print size
conn.sendall(size+msg.as_string())
print conn.recv(4096)