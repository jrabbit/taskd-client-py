from functools import wraps
import email
import logging
import os.path
import socket
import struct
import ssl

import attr
import six
from taskc import transaction

logger = logging.getLogger(__name__)


def _is_path(instance, attribute, s, exists=True):
    "Validator for path-yness"
    if not s:
        # allow False as a default
        return
    if exists:
        if os.path.exists(s):
            return
        else:
            raise OSError("path does not exist")
    else:
        # how do we tell if it's a path if it doesn't exist?
        raise TypeError("Not a path?")


@attr.s
class TaskdConnection(object):
    client_cert = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), type=str, default=None)
    client_key = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), type=str, default=None)
    cacert_file = attr.ib(validator=attr.validators.optional(_is_path), default=False)
    server = attr.ib(default=None)
    port = attr.ib(validator=attr.validators.instance_of(int), type=int, default=53589)
    cacert = attr.ib(default=False)
    group = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), type=str, default=None)
    username = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), type=str, default=None)
    uuid = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), type=str, default=None)

    def manage_connection(f):
        @wraps(f)
        def conn_wrapper(self, *args, **kwargs):
            self._connect()
            x = f(self, *args, **kwargs) # noqa
            self._close()
            return x
        return conn_wrapper

    @classmethod
    def from_taskrc(cls, taskrc="~/.taskrc", **kwargs):
        """
        Build a TaskdConnection from a taskrc file

        classmethod is used to allow inheritance

        taskrc: configuration file for taskwarrior

        kwargs: arguments to pass to the constructor of TaskdConnection
        """

        # Build TaskConnection object
        connection = cls(**kwargs)

        # Read the taskrc file to make a dict of attributes/values
        conf = dict([x.replace("\\/", "/").strip().split('=') for x in open(
            os.path.expanduser(taskrc)) if '=' in x and x[0] != "#"])

        # Set instance variables according to taskrc file
        connection.client_cert = os.path.expanduser(conf['taskd.certificate'])
        connection.client_key = os.path.expanduser(conf['taskd.key'])
        connection.server = conf['taskd.server'].split(":")[-2]
        connection.port = int(conf['taskd.server'].split(":")[-1])
        connection.cacert_file = os.path.expanduser(conf[
            'taskd.ca']) if 'taskd.ca' in conf else None
        connection.group, connection.username, connection.uuid = conf[
            'taskd.credentials'].split("/")

        return connection

    def _connect(self):
        """
        Actually open the socket
        """

        # Initialize an SSL context
        context = ssl.create_default_context()
        logger.info("Loading cert chain: %s, %s", self.client_cert, self.client_key)
        context.load_cert_chain(self.client_cert, keyfile=self.client_key)
        if self.cacert_file:
            logger.info("Loading CA cert: %s", self.cacert_file)
            context.load_verify_locations(cafile=self.cacert_file)
        elif self.cacert:
            logger.info("cacert: %s", self.cacert)
            if six.PY2:
                raise NotImplementedError

            logger.info("Got CA cert as data/string type: %s", type(self.cacert))
            context.load_verify_locations(cadata=self.cacert)

        # enable for non-selfsigned certs
        # print conn.getpeercert()
        context.check_hostname = False

        # create the socket
        self.conn = context.wrap_socket(socket.socket(socket.AF_INET))
        self.conn.connect((self.server, self.port))

    def recv(self):
        """
        Parse out the size header & read the message

        Returns :py:class:`taskc.transaction.TaskdResponse`
        """

        # receive data through the socket
        a = self.conn.recv(4)

        # Read the number of bytes of the message
        # ">L" is 4 bytes long in big endian
        bytes = struct.unpack('>L', a[:4])[0]
        # Read the message itself
        # This approach assumes taskd responses will not be paged
        chunks = []
        bytes_recd = 0
        while bytes_recd < bytes - 4:
            chunk = self.conn.recv(min(bytes - bytes_recd, 2048))
            if chunk == b'':
                logger.error("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        msg = b''.join(chunks)

        # logging data
        logger.info("%s Byte Response", bytes)
        logger.debug(msg)

        # parse the response
        if six.PY3:
            resp = email.message_from_bytes(msg, _class=transaction.TaskdResponse)
        else:
            resp = email.message_from_string(
                msg, _class=transaction.TaskdResponse)

        if 'code' in resp:
            if int(resp['code']) >= 400:
                logger.error("Status Bad! %s", resp['code'])
            if int(resp['code']) == 200:
                logger.info("Status Good!")

        return resp

    def _mkmsg(self, ttype):
        """
        Make message
        """

        msg = transaction.mk_message(self.group, self.username, self.uuid)
        msg['type'] = ttype

        return transaction.prep_message(msg)

    def _close(self):
        """
        Close the taskd connection when you're done!
        """
        self.conn.close()

    @manage_connection
    def stats(self):
        """
        Get some statistics from the server

        Returns :py:class:`taskc.transaction.TaskdResponse`

        """

        self.conn.sendall(self._mkmsg("statistics"))

        return self.recv()

    @manage_connection
    def pull(self):
        """
        Get all the tasks down from the server

        Returns :py:class:`taskc.transaction.TaskdResponse`
        """

        self.conn.sendall(self._mkmsg("sync"))

        return self.recv()

    @manage_connection
    def put(self, tasks):
        """
        Push all our tasks to server

        tasks: flat formatted taskjson according to spec

        Returns :py:class:`taskc.transaction.TaskdResponse`
        """
        msg = transaction.mk_message(self.group, self.username, self.uuid)
        # returns a email.message.Message
        logger.debug("email str: %s", msg.as_string())
        msg.set_payload(tasks)
        msg['type'] = 'sync'
        logger.debug("final email str: %s", msg.as_string())
        # logging.info(type(msg))
        tx_msg = transaction.prep_message(msg)
        self.conn.sendall(tx_msg)

        return self.recv()

    # def sync(self, sync_key):
    #     """
    #     Sync our tasks and server's, takes sync_key (uuid debounce from previous txn)
    #     """
    #     pass
