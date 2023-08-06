# -*- coding: utf-8 -*-

import unittest
from PyThief.utils import Utilities
import numpy as np
import pandas as pd

def testing_data():
    y = [np.array([23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079]),
         np.array([53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973]),
         np.array([69587,
             69587,
             69587,
             69587,
             69587,
             69587,
             69587,
             69587]),
         np.array([96256,
                  96256,
                  96256,
                  96256,
                  96256,
                  96256]),
         np.array([348565,
                  348565,
                  348565,
                  348565]),
         np.array([522803,
                  522803])]
    return y

def testing_data_semi():
    y = [np.array([23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079]),
         np.array([53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973]),
         np.array([69587,
             69587,
             69587,
             69587,
             69587,
             69587,
             69587,
             69587]),
         np.array([348565,
                  348565,
                  348565,
                  348565])]
    return y
    
def testing_data_quar():
        y = [np.array([23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079,
                  23079]),
         np.array([53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973,
             53973]),
         np.array([96256,
                  96256,
                  96256,
                  96256,
                  96256,
                  96256])]
        return y
    
def testing_data_grab():
    y = np.array([477541,
                  238771,
                  238771,
                  159180,
                  159180,
                  159180,
                  119385,
                  119385,
                  119385,
                  119385,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  477541,
                  238771,
                  238771,
                  159180,
                  159180,
                  159180,
                  119385,
                  119385,
                  119385,
                  119385,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  79590.2,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1,
                  39795.1])
    return y

class UtilityTest(unittest.TestCase):
    def test_year_smatrix(self):
        utl = Utilities()
        s_matrix = utl.build_smatrix(True,True)
        self.assertTrue(len(s_matrix) == 56)
        
    def test_semiannual_smatrix(self):
        utl = Utilities()
        s_matrix = utl.build_smatrix(False,True)
        self.assertTrue(len(s_matrix) == 48)
        
    def test_quar_smatrix(self):
        utl = Utilities()
        s_matrix = utl.build_smatrix(False,False)
        self.assertTrue(len(s_matrix) == 42)

    def test_year_yhat(self):
        y = testing_data()
        utl = Utilities()
        y_hat = utl.build_y_hat(y,True,True)
        self.assertTrue(len(y_hat) == 56)
        
    def test_semiannual_yhat(self):
        y = testing_data_semi()
        utl = Utilities()
        y_hat = utl.build_y_hat(y,False,True)
        self.assertTrue(len(y_hat) == 48)
        
    def test_quar_yhat(self):
        y = testing_data_quar()
        utl = Utilities()
        y_hat = utl.build_y_hat(y,False,False)
        self.assertTrue(len(y_hat) == 42)
        
    def test_year_grab(self):
        y = testing_data_grab()
        utl = Utilities()
        y_recon = utl.grab_month(y,True,True)
        self.assertTrue(len(y_recon) == 24)
        
    def test_semiannual_grab(self):
        y = testing_data_grab()
        y = y[:48]
        utl = Utilities()
        y_recon = utl.grab_month(y,False,True)
        self.assertTrue(len(y_recon) == 24)
        
    def test_quar_grab(self):
        y = testing_data_grab()
        y = y[:42]
        utl = Utilities()
        y_recon = utl.grab_month(y,False,False)
        self.assertTrue(len(y_recon) == 24)
        
    def test_year_grab_null(self):
        y = testing_data_grab()
        utl = Utilities()
        y_recon = utl.grab_month(y,True,True)
        self.assertFalse(np.isnan(np.min(y_recon)))
        
    def test_semiannual_grab_null(self):
        y = testing_data_grab()
        y = y[:48]
        utl = Utilities()
        y_recon = utl.grab_month(y,False,True)
        self.assertFalse(np.isnan(np.min(y_recon)))
        
    def test_quar_grab_null(self):
        y = testing_data_grab()
        y = y[:42]
        utl = Utilities()
        y_recon = utl.grab_month(y,False,False)
        self.assertFalse(np.isnan(np.min(y_recon)))
    
    
    
if __name__ == '__main__':
    unittest.main()