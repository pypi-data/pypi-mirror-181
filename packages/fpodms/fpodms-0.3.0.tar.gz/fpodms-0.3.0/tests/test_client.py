import os

from fpodms import Client


def test_client_init():
    fpodms = Client(
        email_address=os.getenv("FPODMS_EMAIL_ADDRESS"),
        password=os.getenv("FPODMS_PASSWORD"),
    )
    assert isinstance(fpodms, Client)
