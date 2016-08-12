import struct
import logging

from email.message import Message

import six

from taskc.errors import TaskdError
from taskc import __version__


def mk_message(org, user, key):
    """
    Make message
    """

    m = Message()
    m['client'] = "taskc-py {0}".format(__version__)
    m['protocol'] = "v1"
    m['org'] = org
    m['user'] = user
    m['key'] = key

    return m


def prep_message(msg):
    """
    Add the size header
    """
    if six.PY3:
        msg_out = msg.as_string().encode("utf-8")
    else:
        msg_out = msg.as_string()

    our_len = len(msg_out) + 4
    size = struct.pack('>L', our_len)
    # why the hell is this "bytes" on python3?

    return size + msg_out

class TaskdResponse(Message):

    """Represents a reponse of a taskd server"""

    def __init__(self):
        Message.__init__(self)

    @property
    def data(self):
        "front bit of payload"
        return self.get_payload().strip().split("\n")[:-1]

    @property
    def sync_key(self):
        "last bit of payload"
        return self.get_payload().strip().split("\n")[-1]

    @property
    def status_code(self):
        return int(self.get("code"))

    @property
    def status(self):
        return self.status_code

    def raise_for_status(self):
        "Ala requests"
        if 400 <= self.status_code < 600:
            raise TaskdError(self.status_code)

    def __str__(self):
        return "Response: %s" % self.get('status')
