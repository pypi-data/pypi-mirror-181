from datetime import datetime
import uuid
import requests
from one_py_sdk.enterprise.authentication import AuthenticationApi
from one_py_sdk.shared.helpers.protobufhelper import DeserializeResponse
from one_py_sdk.shared.helpers.datetimehelper import *
from one_interfaces import row_pb2 as row
from one_interfaces import cell_pb2 as cell   
from one_interfaces import celldata_pb2 as celldata   
from one_interfaces import auditevent_pb2 as audit


class SpreadsheetApi:
    def __init__(self, env: str, auth: AuthenticationApi):
        self.Environment = env
        self.Auth = auth
        self.AppUrl = "/operations/spreadsheet/v1/"

    def SaveRows (self, plantId, wsType, rows):
        url = f"{self.Environment}{self.AppUrl}{plantId}/worksheet/{str(wsType)}/rows"
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Content-Type": "application/x-protobuf", "Accept": "application/x-protobuf" }        
        response = DeserializeResponse(requests.post(url, headers=headers, data=rows.SerializeToString()))
        return response
    
    def RowBuilder(self, valueDict, wsType):
        r = row.Rows()        
        for key in valueDict.keys():
            r2 =row.Row() 
            for item in valueDict[key]:
                for k in item.keys():        
                    cd = celldata.CellData()
                    c = cell.Cell()
                    s =audit.AuditEvent()
                    s.id = str(uuid.uuid4())
                    s.userId = self.Auth.User.id
                    s.timeStamp.jsonDateTime.value = ToJsonTicksDateTime(datetime.utcnow)
                    s.details = "Python SDK import"
                    s.enumDataSource = 5
                    s.enumDomainSource = 2
                    cd.auditEvents.append(s)
                    cd.stringValue.value=item[k]             
                    c.columnNumber=k
                    c.cellDatas.append(cd)
                    r2.rowNumber = GetRowNumber(key, wsType)
                    r2.cells.append(c) 
                    r.items[r2.rowNumber].MergeFrom(r2)     
        return r
    
    def GetWorksheetColumnIds(self, plantId, wsType):        
        url = self.Environment + self.AppUrl + plantId + \
            "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        columnIds = [
            col.columnId for col in response.content.worksheetDefinitions.items[0].columns if col.isActive == True]
        return columnIds

    def GetWorksheetColumnNumbers(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + \
            "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        columnNumbers = [
            col.columnNumber for col in response.content.worksheetDefinitions.items[0].columns if col.isActive == True]
        return columnNumbers

    def GetWorksheetDefinition(self, plantId, wsType):
        url = self.Environment + self.AppUrl + plantId + \
            "/worksheet/"+str(wsType)+"/definition"
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.worksheetDefinitions.items

    def GetSpreadsheetDefinition(self, plantId):
        url = f'{self.Environment}{self.AppUrl}{plantId}/definition'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        return response.content.spreadsheetDefinitions.items

    def GetColumnByDay(self, plantId, wsType, columnId, date: datetime):
        url = self.Environment + self.AppUrl + plantId + \
            f'/worksheet/{str(wsType)}/column/{columnId}/byday/{date.year}/{date.month}/{date.day}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.measurements.items

    def GetColumnByMonth(self, plantId: str, wsType: int, columnId: int, date: datetime):
        url = self.Environment + self.AppUrl + plantId + \
            f'/worksheet/{str(wsType)}/column/{columnId}/bymonth/{date.year}/{date.month}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.measurements.items

    def GetColumnByYear(self, plantId, wsType, columnId, date: datetime):
        url = self.Environment + self.AppUrl + plantId + \
            f'/worksheet/{str(wsType)}/column/{columnId}/byyear/{date.year}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.measurements.items

    def GetRows(self, plantId, wsType, startRow=None, endRow=None, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        requestId = uuid.uuid4()
        url = f'{self.Environment}{self.AppUrl}{plantId}/worksheet/{str(wsType)}/rows?requestId={requestId}'
        if startRow:
            url = url+f'&startRow={startRow}'
        if endRow:
            url = url+f'&endRow={endRow}'
        if columns:
            url = url+f'&columns={columns}'
        if viewId:
            url = url+f'&viewId={viewId}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.rows.items

    def __getRows(self, plantId, wsType, startRow=None, endRow=None, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        requestId = uuid.uuid4()
        url = f'{self.Environment}{self.AppUrl}{plantId}/worksheet/{str(wsType)}/rows?requestId={requestId}'
        if startRow:
            url = url+f'&startRow={startRow}'
        if endRow:
            url = url+f'&endRow={endRow}'
        if columns:
            url = url+f'&columns={columns}'
        if viewId:
            url = url+f'&viewId={viewId}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response        
        return response.content.rows

    def GetRowsByDay(self, plantId, wsType, date: datetime, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        url = self.Environment + self.AppUrl + \
            f'{plantId}/worksheet/{str(wsType)}/rows/byday/{date.year}/{date.month}/{date.day}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.rows.items

    def GetRowsByMonth(self, plantId, wsType, date: datetime, columns=None, viewId=None):
        if columns and viewId:
            return print("Using both columns and viewId parameters together is not supported.")
        url = self.Environment + self.AppUrl + \
            f'{plantId}/worksheet/{str(wsType)}/rows/bymonth/{date.year}/{date.month}'
        headers = {'Authorization': self.Auth.Token.access_token,
                   "Accept": "application/x-protobuf"}
        response = DeserializeResponse(requests.get(url, headers=headers))
        if response.errors:
            return response
        return response.content.rows.items

    def GetRowsForTimeRange(self, plantId, wsType, startDate: datetime, endDate: datetime):
        startRow = GetRowNumber(startDate, wsType)
        endRow = GetRowNumber(endDate, wsType)
        rows = row.Rows()
        while endRow - startRow > 5000:
            newEndRow = startRow+5000
            rows.MergeFrom(self.__getRows(
                plantId, wsType, startRow, newEndRow))
            startRow = newEndRow+1
        rows.MergeFrom(self.__getRows(plantId, wsType, startRow, endRow))
        return rows.items
