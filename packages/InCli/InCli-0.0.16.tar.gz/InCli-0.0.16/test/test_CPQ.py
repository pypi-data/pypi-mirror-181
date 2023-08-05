import unittest
from InCli.SFAPI import restClient,CPQ,account,Sobjects,utils

class Test_Query(unittest.TestCase):
    def test_createCart(self):
        restClient.init('NOSDEV')

        acc = account.createAccount('Name:unaiTest1',recordTypeName='Consumer')

        self.assertTrue(Sobjects.checkId(acc['Id']))

        cartId = CPQ.createCart(accountF= acc['Id'], pricelistF='Name:WOO Price List',name="test2",checkExists=True)

        self.assertTrue(Sobjects.checkId(cartId))

        promotions = CPQ.getCartPromotions_api(cartId)

        promotionId = None
        promos = []
        for promotion in promotions:
            promo = {
                "name":promotion['Name'],
                "code":promotion['vlocity_cmt__Code__c']
            }
            promos.append(promo)
            if promotion['vlocity_cmt__Code__c'] == 'PROMO_NOS_OFFER_016':
                promotionId = promotion['Id']

        utils.printFormated(promos)

        res = CPQ.postCartsPromoItems_api(cartId,promotionId)

        print()



