from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

import transaction


# - Server address and port - TaskdConnection call
# - Organization name -
# - User name
# - Password [secret]
# - Certificate [secret]
# - Key [secret]

# class TaskdConnection(object):

#     def __init__(self, host, port=53589, **kwargs):
#         pass
#     def connect(self):
# do we need this?
# self.cadata = getcadata()
#         self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
#         self.connection =  context.wrap_socket(socket.socket(socket.AF_INET))
#         self.connection.connect(self.host, self.port)



class TaskClient(Protocol):
    def sendMessage(self, msg):
        m = transaction.mk_message(org="public",user="jack",key="a69f8b68-5747-4ed3-af70-e891e9888fff")
        self.transport.write("Hello")


def got_protocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, "localhost", 53589)
d = connectProtocol(point, TaskClient())
d.addCallback(got_protocol)
reactor.run()
