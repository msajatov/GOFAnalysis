import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import sys
sys.path.append("../") # go to parent dir

import argparse

import GOFTools.evalgof as evalgof

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val <= 0.05 else 'black'
    return 'color: %s' % color

def highlight_sum(val):
    '''
    highlight the maximum in a Series green.
    '''
    fw = 'bold' if val != '-' else 'normal'
    return 'font-weight: %s' % fw

def highlight_max(s):
    '''
    highlight the maximum in a Series green.
    '''
# is_max is an array!
#     is_max = (s == s.max() and s.apply(lambda x: x > 0))
    is_max = (s == s.max())
    
    return ['background-color: rgba(171, 243, 108, 142)' if v else '' for v in is_max]

# def highlight_greater_than_base(s):
#     '''
#     highlight yellow if greater than the value in a base column
#     '''
#     is_greater = s > s["cc"]
#     return ['background-color: yellow' if v else '' for v in is_max]

def highlight_greater_than_base(row):
    ret = ["" for _ in row.index]
    for colname in row.index:
        if row[colname] > row["cc"] and row[colname] > row["cc1"] and row[colname] > row["cc2"]:
            ret[row.index.get_loc(colname)] = "background-color: rgba(171, 243, 108, 142)"
    return ret

def highlight_smaller_than_base(row):
    ret = ["" for _ in row.index]
    for colname in row.index:
        if row[colname] < row["cc"] and row[colname] < row["cc1"] and row[colname] < row["cc2"]:
            ret[row.index.get_loc(colname)] = "background-color: rgba(255, 170, 170, 170)"
    return ret


class Cell:
    def __init__(self, text):
        self.text = text
        self.font = ""
        self.color = ""
        self.backgroundcolor = ""
        self.cleanUpFloatFormating()
        
    def toLatex(self):
        output = str(self.text)
        output = output.replace("_", "\_")
        if self.font == "bold":
            output = "\\textbf{" + output + "}"
        if self.backgroundcolor:            
            output = self.backgroundcolor + output
        if self.color:
            output = self.color + output
        
            
        return output
    
    def cleanUpFloatFormating(self):
        if not "." in str(self.text):
            return
        try:
            floatvalue = float(self.text)
            rounded = round(floatvalue, 3)
#             print rounded
            self.text = "{:1.3f}".format(rounded)
        except ValueError:
            pass
#             print "not a float"
#             print self.text
        
class Row:
    def __init__(self):
        self.confs = []
        self.var = []
        
    def toLatex(self):
        output = self.var.toLatex()
        for conf in self.confs:
            output += " & " + conf.toLatex()            
        output = output + " \\\\"
        return output
        
class Grid:
    def __init__(self):
        self.header = None
        self.rows = []
        self.failing = None
        
    def toLatex(self):
        output = self.header.toLatex()  
        output = output + "\midrule"      
        for row in self.rows:
            output += " \n " + row.toLatex()
        output = output + "\midrule"      
        output += " \n " + self.failing.toLatex() + " \n "
        return output

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
#     parser.add_argument('-m', dest='mode', help='Config to compare', default='')
    parser.add_argument('mode', nargs="*", help='Variable', default=[])
    parser.add_argument('-f', dest="failing", help='Variable', action="store_true")
    args = parser.parse_args()
    
    
    
#     if not args.mode:
#         variables = ["pt_1","pt_2","jpt_1","jpt_2","bpt_1","bpt_2","njets","nbtag","m_sv","mt_1",
#                     "mt_2","pt_vis","pt_tt","mjj","jdeta","m_vis","dijetpt","met","eta_1","eta_2"]
#         modes = ["nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
#                    "nn13", "nn14", "nn15", "nn16", "nn17", "nn18"]
#     else:
#         modes = args.mode

    modes = args.mode

#     makeHtml(args.channel, modes, args.failing)
    
    if "all" in args.channel:
        channels = ["et", "mt", "tt"]
    else:                     
        channels = ["tt"]
        
