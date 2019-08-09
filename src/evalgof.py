import json
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    #path = "output3/pvalues3.json"
    path = "output/pvalues.json"
    pvalues = load(path)
    
    # pvalues[conf][var][test][channel]
    
    dc_types = ["mc_dc"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    gof_modes = ["results_w_emb"]
    confs = []
    variables = []
    tests = ["saturated", "KS", "AD"]
    channels = ["et", "mt", "tt"]
           
        
    temp = next(pvalues.itervalues())
    temp = next(temp.itervalues())
    
    for key, value in temp.items():
        #print key
        confs.append(key)
        
    temp = next(temp.itervalues())
    for key, value in temp.items():
        #print key
        variables.append(key)
        
#         
#     from pandas.io.json import json_normalize
#     json_normalize(pvalues)
#     
#     print pvalues

#     flattened = flatten_json(pvalues)
#     print flattened

    df = pd.DataFrame(columns=["dc_type", "gof_mode", "conf", "var", "test", "channel", "pvalue"])
        
    # this is much faster than adding to the df row by row
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
    #print df
    
#     embComparer = EmbComparer(df, dc_types, gof_modes, confs, variables, tests, channels)
#     embComparer.compareEmbedding()
#     
#     return
    
    
    threshold = 0.05
    failing = df.query("pvalue < {0}".format(threshold))
    
#     failing = getFailingVars(df, 0.05, "cc", "et", "saturated")

    failing = failing.query("dc_type == 'mc_dc'")
    failing = failing.query("gof_mode == 'results_w_emb'")
    
    #print "failing:"
    #print failing
    
    for conf in confs:
        f = failing.query("conf == '{0}'".format(conf))
        vars = list(set(f["var"]))
        print "failing for {0}: {1}    {2}".format(conf, len(f), vars)
        
    print "\n"
    
    for test in tests:
        for conf in confs:
            f = failing.query("conf == '{0}'".format(conf)) \
                        .query("test == '{0}'".format(test))
            vars = list(set(f["var"]))
            print "failing for {0} {1}: {2}    {3}".format(test, conf, len(f), vars)#
        print ""
            
    print "\n"
    
    for channel in channels:
        for conf in confs:
            f = failing.query("conf == '{0}'".format(conf)) \
                        .query("channel == '{0}'".format(channel))
            vars = list(set(f["var"]))
            print "failing for {0} {1}: {2}    {3}".format(channel, conf, len(f), vars)
        print ""
        
    for test in tests:
        for channel in channels:
            for conf in confs:
                f = failing.query("conf == '{0}'".format(conf)) \
                            .query("test == '{0}'".format(test)) \
                            .query("channel == '{0}'".format(channel))
                vars = list(set(f["var"]))
                print "failing for {0} {1} {2}: {3}    {4}".format(test, channel, conf, len(f), vars)#
            print ""
        print ""
            
#     for channel in channels:
#         for test in tests:
#             for conf in confs:
#                 f = failing.query("conf == '{0}'".format(conf)) \
#                             .query("test == '{0}'".format(test)) \
#                             .query("channel == '{0}'".format(channel))
#                 print "failing for {0} {1} {2}: {3}".format(channel, test, conf, len(f))#
#             print ""
#         print ""
#             
#     print "\n"
    
    baseconf = "cc"
    #listFailingForConf(conf, failing, tests, channels)
    
    configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
    
    for conf in configs:
        printFailingVariablesDifferentially(conf, baseconf, failing, tests, channels)
    
#     makePValuePlots(df, confs, "tt", "saturated")
#         
#     fig1 = plt.figure()
#     plt.show()

    newdf = df.query("dc_type == 'emb_dc'") \
        .query("gof_mode == 'results_w_emb'") \
        .query("test == '{0}'".format(test)) \
        .query("channel == '{0}'".format(channel)) \
        .query("conf == '{0}'".format(conf)) \
        
    #plotWithThreshold(newdf, threshold)
    
    #plotPValues(newdf, ["cc"])


def plotWithThreshold(df, threshold):
    
    print "attempting to plot df: "
    print df
    
    print "cols: "
    print df.columns
    
    df.reset_index(inplace=True)
            
    df.plot(x='var', y='pvalue')
    plt.show()

class EmbComparer():
    def __init__(self, df, dc_types, gof_modes, confs, variables, tests, channels):
        self.df = df
        self.dc_types = dc_types
        self.gof_modes = gof_modes
        self.confs = confs
        self.variables = variables
        self.tests = tests
        self.channels = channels
        pass

    def compareEmbedding(self):
#         threshold = 0.05
#         failing = self.df.query("pvalue < {0}".format(threshold))
#         print failing
#         failing = failing.query("dc_type == 'mc_dc'")
#         failing = failing.query("gof_mode == 'results_wo_emb'")
        for test in self.tests:
            for channel in self.channels:
                for conf in self.confs:       
                    for variable in self.variables:             
#                     for dc_type in self.dc_types:
#                         for gof_mode in self.gof_modes:             
#                     f = failing.query("dc_type == '{0}'".format(dc_type)) \
#                                 .query("gof_mode == '{0}'".format(gof_mode)) \
#                                 .query("conf == '{0}'".format(conf)) \
#                                 .query("test == '{0}'".format(test)) \
#                                 .query("channel == '{0}'".format(channel))
                                
                        f = self.df.query("conf == '{0}'".format(conf)) \
                                    .query("test == '{0}'".format(test)) \
                                    .query("channel == '{0}'".format(channel)) \
                                    .query("var == '{0}'".format(variable))
                                    
                        print f
#                             print "failing for {0} {1} {2}: {3}".format(test, channel, conf, len(f))#
                        print ""
                    print ""
                print ""
            print ""
            data = self.df.query()
    

def printFailingVariablesDifferentially(conf, baseconf, failing, tests, channels):
        
    for test in tests:
        for channel in channels:
            f = failing.query("conf == '{0}'".format(conf)) \
                        .query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))
                        
            fbase = failing.query("conf == '{0}'".format(baseconf)) \
                        .query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))
                        
            vars = list(f["var"])
            basevars = list(fbase["var"])
                        
            failing_comp_only = []
            for v in vars:
                if v not in basevars:
                    failing_comp_only.append(v)
            
            print "failing for {0} {1} {2} but NOT {3}: {4}    {5}".format(test, channel, conf, baseconf, len(failing_comp_only), failing_comp_only)
            
            failing_base_only = []
            for v in basevars:
                if v not in vars:
                    failing_base_only.append(v)
            
            print "failing for {0} {1} {3} but NOT {2}: {4}    {5}".format(test, channel, conf, baseconf, len(failing_base_only), failing_base_only)
        print ""

