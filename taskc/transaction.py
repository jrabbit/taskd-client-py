from email.message import Message
import struct
from errors import TaskdError

def mk_message(org, user, key):
    m = Message()
    m['client'] = "taskc-py 0.0.1a1"
    m['protocol'] = "v1"
    m['org'] = org
    m['user'] = user
    m['key'] = key
    return m

def prep_message(msg):
    """Add the size header"""
    our_len = len(msg.as_string()) + 4
    size = struct.pack('>L', our_len)
    return size+msg.as_string()


class Transaction(object):
    """ Each transaction is a single incoming message, with a single response
    message.  All communication therefore consists of a single 'send', followed
    by a single 'receive', then termination."""
    pass

class TaskdResponse(Message):

    """docstring for TaskdResponse"""
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

