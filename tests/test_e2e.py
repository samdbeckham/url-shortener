import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app, follow_redirects=False)
ALIAS = "heisenberg"
URL = "https://www.savewalterwhite.com"

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == { "status": "healthy" }

def test_no_redirect():
    response = client.get(f"/{ALIAS}")
    assert response.status_code == 404
    assert response.json() == { "detail": "Alias not found" }

def test_not_found():
    response = client.get("/api/read", params={"alias_id": ALIAS})
    assert response.status_code == 404
    assert response.json() == { "detail": "Alias not found" }

def test_shorten():
    response = client.put("/api/shorten", params={"alias": ALIAS, "url": URL})
    assert response.status_code == 200
    assert response.json()['short_url'] == f"https://url.beckham.io/{ALIAS}"
    assert response.json()['alias'] == ALIAS
    assert response.json()['url'] == URL

def test_is_found():
    response = client.get("/api/read", params={"alias_id": ALIAS})
    assert response.status_code == 200
    assert response.json()['alias'] == ALIAS
    assert response.json()['url'] == URL

def test_redirect():
    response = client.get(f"{ALIAS}")
    assert response.status_code == 302
    assert response.headers["location"] == URL

def test_shorten_override():
    pass

def test_delete():
    pass

def test_still_not_found():
    pass

def test_still_no_redirect():
    pass

def test_double_delete():
    pass

