from decimal import Decimal

import pytest

from andreani.core.api import SDK
from andreani.core.utils import Address, Order, Person, Shipment


@pytest.fixture
def username():
    return "usuario_test"


@pytest.fixture
def password():
    return "DI$iKqMClEtM"


@pytest.fixture
def sdk():
    return SDK(sandbox=True)


@pytest.fixture
def simple_order():
    return Order(
        price=Decimal(1),
        weight=Decimal(1),
        width=Decimal(1),
        height=Decimal(1),
        length=Decimal(1),
    )


@pytest.fixture
def person():
    return Person(
        first_name="Juan",
        last_name="Perez",
        email="juanp@gmail.com",
        document_number="40249081",
        phone_number="+543513840242",
    )


@pytest.fixture
def address():
    return Address(
        postalcode="5000",
        street="Av Falsa",
        number="1400",
        apartment="B",
        floor="5",
        region="Capital",
        province="J",
        country="AR",
    )


@pytest.fixture
def shipment(person, address, simple_order):
    return Shipment(
        "400006711",
        person,
        address,
        person,
        address,
        simple_order,
    )


@pytest.fixture
def example_url():
    return "https://apisqa.andreani.com/v2/ordenes-de-envio/API0000000948168/etiquetas?bulto=1"
