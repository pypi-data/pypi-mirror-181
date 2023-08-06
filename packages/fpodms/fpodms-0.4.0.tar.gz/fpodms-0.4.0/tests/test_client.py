import os

import pytest

from fpodms import Client


@pytest.fixture(scope="module")
def fp():
    yield Client(
        email_address=os.getenv("FPODMS_EMAIL_ADDRESS"),
        password=os.getenv("FPODMS_PASSWORD"),
    )


def test_client_init(fp):
    assert isinstance(fp, Client)