def listFailingForConf(conf, failing, tests, channels):
    print "failing for {0}:".format(conf)
    print failing.query("conf == '{0}'".format(conf))
    
    print "\n"
    
    for test in tests:
        f = failing.query("conf == '{0}'".format(conf)) \
                    .query("test == '{0}'".format(test))
        print "failing for {0} {1}: {2}".format(test, conf, len(f))#
        print f
        print ""
            
    print "\n"
    
    for channel in channels:
        f = failing.query("conf == '{0}'".format(conf)) \
                    .query("channel == '{0}'".format(channel))
        print "failing for {0} {1}: {2}".format(channel, conf, len(f))
        print f
        print ""
        
        
    for test in tests:
        for channel in channels:
            f = failing.query("conf == '{0}'".format(conf)) \
                        .query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))
            print "failing for {0} {1} {2}: {3}".format(test, channel, conf, len(f))#
            print f
            print ""
        print ""
        
    print "\n"
            
#     for channel in channels:
#         for test in tests:
#             f = failing.query("conf == '{0}'".format(conf)) \
#                         .query("test == '{0}'".format(test)) \
#                         .query("channel == '{0}'".format(channel))
#             print "failing for {0} {1} {2}: {3}".format(channel, test, conf, len(f))#
#             print ""
#             print f
#         print ""
#             
#     print "\n"
    
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
        plt.xticks(np.arange(len(df)), df["var"], rotation="vertical")
#         plt.plot(variables, df.query(df.name.str.contains(conf)), label=conf)

    plt.legend()
    plt.show(block=True)
    

    
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

def getFailingVars(df, threshold, conf, channel, test):
    filtered = df.query("test == '{0}'".format(test)) \
                .query("channel == '{0}'".format(channel)) \
                .query("conf == '{0}'".format(conf)) \
                .query("pvalue < {0}".format(threshold))
    
#     print filtered           
    return filtered

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
    
def load(path):
    try:
        with open(path, "r") as FSO:
            pvalues = json.load(FSO)
    except ValueError as e:
        print e
        print "ValueError while parsing pvalues"
    except IOError as e:
        print "IOError while parsing pvalues"
        print e
    return pvalues
    
if __name__ == '__main__':
    main()
