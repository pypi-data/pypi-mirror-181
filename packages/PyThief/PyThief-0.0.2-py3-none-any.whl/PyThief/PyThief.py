# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from PyThief.recon_methods.ols import OLS
from PyThief.recon_methods.wls import WLS
from PyThief.utils import Utilities
from PyThief.fit_helper import Fit_Helper

class PyThief:
    def __init__(self,
                 method:str='snaive',
                 recon:str='ols',
                 seasonality:str='additive',
                 damped:bool=False):
        self.method = method
        self.recon = recon
        self.damped = damped
        self.seasonality = seasonality
        self.annual_agg = True
        self.semiannual_agg = True
    
    
    def fit(self, y):
        fh = Fit_Helper(self.method,self.annual_agg,self.semiannual_agg,self.damped,self.seasonality)
        predict_values, fitted_values, res_values, semiannual_agg, annual_agg = fh.fit_helper(y)
        self.annual_agg = annual_agg
        self.semiannual_agg = semiannual_agg
        return predict_values, fitted_values, res_values
    
    def predict(self, y):
        utl = Utilities()
        s_matrix = utl.build_smatrix(self.annual_agg,self.semiannual_agg)
        y_recon = utl.build_y_hat(y,self.annual_agg,self.semiannual_agg)
        if self.recon == 'ols':
            beta = OLS().recon(s_matrix,y_recon)
        elif self.recon == 'struc':
            beta = WLS().recon(s_matrix,y_recon)
        recon_p = s_matrix.dot(beta)
        recon_fore = utl.grab_month(recon_p,self.annual_agg,self.semiannual_agg)
        return recon_fore
