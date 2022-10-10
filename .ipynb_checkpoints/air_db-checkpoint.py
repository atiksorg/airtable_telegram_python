import os
from pyairtable import Api, Base, Table
from pyairtable.formulas import match

apikey = os.environ['AIRTABLE_API_KEY']
base_id = os.environ['BASE_ID']
    
    
def CreateRecord(TableName, record, base_id = base_id):
    table = Table(apikey, base_id, TableName)
    table.create(record)
    
    
def GetRecord(TableName, Field='', Value='', base_id = base_id):
    table = Table(apikey, base_id, TableName)
    if Field == '' and Value == '':
        formula = ''
    else:
        formula = match({Field: Value})
    data = table.first(formula=formula)
    return data


def GetByRecordId(TableName, record_id, base_id = base_id):
    api = Api(apikey)
    record = api.get(base_id, TableName, record_id)
    return record


def GetAllRecord(TableName, Field='', Value='', base_id = base_id):
    table = Table(apikey, base_id, TableName)
    if Field == '' and Value == '':
        formula = ''
    else:
        formula = match({Field: Value})
    data = table.all(formula=formula)
    return data


def GetAllRecordOnView(TableName, base_id=base_id, view=''):
    api = Api(apikey)
    data = api.all(base_id, TableName, view=view)
    return data