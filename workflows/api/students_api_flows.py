import json
from urllib import response
import allure
from dotenv import load_dotenv
import os
from playwright.sync_api import APIRequestContext, APIResponse
from data.api.students_api_data import *
from extensions.api_actions import APIActions
from google import genai

from extensions.api_verifications import APIVerify
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class StudentsApiFlows:

    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)
    
    @allure.step("Get students list")
    def get_students_list(self):
        response = self.api.get(url="list")
        print(json.dumps(response.json(), indent=2))
        return response 
    
    @allure.step("Calculate total students")
    def get_calculate_total_students(self):
        response = self.api.get(url="list")
        total_students = len(response.json())
        print(f"\nTotal number of students: {total_students}")
        return total_students
    
    @allure.step("Get courses for each student")
    def show_courses(self):
        response = self.api.get(url="list")
        students = response.json()
        student_courses = {}  # key: student full name, value: courses list

        for student in students:
            full_name = f"{student['firstName']} {student['lastName']}"
            courses_list = student.get("courses", [])
            student_courses[full_name] = courses_list

            # אפשר להוסיף logging במקום print
            print(f"Student: {full_name}, Courses: {courses_list}")

        return student_courses

    @allure.step("Get list of student IDs")
    def get_id_list(self):
        response = self.api.get(url="list")
        students = response.json()
        ids = []
        print("\nStudent IDs:")
        for student in students:
            ids.append(student["id"])
        print(f"\nStudent IDs: {ids}")
        return ids

    @allure.step("Get list of student emails")
    def get_students_emails(self):
        response = self.api.get(url="list")
        students = response.json()
        return [student["email"] for student in students]
    
    @allure.step("Create a new student")
    def create_student(self):
        response = self.api.post(STUDENTS_BASE_URL,payload={
            "firstName": "Aviel",
            "lastName": "Levin",
            "email": "aviel.levin@example.com",
            "programme": "Computer Science",
            "courses": ["Java", "Python"]})
        return response

    @allure.step("Update a student")
    def update_student(self,student_id):
        response = self.api.put(F"{STUDENTS_BASE_URL}{student_id}", payload={
        "firstName": "Aviel",
        "lastName": "Levin",
        "email": "aviel.levin@example.com",
        "programme": "Computer Science",
        "courses": [
        "Java script",
        "C++",
        "Python"
        ]})
        status_update = response.status
        print(f"Update student response: {response.status}")
        return status_update

    @allure.step("Delete a student")
    def delete_student_status(self,student_id):
        #Known BUG - DELETE is not retruning reponse.json()
        response = self.api.delete(student_id,log_response=False)
        status_code = response.status
        print(f"Delete student response: {status_code}")
        return status_code
    
    @allure.step("Get list of student emails")
    def get_email_list(self):
        response = self.api.get(url="list")
        students = response.json()
        emails = []
        for student in students:
            emails.append(student["email"])
        print(f"\nStudent Emails: {emails}")
        return emails

    @allure.step("Check if student details have parameters")
    def have_parameters(self):
        return self.api.get(url="list")

    @allure.step("Check if getting removed student returns expected status code")
    def get_status_after_student_deletion(self,student_id):
        response = self.api.delete(f"{STUDENTS_BASE_URL}{student_id}",log_response=False)
        print(f"\nstatus: {response.status}")
        get_response = self.api.get(f"{STUDENTS_BASE_URL}{student_id}")
        student_status = get_response.status
        print(f"Get removed student status: {student_status}")
        return student_status

    @allure.step("Verify total students using Gemini Vision")
    def verify_total_students_with_gemini(self, expected: int):

        # קריאה ל-API
        response = self.api.get(url="list")
        students = response.json()

        # יצירת Gemini client
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        Here is a JSON list of students:

        {students}

        Count how many students are in the list.

        Expected number of students: {expected}

        Answer in this format:
        Count: <number>
        Match: Yes or No
        """

        response_ai = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response_ai.text

        print("Gemini response:")
        print(result)

        if "yes" not in result.lower():
            raise AssertionError(
                f"Gemini verification failed. Expected {expected} students."
            )


    @allure.step("Verify updating student with non-existent ID using Gemini AI validation")
    def verify_update_student_with_nonexistent_id_gemini(self, fake_student_id):

        # שליחת הבקשה ל-API
        response_status = self.update_student(fake_student_id)

        # הצגת הסטטוס בדוח
        allure.attach(
            str(response_status),
            name="API Response Status Code",
            attachment_type=allure.attachment_type.TEXT
        )

        # יצירת client ל-Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are given an API response status code.

        Response status: {response_status}

        Valid statuses are: 404.
        Verify if the response status is one of the valid statuses.

        Answer only in this format:
        Match: Yes or No
        """

        response_ai = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response_ai.text

        # שמירת תשובת ה-AI בדוח
        allure.attach(
            result,
            name="Gemini AI Verification Result",
            attachment_type=allure.attachment_type.TEXT
        )

        if "yes" not in result.lower():
            raise AssertionError(
                f"Gemini verification failed. Expected 404, got {response_status}"
            )

    
    
    def validate_student_fields(self,response, data):
        response = self.api.get(STUDENTS_BASE_URL)
        students = response.json()

        field = data["field"]
        expected_type = data["expected_type"]
        not_null = data["not_null"] == "True"
        APIVerify.verify_students_field(students,field,expected_type,not_null)