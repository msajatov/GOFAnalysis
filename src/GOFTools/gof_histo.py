import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse
import evalgof
import os
from numpy import histogram



def plotPValueHisto(df, type, testname):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    fig = plt.figure(facecolor="w", figsize=(20, 15))
    df.hist(bins=20, ax=plt.axes())
    
    plotpath = "histo_plots"
    
    plt.savefig(os.path.join(plotpath, "allChannels{0}_{1}.png".format(testname, type)), bbox_inches="tight")
    plt.savefig(os.path.join(plotpath, "allChannels{0}_{1}.pdf".format(testname, type)), bbox_inches="tight")
    
def getCompleteDataFrame(modes, type, tests):   
    
    complete = pd.DataFrame()    
#     for test in ["saturated", "KS", "AD"]:    
    for test in tests:        
        test_df = getDataFrameForTest(test, modes, type)
        
        if complete.empty:
            complete = pd.DataFrame(columns=test_df.columns)
            
        complete = complete.append(test_df, ignore_index=True)
        
    print complete
    return complete
    
def getDataFrameForTest(test, modes, type):
    print "getting df for {0}".format(test)    
    
    name = "custom"
            
    complete = pd.DataFrame()    
#     for ch in ["tt"]:
    for ch in ["et", "mt", "tt"]:
        print "getting df for {0}".format(ch)
        if ch == "tt":            
            modes = replaceModesForTauTau(modes, type)
            
        in_df = evalgof.loadDF("output6/{0}_pvalues.json".format(ch))            
            
        reduced = getReducedDataframe(in_df, ch, test, modes, modes)
        
        if ch == "tt":
            renamed = renameForTauTau(reduced, modes, type)
        else:
            renamed = reduced
        
        if complete.empty:
            complete = pd.DataFrame(columns=renamed.columns)
            print "created complete df"
        
        complete = complete.append(renamed, ignore_index=True)
    
    print complete
    return complete

def replaceModesForTauTau(modes, type):
    new = []
    for mode in modes:
        if type == "a":
            new.append(mode + "a")
        elif type == "a2":
            new.append(mode + "a2")
        elif type == "e":
            if mode in ["nn11", "nn12", "nn14", "nn16", "nn18"]:
                new.append(mode + "e")
            else:
                new.append(mode)
        else:
            new.append(mode)
        
    return new

def renameForTauTau(df, modes, type):
    for mode in modes:
        if type == "a":
            df = df.rename(columns = {mode:mode.replace("a","")})
        elif type == "a2":
            df = df.rename(columns = {mode:mode.replace("a2","")})
        elif type == "e":
            if mode in ["nn11e", "nn12e", "nn14e", "nn16e", "nn18e"]:
                df = df.rename(columns = {mode:mode.replace("e","")})
            
    return df
                

def getReducedDataframe(df, ch, test, configs, cols):
    result = evalgof.compareSideBySide(df, cols[0], cols[1:], test, ch)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    
    return result