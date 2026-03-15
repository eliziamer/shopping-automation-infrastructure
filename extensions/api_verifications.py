

from smart_assertions import soft_assert, verify_expectations

class APIVerify:
    @staticmethod
    def status_code(response, expected_status_code: int):
        """
        Verifies that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  # If it's already JSON, we can't check status
            raise ValueError("Expected a Playwright response object, but got a dictionary. Ensure status code is checked before calling .json()")
        assert response.status == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status}"
        

    @staticmethod
    def json_key_exists(response_data, key: str):
        """
        Verifies that a specific key exists in the JSON response.
        """
        assert key in response_data, f"Key '{key}' not found in the response JSON"

    
    @staticmethod
    def json_value_equals(response_data, key: str, expected_value):
        """
        Verifies that a specific key in the JSON response has the expected value.
        """
        assert response_data[key] == expected_value, (
            f"Expected value for key '{key}' is '{expected_value}', but got '{response_data[key]}'"
        )

    
    @staticmethod
    def json_contains(response_data, expected_data: dict):
        """
        Verifies that the JSON response contains the expected data.
        """
        for key, value in expected_data.items():
            assert key in response_data, f"Key '{key}' not found in the response JSON"
            assert response_data[key] == value, (
                f"Expected value for key '{key}' is '{value}', but got '{response_data[key]}'"
            )

    # Soft Assertions
    @staticmethod
    def soft_assert_status_code(response, expected_status_code: int):
        """
        Soft asserts that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  
            APIVerify.errors.append("Expected a Playwright response object, got a dictionary.")

        elif response.status != expected_status_code:
            APIVerify.errors.append(
                f"Expected status code {expected_status_code}, but got {response.status}."
            )

    @staticmethod
    def assert_all():
        """
        Raises all collected assertion errors at once.
        """
        if APIVerify.errors:
            error_message = "\n".join(APIVerify.errors)
            APIVerify.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")
        
    @staticmethod
    def check_unique_list(ids: list):
        """
        Verifies that all items in the list are unique.
        """
        assert len(ids) == len(set(ids)), "The list is not unique"

    @staticmethod
    def check_delete_student(response,expected_delete_status_code):
        assert response == expected_delete_status_code, f"Expected status code {expected_delete_status_code} for delete operation, but got {response}"

    @staticmethod
    def check_unique_courses(courses_list: list):
        unique_courses = set(courses_list)
        soft_assert(len(courses_list) == len(unique_courses), (
                f"The courses list is not unique: {courses_list}"
            ))

    @staticmethod
    def check_courses_is_not_empty(student_courses: dict):
        for student, courses in student_courses.items():
            assert courses, f"Courses list for {student} is empty"

    @staticmethod
    def check_email_format(emails: list):
        for email in emails:
            soft_assert( "@" in email and "." in email, f"Invalid email found: {email}")
    @staticmethod
    def check_status_create_student(response,expected_create_status_code):
        print(f"\nCreate student response: {response.status}")
        assert response.status == expected_create_status_code, f"\nExpected status code {expected_create_status_code} for create operation, but got {response}"
    
    @staticmethod
    def check_status_update_student(response,expected_update_status_code):
        assert response == expected_update_status_code, f"\nExpected status code {expected_update_status_code} for update operation, but got {response}"
       
    @staticmethod
    def check_student_details(response):
        details = ["id", "firstName", "lastName", "email", "programme", "courses"]
        students = response.json()
        for student in students:
            for i in range(len(details)):
                soft_assert(details[i] in student)  


    @staticmethod
    def assert_removed_student_status(response,expected_status_code):
        assert response == expected_status_code, f"\nExpected status code {expected_status_code} for getting removed student, but got {response}"

    @staticmethod
    def check_total_students(response,expected_total_students):
        assert response == expected_total_students, f"\nExpected total students to be {expected_total_students}, but got {response}"
        

    @staticmethod
    def verify_students_field(students, field, expected_type, not_null):

        type_map = {
            "int": int,
            "str": str,
            "list": list
        }

        for student in students:

            value = student.get(field)

            if not_null:
                soft_assert(value is not None,
                            f"{field} should not be None")

            soft_assert(
                isinstance(value, type_map[expected_type]),
                f"{field} should be {expected_type}"
            )

        verify_expectations()