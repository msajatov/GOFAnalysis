import json
#import matplotlib as mpl
# mpl.use('Agg')
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
sys.path.append("../") # go to parent dir


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


def compareFailingVars(df, channel, modes=[]):
    dc_types = ["emb_dc"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    gof_modes = ["results_w_emb"]
    
    if "all" in channel:
        confs = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", 
                 "nn16", "nn17", "nn18", "nn21"]
        channels = ["et", "mt", "tt"]
    else:
        confs = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", 
                 "nn15a", "nn16", "nn16a", "nn17", "nn17a", "nn18", "nn18a", "nn19", "nn20"]
        channels = ["tt"]
    variables = []
    tests = ["saturated", "KS", "AD"]
    
    
    failingVarComp = FailingVariableComparer(dc_types, gof_modes, confs, variables, tests, channels)
    failingVarComp.set_threshold(0.05)
    failingVarComp.printFailingVariables(df, ["conf", "channelconf", "testchannelconf"])
     
#     baseconf = "cc"
#     configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
#      
#     failingVarComp.compareAgainstBase(df, baseconf, configs)

def compareAgainstBase(df):
    dc_types = ["emb_dc"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    gof_modes = ["results_w_emb"]
    confs = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", "nn16", "nn17", "nn18"]
    variables = []
    tests = ["saturated", "KS", "AD"]
    channels = ["et", "mt", "tt"]
    
    failingVarComp = FailingVariableComparer(dc_types, gof_modes, confs, variables, tests, channels)
    failingVarComp.set_threshold(0.05)
     
    baseconf = "cc"
    configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", "nn16", "nn17", "nn18"]
      
    failingVarComp.compareAgainstBase(df, baseconf, configs)    


def main():      
    
    print "Sorry, not implemented. Use this as part of a module and call the functions."
#     df = loadDF("../output/{0}_pvalues.json".format(args.channel))
    
#     result = compareSideBySide(df, "cc", configs, "saturated", "et")
#     
#     print result

#     compareFailingVars(df, args.channel)


def compareSideBySide(df, baseconf, configs, test="saturated", channel="et"):  
    subset = df.query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))                        
        
    subset = subset.sort_values(by=["var", "conf"])
    basedf = subset.query("conf == '{0}'".format(baseconf))  
    basedf = basedf.rename(columns = {"pvalue":baseconf})
    basedf = basedf.drop("conf", axis=1)   
    #print basedf
    
    result = basedf
    
    for conf in configs: 
        confdf = subset.query("conf == '{0}'".format(conf))
        confdf = confdf.rename(columns = {"pvalue":conf})
        confdf = confdf.drop("conf", axis=1)   
        #print confdf            
        
        result = pd.merge(result, confdf, on=["dc_type", "gof_mode", "var", "test", "channel"])
        
    #printWithStyle(result)
    #applyStyle(result)
    return result
        
        
def printWithStyle(df):
    columns = list(df.columns)
    columns.remove("dc_type")
    columns.remove("gof_mode")
    columns.remove("var")
    columns.remove("test")
    columns.remove("channel")
    
    df.style.apply(color_negative_red, subset=columns, axis=1)
    widget1 = widgets.Output()
    with widget1:
        display.display(df)
    hbox = widgets.HBox([widget1])
    hbox  
    
