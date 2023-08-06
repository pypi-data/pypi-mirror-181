from InCli.SFAPI import utils,query,restClient
import sys, os
#python3 -m unittest

import unittest
from InCli import InCli
#from InCli.SFAPI import restClient
import traceback,time

#/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg
# python3 -m build
#python3 -m twine upload --repository pypi dist/InCli-0.0.29*

class Test_Main(unittest.TestCase):

    def test_q(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_q_System(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-system"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_nulls(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-null"])       
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2) 
    def test_q_all(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-all"])   
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_fields_all(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 10","-fields","AccountId"])  
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_fields_all(self):
        try:
            InCli._main(["-u","NOSDEV","-q", "select AccountId,Pricebook2Id,OrderNumber,TotalContractCost__c,State__c from Order limit 50","-fields","all"])  
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_o(self):
        try:
            InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_o_name(self):
        try:
            InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o","-name","order"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_o_like(self):
        try:
            InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o","-like","XOM"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_h(self):
        try:
            InCli._main(["-h"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc(self):
        try:
            InCli._main(["-u","NOSDEV","-cc"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_list(self):
        try:
            InCli._main(["-u","NOSDEV","-cc","-list"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_code(self):
        try:
            InCli._main(["-u","NOSDEV","-cc","-code","TESTERRORS"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_account(self):
        try:
            InCli._main(["-u","NOSDEV","-cc","-account","name:unaiTest4","-code","DC_CAT_MPO_CHILD_003"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs(self):
        try:
            InCli._main(["-u","NOSDEV","-logs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_user(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-loguser","Alias:ana.r"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_query(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-where","Operation='Batch Apex'","-last","10"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_userDefault(self):
        try:
            InCli._main(["-default:set","loguser","Alias:ana.r"])
            InCli._main(["-u","NOSDEV","-logs"])
            InCli._main(["-default:del","loguser"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_userWrong(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-loguser","Alias:xxxx"])
        except Exception as e:
            self.assertTrue(e.args[0]['error']=='User with field Alias = xxxx does not exist in the User Object.')
            utils.printException(e)

    def test_logs_limit(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-limit","2"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs(self):
        try:
            InCli._main(["-u","NOSDEV","-logs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
   
    def test_log_ID_2(self):
        try:
            id = '07L3O00000Dgx4nUAB'
            if id == None:
                restClient.init('NOSDEV')
                id = query.queryField("Select Id FROM ApexLog order by StartTime desc limit 1")
            InCli._main(["-u","NOSDEV","-logs",id])
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_IDflow(self): #flow
        try:
            InCli._main(["-u","NOSDEV","-logs","-inputfile","/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/flowAndWF.log"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def test_log_ID(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","07L3O00000DgtB6UAJ"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def test_log_file(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/07L3O00000Dgt4sUAB.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_2(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/07L3O00000DgwlbUAB.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_exception_wf(self):
        try:
            res = InCli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/ExceptionThrown.log"])
            self.assertTrue(res['exception']==True)
            last = res['debugList'][-1]
            self.assertTrue(last['cmtSOQLQueries'][0] == '43')
            self.assertTrue(last['CPUTime'][0] == '13363')
            
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_last(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-last","10"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_tail(self):
        try:
            #return
            InCli._main(["-u","NOSDEV","-logs","-tail"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)   

    def test_log_tail_delete(self):
        try:
            #return
            InCli._main(["-u","NOSDEV","-logs","-tail","-deletelogs","-debug"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)     
    def test_log_tail_where(self):
        try:
            return

            InCli._main(["-u","NOSDEV","-logs","-tail","-where","LogLength>3000"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)    
    def test_log_tailx(self):
        try:
            restClient.init('NOSDEV')
            logRecords = query.queryRecords("Select fields(all) FROM ApexLog order by StartTime desc limit 1")
            _time = logRecords[0]['StartTime']
            timez = _time.split('.')[0] + "Z"
            while (True):
                logRecords = query.queryRecords(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog where StartTime > {timez} order by StartTime asc ")

                if len(logRecords) > 0:
                    print()
                    for record in logRecords:
                        print(f"{record['StartTime']}  {record['Operation']}")
                        _time = record['StartTime']
                        timez = _time.split('.')[0] + "Z"
                        
                time.sleep(5)
            print()

          #  InCli._main(["-u","NOSDEV","-logs","-last","10"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_default(self):
        try:
            InCli._main(["-default:set","u"])
            InCli._main(["-default:set","u","NOSDEV"])
            InCli._main(["-default:get","u"])        
            InCli._main(["-logs","-last","1"])
            InCli._main(["-default:del","u"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_d(self):
        try:
            InCli._main(["-u","NOSDEV","-d"])
            InCli._main(["-u","NOSDEV","-d","Order"])
            InCli._main(["-u","NOSDEV","-d","Order:Status"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_l(self):
        try:
            InCli._main(["-u","NOSDEV","-l"])
            InCli._main(["-u","DEVNOSCAT2","-l"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)