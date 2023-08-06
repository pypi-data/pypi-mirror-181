import os

import pytest

from fpodms import Client

TEST_SCHOOL_ID = os.getenv("TEST_SCHOOL_ID")
TEST_STUDENT_ID = os.getenv("TEST_STUDENT_ID")


@pytest.fixture(scope="module")
def fp():
    yield Client(
        email_address=os.getenv("FPODMS_EMAIL_ADDRESS"),
        password=os.getenv("FPODMS_PASSWORD"),
    )


def test_all_years(fp):
    for is_north_hemisphere in [None, True, False]:
        data = fp.api.all_years(is_north_hemisphere=is_north_hemisphere)
        dict_keys = set().union(*(d.keys() for d in data))

        assert isinstance(data, list)
        assert dict_keys == {"id", "name"}


def test_school_by_district(fp):
    data = fp.api.school_by_district()
    dict_keys = set().union(*(d.keys() for d in data))

    assert isinstance(data, list)
    assert dict_keys == {
        "id",
        "name",
        "groupCount",
        "districtId",
        "studentCount",
        "fPCClassCount",
        "classCount",
        "schoolYearId",
    }


def test_basclass_by_school(fp):
    data = fp.api.basclass_by_school(school_id=TEST_SCHOOL_ID)
    dict_keys = set().union(*(d.keys() for d in data))

    assert isinstance(data, list)
    assert dict_keys == {
        "id",
        "name",
        "teacherUserId",
        "gradeName",
        "teacherFirstName",
        "classStartDate",
        "studentCount",
        "gradeId",
        "schoolId",
        "teacherLastName",
        "schoolYearId",
        "classEndDate",
        "teacherMiddleName",
    }


def test_students_by_school_and_school_year(fp):
    data = fp.api.students_by_school_and_school_year(school_id=TEST_SCHOOL_ID)
    dict_keys = set().union(*(d.keys() for d in data))

    assert isinstance(data, list)
    assert dict_keys == {
        "schoolId",
        "studentSchoolYearId",
        "firstName",
        "dateOfBirth",
        "middleName",
        "active",
        "gender",
        "studentId",
        "studentIdentifier",
        "lastName",
        "schoolYearId",
    }


def test_grade_by_school(fp):
    data = fp.api.grade_by_school(school_id=TEST_SCHOOL_ID)
    dict_keys = set().union(*(d.keys() for d in data))

    assert isinstance(data, list)
    assert dict_keys == {"gradeId", "gradeName"}


def test_student_school_years_and_classes(fp):
    data = fp.api.student_school_years_and_classes(student_id=TEST_STUDENT_ID)
    dict_keys = set().union(*(d.keys() for d in data))

    assert isinstance(data, list)
    assert dict_keys == {
        "gradeId",
        "englishLanguageLearner",
        "northernSchoolYearName",
        "schoolYearId",
        "classId",
        "otherServicesPrograms",
        "specialEducationServices",
        "classStudentEndDate",
        "schoolName",
        "additionalReadingServices",
        "studentSchoolYearId",
        "classStudentStartDate",
        "schoolLunchProgram",
        "primaryLanguageId",
        "otherServicesDescription",
        "schoolId",
        "southernSchoolYearName",
        "classStudentId",
        "gradeName",
        "className",
    }
