from data.api.chuck_api_data import *
from extensions.api_verifications import APIVerify
from workflows.api.chuck_api_flows import ChuckApiFlows


class TestChuckAPI:

    def test01_verify_joke(self,chuck_flows:ChuckApiFlows):
        APIVerify.status_code(  chuck_flows.search_for_joke(SEARCH_VALUE),EXPECTED_STATUS_SUCCESS_CODE)

