import json
import traceback
import unittest
import requests

class ClassName(unittest.TestCase):

    """
    Testcases for Category api
    """
    def setUp(self):
        self.headers = {'content-type': 'application/json'}

    def _process_post(self, category_id, category_name):
        request_data = {
            "id": category_id,
            "name": category_name,
        }
        try:
            response = requests.post(
                "http://127.0.0.1:5000/category/",
                data=json.dumps(request_data),
                headers=self.headers
            )
            print response.json()
            return response
        except:
            traceback.print_exc()
            return {}

    def test_basic_post(self):
        response = self._process_post(13, 'makeupdo')
        self.assertNotEqual(response.status_code,
                        201,
                        "Error code is correct")


if __name__ == "__main__":
    unittest.main()
