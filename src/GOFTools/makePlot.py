import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import sys
import os
sys.path.append("../") # go to parent dir
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt



import argparse

import GOFTools.evalgof as evalgof

def plotWithThreshold(df, threshold):
    
    print "attempting to plot df: "
    print df
    
    print "cols: "
    print df.columns
    
    df.reset_index(inplace=True)
            
    df.plot(x='conf', y='pvalue')
    plt.show()
 
    
def getVarsInRange(df, lower, upper):         
    varsInRange = df.query("conf == 'cc'") \
                    .query("pvalue >= {0}".format(lower)) \
                    .query("pvalue < {0}".format(upper))
#     print "Vars between {0} and {1}: ".format(lower, upper)
#     print varsInRange
    return varsInRange
        
def plotPValues(df, confs):
    fig1 = plt.figure()
    
    for conf in confs:
#         subset = df.query(df['conf'] == conf & df['test'] == "saturated" & df['channel'] == "et")
#         subset = df.query("conf == '{0}'".format(conf))
#         print subset
                
        plt.plot(xrange(len(df)), df["pvalue"], label=conf)
        plt.xticks(np.arange(len(df)), df["conf"], rotation="vertical")
#         plt.plot(variables, df.query(df.name.str.contains(conf)), label=conf)


    
    
    
def plotPVal(df, label, marker, color):
    
#     fig1 = plt.figure()
    
    print df
    
    new = df[["conf", "pvalue"]]
    
    new = new.reset_index(drop=True)
    
    print new
    
    newer = new.set_index("conf")
    
    print newer
    
    newindex = ["cc", "cc1", "cc2", "nn1", "nn4", "nn23", "nn2", "nn3", "nn5", "nn6", "nn7", "nn8",
            "nn9", "nn10", "nn11", "nn12", "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn22"] 
    
    newest = newer.reindex(newindex)
    
    print newest
    
    newest = newest.reset_index()
    
    print newest
    
    plt.plot(xrange(len(newest)), newest["pvalue"], marker, color=color, markeredgecolor=color, label=label)
    plt.xticks(np.arange(len(newest)), newest["conf"], rotation="vertical")
         
#     plt.legend()
#     plt.show(block=True)

#     reordered = df[cols]
    
#     plt.plot(xrange(len(df)), df["pvalue"], label=conf)
#     plt.xticks(np.arange(len(df)), df["conf"], rotation="vertical")
#         
#     plt.legend()
#     plt.show(block=True)
    

    
def makePValuePlots(df, confs, channel, test):
    lower = [0, 0.25, 0.5, 0.75]
    upper = [0.25, 0.5, 0.75, 1.01]
    
    for i, val in enumerate(lower):
        filtered = df.query("test == '{0}'".format(test)) \
            .query("channel == '{0}'".format(channel))
        varsInRange = getVarsInRange(filtered, lower[i], upper[i])
        vars = list(set(varsInRange["var"]))
        
#         print "vars:"
#         for var in vars:
#             print var
        
        filteredByVars = df[df['var'].isin(vars)]
        
#         print filteredByVars
        
        subset = filteredByVars.query("test == '{0}'".format(test)) \
                    .query("channel == '{0}'".format(channel))
        
        plotPValues(subset, confs)


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
    
#     result = evalgof.compareSideBySide(df, "cc", configs, "KS", channel)
#     result = result.rename(columns = {"var":"variable"})
#     result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
#     
#     print result
#     
#     new = result[result].astype(float)
#     
#     row = result.iloc[12]
#     print row
#     
#     
#     row.plot()
#     
#     plt.show()

    
         
#     plotWithThreshold(newdf, 0.05)

    
    
    
    fig = plt.figure()
       
    test = "saturated"
    newdf = df.query("dc_type == 'emb_dc'") \
        .query("gof_mode == 'results_w_emb'") \
        .query("test == '{0}'".format(test)) \
        .query("channel == '{0}'".format(channel)) \
        .query("var == 'nbtag'")   
    
    plotPVal(newdf, "saturated", "v", "black")
    
       
    test = "KS"

    newdf = df.query("dc_type == 'emb_dc'") \
        .query("gof_mode == 'results_w_emb'") \
        .query("test == '{0}'".format(test)) \
        .query("channel == '{0}'".format(channel)) \
        .query("var == 'nbtag'")   
    
    plotPVal(newdf, "KS", "v", "green")
    
    
    test = "AD"
    newdf = df.query("dc_type == 'emb_dc'") \
        .query("gof_mode == 'results_w_emb'") \
        .query("test == '{0}'".format(test)) \
        .query("channel == '{0}'".format(channel)) \
        .query("var == 'nbtag'")   
    
    plotPVal(newdf, "AD", "v", "dodgerblue")
    
    plt.xlabel("Configuration")
    plt.ylabel("P-value")
    
    plt.legend(loc="upper left", numpoints=1)
#     plt.show(block=True)
    
    plotpath = "plots"
    if not os.path.exists(plotpath):
        os.mkdir(plotpath)
    plt.savefig(os.path.join(plotpath, "nbtag_tests.png"), bbox_inches="tight")
    plt.savefig(os.path.join(plotpath, "nbtag_tests.pdf"), bbox_inches="tight")
    
if __name__ == '__main__':
    main()



# def main(): 

    
#     baseconf = "cc"
#     #listFailingForConf(conf, failing, tests, channels)
#     
#     configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
#     
#     for conf in configs:
#         printFailingVariablesDifferentially(conf, baseconf, failing, tests, channels)
#     
# #     makePValuePlots(df, confs, "tt", "saturated")
# #         
# #     fig1 = plt.figure()
# #     plt.show()
# 
#     newdf = df.query("dc_type == 'emb_dc'") \
#         .query("gof_mode == 'results_w_emb'") \
#         .query("test == '{0}'".format(test)) \
#         .query("channel == '{0}'".format(channel)) \
#         .query("conf == '{0}'".format(conf)) \
#         
#     #plotWithThreshold(newdf, threshold)
#     
#     #plotPValues(newdf, ["cc"])





   
