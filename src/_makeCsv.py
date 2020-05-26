import json
import pandas as pd
import numpy as np
import sys
sys.path.append("../") # go to parent dir

import argparse

import GOFTools.evalgof

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('mode', nargs="*", help='Variable', default=[])
    args = parser.parse_args()
    
    if not args.mode:
        modes = []
    else:
        modes = args.mode

    makeCsv(args.channel, modes)
    
    
def makeCsv(channel, modes):
    reload(GOFTools.evalgof)
    from IPython.display import display, HTML
    import GOFTools.evalgof as evalgof
    df = evalgof.loadDF("../output/{0}_pvalues.json".format(channel))
    
    print df
    
    if not modes:
        base = "cc"
        if "all" in channel:
            configs = ["cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
                   "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn21"]
            channels = ["et", "mt", "tt"]
        else:
            
    #         vanilla
            configs = ["cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
                       "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn19", "nn20"]
            
    #         aiso2
    #         configs = ["cc1", "cc2", "nn1a2", "nn2a2", "nn3a2", "nn4a2", "nn5a2", "nn6a2", "nn7a2", "nn8a2", "nn9a2", "nn10a2", 
    #                     "nn11a2", "nn12a2","nn13a2", "nn14a2", "nn15a2", "nn16a2", "nn17a2", "nn18a2"]
    
    #         aiso
    #         configs = ["cc1", "cc2", "nn1a", "nn2a", "nn3a", "nn4a", "nn5a", "nn6a", "nn7a", "nn8a", "nn9a", "nn10a", 
    #                     "nn11a", "nn12a","nn13a", "nn14a", "nn15a", "nn16a", "nn17a", "nn18a"]
            
    #         emb
    #         configs = ["cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11e", "nn12e",
    #                     "nn13", "nn14e", "nn15", "nn16e", "nn17", "nn18e"]
            
            channels = ["tt"]
        
        cols = [base] + configs
        
        for ch in channels:    
            
            result = evalgof.compareSideBySide(df, "cc", configs, "saturated", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
                        
            saveCsv(result, "{0}_{1}_complete.csv".format(ch, "saturated"))
            
            result = evalgof.compareSideBySide(df, "cc", configs, "KS", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
                        
            saveCsv(result, "{0}_{1}_complete.csv".format(ch, "KS"))
            
            result = evalgof.compareSideBySide(df, "cc", configs, "AD", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
            
            saveCsv(result, "{0}_{1}_complete.csv".format(ch, "AD"))  
            
    else:
        base = "cc"
        name = "custom"
        if "all" in channel:
            configs = ["cc1", "cc2"] + modes
            channels = ["et", "mt", "tt"]
        else:            
            configs = ["cc1", "cc2"] + modes            
            channels = ["tt"]
        
        cols = [base] + configs
        
        for ch in channels:    
            result = evalgof.compareSideBySide(df, "cc", configs, "saturated", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
                        
            saveCsv(result, "{0}_{1}_{2}.csv".format(ch, "saturated", name))
            
            result = evalgof.compareSideBySide(df, "cc", configs, "KS", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
                        
            saveCsv(result, "{0}_{1}_{2}.csv".format(ch, "KS", name))
            
            result = evalgof.compareSideBySide(df, "cc", configs, "AD", ch)
            result = result.rename(columns = {"channel":"ch"})
            result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
            
            saveCsv(result, "{0}_{1}_{2}.csv".format(ch, "AD", name))  
            
def saveCsv(df, filename):
    csv = df.to_csv(index=False, sep=";")
    file = open(filename, "w+")
    file.write(csv)
    file.close()
 
    
if __name__ == '__main__':
    main()
