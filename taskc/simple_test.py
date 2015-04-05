import unittest
from simple import TaskdConnection


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.tc = TaskdConnection()

    def test_rc(self):
        self.tc.from_taskrc("taskc/fixture/.taskrc")

        self.assertEqual(
            self.tc.client_cert, "/home/jack/.task/jacklaxson.cert.pem")
        self.assertEqual(
            self.tc.client_key, "/home/jack/.task/jacklaxson.key.pem")
        self.assertEqual(self.tc.cacert, "/home/jack/.task/ca.cert.pem")
        self.assertEqual(self.tc.server, "192.168.1.112")
        self.assertEqual(self.tc.port, 53589)
        self.assertEqual(self.tc.group, "Public")
        self.assertEqual(self.tc.username, "Jack Laxson")
        self.assertEqual(self.tc.uuid, "f60bfcb9-b7b8-4466-b4c1-7276b8afe609")

    def test_connect(self):
        self.tc.from_taskrc("taskc/fixture/.taskrc")

        self.tc.connect()
        self.assertEqual(self.tc.conn.getpeername(), ('192.168.1.112', 53589))
        # make sure we're on TLS v2 per spec
        self.assertEqual(self.tc.conn.context.protocol, 2)

        # from IPython import embed
        # embed()

if __name__ == '__main__':
    unittest.main()
