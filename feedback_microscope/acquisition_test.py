# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pycromanager as pm



if __name__=='__main__':
    

    with pm.Acquisition(directory='C:/Users/Jean/Documents/Python Scripts/feedback_microscope', name='acquisition_name') as acq:
        
        events = pm.multi_d_acquisition_events(z_start=0, z_end=10, z_step=0.5)
        acq.acquire(events)