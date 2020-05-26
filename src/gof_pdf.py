import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse
import os

import evalgof


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
    
    return ['background-color: green' if v else '' for v in is_max]

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


def saveHtml(basepath, html, ch, test, name):
	path = os.path.join(basepath, '{0}_{1}_{2}.html'.format(ch, test, name))
	file = open(path, "w+")
	file.write(html)
	file.close()   

def savePdf(basepath, html, ch, test, name):
	path = os.path.join(basepath, '{0}_{1}_{2}.pdf'.format(ch, test, name))
	pdf.from_string(html, path)
    
def createHtml(result, cols):
                        
    styler = result.style.applymap(color_negative_red) \
                        .apply(highlight_greater_than_base, subset=cols, axis=1) \
                        .apply(highlight_smaller_than_base, subset=cols, axis=1) \
                        .apply(highlight_max, subset=cols, axis=1)
    
    html = styler.render()    
    return html
                        
    
#     styler = result.style.applymap(color_negative_red)

#     bla = 0

    
	
# 	base = "cc"
#         name = "custom"
#         if "all" in channel:
#             configs = ["cc1", "cc2"] + modes
#             channels = ["et", "mt", "tt"]
#         else:            
#             configs = ["cc1", "cc2"] + modes            
#             channels = ["tt"]
#         
#         cols = [base] + configs
#         
#         for ch in channels:    
#             html = ""
#             
#             result = evalgof.compareSideBySide(df, "cc", configs, "saturated", ch)
#             result = result.rename(columns = {"channel":"ch"})
#             result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
#             styler = result.style.applymap(color_negative_red) \
#                         .apply(highlight_greater_than_base, subset=cols, axis=1) \
#                         .apply(highlight_smaller_than_base, subset=cols, axis=1) \
#                         .apply(highlight_max, subset=cols, axis=1)
#                         
#             html = html + styler.render()
#             
#             result = evalgof.compareSideBySide(df, "cc", configs, "KS", ch)
#             result = result.rename(columns = {"channel":"ch"})
#             result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
#             styler = result.style.applymap(color_negative_red) \
#                         .apply(highlight_greater_than_base, subset=cols, axis=1) \
#                         .apply(highlight_smaller_than_base, subset=cols, axis=1) \
#                         .apply(highlight_max, subset=cols, axis=1)
#                         
#             html = html + "<br/>"
#             html = html + styler.render()
#             
#             result = evalgof.compareSideBySide(df, "cc", configs, "AD", ch)
#             result = result.rename(columns = {"channel":"ch"})
#             result.drop(["dc_type", "gof_mode"], axis=1, inplace=True)
#             styler = result.style.applymap(color_negative_red) \
#                         .apply(highlight_greater_than_base, subset=cols, axis=1) \
#                         .apply(highlight_smaller_than_base, subset=cols, axis=1) \
#                         .apply(highlight_max, subset=cols, axis=1)
#                         
#             html = html + "<br/>"
#             html = html + styler.render()