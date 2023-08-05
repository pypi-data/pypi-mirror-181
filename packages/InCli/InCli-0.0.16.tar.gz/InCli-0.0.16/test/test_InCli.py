from InCli.SFAPI import utils

#python3 -m unittest

import unittest
from InCli import InCli
#from InCli.SFAPI import restClient

class Test_Main(unittest.TestCase):

    def test_q(self):
        InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1"])
    def test_q_System(self):
        InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-system"])
    def test_q_nulls(self):
        InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-null"])        
    def test_q_all(self):
        InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-all"])   
    def test_q_fields_all(self):
        InCli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 10","-fields","AccountId"])  
    def test_q_fields_all(self):
        InCli._main(["-u","NOSDEV","-q", "select AccountId,Pricebook2Id,OrderNumber,TotalContractCost__c,State__c from Order limit 50","-fields","all"])  
    def test_o(self):
        InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o"])

    def test_o_name(self):
        InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o","-name","order"])

    def test_o_like(self):
        InCli._main(["-u","uormaechea.devnoscat2@nos.pt","-o","-like","XOM"])

    def test_h(self):
        InCli._main(["-h"])

    def test_check_Catalog(self):
        try:
            InCli._main(["-u","NOSQSM","-checkCatalogs"])
        except Exception as e:
            utils.printException(e)
            print()

    def test_logs(self):
        InCli._main(["-u","NOSDEV","-logs"])

    def test_logs_user(self):
        InCli._main(["-u","NOSDEV","-logs","-loguser","Alias:ana.r"])

    def test_logs_userDefault(self):
        InCli._main(["-default:set","loguser","Alias:ana.r"])
        InCli._main(["-u","NOSDEV","-logs"])
        InCli._main(["-default:del","loguser"])

    def test_logs_userWrong(self):
        try:
            InCli._main(["-u","NOSDEV","-logs","-loguser","Alias:xxxx"])
        except Exception as e:
            self.assertTrue(e.args[0]['error']=='User with field Alias = xxxx does not exist in the User Object.')
            utils.printException(e)

    def test_logs_limit(self):
        InCli._main(["-u","NOSDEV","-logs","-limit","2"])

    def test_logs(self):
        InCli._main(["-u","NOSDEV","-logs"])

    def test_log_ID(self):
        InCli._main(["-u","NOSDEV","-logs","07L3O00000DaoiNUAR"])

    def test_log_file(self):
        InCli._main(["-u","NOSDEV","-logs","07L3O00000DfytZUAR","-level","0"])

    def test_log_last(self):
        InCli._main(["-u","NOSDEV","-logs","-last","100"])

    def test_default(self):
        InCli._main(["-default:set","u"])
        InCli._main(["-default:set","u","NOSDEV"])
        InCli._main(["-default:get","u"])        
        InCli._main(["-logs","-last","1"])
        InCli._main(["-default:del","u"])

    def test_d(self):
        InCli._main(["-u","NOSDEV","-d"])
        InCli._main(["-u","NOSDEV","-d","Order"])
        InCli._main(["-u","NOSDEV","-d","Order:Status"])

    def test_l(self):
        InCli._main(["-u","NOSDEV","-l"])
        InCli._main(["-u","DEVNOSCAT2","-l"])