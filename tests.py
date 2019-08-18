import pytest
from flask import jsonify
from mmf.app import create_app


def test_assert():
    assert True


@pytest.fixture
def client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()
    return client


def test_mmf_app(client):
    response = client.get('/mmf_app')
    assert response == jsonify(status="success")

