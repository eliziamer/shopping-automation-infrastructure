import allure
import pytest

from data.api.students_api_data import *
from extensions.api_verifications import APIVerify
from extensions.ui_actions import CONFIG
from utils.common_ops import load_csv_data
from workflows.api.students_api_flows import StudentsApiFlows   

class TestStudentsAPI:

    @allure.title("Verify list of students")
    @allure.description("Verify that the API returns a list of students with the expected status code.")
    def test01_verify_list_students(self, students_flows:StudentsApiFlows):
        APIVerify.status_code(students_flows.get_students_list(), EXPECTED_STATUS_SUCCESS_CODE)
 

    @allure.title("Verify total number of students")
    @allure.description("Verify that the total number of students returned by the API matches the expected total.")
    def test02_verify_total_students(self,students_flows:StudentsApiFlows):
        APIVerify.check_total_students(students_flows.get_calculate_total_students(),EXPECTED_TOTAL_STUDENTS)

    @allure.title("Verify total number of students using Gemini")
    @allure.description("Verify student count using API and Gemini AI")
    def test03_verify_total_students_using_ai(self, students_flows: StudentsApiFlows):
        students_flows.verify_total_students_with_gemini(EXPECTED_TOTAL_STUDENTS)

    @allure.title("Verify courses for each student")
    @allure.description("Verify that the API returns at least one course for each student.")
    def test04_verify_courses_are_displayed(self, students_flows: StudentsApiFlows):
        APIVerify.check_courses_is_not_empty(students_flows.show_courses())

    @allure.title("Verify student IDs are unique")
    @allure.description("Verify that the list of student IDs returned by the API contains unique values.")
    def test05_verify_id_is_unique(self,students_flows:StudentsApiFlows):
        APIVerify.check_unique_list(students_flows.get_id_list())

    @allure.title("Verify email format")
    @allure.description("Verify that the email addresses of students returned by the API are in a valid format.")
    def test06_verify_email_is_valid(self,students_flows:StudentsApiFlows):
        APIVerify.check_email_format(students_flows.get_email_list())

    @allure.title("Verify create student")
    @allure.description("Verify that creating a new student returns the expected status code.")
    def test07_verify_create_student(self,students_flows:StudentsApiFlows):
        APIVerify.check_status_create_student(students_flows.create_student(),EXPECTED_CREATE_STATUS_CODE)

    @allure.title("Verify update student")
    @allure.description("Verify that updating a student returns the expected status code.")
    def test08_verify_update_student(self,students_flows:StudentsApiFlows):
        APIVerify.check_status_update_student(students_flows.update_student(STUDENT_ID),EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Verify delete student")
    @allure.description("Verify that deleting a student returns the expected status code.")
    def test09_verify_delete_student(self,students_flows:StudentsApiFlows):
        APIVerify.check_delete_student(students_flows.delete_student_status(STUDENT_ID),EXPECTED_DELETE_STATUS_CODE)

    @allure.title("Verify email uniqueness")
    @allure.description("Verify that the email addresses of students returned by the API are unique.")
    def test10_verify_email_is_unique(self,students_flows:StudentsApiFlows):
        APIVerify.check_unique_list(students_flows.get_email_list())

    @allure.title("Verify courses uniqueness")
    @allure.description("Verify that the list of courses for each student returned by the API contains unique values.")
    def test11_verify_list_courses_is_unique(self,students_flows:StudentsApiFlows):
        APIVerify.check_unique_courses(students_flows.show_courses())

    @allure.title("Verify student details have parameters")
    @allure.description("Verify that the student details returned by the API contain the expected parameters.")
    def test12_verify_have_parameters(self,students_flows:StudentsApiFlows):
        APIVerify.check_student_details(students_flows.have_parameters())

    @pytest.mark.parametrize("data", load_csv_data(CONFIG["CSV_DATA_PATH"]))
    @allure.title("Verify student details have parameters with DDT")
    @allure.description("Verify that the student details returned by the API contain the expected parameters using DDT.")
    def test13_verify_students_fields_using_ddt(self,students_flows:StudentsApiFlows, data):
        response = students_flows.api.get(url="list")
        students_flows.validate_student_fields( response ,data)

    @allure.title("Verify getting removed student returns expected status code")
    @allure.description("Verify that attempting to get a removed student returns the expected error status code.")
    def test14_verify_get_removed_student(self,students_flows:StudentsApiFlows):
        APIVerify.assert_removed_student_status(students_flows.get_status_after_student_deletion(NORMAL_STUDENT_ID),EXPECTED_ERROR_STATUS_CODE)

    @allure.title("Verify updating a non-existent student")
    @allure.description("Verify that updating a student that doesn't exist returns the expected error status code.")
    def test15_verify_update_nonexistent_student_using_ai(self, students_flows: StudentsApiFlows):
        students_flows.verify_update_student_with_nonexistent_id_gemini(FAKE_STUDENT_ID)
    



   
    


        