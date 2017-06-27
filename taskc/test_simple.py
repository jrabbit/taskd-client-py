import logging
import os
import time
import unittest
import uuid

import six
from docker import Client
from docker.errors import APIError
from taskc.simple import TaskdConnection

try:
    import unittest.mock as mock
except ImportError:
    import mock

logging.basicConfig(level=logging.INFO)

class TestRCParse(unittest.TestCase):

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

class TestConnectionUnit(unittest.TestCase):

    def setUp(self):
        self.tc = TaskdConnection()
        self.tc.server = "localhost"
        self.tc.group = "Public"
        self.tc.uuid = str(uuid.uuid4())
        self.tc.username = "test_user"
        self.tc.client_cert = "taskc/fixture/pki/client.cert.pem"
        self.tc.client_key = "taskc/fixture/pki/client.key.pem"
        self.tc.cacert_file = "taskc/fixture/pki/ca.cert.pem"

    @mock.patch("taskc.simple.TaskdConnection.recv")
    @mock.patch("taskc.simple.TaskdConnection.conn",  create=True)
    @mock.patch("taskc.simple.TaskdConnection._mkmsg")
    @mock.patch("taskc.simple.TaskdConnection._connect")
    def test_pull(self, tdc_connect, mk_msg, conn, recv):
        output = "timbo?"
        recv.return_value = output
        self.assertEqual(self.tc.pull(), output)
        tdc_connect.assert_called_with()
        mk_msg.assert_called_with('sync')

    @mock.patch("taskc.simple.TaskdConnection.recv")
    @mock.patch("taskc.simple.TaskdConnection.conn",  create=True)
    # @mock.patch("taskc.transaction.prep_message")
    @mock.patch("taskc.simple.TaskdConnection._connect")
    def test_put(self, tdc_connect, conn, recv):
        tasks = "{This is a task}\n{this is another task}"
        self.tc.put(tasks)
        # prep_msg.assert_
        tdc_connect.assert_called_with()



class TestConnection(unittest.TestCase):

    def setUp(self):
        # logging.basicConfig(level=logging.DEBUG)
        self.docker = Client(base_url='unix://var/run/docker.sock')
        # self.volume_name = "taskc_fixture_pki"
        try:
            self.docker.remove_container("taskc_test", force=True)
        except APIError as e:
            logging.error(e)
        # volume = self.docker.create_volume(self.volume_name)
        # logging.debug(volume)
        pki_abs_path = os.path.abspath("taskc/fixture/pki")
        host_config = self.docker.create_host_config(binds=['{}:/var/lib/taskd/pki'.format(pki_abs_path)],publish_all_ports=True)
        self.container = self.docker.create_container("jrabbit/taskd", volumes=["/var/lib/taskd/pki"], name="taskc_test", host_config=host_config)
        # print(self.container)
        self.docker.start(self.container["Id"])
        time.sleep(1)
        our_exec = self.docker.exec_create(self.container["Id"], "taskd add user Public test_user")
        self.tc = TaskdConnection()
        o = self.docker.exec_start(our_exec['Id'])
        logging.debug(o)
        #bytes
        our_uuid = o.split(b'\n')[0].split()[-1]
        if six.PY3:
            our_uuid = our_uuid.decode("utf8")
        self.tc.uuid = our_uuid
        logging.debug("Type of uuid: %s", type(self.tc.uuid))

        self.tc.server = "localhost"
        c = self.docker.inspect_container("taskc_test")
        
        self.tc.port = int(c['NetworkSettings']['Ports']['53589/tcp'][0]['HostPort'])
        # self.tc.uuid = os.getenv("TEST_UUID")
        self.tc.group = "Public"
        self.tc.username = "test_user"
        self.tc.client_cert = "taskc/fixture/pki/client.cert.pem"
        self.tc.client_key = "taskc/fixture/pki/client.key.pem"
        self.tc.cacert_file = "taskc/fixture/pki/ca.cert.pem"
        time.sleep(1)

    def test_connect(self):

        self.tc._connect()
        # print self.tc.conn.getpeername()
        self.assertEqual(self.tc.conn.getpeername(), ('127.0.0.1', self.tc.port))
        # make sure we're on TLS v2 per spec
        self.assertEqual(self.tc.conn.context.protocol, 2)
        self.tc.conn.close()
        # from IPython import embed
        # embed()

    def test_put(self):
        assert self.tc.uuid
        self.tc.put("")
        tasks = """{"description":"hang up posters","entry":"20141130T081652Z","status":"pending","uuid":"0037aa92-45e5-44a6-8f34-2f92989f173a"}
{"description":"make pb ramen","entry":"20141130T081700Z","status":"pending","uuid":"dd9b71db-f51c-4026-9e46-bb099df8dd3f"}
{"description":"fold clothes","entry":"20141130T081709Z","status":"pending","uuid":"d0f53865-2f01-42a8-9f9e-3652c63f216d"}"""
        resp = self.tc.put(tasks)
        self.assertEqual(resp.status_code, 200)
        # might not be correct depends on state of taskd

    def test_cadata(self):
        "This doesn't work in python2.7??"
        self.tc.cacert_file = False
        with open("taskc/fixture/pki/ca.cert.pem") as ca:
            self.tc.cacert = ca.read()
        self.tc._connect()
        # print self.tc.conn.getpeername()
        self.assertEqual(self.tc.conn.getpeername(), ('127.0.0.1', self.tc.port))
        # make sure we're on TLS v2 per spec
        self.assertEqual(self.tc.conn.context.protocol, 2)
        self.tc.conn.close()

    def tearDown(self):
        print(self.docker.logs(self.container['Id'], stdout=True, stderr=True))
        self.docker.remove_container(self.container['Id'], force=True)
        # self.docker.remove_volume(name=self.volume_name)

# class TestStringIO(unittest.TestCase):
#     def setUp(self):
#         self.tc = TaskdConnection()
#         self.tc.server = "localhost"
#         self.tc.port = 53589
#         self.tc.uuid = os.getenv("TEST_UUID")
#         self.tc.group = "Public"
#         self.tc.username = "test_user"
#         self.tc.client_cert = "taskc/fixture/pki/client.cert.pem"
#         self.tc.client_key = "taskc/fixture/pki/client.key.pem"
#         self.tc.cacert_file = "taskc/fixture/pki/ca.cert.pem"

if __name__ == '__main__':
    unittest.main()
