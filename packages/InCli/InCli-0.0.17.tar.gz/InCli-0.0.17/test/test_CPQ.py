import unittest
from InCli.SFAPI import restClient,CPQ,account,Sobjects,utils,query,jsonFile

class Test_Query(unittest.TestCase):
    def test_createCart(self):
        restClient.init('NOSDEV')

        acc = account.createAccount('Name:unaiTest2',recordTypeName='Consumer')

        self.assertTrue(Sobjects.checkId(acc['Id']))

        cartId = CPQ.createCart(accountF= acc['Id'], pricelistF='Name:WOO Price List',name="testa2",checkExists=True)

        self.assertTrue(Sobjects.checkId(cartId))

        promotions = CPQ.getCartPromotions_api(cartId)



        promotionId = query.queryField(" select Id from  vlocity_cmt__Promotion__c where vlocity_cmt__Code__c='PROMO_NOS_OFFER_016'")
      #  promos = []
      #  for promotion in promotions:
      #      promo = {
      #          "name":promotion['Name'],
      #          "code":promotion['vlocity_cmt__Code__c']
      #      }
      #      promos.append(promo)
      #      if promotion['vlocity_cmt__Code__c'] == 'PROMO_NOS_OFFER_016':
      #          promotionId = promotion['Id']

      #  utils.printFormated(promos)

        res = CPQ.postCartsPromoItems_api(cartId,promotionId)

        print()

    def test_findRepeating(self):

        objs = jsonFile.read('/Users/uormaechea/Documents/Dev/python/VirtualEnvs/prj1/.incli/logs/07L3O00000Dg1OSUAZ')

        



