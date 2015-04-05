class Status(object):
    # From https://git.tasktools.org/projects/TM/repos/taskd/browse/doc/protocol.txt
    # Taskserver Protocol v 1
    status_table = {
        200: "Success",
        201: "No change",
        300: "Deprecated message",
        301: "Redirect",
        302: "Retry",
        400: "Malformed data",
        401: "Unsupported encoding",
        420: "Server temporarily unavailable",
        421: "Server shutting down at operator request",
        430: "Access denied",
        431: "Account suspended",
        432: "Account terminated",
        500: "Syntax error in request",
        501: "Syntax error, illegal parameters",
        502: "Not implemented",
        503: "Command parameter not implemented",
        504: "Request too big",
    }

    def __init__(self, code):
        self.code = int(code)

    def __str__(self):
        return "Status: {} \nExplanation: {}".format(self.code, self.status_table[self.code])  # ok because of int use


class TaskdError(Status, Exception):
    pass
