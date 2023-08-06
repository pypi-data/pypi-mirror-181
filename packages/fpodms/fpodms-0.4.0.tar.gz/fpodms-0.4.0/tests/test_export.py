import os

import pytest

from fpodms import Client
from fpodms.export import ExportFile


@pytest.fixture(scope="module")
def fp():
    yield Client(
        email_address=os.getenv("FPODMS_EMAIL_ADDRESS"),
        password=os.getenv("FPODMS_PASSWORD"),
    )


def test_fpc_assessments_by_district_and_year(fp):
    export = fp.export.fpc_assessments_by_district_and_year()

    assert isinstance(export, ExportFile)
    assert isinstance(export.data, str)


def test_assessments_by_district_and_year(fp):
    export = fp.export.assessments_by_district_and_year()

    assert isinstance(export, ExportFile)
    assert isinstance(export.data, str)


def test_intervention_records_by_district_and_year(fp):
    export = fp.export.intervention_records_by_district_and_year()

    assert isinstance(export, ExportFile)
    assert isinstance(export.data, str)
