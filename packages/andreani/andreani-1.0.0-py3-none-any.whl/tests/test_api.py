from decimal import Decimal

import pytest

from andreani.core.exceptions import AndreaniException
from andreani.core.utils import FeesResponse, LoginResponse


def test_login_successfully(username, password, sdk):
    auth = sdk.login(username, password)

    assert type(auth) == LoginResponse
    assert auth.token is not None


def test_login_unsuccessful(sdk):
    with pytest.raises(AndreaniException):
        sdk.login("abc", "fake")


def test_estimate_price(simple_order, sdk):
    fees = sdk.estimate_price(
        "1400",
        "300006611",
        "CL0003750",
        "BAR",
        simple_order,
    )

    assert type(fees) == FeesResponse
    assert fees.messured_weight == Decimal(1)


def test_estimate_price_unsuccessful(simple_order, sdk):
    with pytest.raises(AndreaniException):
        sdk.estimate_price(
            "1400",
            "",
            "",
            "BAR",
            simple_order,
        )


def test_submit_shipment(shipment, username, password, sdk):
    sdk.login(username, password)
    response = sdk.submit_shipment(shipment)
    print(response)
    assert response.status == "Pendiente"


def test_get_shipment_status(username, password, sdk):
    sdk.login(username, password)
    response = sdk.get_shipment_status("360000069614630")
    assert isinstance(response.status, str)


def test_get_label(username, password, sdk, example_url):
    sdk.login(username, password)
    response = sdk.get_label(example_url)
    assert response is not None
