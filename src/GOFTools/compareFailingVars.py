import json
import pandas as pd
import numpy as np
import sys
import argparse
sys.path.append("../") # go to parent dir

import GOFTools.evalgof as evalgof
    
def main():      
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    args = parser.parse_args()
    
    print args.channel
    df = loadDF("../output/{0}_pvalues.json".format(args.channel))

    evalgof.compareFailingVars(df, args.channel)
    
def loadDF(relpath):
    
    pvalues = load(relpath)
    
    # pvalues[dc_type][gof_mode][conf][var][test][channel]
    
    ignorevars = ["eta_1", "eta_2"]
    #ignorevars = []
    
    dc_types = ["emb_dc"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    gof_modes = ["results_w_emb"]
    confs = []
    variables = []
    tests = ["saturated", "KS", "AD"]
    channels = ["et", "mt", "tt"]
    
    temp = next(pvalues.itervalues())
    temp = next(temp.itervalues())
    
    for key, value in temp.items():
        confs.append(key)
        
    temp = next(temp.itervalues())
    for key, value in temp.items():
        variables.append(key)
    
    for igv in ignorevars:
        variables.remove(igv)
    
    rows_list = []
    for dc_type_key, dc_type_val in pvalues.items():
        for gof_mode_key, gof_mode_val in dc_type_val.items():            
            for confkey, confval in gof_mode_val.items():
                for varkey, varval in confval.items():
                    for testkey, testval in varval.items():
                        for chkey, chval in testval.items():
                            new_row = {'dc_type':dc_type_key, 'gof_mode':gof_mode_key, 'conf':confkey, 'var':varkey, 'test':testkey, 'channel':chkey, 'pvalue':chval}
                            rows_list.append(new_row)
        #                     df = df.append(new_row, ignore_index=True)
                    
            
    df = pd.DataFrame(rows_list, columns=["dc_type", "gof_mode", "conf", "var", "test", "channel", "pvalue"])     
    df = df[~df['var'].isin(ignorevars)]
    return df
    
def load(path):
    try:
        with open(path, "r") as FSO:
            pvalues = json.load(FSO)
    except ValueError as e:
        print e
        print "ValueError while parsing pvalues"
        return
    except IOError as e:
        print "IOError while parsing pvalues"
        print e
        return
    return pvalues
    
if __name__ == '__main__':
    main()
