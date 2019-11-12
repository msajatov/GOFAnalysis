import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse
import os

import evalgof as evalgof


defaultConfigs = ["cc", "cc1", "cc2", "nn1", "nn6", "nn13", "nn21", "nn5", "nn10", "nn18"]


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
    import gof_pdf    
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
    basepath = "/eos/user/m/msajatov/wormhole/thesis/tables/html_output"
    name = "default"
        
    for ch in channels:
        html = ""
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        for test in ["saturated", "KS", "AD"]:
            result = getCompact(df, ch, test, configs)
            html = html + gof_pdf.createHtml(result, configs)    
            html = html + "<br/>"    
    
        print "html: "
        print html
        gof_pdf.saveHtml(basepath, html, ch, "all", name)

def makePdf(args):
    import gof_pdf    
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
        
    basepath = "/eos/user/m/msajatov/wormhole/thesis/tables/pdf_output"
    name = "default"
        
    for ch in channels:
        html = ""
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        for test in ["saturated", "KS", "AD"]:
            result = getCompact(df, ch, test, configs)
            html = html + gof_pdf.createHtml(result, configs)    
            html = html + "<br/>"    
    
        print "html: "
        print html
        gof_pdf.savePdf(basepath, html, ch, "all", name)

def makeCsv(args):
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
        
    completedf = pd.DataFrame()
        
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        completedf = completedf.append(df, ignore_index=True)   
        
    add_failing = False
    
#     if "all" in args.channel:
#         do something special
    
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        for test in ["saturated", "KS", "AD"]:
            if add_failing:
                result = getCompact(df, ch, test, configs)   
                print result 
                csv = result.to_csv(index=False, sep=";")
                print csv
                
                #add failing using evalgof.compareFailingVarsNew(in_df, channel)
            else:
                result = getCompact(df, ch, test, configs)
                print result
                csv = result.to_csv(index=False, sep=";")
                print csv              
        

def printToConsole(args):        
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
    completedf = pd.DataFrame()
        
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        completedf = completedf.append(df, ignore_index=True)
        
    add_failing = False
    
    #     if "all" in args.channel:
#         do something special
    
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        for test in ["saturated", "KS", "AD"]:
            if add_failing:
                result = getCompact(df, ch, test, configs)   
                print result 
                
                #add failing using evalgof.compareFailingVarsNew(in_df, channel)
            else:
                result = getCompact(df, ch, test, configs)
                print result
            



        


def makeLatex(args):
    import gof_latex    
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.configs:            
        configs = args.configs
    else:
        configs = defaultConfigs
        
    completedf = pd.DataFrame()
        
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        completedf = completedf.append(df, ignore_index=True)
        
    add_failing = False
    
    #     if "all" in args.channel:
#         do something special
    
    tests = ["saturated", "KS", "AD"]
    
    for ch in channels:
        df = evalgof.loadDF("output/{0}_pvalues.json".format(ch))
        for test in tests:
            if "tt" in ch:
                shaped = gof_latex.shape(df, ch, test, configs[1:], configs, False)
            else:
                shaped = gof_latex.shape(df, ch, test, configs[1:], configs, False)
                
#             print df
            gof_latex.toGrid(shaped)
    
    

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


def getFailing(in_df, ch, test, configs):
    df = getReducedDataframe(in_df, ch, test, configs)
        
    series = df.apply(lambda x: x <= 0.05).sum(numeric_only=True)
#     print series
    series = series.astype(int)
#     print series
    return series

def getReducedDataframe(df, ch, test, configs):
    result = evalgof.compareSideBySideNew(df, configs[0], configs[1:], test, ch)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    return result

def saveCsv(df, filename):
    csv = df.to_csv(index=False, sep=";")
    file = open(filename, "w+")
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()