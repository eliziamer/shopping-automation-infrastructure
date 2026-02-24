import allure

from data.web.sauce_demo_data import *
from extensions.web_verifications import WebVerify
from workflows.web.sauce_flows import SauceFlows

class TestSauceDemoWeb:

    @allure.title("Test - Login")
    @allure.description("This test verify login is successful")
    def test_example(self,sauce_flows:SauceFlows):
        sauce_flows.sign_in(USER_NAME,PASSWORD)
        #WebVerify.strings_are_equal(sauce_flows.get_home_header(),EXPECTED_HOME_HEADER)
        WebVerify.text(sauce_flows.home.header,EXPECTED_HOME_HEADER)

    