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

def highlight_max(s):
    '''
    highlight the maximum in a Series green.
    '''
    is_max = s == s.max()
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


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
#     parser.add_argument('-m', dest='mode', help='Config to compare', default='')
    parser.add_argument('mode', nargs="*", help='Variable', default=[])
    args = parser.parse_args()
    
    
    
    if not args.mode:
        modes = ["pt_1","pt_2","jpt_1","jpt_2","bpt_1","bpt_2","njets","nbtag","m_sv","mt_1",
                    "mt_2","pt_vis","pt_tt","mjj","jdeta","m_vis","dijetpt","met","eta_1","eta_2"]
#         variables = ["pt_1","pt_2"]
    else:
        modes = args.mode

    makeHtml(args.channel, modes)
    
    
def makeHtml(channel, modes):
    df = evalgof.loadDF("../output/{0}_pvalues.json".format(channel))
    
    print df
    
    if not modes:
        base = "cc"
        name = "default"
        if "all" in channel:
            configs = ["cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn12",
                   "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn21"]
            channels = ["et", "mt", "tt"]
        else:
    #         configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", 
    #                  "nn16", "nn17", "nn18", "nn19", "nn20", "nn15a", "nn16a", "nn17a", "nn18a"]
    #         configs = ["cc1", "nn5", "nn10", "nn13", "nn15", "nn15a", "nn15a2", "nn16", "nn16a", "nn16a2", "nn17", "nn17a", "nn17a2", 
    #                    "nn18", "nn18a", "nn18a2", "nn19", "nn20"]
    #         configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", 
    #                "nn13", "nn13a2", "nn14", "nn14a2", "nn15a2", "nn16a2", "nn17a2", "nn18a2"]
    #         configs = ["cc1", "cc2", "nn13", "nn13a2", "nn14", "nn14a2", "nn15", "nn15a", "nn15a2", "nn16", "nn16a", "nn16a2", 
    #                    "nn17", "nn17a", "nn17a2", "nn18", "nn18a", "nn18a2",
    #                    "nn1a2", "nn2a2", "nn3a2", "nn4a2", "nn5a2", "nn6a2", "nn7a2", "nn8a2", "nn9a2", "nn10a2", "nn11a2", "nn12a2"]
    #         configs = ["cc1", "cc2", "nn1a2", "nn2a2", "nn3a2", "nn4a2", "nn5a2", "nn6a2", "nn7a2", "nn8a2", "nn9a2", "nn10a2", 
    #                    "nn11a2", "nn12a2", "nn13a2", "nn14a2", "nn15a2", "nn16a2", "nn17a2", "nn18a2"]
    #         configs = ["cc1", "cc2", "nn11", "nn11a2", "nn11e", "nn12a2", "nn12e", "nn14a2", "nn14e", "nn16", "nn16a2", "nn16e", "nn18", "nn18a2", "nn18e"]
            
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
            html = ""
            for test in ["saturated", "KS", "AD"]:
                res = makeSingleHtml(df, ch, test, configs, cols, name)                        
                html = html + res
            
#             file = open('{0}_{1}.html'.format(ch, name), "w+")
#             file.write(res)
#             file.close()                        
#                         
#             
#             pdf.from_string(res, '{0}_{1}.pdf'.format(ch, name))
            
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
            html = ""
            for test in ["saturated", "KS", "AD"]:
                res = makeSingleHtml(df, ch, test, configs, cols, name)                        
                html = html + res
            
#             file = open('{0}_{1}.html'.format(ch, name), "w+")
#             file.write(res)
#             file.close()                        
#                         
#             
#             pdf.from_string(res, '{0}_{1}.pdf'.format(ch, name))
            
def makeSingleHtml(df, ch, test, configs, cols, name):
    html = ""
            
    result = evalgof.compareSideBySide(df, "cc", configs, "saturated", ch)
    result = result.rename(columns = {"channel":"ch"})
    result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
    styler = result.style.applymap(color_negative_red) \
                .apply(highlight_greater_than_base, subset=cols, axis=1) \
                .apply(highlight_smaller_than_base, subset=cols, axis=1) \
                .apply(highlight_max, subset=cols, axis=1)
                
    html = html + styler.render()
    
    file = open('{0}_{1}_{2}.html'.format(ch, test, name), "w+")
    file.write(html)
    file.close()
    
    pdf.from_string(html, '{0}_{1}_{2}.pdf'.format(ch, test, name))
    
    return html
 
    
if __name__ == '__main__':
    main()
