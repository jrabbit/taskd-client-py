import unittest
import email
from transaction import TaskdResponse


class TestTaskdResponse(unittest.TestCase):

    def setUp(self):
        with open("taskc/fixture/taskdresponse.txt") as f:
            wire = f.read()
            self.resp = email.message_from_string(wire, _class=TaskdResponse)

    def test_properties(self):
        payload = [
            '{"description":"hang up posters","entry":"20141130T081652Z","status":"pending","uuid":"0037aa92-45e5-44a6-8f34-2f92989f173a"}',
            '{"description":"make pb ramen","entry":"20141130T081700Z","status":"pending","uuid":"dd9b71db-f51c-4026-9e46-bb099df8dd3f"}',
            '{"description":"fold clothes","entry":"20141130T081709Z","status":"pending","uuid":"d0f53865-2f01-42a8-9f9e-3652c63f216d"}',
            '{"description":"shower","entry":"20141130T134051Z","status":"pending","uuid":"1c21d262-a6a1-4f4a-ae40-09c468f931cd"}',
            '{"description":"make pb ramen","end":"20150222T223915Z","entry":"20141130T081700Z","modified":"20150222T223915Z","status":"completed","uuid":"dd9b71db-f51c-4026-9e46-bb099df8dd3f"}',
            '{"description":"fold clothes","end":"20150222T224002Z","entry":"20141130T081709Z","modified":"20150222T224002Z","status":"completed","uuid":"d0f53865-2f01-42a8-9f9e-3652c63f216d"}',
            '{"description":"foo","entry":"20150222T224145Z","status":"pending","uuid":"9fec62b7-9db5-478e-a54b-11c2c2531695"}',
            '{"description":"bar","entry":"20150222T224337Z","status":"pending","uuid":"7b51cc8e-845c-4666-99a5-fa2e4132dd1e"}',
            '{"description":"beep","entry":"20150222T224916Z","status":"pending","uuid":"0a459069-a8db-4b62-963c-f4719c4061eb"}',
            '{"description":"foo","end":"20150222T232658Z","entry":"20150222T224145Z","modified":"20150222T232658Z","status":"completed","uuid":"9fec62b7-9db5-478e-a54b-11c2c2531695"}',
            '{"description":"bar","end":"20150222T232838Z","entry":"20150222T224337Z","modified":"20150222T232838Z","status":"completed","uuid":"7b51cc8e-845c-4666-99a5-fa2e4132dd1e"}',
            '{"description":"make tests","entry":"20150322T054651Z","status":"pending","uuid":"90ddd596-5f49-44bd-9e45-b78ff3ca6eb8"}',
            '{"description":"AAA Batteries","entry":"20150327T202948Z","status":"pending","uuid":"f00dad17-8291-4939-9ecf-6fb426c811e1"}',
        ]

        self.assertEqual(
            self.resp.sync_key, "bdf5e970-e337-4023-9d28-ee85e2291b40")
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.resp.data, payload)

if __name__ == '__main__':
    unittest.main()
