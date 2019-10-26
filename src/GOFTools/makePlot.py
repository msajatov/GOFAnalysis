import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import sys
sys.path.append("../") # go to parent dir

import argparse

import GOFTools.evalgof as evalgof




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

#     makeHtml(args.channel, modes, args.failing)
    
    if "all" in args.channel:
        channels = ["et", "mt", "tt"]
    else:                     
        channels = ["tt"]
    
    mtet_df = evalgof.loadDF("../output/all_pvalues.json")
    tt_df = evalgof.loadDF("../output/tt_pvalues.json")
        
    base = "cc"
    name = "custom"
    
    configs = ["cc1", "cc2"] + modes
    
    cols = [base] + configs
    
    plotAllTests("mt", "nbtag", mtet_df, configs)
    

def plotAllTests(channel, variable, df, configs):
    
    result = evalgof.compareSideBySide(df, "cc", configs, "KS", channel)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    
    print result
    
    indexrow = result.columns
    print indexrow
    row = result.iloc[12]
    print row
    
    import matplotlib.pyplot as plt
    
    plt.plot(indexrow, row)
    
if __name__ == '__main__':
    main()
