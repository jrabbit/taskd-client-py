import ssl
import socket
import struct
import email
import os.path

import transaction
import errors

def connect(client_cert, client_key, server, port=53589, cacert=None):
    c = ssl.create_default_context()
    print client_cert, client_key, server, port, cacert
    c.load_cert_chain(client_cert, client_key)
    if cacert:
        c.load_verify_locations(cacert)
    c.check_hostname = False
    conn = c.wrap_socket(socket.socket(socket.AF_INET))
    conn.connect((server, port))
    return conn

def from_taskrc():
    conf = dict([x.replace("\\/", "/").strip().split('=') for x in open(
        os.path.expanduser("~/.taskrc")).readlines() if '=' in x and x[0] != "#"])
    #TODO parse out credentials
    return connect(client_cert=conf['taskd.certificate'],
        client_key=conf['taskd.key'],
        server=conf['taskd.server'].split(":")[0],
        port=int(conf['taskd.server'].split(":")[1]),
        cacert=conf['taskd.ca'] if 'taskd.ca' in conf else None,
        )
def manual():
    # Task 2.3.0 doesn't let you have a cacert if you enable trust
    return connect(client_cert="/home/jack/.task/jacklaxson.cert.pem",
        client_key="/home/jack/.task/jacklaxson.key.pem",
        cacert="/home/jack/.task/ca.cert.pem",
        server="192.168.1.110",
        )
# print conn.getpeercert()
conn = manual()
msg = transaction.mk_message("Public", "Jack Laxson", "f60bfcb9-b7b8-4466-b4c1-7276b8afe609")
msg['type'] = "statistics"
our_len = long(len(msg.as_string()) + 4)
size = struct.pack('>L', our_len)
conn.sendall(size+msg.as_string())

a = conn.recv(4096)
print struct.unpack('>L',a[:4])[0], "Byte Response"

resp = email.message_from_string(a[4:])
if 'code' in resp:
    # print errors.Status(resp['code'])
    if int(resp['code']) >= 400:
        raise errors.Error(resp['code'])
print resp