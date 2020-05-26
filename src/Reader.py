import json
#import matplotlib as mpl
# mpl.use('Agg')
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
    


import Plotter


def main():
#     path = "output/gof.json"
#     full = load(path)
#  
# #     df = loadDF("")    
#     
#     test = "saturated"
#     channel = "et"
#     sampleData = full["emb_dc"]["results_w_emb"]["cc"]["mjj"][test][channel]
#     
#     print sampleData
#     
#     reformatedData = getReformatedData("125.0", test, channel, sampleData)
#     
#     print "before plotter"
#     Plotter.main("125.0", test, reformatedData)
    
    
    completeDF = loadCompleteDF("")
    
#     print completeDF
    
    #pvalueOnlyDF = pd.DataFrame(completeDF)
    #pvalueOnlyDF["pvalue"] = pvalueOnlyDF["pvalue"].map(lambda x: x["p"])
    
    #print pvalueOnlyDF
    
#     failing = completeDF[completeDF["pvalue"] < 0.05]    
#     print failing
        
    test = "saturated"
    channel = "tt"
    var = "pt_2"
    
    selection = completeDF.query("test == '{0}'".format(test)) \
                .query("channel == '{0}'".format(channel)) \
                .query("gof_mode == '{0}'".format("results_w_emb")) \
                .query("dc_type == '{0}'".format("emb_dc")) \
                .query("var == '{0}'".format(var))
                
    print selection

def getReformatedData(mass, test, channel, data):
    if test in ["KS", "AD"]:
        result = {}
        result[mass] = {}
        result[mass]["htt_{0}_100_Run2017".format(channel)] = data
    else:
        result = {}
        result[mass] = data        
    return result
        

def loadDF(relpath):
    
    path = "output/gof.json"
    pvalues = load(path)
    
    # pvalues[dc_type][gof_mode][conf][var][test][channel]
    
    ignorevars = ["eta_1", "eta_2"]
    
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
                            new_row = {'dc_type':dc_type_key, 'gof_mode':gof_mode_key, 'conf':confkey, 'var':varkey, 'test':testkey, 'channel':chkey, 'pvalue':chval["p"]}
                            rows_list.append(new_row)
        #                     df = df.append(new_row, ignore_index=True)
                    
            
    df = pd.DataFrame(rows_list, columns=["dc_type", "gof_mode", "conf", "var", "test", "channel", "pvalue"])     
    df = df[~df['var'].isin(ignorevars)]
    return df

def loadCompleteDF(relpath):
    
    path = "output/gof.json"
    pvalues = load(path)
    
    # pvalues[dc_type][gof_mode][conf][var][test][channel]
    
    ignorevars = ["eta_1", "eta_2"]
    
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
                            new_row = {'dc_type':dc_type_key, 'gof_mode':gof_mode_key, 'conf':confkey, 'var':varkey, 'test':testkey, 'channel':chkey, \
                                       'pvalue':chval["p"], 'obs':chval["obs"], 'toy':chval["toy"], 'gof':chval}
                            rows_list.append(new_row)
        #                     df = df.append(new_row, ignore_index=True)
                    
            
    df = pd.DataFrame(rows_list, columns=["dc_type", "gof_mode", "conf", "var", "test", "channel", "pvalue", "obs", "toy", "gof"])     
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