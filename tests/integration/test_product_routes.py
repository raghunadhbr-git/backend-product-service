def test_get_products(client):
    res = client.get("/api/angularProduct/get")
    assert res.status_code == 200
    assert isinstance(res.json, list)
