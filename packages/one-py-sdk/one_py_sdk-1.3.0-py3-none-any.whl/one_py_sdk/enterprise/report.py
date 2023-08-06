import requests
import json
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse
import uuid


class ReportApi:
    def __init__(self, env, auth: AuthenticationApi):
        self.AppUrl = "/enterprise/report/v1/"
        self.Environment = env
        self.Authentication = auth
        
    def GetReportDefinitions(self, plantId=None):
        url = f'{self.Environment}{self.AppUrl}definitions'
        if plantId:
            url= url+f"?plantId={plantId}"
        headers = {'Authorization': self.Authentication.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.ReportDefinitions.items
    
    def GetColumnsIdsFromReportDefinitions(self, lst):       
        reportDefs = [json.loads(report.reportDefinitionJson.value) for report  in lst]
        columns = [d.get('columns') for d in reportDefs]
        ids =[]
        for colLst in columns:
            for col in colLst:
                ids.append(col.get('id'))
        return ids
