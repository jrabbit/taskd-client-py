from email.message import Message
import struct

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
