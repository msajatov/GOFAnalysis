import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse

import evalgof as evalgof

import gof_histo

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
    pass

def makeHtml(args):
    pass

def makePdf(args):
    pass

def makeCsv(args):
    pass

def printToConsole(args):
    pass

def makeLatex(args):
    pass

def makeHisto(args):
    
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

if __name__ == '__main__':
    main()