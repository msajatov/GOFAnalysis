import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse
import evalgof
import os
from numpy import histogram

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
#     parser.add_argument('-m', dest='mode', help='Config to compare', default='')
    parser.add_argument('mode', nargs="*", help='Variable', default=[])
    parser.add_argument('-f', dest="failing", help='Variable', action="store_true")
    args = parser.parse_args()
    
    
    
    if not args.mode:
        variables = ["pt_1","pt_2","jpt_1","jpt_2","bpt_1","bpt_2","njets","nbtag","m_sv","mt_1",
                    "mt_2","pt_vis","pt_tt","mjj","jdeta","m_vis","dijetpt","met","eta_1","eta_2"]
        modes = ["nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
                   "nn13", "nn14", "nn15", "nn16", "nn17", "nn18"]
    else:
        modes = args.mode    
        
    for type in ["", "a", "a2", "e"]:
        df = getCompleteDataFrame(modes, type)    
        plotPValueHisto(df, type)       
    
    
def plotPValueHisto(df, type):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    fig = plt.figure(facecolor="w", figsize=(20, 15))
    df.hist(bins=20, ax=plt.axes())
    
    plotpath = "plots"
    
    test = "Saturated"
    
    plt.savefig(os.path.join(plotpath, "allChannels{0}_{1}.png".format(test, type)), bbox_inches="tight")
    plt.savefig(os.path.join(plotpath, "allChannels{0}_{1}.pdf".format(test, type)), bbox_inches="tight")
    
def getCompleteDataFrame(modes, type):   
    
    complete = pd.DataFrame()    
#     for test in ["saturated", "KS", "AD"]:    
    for test in ["saturated"]:        
        test_df = getDataFrameForTest(test, modes, type)
        
        if complete.empty:
            complete = pd.DataFrame(columns=test_df.columns)
            
        complete = complete.append(test_df, ignore_index=True)
        
    print complete
    return complete
    
def getDataFrameForTest(test, modes, type):
    print "getting df for {0}".format(test)
    
    et_df = evalgof.loadDF("output/et_pvalues.json")
    mt_df = evalgof.loadDF("output/mt_pvalues.json")
    tt_df = evalgof.loadDF("output/tt_pvalues.json")
    
    base = "cc"
    name = "custom"
            
    complete = pd.DataFrame()    
#     for ch in ["tt"]:
    for ch in ["et", "mt", "tt"]:
        print "getting df for {0}".format(ch)
        if ch == "tt":
            in_df = tt_df
            modes = replaceModesForTauTau(modes, type)
        elif ch == "et":
            in_df = et_df
        elif ch == "mt":
            in_df = mt_df
            
        configs = ["cc1", "cc2"] + modes
    
        cols = [base] + configs
            
        reduced = getReducedDataframe(in_df, ch, test, configs, cols)
        
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
    result = evalgof.compareSideBySideNew(df, "cc", configs, test, ch)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    
    return result

if __name__ == '__main__':
    main()