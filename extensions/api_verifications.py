
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
            VerifyAPI.errors.append("Expected a Playwright response object, got a dictionary.")

        elif response.status != expected_status_code:
            VerifyAPI.errors.append(
                f"Expected status code {expected_status_code}, but got {response.status}."
            )

    @staticmethod
    def assert_all():
        """
        Raises all collected assertion errors at once.
        """
        if VerifyAPI.errors:
            error_message = "\n".join(VerifyAPI.errors)
            VerifyAPI.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")