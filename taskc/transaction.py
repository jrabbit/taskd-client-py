from email.message import Message

def mk_message(org, user, key):
    m = Message()
    m['client'] = "taskc-py 0.0.1a1"
    m['protocol'] = "v1"
    m['org'] = org
    m['user'] = user
    m['key'] = key
    return m

class Transaction(object):
    """ Each transaction is a single incoming message, with a single response
    message.  All communication therefore consists of a single 'send', followed
    by a single 'receive', then termination."""
    pass
