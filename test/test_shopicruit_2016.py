# -*- coding: utf-8 -*-
import unittest
import shopicruit_2016 

class Test_shopicruit(unittest.TestCase):
    def test_budget(self):
        input_value = 169.13
        total_grams = shopicruit_2016.report_for_Alice(input_value)        

    def test_items(self):
        input_value = 23
        total_grams = shopicruit_2016.report_for_Alice(input_value)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Test_shopicruit))
    return suite

#if __name__ == '__main__':
#    unittest.main()
