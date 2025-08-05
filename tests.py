import unittest
from fastapi.testclient import TestClient
from functions.get_db import get_db
from main import app

client = TestClient(app)
ALIAS = "heisenberg"
URL = "https://www.savewalterwhite.com"

class Tests(unittest.TestCase):
    # get_db
    def test_get_db(self):
        data = get_db()
        self.assertIsNotNone(data)
        (con,cur) = data
        self.assertIsNotNone(con.cursor)
        self.assertIsNotNone(cur.execute)

    def health(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == { "status": "healthy" }

    def test_no_redirect(self):
        response = client.get(f"/{ALIAS}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })

    def test_not_found(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })

    def test_shorten(self):
        response = client.put("/api/shorten", params={"alias": ALIAS, "url": URL})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['short_url'], "https://url.beckham.io/heisenberg")
        self.assertEqual(response.json()['alias'], "heisenberg")
        self.assertEqual(response.json()['url'], "https://www.savewalterwhite.com")

    def test_is_found(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_redirect(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_shorten_override(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_delete(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_still_not_found(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_still_no_redirect(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })
        
    def test_double_delete(self):
        response = client.get("/api/read", params={"alias_id": ALIAS})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { "detail": "Alias not found" })

if __name__ == "__main__":
    unittest.main()
