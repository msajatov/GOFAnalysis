import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse

import evalgof as evalgof


defaultConfigs = ["cc", "cc1", "cc2", "nn1", "nn6", "nn13", "nn21"]


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('-t', dest='test', help='Test', choices = ['saturated', 'KS', 'AD', 'all'], default='all')
    parser.add_argument('configs', nargs="*", help='Configurations', default=[])
    parser.add_argument('-m', dest='method', help='Method to use', default=[])
    parser.add_argument('-tt', dest='tt_variant', help='tt Variant', choices = ['vanilla', 'a', 'a2', 'e'], default='vanilla')
    args = parser.parse_args()


    switcher = {
        "list": listFailing,
        "html": makeHtml,
        "pdf": makePdf,
        "csv": makeCsv,
        "print": printToConsole,
        "latex": makeLatex,
        "histo": makeHisto,
        "plot": makePlot
    }
    
    if not args.method in switcher:
        print "Invalid method"
        return
    # Get the function from switcher dictionary
    func = switcher.get(args.method, None)
    # Execute the function
    func(args)

def listFailing(args):    
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
        
    completedf = pd.DataFrame()
        
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        completedf = completedf.append(df, ignore_index=True)   
        
    if "all" in args.channel:
        f = evalgof.compareFailingVarsNew(completedf, channels, configs)
    else:
        for ch in channels:
            df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
            f = evalgof.compareFailingVarsNew(df, [ch], configs)     

def makeHtml(args):
    pass

def makePdf(args):
    pass

def makeCsv(args):
    in_df = evalgof.loadDF("output/{0}_pvalues.json".format(args.channel))    
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
    add_failing = False
    
    for ch in channels:
        for test in ["saturated", "KS", "AD"]:
            if add_failing:
                result = getCompact(in_df, ch, test, configs)   
                print result 
                csv = result.to_csv(index=False, sep=";")
                print csv
                
                #add failing using evalgof.compareFailingVarsNew(in_df, channel)
            else:
                result = getCompact(in_df, ch, test, configs)
                print result
                csv = result.to_csv(index=False, sep=";")
                print csv

def printToConsole(args):    
    in_df = evalgof.loadDF("output/{0}_pvalues.json".format(args.channel))    
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
    add_failing = False
    
    for ch in channels:
        for test in ["saturated", "KS", "AD"]:
            if add_failing:
                result = getCompact(in_df, ch, test, configs)   
                print result 
                
                #add failing using evalgof.compareFailingVarsNew(in_df, channel)
            else:
                result = getCompact(in_df, ch, test, configs)
                print result
            



        


def makeLatex(args):
    pass

def makeHisto(args):
    import gof_histo
    
    modes = args.configs
    print "modes:"
    print modes
    
    tests = ["saturated", "KS", "AD"]
    
#     for type in ["", "a", "a2", "e"]:
    for type in [""]:
        for test in tests:
            df = gof_histo.getCompleteDataFrame(modes, type, [test])    
            gof_histo.plotPValueHisto(df, type, test)
            
        df = gof_histo.getCompleteDataFrame(modes, type, tests)    
        gof_histo.plotPValueHisto(df, type, "allTests")

def makePlot(args):
    pass


def getCompact(df, ch, test, configs):
    result = evalgof.compareSideBySideNew(df, configs[0], configs[1:], test, ch)
    result = result.rename(columns = {"channel":"ch"})
    result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
    return result




if __name__ == '__main__':
    main()