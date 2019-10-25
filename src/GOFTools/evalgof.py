import json
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
        confs = ["cc", "cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
                 "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn21", "nn22", "nn23"]
        channels = ["et", "mt", "tt"]
    else:
        confs = ["cc", "cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", 
                          "nn11", "nn12", "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn19", "nn20",                          
                          "nn1a2", "nn2a2", "nn3a2", "nn4a2", "nn5a2", "nn6a2", "nn7a2", "nn8a2", "nn9a2", "nn10a2", 
                          "nn11a2", "nn12a2", "nn13a2", "nn14a2", "nn15a2", "nn16a2", "nn17a2", "nn18a2",
                          "nn11e", "nn12e", "nn14e", "nn16e", "nn18e",
                          "nn1a", "nn2a", "nn3a", "nn4a", "nn5a", "nn6a", "nn7a", "nn8a", "nn9a", "nn10a",
                          "nn11a", "nn12a", "nn13a", "nn14a", "nn15a", "nn16a", "nn17a", "nn18a", "nn22a", "nn23a", "xx"]
        channels = ["tt"]
    variables = []
    tests = ["saturated", "KS", "AD"]
    
    
    failingVarComp = FailingVariableComparer(dc_types, gof_modes, confs, variables, tests, channels)
    failingVarComp.set_threshold(0.05)
    f = failingVarComp.printFailingVariables(df, ["conf", "channelconf", "testchannelconf", "channelconfshort"])
    
    return f
     
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


def saveCsv(df, filename):
    csv = df.to_csv(index=False, sep=";")
    file = open(filename, "w+")
    file.write(csv)
    file.close()

def compareSideBySide(df, baseconf, configs, test="saturated", channel="et", merge_on=["dc_type", "gof_mode", "var", "test", "channel"]):  
    subset = df.query("test == '{0}'".format(test)) \
                        .query("channel == '{0}'".format(channel))  
    
    # only keep necessary columns (otherwise problems with merge)
    subset = subset.loc[:, merge_on + ["pvalue"] + ["conf"]]    
    print "subset:"
    print subset                      
        
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
        
        result = pd.merge(result, confdf, on=merge_on)
        
    return result
                      
            
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
            f = self.printByTestChannelConf(failing)
        else:
            if "conf" in modes:
                self.printByConf(failing)
            if "testconf" in modes:
                self.printByTestConf(failing)
            if "channelconf" in modes:
                self.printByChannelConf(failing)
            if "testchannelconf" in modes:
                f = self.printByTestChannelConf(failing, False)
                self.printByTestChannelConf(failing, True)
            if "channelconfshort" in modes:
                self.printByChannelConf(failing, True)
                
        print f
        return f
            
            
    def compareAgainstBase(self, df, baseconf, configs):
        for conf in configs:
            self.printFailingVariablesDifferentially(df, baseconf, conf)                
    
    def printByConf(self, failing):
        fail = {}
        for conf in self.confs:
            f = failing.query("conf == '{0}'".format(conf))
            vars = list(set(f["var"]))
            print "failing for {0}: {1}    {2}".format(conf, len(f), vars)
            fail[conf] = len(f)
    
    def printByTestConf(self, failing):
        fail = {}
        for test in self.tests:
            fail[test] = {}
            for conf in self.confs:
                f = failing.query("conf == '{0}'".format(conf)) \
                            .query("test == '{0}'".format(test))
                vars = list(set(f["var"]))
                print "failing for {0} {1}: {2}    {3}".format(test, conf, len(f), vars)#
                fail[test][conf] = len(f)
            print ""
        
    
    def printByChannelConf(self, failing, short=False):
        fail = {}
        for channel in self.channels:
            fail[channel] = {}
            for conf in self.confs:
                f = failing.query("conf == '{0}'".format(conf)) \
                            .query("channel == '{0}'".format(channel))
                vars = list(set(f["var"]))
                print "failing for {0} {1}: {2}    {3}".format(channel, conf, len(f), vars)
                fail[channel][conf] = len(f)
            print ""
            
        if short:
            for channel in self.channels:
                for conf in self.confs:
                    f = failing.query("conf == '{0}'".format(conf)) \
                                .query("channel == '{0}'".format(channel))
                    vars = list(set(f["var"]))
                    print "{1};{2}".format(channel, conf, len(f), vars)
                print ""
    
    def printByTestChannelConf(self, failing, short=False):
        fail = {}
        for test in self.tests:
            fail[test] = {}
            for channel in self.channels:
                fail[test][channel] = {}
                for conf in self.confs:
                    f = failing.query("conf == '{0}'".format(conf)) \
                                .query("test == '{0}'".format(test)) \
                                .query("channel == '{0}'".format(channel))
                    vars = list(set(f["var"]))
                    print "failing for {0} {1} {2}: {3}    {4}".format(test, channel, conf, len(f), vars)
                    fail[test][channel][conf] = len(f)
                print ""
            print ""
            
        if short:
            for test in self.tests:
                for channel in self.channels:
                    print "{0}, {1}".format(test, channel)
                    for conf in self.confs:
                        f = failing.query("conf == '{0}'".format(conf)) \
                                    .query("test == '{0}'".format(test)) \
                                    .query("channel == '{0}'".format(channel))
                        vars = list(set(f["var"]))
                        print "{3}".format(test, channel, conf, len(f), vars)
                    print ""
                print ""
                
        return fail
    
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
