import allure
import pytest

from data.web.shopping_cart_data import *
from utils.common_ops import read_data_from_csv
from workflows.web.shopping_cart_flows import SauceFlows


LOGIN_DATA_PATH = r"data/ddt/login_data.csv"

class TestSauceDDT:

    @allure.title("Test - Verify LOGIN with DDT")
    @allure.step("This test verify LOGIN DATA")
    @pytest.mark.parametrize("login_data",read_data_from_csv(LOGIN_DATA_PATH))
    def test_login_ddt(self,sauce_flows:SauceFlows,login_data):
        sauce_flows.navigate_to(SAUCE_URL)
        sauce_flows.sign_in(login_data["username"],login_data["password"])
        sauce_flows.verify_ddt_flow(login_data["expected_status"])