def applyStyle(df):
    columns = list(df.columns)
    columns.remove("dc_type")
    columns.remove("gof_mode")
    columns.remove("var")
    columns.remove("test")
    columns.remove("channel")
    
    #print columns
    df.style.apply(color_negative_red, subset=columns, axis=1)

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
                        
            
class FailingVariableComparer():
    def __init__(self, dc_types, gof_modes, confs, variables, tests, channels):
        self.dc_types = dc_types
        self.gof_modes = gof_modes
        self.confs = confs
        self.variables = variables
        self.tests = tests
        self.channels = channels
        self.threshold = 0.05
        
    def set_threshold(self, threshold):
        self.threshold = threshold
        
    def getFailingVariables(self, df):
        failing = df.query("pvalue <= {0}".format(self.threshold))
        return failing
        
    def printFailingVariables(self, df, modes=[]):
        failing = self.getFailingVariables(df)
                
        if not modes :
            self.printByConf(failing)
            self.printByTestConf(failing)
            self.printByChannelConf(failing)
            self.printByTestChannelConf(failing)
        else:
            if "conf" in modes:
                self.printByConf(failing)
            if "testconf" in modes:
                self.printByTestConf(failing)
            if "channelconf" in modes:
                self.printByChannelConf(failing)
            if "testchannelconf" in modes:
                self.printByTestChannelConf(failing)
            
            
    def compareAgainstBase(self, df, baseconf, configs):
        for conf in configs:
            self.printFailingVariablesDifferentially(df, baseconf, conf)                
    
    def printByConf(self, failing):
        for conf in self.confs:
            f = failing.query("conf == '{0}'".format(conf))
            vars = list(set(f["var"]))
            print "failing for {0}: {1}    {2}".format(conf, len(f), vars)
    
    def printByTestConf(self, failing):
        for test in self.tests:
            for conf in self.confs:
                f = failing.query("conf == '{0}'".format(conf)) \
                            .query("test == '{0}'".format(test))
                vars = list(set(f["var"]))
                print "failing for {0} {1}: {2}    {3}".format(test, conf, len(f), vars)#
            print ""
    
    def printByChannelConf(self, failing):
        for channel in self.channels:
            for conf in self.confs:
                f = failing.query("conf == '{0}'".format(conf)) \
                            .query("channel == '{0}'".format(channel))
                vars = list(set(f["var"]))
                print "failing for {0} {1}: {2}    {3}".format(channel, conf, len(f), vars)
            print ""
    
    def printByTestChannelConf(self, failing):
        for test in self.tests:
            for channel in self.channels:
                for conf in self.confs:
                    f = failing.query("conf == '{0}'".format(conf)) \
                                .query("test == '{0}'".format(test)) \
                                .query("channel == '{0}'".format(channel))
                    vars = list(set(f["var"]))
                    print "failing for {0} {1} {2}: {3}    {4}".format(test, channel, conf, len(f), vars)
                print ""
            print ""
    
    def printFailingVariablesDifferentially(self, df, baseconf, conf, verbose=True):        
        failing = self.getFailingVariables(df)
        for test in self.tests:
            for channel in self.channels:
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
                                
                if verbose:
                    diff_failing_union = failing_comp_only + failing_base_only                    
                    print "comparison:"
                    dfcomparison = df[df['var'].isin(diff_failing_union)]
                    dfcomparison = dfcomparison[dfcomparison['conf'].isin([conf, baseconf])] \
                            .query("test == '{0}'".format(test)) \
                            .query("channel == '{0}'".format(channel))
                    print dfcomparison
                
            print ""
            
    def showSideBySide2(self, df, baseconf, configs, test="saturated", channel="et"):  
        subset = df.query("test == '{0}'".format(test)) \
                            .query("channel == '{0}'".format(channel))                        
            
        subset = subset.sort_values(by=["var", "conf"])
        basedf = subset.query("conf == '{0}'".format(baseconf))  
        basedf = basedf.rename(columns = {"pvalue":baseconf})
        basedf = basedf.drop("conf", axis=1)   
        print basedf
        
        result = basedf
        
        for conf in configs: 
            confdf = subset.query("conf == '{0}'".format(conf))
            confdf = confdf.rename(columns = {"pvalue":conf})
            confdf = confdf.drop("conf", axis=1)   
            print confdf            
            
            result = pd.merge(result, confdf, on=["dc_type", "gof_mode", "var", "test", "channel"])
            
        print result
        
        
#         widget1 = widgets.Output()
#         with widget1:
#             display.display(subset)
#         hbox = widgets.HBox([widget1])
#         hbox  
            
    def showSideBySide(self, df, baseconf, conf, test="saturated", channel="et"):    
        subset = df[df['conf'].isin([conf, baseconf])]        
        #print subset
        
        subset = subset.query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))
                        
        #print subset
        
        subset = subset.sort_values(by=["var", "conf"])
        #print subset
        
        subset.style.apply(highlight_greaterthan_1, axis=1)
        
        #display(subset)
        
        # create output widgets
        widget1 = widgets.Output()
        #widget2 = widgets.Output()
        
        # render in output widgets
        with widget1:
            display.display(subset)
        #with widget2:
            #display.display(df2)
        
        # create HBox
        #hbox = widgets.HBox([widget1, widget2])
        hbox = widgets.HBox([widget1])
        
        # render hbox
        hbox
        
        #dff.groupby('B').filter(lambda x: len(x['C']) > 2)



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
        return
    except IOError as e:
        print "IOError while parsing pvalues"
        print e
        return
    return pvalues
    
if __name__ == '__main__':
    main()
