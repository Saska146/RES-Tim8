import enum

class CodeEnum(enum.Enum):
    CODE_ANALOG = 1
    CODE_DIGITAL = 2
    CODE_CUSTOM = 3
    CODE_LIMITSET = 4
    CODE_SINGLENODE = 5 
    CODE_MULTIPLENODE = 6
    CODE_CONSUMER = 7
    CODE_SOURCE = 8

class DataSet:
    def __init__(self, code1 : CodeEnum , code2 : CodeEnum):
        self.Code1 = code1
        self.Code2 = code2

class Item:
    def __init__(self, code : CodeEnum, value : int):
        self.Code = code
        self.Value = value

class Description:
    def __init__(self, id : int, items : Item, dataSet : DataSet):
        self.Id = id
        self.Items = items
        self.DataSet = dataSet

class DescriptionList:
    def __init__(self, descriptions : Description):
        self.Descriptions = descriptions

class WorkerProperty:
    def __init__(self, code : CodeEnum, workerValue : int ):
        self.Code = code
        self.WorkerValue = workerValue

class HistoricalCollection:
    def __init__(self, workers : WorkerProperty):
        self.Workers = workers

class CollectionDescription:
    def __init__(self, id : int, 
        historicalCollection : HistoricalCollection,
        dataSet : DataSet):
        self.Id = id
        self.HistoricalCollection = historicalCollection
        self.DataSet = dataSet