#     generate(channels, modes, args.failing)
    
    makeHtml(args.channel, modes, args.failing)   


def getReducedDataframe(df, ch, test, configs, cols):
    result = evalgof.compareSideBySide(df, "cc", configs, test, ch)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    
    return result
    
def makeHtml(channel, modes, add_failing):
    et_df = evalgof.loadDF("output/et_pvalues.json")
    mt_df = evalgof.loadDF("output/mt_pvalues.json")
    tt_df = evalgof.loadDF("output/tt_pvalues.json")
#     tt_df = None
    
    
    print et_df
    print mt_df
    
    if not modes:
        base = "cc"
        name = "default"

        channels = [channel]
        configs = ["cc1", "cc2"]
        
        cols = [base] + configs
        
        for ch in channels:    
            html = ""
            if ch == "tt":
                in_df = tt_df
            elif ch == "et":
                in_df = et_df
            elif ch == "mt":
                in_df = mt_df
            
            for test in ["saturated", "KS", "AD"]:
                if add_failing:
                    res = makeSingleHtml(in_df, ch, test, configs, cols, name, evalgof.compareFailingVarsNew(in_df, channel))    
                else:
                    res = makeSingleHtml(in_df, ch, test, configs, cols, name, None)                                         
                html = html + res
            
    else:
        base = "cc"
        name = "custom"

        channels = [channel]
        configs = ["cc1", "cc2"] + modes
        
#         cols = [base] + configs
        cols = modes
        
        for ch in channels:    
            html = ""
            if ch == "tt":
                in_df = tt_df
            elif ch == "et":
                in_df = et_df
            elif ch == "mt":
                in_df = mt_df
            
            for test in ["saturated", "KS", "AD"]:
                if add_failing:
                    res = makeSingleHtml(in_df, ch, test, configs, cols, name, evalgof.compareFailingVarsNew(in_df, channel))    
                else:
                    res = makeSingleHtml(in_df, ch, test, configs, cols, name, None)                   
                html = html + res
            
            
def makeSingleHtml(df, ch, test, configs, cols, name, failing):
    html = ""
            
    result = evalgof.compareSideBySideNew(df, cols[0], cols[1:], test, ch)
    result = result.rename(columns = {"channel":"ch"})
    result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
#     styler = result.style.applymap(color_negative_red) \
#                 .apply(highlight_greater_than_base, subset=cols, axis=1) \
#                 .apply(highlight_smaller_than_base, subset=cols, axis=1) \
#                 .apply(highlight_max, subset=cols, axis=1) \
#                 .apply(highlight_sum, subset=['18'], axis=0)
#                 
#     html = html + styler.render()
    
    if failing:
        f = failing[test][ch]
        print "failing:"
        print f
        
        new_row = {'var':"total failing", 'test':test, 'ch':ch}
        for conf in cols:
            new_row[conf] = str(int(f[conf]))
            
        sum_df = pd.DataFrame([new_row], columns=["var", "test", "ch"] + cols)  
        print sum_df   
        
        result = pd.concat([result, sum_df])
    
    new_index = range(len(result))
    print new_index
    result.index = new_index
    
    print result
    
    csv = result.to_csv(index=False, sep=";")
    print csv
    
#     styler = result.style.applymap(color_negative_red) \
#                 .apply(highlight_greater_than_base, subset=cols, axis=1) \
#                 .apply(highlight_smaller_than_base, subset=cols, axis=1) \
#                 .apply(highlight_max, subset=cols, axis=1) 
#                 
#     html = html + styler.render()
#     
#     
#     
#     
#     file = open('{0}_{1}_{2}.html'.format(ch, test, name), "w+")
#     file.write(html)
#     file.close()
#     
#     pdf.from_string(html, '{0}_{1}_{2}.pdf'.format(ch, test, name))
#     
#     return html

    return ""
 
    
if __name__ == '__main__':
    main()
