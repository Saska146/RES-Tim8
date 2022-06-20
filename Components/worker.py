from datetime import date, datetime
import threading
from writer import code
import logger
from models import *
from database import *


def DataSetForCode(code_:str):
    if code_==code[0] or code_ == code[1]:
        return 1
    elif code_==code[2] or code_ == code[3]:
        return 2
    elif code_==code[4] or code_ == code[5]:
        return 3
    elif code_==code[6] or code_ == code[7]:
        return 4
    
def CodesForDataSet(dataSet:int):
    if dataSet == 1:
        return (CodeEnum.CODE_ANALOG, CodeEnum.CODE_DIGITAL)
    elif dataSet == 2:
        return (CodeEnum.CODE_CUSTOM, CodeEnum.CODE_LIMITSET)
    elif dataSet == 3:
        return (CodeEnum.CODE_SINGLENODE, CodeEnum.CODE_MULTIPLENODE)
    elif dataSet == 4:
        return (CodeEnum.CODE_CONSUMER, CodeEnum.CODE_SOURCE)


def ConvertWorkerData(self, desc: Description)->CollectionDescription:
        return CollectionDescription(
            desc.Id,
            HistoricalCollection(
                [WorkerProperty(it.Code, it.Value) for it in desc.Items]
            ),
            desc.DataSet
        )


def GetDbValue(code:CodeEnum)->int:
    return -1


def Deadband(fromDB:int, newOne:int) -> bool:
    difference = fromDB - newOne
    if difference < 0:
        difference *= -1
    twopercent = 0.02 * fromDB
    return difference > twopercent


class Worker:
    def __init__(self):
        self.id = 0
        self.CDS:dict[int, CollectionDescription] = {
            1: CollectionDescription(
                0, HistoricalCollection([]), 1
            ),
            2: CollectionDescription(
                0, HistoricalCollection([]), 2
            ),
            3: CollectionDescription(
                0, HistoricalCollection([]), 3
            ),
            4: CollectionDescription(
                0, HistoricalCollection([]), 4
            )
        }

    def readByDateTimeAndCode(dfrom:datetime, dto:datetime, code_:int): 
        return readByDateAndCode(dfrom, dto, code_) # poziv metode iz baze

    def GetLastForCodes(): 
        return readAll()

    def GetNewValues(self, dataset:int)->dict[CodeEnum, int]:
        ret: dict[CodeEnum, int] = {}
        for p in self.CDS[dataset].HistoricalCollection.Workers:
            ret[CodeEnum(p.Code)] = p.WorkerValue 
        return ret

    def GetCodesCount(self, dataset:int)->dict[CodeEnum, int]:
        codeCount: dict[CodeEnum, int] = {
            c:0 for c in CodeEnum
        }
        for p in self.CDS[dataset].HistoricalCollection.Workers:
            codeCount[CodeEnum(p.Code)] += 1

        return codeCount

    def ReceiveDescriptions(self, desc: Description):
        currentColDes:CollectionDescription = ConvertWorkerData(desc)

        for p in currentColDes.HistoricalCollection.Workers:
            self.CDS[currentColDes.DataSet].HistoricalCollection.Workers.append(p)

        currentValues:dict[CodeEnum, int] = {
            c:readLastValueByCode(c.value)[1] for c in CodeEnum
        }
        newValues:dict[CodeEnum, int] = self.GetNewValues(currentColDes.DataSet)
        codesCount:dict[CodeEnum, int] = self.GetCodesCount(currentColDes.DataSet)

        datasetCodes = CodesForDataSet(currentColDes.DataSet)

        if (codesCount[datasetCodes[0]] > 0 and codesCount[datasetCodes[1]] > 0):
            if(datasetCodes[1] == CodeEnum.CODE_DIGITAL):
                # Insert digital desctiption
                insertData(ModelDB(2,newValues[CodeEnum.CODE_DIGITAL],datetime.now(),1))
                if (Deadband(currentValues[CodeEnum.CODE_ANALOG], newValues[CodeEnum.CODE_ANALOG])):
                    insertData(ModelDB(1,newValues[CodeEnum.CODE_ANALOG],datetime.now(),1))
            else:
                for c in datasetCodes:
                    if (Deadband(currentValues[c], newValues[c])):
                        insertData(ModelDB(c,newValues[c],datetime.now(),currentColDes.DataSet))    
            self.CDS[currentColDes.DataSet].HistoricalCollection.Workers.clear()  
