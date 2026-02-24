from playwright.sync_api import APIRequestContext, APIResponse

from data.api.chuck_api_data import *
from extensions.api_actions import APIActions

class ChuckApiFlows:

    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)

    def search_for_joke(self,query:str)->APIResponse:
        params = {"query":query}
        return self.api.get(FREE_SEARCH_RESOURCE,params)
