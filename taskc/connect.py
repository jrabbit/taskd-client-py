import ssl
# - Server address and port - TaskdConnection call
# - Organization name - 
# - User name
# - Password [secret]
# - Certificate [secret]
# - Key [secret]
class TaskdConnection(object):

    def __init__(self, host, port=53589, **kwargs):
        pass
    def connect(self):
        # do we need this?
        # self.cadata = getcadata()
        self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        self.connection =  context.wrap_socket(socket.socket(socket.AF_INET))
        self.connection.connect(self.host, self.port)
