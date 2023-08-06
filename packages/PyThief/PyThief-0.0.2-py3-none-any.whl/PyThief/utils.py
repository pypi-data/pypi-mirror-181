# -*- coding: utf-8 -*-
import numpy as np


class Utilities:
    
    def __init__(self):
        pass
    
    def build_smatrix(self,annual_agg,semiannual_agg):
        if annual_agg:
            s_matrix = np.ones((12,),dtype=int)
            s_matrix = np.atleast_2d(s_matrix)
            s_matrix = np.concatenate((s_matrix,[[1,1,1,1,1,1,0,0,0,0,0,0]]))
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,1,1,1,1,1,1]],axis = 0)
            s_matrix = np.append(s_matrix, [[1,1,1,1,0,0,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,1,1,1,1,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,0,0,1,1,1,1]],axis = 0)
            s_matrix = np.append(s_matrix, [[1,1,1,0,0,0,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,1,1,1,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,1,1,1,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,0,0,0,1,1,1]],axis = 0)
            s_matrix = np.append(s_matrix, [[1,1,0,0,0,0,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,1,1,0,0,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,1,1,0,0,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,1,1,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,0,0,1,1,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,0,0,0,0,0,0,1,1]],axis = 0)
            s_matrix = np.concatenate((s_matrix,np.eye(12)))
        elif semiannual_agg:
            s_matrix = np.ones((6,),dtype=int)
            s_matrix = np.atleast_2d(s_matrix)
            s_matrix = np.concatenate((s_matrix,[[1,1,1,0,0,0]]))
            s_matrix = np.append(s_matrix, [[0,0,0,1,1,1]],axis = 0)
            s_matrix = np.append(s_matrix, [[1,1,0,0,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,1,1,0,0]],axis = 0)
            s_matrix = np.append(s_matrix, [[0,0,0,0,1,1]],axis = 0)
            s_matrix = np.concatenate((s_matrix,np.eye(6)))
        else:
            s_matrix = np.ones((4,),dtype=int)
            s_matrix = np.atleast_2d(s_matrix)
            s_matrix = np.concatenate((s_matrix,[[1,1,0,0]]))
            s_matrix = np.append(s_matrix, [[0,0,1,1]],axis = 0)
            s_matrix = np.concatenate((s_matrix,np.eye(4)))
        s_matrix = np.append(s_matrix,s_matrix,axis=0)
        s_matrix_low = s_matrix
        if semiannual_agg and not annual_agg:
            s_matrix = np.append(s_matrix,s_matrix,axis=0)
        elif not semiannual_agg and not annual_agg:
            s_matrix = np.append(s_matrix,s_matrix,axis=0)
            s_matrix = np.append(s_matrix,s_matrix_low,axis=0)
        return s_matrix

    def build_y_hat(self,predict_values,annual_agg,semiannual_agg):
        if annual_agg:
            forecast_number = 2
        elif semiannual_agg and not annual_agg:
            forecast_number = 4
        else:
            forecast_number = 6
        for horizon in range(forecast_number):
            if not horizon:
                y_recon = predict_values[-1][horizon]
            else:
                y_recon = np.append(y_recon,predict_values[-1][horizon])
            for i in range(2,len(predict_values)+1):
                freq = int(len(predict_values[-i])/forecast_number)
                y_recon = np.append(y_recon,predict_values[-i][horizon*freq:(horizon+1)*freq])
        return y_recon
    
    def grab_month(self,recon_p,annual_agg,semiannual_agg):
        if annual_agg:
            frecon = recon_p[:int(len(recon_p)/2)]
            frecon = frecon[-12:]
            srecon = recon_p[int(len(recon_p)/2):]
            srecon = srecon[-12:]
            recon_fore = np.append(frecon,srecon) 
            recon_fore[recon_fore<0] = 0
        elif semiannual_agg:
            fqrecon = recon_p[:int(len(recon_p)/4)]
            fqrecon = fqrecon[-6:]
            sqrecon = recon_p[:int(len(recon_p)/2)]
            sqrecon = sqrecon[-6:]
            tqrecon = recon_p[int(len(recon_p)/2):3*int(len(recon_p)/4)]
            tqrecon = tqrecon[-6:]
            lqrecon = recon_p[int(len(recon_p)/2):]
            lqrecon = lqrecon[-6:]
            recon_fore = np.append(fqrecon,sqrecon) 
            recon_fore = np.append(recon_fore,tqrecon)
            recon_fore = np.append(recon_fore,lqrecon)
            recon_fore[recon_fore<0] = 0
        else:
            trecon1 = recon_p[:int(len(recon_p)/6)]
            trecon1 = trecon1[-4:]
            trecon2 = recon_p[int(len(recon_p)/6):2*int(len(recon_p)/6)]
            trecon2 = trecon2[-4:]
            trecon3 = recon_p[2*int(len(recon_p)/6):3*int(len(recon_p)/6)]
            trecon3 = trecon3[-4:]
            trecon4 = recon_p[3*int(len(recon_p)/6):4*int(len(recon_p)/6)]
            trecon4 = trecon4[-4:]
            trecon5 = recon_p[4*int(len(recon_p)/6):5*int(len(recon_p)/6)]
            trecon5 = trecon5[-4:]
            trecon6 = recon_p[int(len(recon_p)/6):]
            trecon6 = trecon6[-4:]
            recon_fore = np.append(trecon1,trecon2) 
            recon_fore = np.append(recon_fore,trecon3)
            recon_fore = np.append(recon_fore,trecon4)
            recon_fore = np.append(recon_fore,trecon5)
            recon_fore = np.append(recon_fore,trecon6)
            recon_fore[recon_fore<0] = 0
        return recon_fore
    