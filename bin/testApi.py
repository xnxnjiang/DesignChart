# -*- coding: utf-8 -*-
"""
Created on Mo May 17 14:29:50 2018

@author: xnjiang
"""

import sys
sys.path.append("..")

from api.dcApi import*

if __name__ == "__main__":
    app = showDC()
    dcSetColorOfState("busy", "orange")
    dcSetModuleState("top.inst_tcdx[0]", stateReady)#set module state
    dcSetPortState("top.inst_tcdx[0]", "fti_inp_0", stateFail)
    dcSetPortState("top.inst_tcdx[0]", "fti_out_0", statePass)
    dcSetPortState("top.inst_tcdx[0]", "fti_inp_1", stateBusy)
    dcSetPortState("top.inst_tcdx[0]", "fti_out_1", stateStandby)
    dcSetPortState("top.inst_tcdx[0]", "fti_inp_2", stateReady)
    dcSetPortState("top.inst_tcdx[0]", "fti_out_2", stateStandby)
    dcSetModuleState("top.inst_tcdx[0]", "")#clear moudle state
    importDesign("debug.xml")
    runDC()
#    exitDC()
