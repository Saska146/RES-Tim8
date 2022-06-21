from datetime import date, datetime
import threading
from writer import code
import logger
from models import *
from database import readAll, insertData, readByDateAndCode, readLastValueByCode, ModelDB

    
def DataSetForCodeEnum(code_: CodeEnum):
    if code_==CodeEnum.CODE_ANALOG or code_ == CodeEnum.CODE_DIGITAL:
        return 1
    elif code_==CodeEnum.CODE_CUSTOM or code_ == CodeEnum.CODE_LIMITSET:
        return 2
    elif code_==CodeEnum.CODE_SINGLENODE or code_ == CodeEnum.CODE_MULTIPLENODE:
        return 3
    elif code_==CodeEnum.CODE_CONSUMER or code_ == CodeEnum.CODE_SOURCE:
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


def ConvertWorkerData(desc: Description)->CollectionDescription:
       
        if(desc is None):
            raise TypeError
        else:
            return CollectionDescription(
                desc.Id,
                HistoricalCollection(
                    [WorkerProperty(it.Code, it.Value) for it in desc.Items]
                ),
                desc.DataSet
            )

def Deadband(fromDB:int, newOne:int) -> bool:
   
    if (fromDB is None or newOne is None):
        raise TypeError

    difference = fromDB - newOne  
    if difference < 0:
        difference *= -1
    twopercent = 0.02 * fromDB
    return difference > twopercent


class Worker:
    def __init__(self, id):
        self.id = id
      
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
        if(
            type(dfrom) is not datetime or
            type(dto) is not datetime or
            type(code_) is not int
        ):
            raise TypeError
            
        return readByDateAndCode(dfrom, dto, code_)

    def GetLastForCodes(): 
        return readAll() 

    def GetNewValues(self, dataset:int)->dict[CodeEnum, int]:
       
        ret: dict[CodeEnum, int] = {}
        for p in self.CDS[dataset].HistoricalCollection.Workers:
            ret[CodeEnum(p.Code)] = p.WorkerValue 
        return ret

    def GetCodesCount(self, dataset:int)->dict[CodeEnum, int]:
        
        codeCount: dict[CodeEnum, int] = {
            c:0 for c in CodesForDataSet(dataset)
        }
        for p in self.CDS[dataset].HistoricalCollection.Workers:
            codeCount[CodeEnum(p.Code)] += 1

        return codeCount

    def ReceiveDescriptions(self, desc: Description):
       
        if type(desc) is not Description:
            raise TypeError

        logger.logData('Worker {id} received data from LoadBalancer'.format(id=self.id))
        currentColDes:CollectionDescription = ConvertWorkerData(desc)

  
        for p in currentColDes.HistoricalCollection.Workers:
            self.CDS[DataSetForCodeEnum(currentColDes.DataSet.Code1)].HistoricalCollection.Workers.append(p)

       
        currentValues:dict[CodeEnum, int] = {
            c:readLastValueByCode(c.value)[1] for c in CodeEnum
        }
        newValues:dict[CodeEnum, int] = self.GetNewValues(DataSetForCodeEnum(currentColDes.DataSet.Code1))
        codesCount:dict[CodeEnum, int] = self.GetCodesCount(DataSetForCodeEnum(currentColDes.DataSet.Code1))

        datasetCodes = (currentColDes.DataSet.Code1, currentColDes.DataSet.Code2)
        dataSetInt = DataSetForCodeEnum(currentColDes.DataSet.Code1)

       
        if (codesCount[datasetCodes[0]] > 0 and codesCount[datasetCodes[1]] > 0):
            if(datasetCodes[1] == CodeEnum.CODE_DIGITAL):
              
                insertData(ModelDB(2,newValues[CodeEnum.CODE_DIGITAL],dataSetInt))
                logger.logData('Worker {id} wrote DIGITAL code value to Database'.format(id=self.id))

                if (Deadband(currentValues[CodeEnum.CODE_ANALOG], newValues[CodeEnum.CODE_ANALOG])):
                    insertData(ModelDB(1,newValues[CodeEnum.CODE_ANALOG],dataSetInt))
                    logger.logData('Worker {id} wrote ANALOG code value to Database'.format(id=self.id))
            else:
                for c in datasetCodes:
                    if (Deadband(currentValues[c], newValues[c])):
                        insertData(ModelDB(c.value,newValues[c],dataSetInt))    
                        logger.logData('Worker {id} wrote {code} code value to Database'.format(id=self.id, code=c.value))

            self.CDS[DataSetForCodeEnum(currentColDes.DataSet.Code1)].HistoricalCollection.Workers.clear()  
            logger.logData('Worker {id} cleared internal data for dataset after insert to database'.format(id=self.id))
