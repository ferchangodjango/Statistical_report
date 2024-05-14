import pytest
from app import app


def test_home_route():
    response=app.test_client().get('/')
    print()

test_home_route