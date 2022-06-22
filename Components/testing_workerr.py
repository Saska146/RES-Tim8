from datetime import datetime
import unittest
from unittest.mock import MagicMock, Mock, patch
import database
from models import CodeEnum, CollectionDescription, DataSet, Description, HistoricalCollection, Item, WorkerProperty
import worker

def CheckCollectionDescriptionCorrect(d: Description, cd: CollectionDescription):
   
    res:bool = d.Id == cd.Id
    res &= d.DataSet.Code1 == cd.DataSet.Code1 and d.DataSet.Code2 == cd.DataSet.Code2 
    res &= len(d.Items) == len(cd.HistoricalCollection.Workers)
    
    if(res):
        for i in range(len(d.Items)):
            res &= d.Items[i].Code == cd.HistoricalCollection.Workers[i].Code
            res &= d.Items[i].Value == cd.HistoricalCollection.Workers[i].WorkerValue

    return res

class TestWorker(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def doCleanups(self) -> None:
        return super().doCleanups()

    def testConvertWorkDataGood(self):
        
        d = Description(1, 
            [
                Item(CodeEnum.CODE_DIGITAL, 10),
                Item(CodeEnum.CODE_ANALOG, 10)
            ],
            DataSet(CodeEnum.CODE_ANALOG, CodeEnum.CODE_DIGITAL)
        )

        cd = worker.ConvertWorkerData(d)

        self.assertTrue(CheckCollectionDescriptionCorrect(d, cd))

    def testConvertWorkDataNone(self):
        
        with self.assertRaises(TypeError):
            cd = worker.ConvertWorkerData(None)
         
    def testDeadBandTrue(self):
        
        fromDb = 3
        newOne = 50
        self.assertTrue(worker.Deadband(fromDb, newOne))

    def testDeadBandFalse(self):
        
        fromDb = 3
        newOne = 3
        self.assertFalse(worker.Deadband(fromDb, newOne))

    def testDeadBandError(self):
        
        with self.assertRaises(TypeError):
            worker.Deadband(None, 1)

    def testGetNewValuesPass(self):
        
        retval:dict[CodeEnum, int] = {
            CodeEnum.CODE_ANALOG: 22,
            CodeEnum.CODE_DIGITAL: 1
        }
        w = worker.Worker(1)
        w.CDS = {
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
        w.CDS[1].DataSet = 1
        w.CDS[1].Id = 1
        w.CDS[1].HistoricalCollection.Workers = [
            WorkerProperty(CodeEnum.CODE_ANALOG, 22),
            WorkerProperty(CodeEnum.CODE_DIGITAL, 1)
        ]
        self.assertTrue(w.GetNewValues(1) == retval)

    def testGetNewValuesFails(self):
        
        retval:dict[CodeEnum, int] = {
            CodeEnum.CODE_ANALOG: 44,
            CodeEnum.CODE_DIGITAL: 1
        }
        w = worker.Worker(1)
        w.CDS = {
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
        w.CDS[1].DataSet = 1
        w.CDS[1].Id = 1
        w.CDS[1].HistoricalCollection.Workers = [
            WorkerProperty(CodeEnum.CODE_ANALOG, 22),
            WorkerProperty(CodeEnum.CODE_DIGITAL, 1)
        ]
        self.assertFalse(w.GetNewValues(1) == retval)

    def testGetCodesCountPass(self):
        
        retval:dict[CodeEnum, int] = {
            CodeEnum.CODE_ANALOG: 2, 
            CodeEnum.CODE_DIGITAL: 1
        }
        w = worker.Worker(1)
        w.CDS = {
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
        w.CDS[1].DataSet = 1
        w.CDS[1].Id = 1
        w.CDS[1].HistoricalCollection.Workers = [
            WorkerProperty(CodeEnum.CODE_ANALOG, 22),
            WorkerProperty(CodeEnum.CODE_ANALOG, 23),
            WorkerProperty(CodeEnum.CODE_DIGITAL, 1)
        ]
        self.assertTrue(w.GetCodesCount(1) == retval)

    def testGetCodesCountFails(self):
       
        retval:dict[CodeEnum, int] = {
            CodeEnum.CODE_ANALOG: 0, 
            CodeEnum.CODE_DIGITAL: 1
        }
        w = worker.Worker(1)
        w.CDS = {
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
        w.CDS[1].DataSet = 1
        w.CDS[1].Id = 1
        w.CDS[1].HistoricalCollection.Workers = [
            WorkerProperty(CodeEnum.CODE_ANALOG, 22),
            WorkerProperty(CodeEnum.CODE_ANALOG, 23),
            WorkerProperty(CodeEnum.CODE_DIGITAL, 1)
        ]
        self.assertFalse(w.GetCodesCount(1) == retval)
    
    def testReceiveDescriptionCrash1(self):
       
        w = worker.Worker(1)
        with patch('worker.insertData') as insertMethod:
            with self.assertRaises(TypeError):
                w.ReceiveDescriptions(1) 
                self.assertEqual(insertMethod.call_count, 0)

    def testReceiveDescriptionCrash(self):
        
        w = worker.Worker(1)
        with patch('worker.insertData') as insertMetod:
            with self.assertRaises(TypeError):
                w.ReceiveDescriptions(None) 
                self.assertEqual(insertMetod.call_count, 0)

    def testReceiveDescriptionPass(self):
       
        with patch('worker.insertData') as insertMetod:
            w = worker.Worker(1)

            lastValueAnalog = database.readLastValueByCode(CodeEnum.CODE_ANALOG.value)[1]
            newValue = lastValueAnalog * 1.2 

            w.ReceiveDescriptions(Description(
                1, 
                [
                    Item(CodeEnum.CODE_ANALOG, newValue),
                    Item(CodeEnum.CODE_ANALOG, newValue),
                    Item(CodeEnum.CODE_DIGITAL, 1),
                ],
                DataSet(CodeEnum.CODE_ANALOG, CodeEnum.CODE_DIGITAL)
            ))
            self.assertTrue(len(w.CDS[1].HistoricalCollection.Workers) == 0)
            self.assertEqual(insertMetod.call_count, 2)

    def testReceiveDescriptionPass2(self):
       
        with patch('worker.insertData') as insertMetod:
            w = worker.Worker(1)
            
            lastValues = {
                CodeEnum.CODE_CUSTOM : database.readLastValueByCode(CodeEnum.CODE_CUSTOM.value)[1],
                CodeEnum.CODE_LIMITSET : database.readLastValueByCode(CodeEnum.CODE_LIMITSET.value)[1],
            }

            newValues = {
                CodeEnum.CODE_CUSTOM : lastValues[CodeEnum.CODE_CUSTOM] * 1.2,
                CodeEnum.CODE_LIMITSET : lastValues[CodeEnum.CODE_LIMITSET] * 1.2,
            }

            w.ReceiveDescriptions(Description(
                1, 
                [
                    Item(CodeEnum.CODE_CUSTOM, newValues[CodeEnum.CODE_CUSTOM]),
                    Item(CodeEnum.CODE_CUSTOM, newValues[CodeEnum.CODE_CUSTOM]),
                    Item(CodeEnum.CODE_LIMITSET, newValues[CodeEnum.CODE_LIMITSET]),
                ],
                DataSet(CodeEnum.CODE_CUSTOM, CodeEnum.CODE_LIMITSET)
            ))
            self.assertTrue(len(w.CDS[2].HistoricalCollection.Workers) == 0)
            self.assertEqual(insertMetod.call_count, 2) 


    def testreadByDateTimePass(self):
        
        with patch('worker.readByDateAndCode') as method:
            date1 = datetime(1992, 4, 16)
            date2 = datetime(2043, 5, 29)

            #2
            retVal = worker.Worker.readByDateTimeAndCode(
                date1, date2, 1
            )

            self.assertEqual(method.call_count, 1)

            for r in retVal:
                dstr = r[2].split('.')[0]
                d = datetime.strptime(dstr, '%Y-%m-%d %H:%M:%S')
                self.assertTrue(d > date1 and d < date2)

    def testreadByDateTimeEmpty(self):
        
        with patch('worker.readByDateAndCode') as method:
            date1 = datetime(1992, 4, 16)
            date2 = datetime(2043, 5, 29)

            #2
            retVal = worker.Worker.readByDateTimeAndCode(
                date2, date1, 1
            )
            self.assertEqual(method.call_count, 1)

            self.assertTrue(len(retVal) == 0)

    def testreadByDateTimeNone(self):
        
        with patch('worker.readAll') as method:
            with self.assertRaises(TypeError):
                worker.Worker.readByDateTimeAndCode(
                    None, 2, 1
                )
            self.assertEqual(method.call_count, 0)

    def testreadAllCodesPass(self):
        
        with patch('worker.readAll') as method:
            retVal = worker.Worker.GetLastForCodes()
            self.assertEqual(method.call_count, 1)
        
        retVal = worker.Worker.GetLastForCodes()
        codesNums = [c.value for c in CodeEnum]
        
        for r in retVal:
            if (int(r[4]) in codesNums):
                codesNums.remove(int(r[4]))

        self.assertTrue(len(codesNums) == 0)

if __name__ == '__main__':
    unittest.main()
    