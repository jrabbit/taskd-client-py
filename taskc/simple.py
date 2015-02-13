import ssl
import socket
import struct
import email
import os.path

import transaction
import errors


class TaskdConnection(object):
    def __init__(self):
        self.port = 53589
    
    def from_taskrc(self):
        conf = dict([x.replace("\\/", "/").strip().split('=') for x in open(
            os.path.expanduser("~/.taskrc")).readlines() if '=' in x and x[0] != "#"])
        self.client_cert=conf['taskd.certificate']
        self.client_key=conf['taskd.key']
        self.server=conf['taskd.server'].split(":")[0]
        self.port=int(conf['taskd.server'].split(":")[1])
        self.cacert=conf['taskd.ca'] if 'taskd.ca' in conf else None
        self.group, self.username, self.uuid = conf['taskd.credentials'].split("/")
    
    def connect(self):
        c = ssl.create_default_context()
        c.load_cert_chain(client_cert, client_key)
        if self.cacert:
            c.load_verify_locations(cacert)
        #enable for non-selfsigned certs
        # print conn.getpeercert()
        c.check_hostname = False
        self.conn = c.wrap_socket(socket.socket(socket.AF_INET))
        self.conn.connect((self.server, self.port))

    def stats(self):
        msg = transaction.mk_message(self.group, self.username, self.uuid)
        msg['type'] = "statistics"
        self.conn.sendall(transaction.prep_message(msg))
        return self.recv()

    def recv(self):
        a = conn.recv(4096)
        print struct.unpack('>L',a[:4])[0], "Byte Response"
        resp = email.message_from_string(a[4:])

        if 'code' in resp:
            # print errors.Status(resp['code'])
            if int(resp['code']) >= 400:
                raise errors.Error(resp['code'])
            if int(resp['code']) == 200:
                print "Status Good!"
        return resp

def manual():
    # Task 2.3.0 doesn't let you have a cacert if you enable trust
    return connect(client_cert="/home/jack/.task/jacklaxson.cert.pem",
        client_key="/home/jack/.task/jacklaxson.key.pem",
        cacert="/home/jack/.task/ca.cert.pem",
        server="192.168.1.110",
        )

# from IPython import embed
# embed()
if __name__ == '__main__':
    pass