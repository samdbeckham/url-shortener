import pytest
from fastapi.testclient import TestClient
from main import app
from functions.teardown import teardown

client = TestClient(app, follow_redirects=False)
ALIAS = "heisenberg"
URL = "https://www.savewalterwhite.com"

class TestE2E:
    @classmethod
    def teardown_class(cls):
        teardown()

    def test_health(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == { "status": "healthy" }

    def test_no_redirect(self):
        response = client.get(f"/{ALIAS}")
        assert response.status_code == 404
        assert response.json() == { "detail": "Alias not found" }

    def test_not_found(self):
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 404
        assert response.json() == { "detail": "Alias not found" }

    def test_shorten(self):
        response = client.put("/api/shorten", params={"alias": ALIAS, "url": URL})
        assert response.status_code == 200
        assert response.json()['short_url'] == f"https://url.beckham.io/{ALIAS}"
        assert response.json()['alias'] == ALIAS
        assert response.json()['url'] == URL

    def test_is_found(self):
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 200
        assert response.json()['alias'] == ALIAS
        assert response.json()['url'] == URL

    def test_redirect(self):
        response = client.get(f"{ALIAS}")
        assert response.status_code == 302
        assert response.headers["location"] == URL

    def test_shorten_override(self):
        response = client.put("/api/shorten", params={"alias": ALIAS, "url": URL})
        assert response.status_code == 409
        assert response.json() == { "detail": "Alias already exists" }

    def test_delete(self):
        response = client.delete("/api/delete", params={"alias": ALIAS})
        assert response.status_code == 200
        assert response.json() == { "detail": "Alias deleted" }

    def test_not_found_again(self):
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 404
        assert response.json() == { "detail": "Alias not found" }

    def test_no_redirect_again(self):
        response = client.get(f"/{ALIAS}")
        assert response.status_code == 404
        assert response.json() == { "detail": "Alias not found" }

    def test_double_delete(self):
        response = client.delete("/api/delete", params={"alias": ALIAS})
        assert response.status_code == 404
        assert response.json() == { "detail": "Alias not found" }


