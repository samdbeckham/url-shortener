from fastapi.testclient import TestClient
from main import app
from functions.teardown import teardown

ALIAS = "heisenberg"
URL = "https://www.savewalterwhite.com"

auth_headers = {"x-key": "TEST_KEY"}
wrong_auth_headers = {"x-key": "WRONG_KEY"}

client = TestClient(app, follow_redirects=False)


class TestNotAuthorized:
    def test_read_all(self):
        response = client.get("/api/read_all", headers=wrong_auth_headers)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_shorten(self):
        response = client.put("/api/shorten", headers=wrong_auth_headers)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_delete(self):
        response = client.delete("/api/delete", headers=wrong_auth_headers)
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


class TestNotAuthenticated:
    # NOTE:This tests for 403 instead of 401 due to a quirk in Fast API
    #     https://github.com/fastapi/fastapi/issues/10177
    def test_read_all(self):
        response = client.get("/api/read_all")
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}

    def test_shorten(self):
        response = client.put("/api/shorten")
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}

    def test_delete(self):
        response = client.delete("/api/delete")
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}


class TestE2E:
    @classmethod
    def teardown_class(cls):
        teardown()

    def test_health(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_read_all_empty(self):
        response = client.get("/api/read_all", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()["aliases"]) == 0

    def test_no_redirect(self):
        response = client.get(f"/{ALIAS}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Alias not found"}

    def test_not_found(self):
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 404
        assert response.json() == {"detail": "Alias not found"}

    def test_shorten_bad_url(self):
        response = client.put(
            "/api/shorten",
            params={"alias": ALIAS, "url": "notarealurl"},
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid URL"}

    def test_shorten(self):
        response = client.put(
            "/api/shorten", params={"alias": ALIAS, "url": URL}, headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["short_url"] == f"https://url.beckham.io/{ALIAS}"
        assert response.json()["alias"] == ALIAS
        assert response.json()["url"] == URL

    def test_read_all_one(self):
        response = client.get("/api/read_all", headers=auth_headers)
        first_result = response.json()["aliases"][0]
        assert response.status_code == 200
        assert len(response.json()["aliases"]) == 1
        assert first_result["alias"] == ALIAS
        assert first_result["url"] == URL
        assert first_result["visits"] == 0

    def test_redirect(self):
        response = client.get(f"{ALIAS}")
        assert response.status_code == 302
        assert response.headers["location"] == URL

    def test_is_found(self):
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 200
        assert response.json()["alias"] == ALIAS
        assert response.json()["url"] == URL
        assert response.json()["visits"] == 1

    def test_multiple_visits(self):
        client.get(f"{ALIAS}")
        client.get(f"{ALIAS}")
        client.get(f"{ALIAS}")
        client.get(f"{ALIAS}")
        response = client.get("/api/read", params={"alias": ALIAS})
        assert response.status_code == 200
        assert response.json()["alias"] == ALIAS
        assert response.json()["url"] == URL
        assert response.json()["visits"] == 5

    def test_shorten_no_alias(self):
        response = client.put("/api/shorten", params={"url": URL}, headers=auth_headers)
        alias = response.json()["alias"]
        assert response.status_code == 200
        assert len(response.json()["alias"]) == 8
        assert response.json()["url"] == URL
        assert response.json()["short_url"] == f"https://url.beckham.io/{alias}"

    def test_shorten_override(self):
        response = client.put(
            "/api/shorten", params={"alias": ALIAS, "url": URL}, headers=auth_headers
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Alias already exists"}

    def test_delete(self):
        response = client.delete(
            "/api/delete", params={"alias": ALIAS}, headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "Alias deleted"}

    def test_not_found_again(self):
        response = client.get(
            "/api/read", params={"alias": ALIAS}, headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Alias not found"}

    def test_no_redirect_again(self):
        response = client.get(f"/{ALIAS}", headers=auth_headers)
        assert response.status_code == 404
        assert response.json() == {"detail": "Alias not found"}

    def test_double_delete(self):
        response = client.delete(
            "/api/delete", params={"alias": ALIAS}, headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Alias not found"}
