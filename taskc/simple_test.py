import unittest
from simple import TaskdConnection


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.tc = TaskdConnection.from_taskrc("taskc/fixture/.taskrc")

    def test_rc(self):
        self.assertEqual(
            self.tc.client_cert, "/home/jack/.task/jacklaxson.cert.pem")
        self.assertEqual(
            self.tc.client_key, "/home/jack/.task/jacklaxson.key.pem")
        self.assertEqual(self.tc.cacert_file, "/home/jack/.task/ca.cert.pem")
        self.assertEqual(self.tc.server, "192.168.1.129")
        self.assertEqual(self.tc.port, 53589)
        self.assertEqual(self.tc.group, "Public")
        self.assertEqual(self.tc.username, "Jack Laxson")
        self.assertEqual(self.tc.uuid, "f60bfcb9-b7b8-4466-b4c1-7276b8afe609")

    def test_connect(self):

        self.tc.connect()
        self.assertEqual(self.tc.conn.getpeername(), ('192.168.1.129', 53589))
        # make sure we're on TLS v2 per spec
        self.assertEqual(self.tc.conn.context.protocol, 2)
        self.tc.conn.close()
        # from IPython import embed
        # embed()

    def test_put(self):
        self.tc.connect()
        self.tc.put("")
        self.tc.connect()
        tasks = """{"description":"hang up posters","entry":"20141130T081652Z","status":"pending","uuid":"0037aa92-45e5-44a6-8f34-2f92989f173a"}
{"description":"make pb ramen","entry":"20141130T081700Z","status":"pending","uuid":"dd9b71db-f51c-4026-9e46-bb099df8dd3f"}
{"description":"fold clothes","entry":"20141130T081709Z","status":"pending","uuid":"d0f53865-2f01-42a8-9f9e-3652c63f216d"}"""
        resp = self.tc.put(tasks)
        self.assertEqual(resp.status_code, 200)
                         #might not be correct depends on state of taskd


if __name__ == '__main__':
    unittest.main()
