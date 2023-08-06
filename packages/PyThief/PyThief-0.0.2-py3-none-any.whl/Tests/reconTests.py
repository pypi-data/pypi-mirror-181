# -*- coding: utf-8 -*-

import unittest
from PyThief.recon_methods.ols import OLS
from PyThief.recon_methods.wls import WLS
from PyThief.utils import Utilities
import numpy as np

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

class ReconTest():
    def setUp(self):
        self.recon_obj = None
    
    def set_recon_obj(self, child_recon_obj):
        self.recon_obj = child_recon_obj
    
    def test_ols_series(self):
        y = testing_data()
        s_matrix = Utilities().build_smatrix(True,True)
        y_recon = Utilities().build_y_hat(y,True,True)
        beta = self.recon_obj.recon(s_matrix,y_recon)
        self.assertTrue(isinstance(beta, np.ndarray))
              
    def test_wls_null(self):
        y = testing_data()
        s_matrix = Utilities().build_smatrix(True,True)
        y_recon = Utilities().build_y_hat(y,True,True)
        beta = self.recon_obj.recon(s_matrix,y_recon)
        self.assertFalse(np.isnan(np.min(beta)))
        
class OLSTest(ReconTest, unittest.TestCase):
    def setUp(self):
        self.set_recon_obj(OLS())

class WLSTest(ReconTest, unittest.TestCase):
    def setUp(self):
        self.set_recon_obj(WLS())
        

if __name__ == '__main__':
    unittest.main()
    

    