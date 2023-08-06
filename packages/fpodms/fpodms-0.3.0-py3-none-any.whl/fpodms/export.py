import re

from dateutil import parser


class ExportFile:
    def __init__(self, http_response):
        self.filename = self.parse_filename(
            http_response.headers["Content-Disposition"]
        )
        self.filedate = self.parse_filedate(http_response.headers["Date"])
        self.data = self.clean_data(http_response.text)

    @staticmethod
    def parse_filename(content_disposition):
        filename_pattern = 'attachment; filename="(.*)"'
        filename_match = re.match(filename_pattern, content_disposition)
        return filename_match.group(1)

    @staticmethod
    def parse_filedate(date):
        date_parsed = parser.parse(date)
        return date_parsed.isoformat()

    @staticmethod
    def clean_data(data):
        """
        Export data has a text qualifier: ="{data}", this strips them out
        """
        regex_pattern = r'="([^\"]*)"'
        regex_replacement = r"\1"
        return re.sub(regex_pattern, regex_replacement, data)


class Export:
    def __init__(self, client):
        self._client = client
        self.all_exports = [
            self.fpc_assessments_by_district_and_year,
            self.assessments_by_district_and_year,
            self.intervention_records_by_district_and_year,
        ]

    def export(self, endpoint, year, district_id):
        export_response = self._client._request(
            method="GET",
            path=f"export/{endpoint}/{district_id}",
            params={"year": year},
            content_type=None,
        )
        return ExportFile(export_response)

    def fpc_assessments_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id

        if year is None:
            year = self._client.preferences.year

        return self.export(
            endpoint="FPCAssessmentsByDistrictAndYear",
            year=year,
            district_id=district_id,
        )

    def assessments_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id

        if year is None:
            year = self._client.preferences.year

        return self.export(
            endpoint="AssessmentsByDistrictAndYear", year=year, district_id=district_id
        )

    def intervention_records_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id

        if year is None:
            year = self._client.preferences.year

        return self.export(
            endpoint="InterventionRecordsByDistrictAndYear",
            year=year,
            district_id=district_id,
        )
