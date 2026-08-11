from tests.utils.products import create_product, create_product_list
from tests.utils.auth import create_autenticate_user

def test_list_products_should_return_200(client):
    response = client.get("/products")
    body = response.json()

    assert response.status_code == 200
    assert body["data"] == []
    assert body["total"] == 0
    assert body["page"] == 1

def test_list_products_should_return_one_product(client, session):
    create_product(session)

    response = client.get("/products")

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Calabresa"

def test_should_return_second_page(client):
    response = client.get("/products?page=2")
    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) == 0
    assert body["page"] == 2
    assert body["limit"] == 10

def test_should_filter_products_by_name(client, session):
    create_product(session)

    response = client.get('products?calabresa')
    body = response.json()

    assert body["data"][0]["name"] == "Calabresa"

def test_should_get_by_id(client, session):
    create_product_list(session)

    response = client.get("/products/5")
    body = response.json()

    assert body["id"] == 5
    assert body["name"] == 'Calabresa'

def test_should_create_product(client, session):
    token = create_autenticate_user(session)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "name": "Calabresa",
        "ingredients": ["Molho", "Mussarela", "Calabresa", "Orégano"],
        "price": 53.90,
        "category": "TRADITIONAL",
        "is_popular": True,
        "available": True,
    }

    response = client.post('/products', json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    assert body['product']["name"] == "Calabresa"
    assert body['product']["price"] == 53.90
    assert body['product']["category"] == "TRADITIONAL"
    assert body['product']["is_popular"] is True
    assert body['product']["available"] is True

def test_should_filter_by_name_and_availability(client, session):
    create_product(
        session,
        name="Calabresa",
        available=True
    )

    create_product(
        session,
        name="Calabresa Especial",
        available=False
    )

    response = client.get(
        "/products?search=Calabresa&available=true"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Calabresa"

def test_should_return_404_when_product_does_not_exist(client):
    response = client.get("/products/999")

    assert response.status_code == 404

def test_should_return_422_when_product_id_is_invalid(client):
    response = client.get("/products/abc")

    assert response.status_code == 422

def test_should_not_create_product_without_authentication(client):
    payload = {
        "name": "Calabresa",
        "ingredients": ["Molho", "Mussarela", "Calabresa"],
        "price": 53.90,
        "category": "TRADITIONAL",
        "is_popular": True,
        "available": True,
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 401

def test_should_not_create_product_with_invalid_token(client):
    headers = {
        "Authorization": "Bearer token-invalido"
    }

    payload = {
        "name": "Calabresa",
        "ingredients": ["Molho", "Mussarela", "Calabresa"],
        "price": 53.90,
        "category": "TRADITIONAL",
        "is_popular": True,
        "available": True,
    }

    response = client.post(
        "/products",
        json=payload,
        headers=headers
    )

    assert response.status_code == 401

def test_should_not_create_product_without_name(client, session):
    token = create_autenticate_user(session)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "ingredients": ["Molho", "Mussarela"],
        "price": 53.90,
        "category": "TRADITIONAL",
        "is_popular": True,
        "available": True,
    }

    response = client.post(
        "/products",
        json=payload,
        headers=headers
    )

    assert response.status_code == 422