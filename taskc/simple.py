import ssl
import socket
import struct
import email
import os.path
import logging

import transaction
import errors


class TaskdConnection(object):

    def __init__(self):
        self.port = 53589
        self.cacert_file = False
        self.cacert = False

    def from_taskrc(self, f="~/.taskrc"):
        "Set all the required variables from a taskrc file"
        conf = dict([x.replace("\\/", "/").strip().split('=') for x in open(
            os.path.expanduser(f)).readlines() if '=' in x and x[0] != "#"])
        self.client_cert = conf['taskd.certificate']
        self.client_key = conf['taskd.key']
        self.server = conf['taskd.server'].split(":")[-2]
        self.port = int(conf['taskd.server'].split(":")[-1])
        self.cacert_file = conf['taskd.ca'] if 'taskd.ca' in conf else None
        self.group, self.username, self.uuid = conf['taskd.credentials'].split("/")
        return self

    def connect(self):
        "Actually open the socket"
        c = ssl.create_default_context()
        c.load_cert_chain(self.client_cert, keyfile=self.client_key)
        if self.cacert_file:
            c.load_verify_locations(cafile=self.cacert_file)
        elif self.cacert:
            print self.cacert
            c.load_verify_locations(cadata=self.cacert)
        # enable for non-selfsigned certs
        # print conn.getpeercert()
        c.check_hostname = False
        self.conn = c.wrap_socket(socket.socket(socket.AF_INET))
        self.conn.connect((self.server, self.port))

    def recv(self):
        "Parse out the size header & read the message"
        a = self.conn.recv(4096)
        logging.info("%s Byte Response", struct.unpack('>L', a[:4])[0])
        logging.debug(a)
        resp = email.message_from_string(
            a[4:], _class=transaction.TaskdResponse)

        if 'code' in resp:
            # print errors.Status(resp['code'])
            if int(resp['code']) >= 400:
                print resp['code']
            if int(resp['code']) == 200:
                print "Status Good!"
        return resp

    def _mkmsg(self, ttype):
        msg = transaction.mk_message(self.group, self.username, self.uuid)
        msg['type'] = ttype
        return transaction.prep_message(msg)

    def stats(self):
        """Get some statistics from the server"""
        self.conn.sendall(self._mkmsg("statistics"))
        return self.recv()

    def pull(self):
        """Get all the tasks down from the server"""
        self.conn.sendall(self._mkmsg("sync"))
        return self.recv()

    def put(self, tasks):
        """Push all our tasks to server
           tasks - taskjson list
        """
        msg = transaction.mk_message(self.group, self.username, self.uuid)
        msg.set_payload(tasks)
        msg['type'] = 'sync'
        tx_msg = transaction.prep_message(msg)
        self.conn.sendall(tx_msg)
        return self.recv()

    def sync(self, sync_key):
        """Sync our tasks and server's, takes sync_key (uuid debounce from previous txn)"""
        pass

def manual():
    # Task 2.3.0 doesn't let you have a cacert if you enable trust
    tc = TaskdConnection()
    tc.client_cert = "/home/jack/.task/jacklaxson.cert.pem"
    tc.client_key = "/home/jack/.task/jacklaxson.key.pem"
    tc.cacert_file = "/home/jack/.task/ca.cert.pem"
    tc.server = "iceking.local"
    tc.group = "Public"
    tc.username = "foobar"
    tc.uuid = "730b7377-e548-4cd5-a6b4-5cdbc2696e85"
    return tc


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    taskd = manual()
    taskd.connect()
    print taskd.pull().as_string()
    from IPython import embed
    embed()