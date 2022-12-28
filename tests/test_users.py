import unittest
from . import database


class TestUsers(database.DatabaseAndClientConfig):
    def setUp(self) -> None:
        super(TestUsers, self).setUp()

    def tearDown(self) -> None:
        super(TestUsers, self).tearDown()

    def test_connection(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Hello to FastAPI Social Media App")

    def test_create_user(self) -> None:
        res = self.client.post('/users/',
                               json={"name": "masoud",
                                     "email": "masoud@gmail.com",
                                     "password": "masoud123"})
        print(res.json())
        self.assertEqual(res.status_code, 201)

    def test_login_user(self) -> None:
        _ = self.client.post('/users/',
                             json={"name": "masoud",
                                   "email": "masoud@gmail.com",
                                   "password": "masoud123"})
        res = self.client.post('/login',
                               data={"username": "masoud@gmail.com",
                                     "password": "masoud123"})
        self.assertEqual(res.status_code, 202)


if __name__ == '__main__':
    unittest.main()
