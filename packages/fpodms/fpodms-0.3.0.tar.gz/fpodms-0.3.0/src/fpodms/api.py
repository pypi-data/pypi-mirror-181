class API:
    def __init__(self, client):
        self._client = client

    def all_years(self, is_north_hemisphere=None):
        if is_north_hemisphere is None:
            is_north_hemisphere = self._client.user.is_northern_hemisphere

        return self._client._request(
            method="GET",
            path="api/year/getall",
            params={"isNorthHemisphere": is_north_hemisphere},
        )

    def school_by_district(self, district_id=None, school_year_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        return self._client._request(
            method="GET",
            path=f"api/school/GetByDistrict/{district_id}",
            params={"schoolYearId": school_year_id},
        )

    def basclass_by_school(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        return self._client._request(
            method="GET",
            path=f"api/class/GetBySchool/{school_id}",
            params={"schoolYearId": school_year_id},
        )

    def students_by_school_and_school_year(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        return self._client._request(
            method="GET",
            path="api/school/GetStudentsBySchoolAndSchoolYear",
            params={
                "schoolId": school_id,
                "schoolYear": school_year_id,
            },
        )

    def grade_by_school(self, school_id, in_use_only=True):
        return self._client._request(
            method="GET",
            path=f"api/grade/GetBySchool/{school_id}",
            params={"inUseOnly": in_use_only},
        )

    def student_school_years_and_classes(self, student_id):
        return self._client._request(
            method="GET",
            path="api/student/GetStudentSchoolYearsAndClasses",
            params={"studentId": student_id},
        )

    def add_student(self, **kwargs):
        return self._client._request(
            method="POST",
            path="api/student/AddStudent",
            data={
                "student": {
                    "firstName": kwargs.get("firstName"),
                    "lastName": kwargs.get("lastName"),
                    "studentIdentifier": kwargs.get("studentIdentifier"),
                },
                "studentSchoolYear": {
                    "schoolYearId": kwargs.get("schoolYearId"),
                    "schoolId": kwargs.get("schoolId"),
                    "gradeId": kwargs.get("gradeId"),
                },
                "classStudent": {
                    "classId": kwargs.get("classId"),
                    "fpcclassId": kwargs.get("fpcclassId"),
                    "groupId": kwargs.get("groupId"),
                },
            },
        )

    def add_student_to_school_and_grade_and_maybe_class(self, **kwargs):
        return self._client._request(
            method="POST",
            path="api/student/AddStudentToSchoolAndGradeAndMaybeClass",
            data={
                "studentId": kwargs.get("studentId"),
                "schoolYearId": kwargs.get("schoolYearId"),
                "schoolId": kwargs.get("schoolId"),
                "gradeId": kwargs.get("gradeId"),
                "classStudentStartDate": kwargs.get("classStudentStartDate"),
                "classStudentEndDate": kwargs.get("classStudentEndDate"),
                "active": kwargs.get("active", True),
                "classId": kwargs.get("classId"),
                "className": kwargs.get("className"),
                "classStartDate": kwargs.get("classStartDate"),
                "classEndDate": kwargs.get("classEndDate"),
                "schoolLunchProgram": kwargs.get("schoolLunchProgram", False),
                "specialEducationServices": kwargs.get(
                    "specialEducationServices", False
                ),
                "additionalReadingServices": kwargs.get(
                    "additionalReadingServices", False
                ),
                "otherServicesPrograms": kwargs.get("otherServicesPrograms", False),
                "otherServicesDescription": kwargs.get("otherServicesDescription"),
                "calendar": {
                    "sortComprehension": kwargs.get("sortComprehension", {}),
                    "loadingHelper": kwargs.get("loadingHelper", {}),
                    "isReady": kwargs.get("isReady", True),
                    "start": kwargs.get("start", {}),
                    "end": kwargs.get("end", {}),
                    "holidays": kwargs.get("holidays", []),
                },
            },
        )

    def move_students(
        self,
        source_school_id,
        destination_school_id,
        *args,
        **kwargs,
    ):
        return self._client._request(
            method="POST",
            path="api/student/MoveStudents",
            params={
                "sourceSchoolId": source_school_id,
                "destinationSchoolId": destination_school_id,
                "sourceSchoolYearId": kwargs.get("source_school_year_id")
                or self._client.preferences.year,
                "destinationSchoolYearId": kwargs.get("destination_school_year_id")
                or self._client.preferences.year,
            },
            data=args,
        )
