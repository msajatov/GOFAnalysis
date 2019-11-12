import json
import pandas as pd
import pdfkit as pdf
import numpy as np

import argparse
import evalgof

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
        self.tableprefix = ""
        self.tablepostfix = ""
        self.header = None
        self.rows = []
        self.failing = None
        
    def toLatex(self):
        output = self.tableprefix
        output = output + self.header.toLatex()  
        output = output + "\midrule"      
        for row in self.rows:
            output += " \n " + row.toLatex()
        output = output + "\midrule"      
        output += " \n " + self.failing.toLatex() + " \n "
        output = output + self.tablepostfix
        return output
            

def shape(in_df, ch, test, configs, cols, dropCC=False):
    df = getReducedDataframe(in_df, ch, test, configs, cols)
        
    series = df.apply(lambda x: x <= 0.05).sum(numeric_only=True)
#     print series
    series = series.astype(int)
#     print series
    new = df.append(series, ignore_index=True)
#     print new
    
    length = len(new)
    new.iloc[length - 1] = new.iloc[length - 1].map('{:,.0f}'.format)
    
    new["variable"][length - 1] = "failing"
    
#     print new
    if not dropCC:
#         renamed = renameCC(new)
#         print renamed
#         return renamed
    else:
        new.drop(["cc", "cc1", "cc2"], axis=1, inplace=True)
        return new

def toGrid(df):
    
    header_df = df.columns
    header = toRow(map(lambda x: Cell(x), header_df.values))    
#     print header.confs

    spacing = 7.5
    tableprefix = "\\begin{tabular}{p{18mm}"
    for i in range(0, len(header.confs)):
        tableprefix += "p{" + str(spacing) + "mm}"
        
    tableprefix += "}\n"
    
    tablepostfix = "\\end{tabular}"
        
    rows = []
    for i in range(0,len(df)-1):        
        r_df = df.iloc[i]
        row = toRow(map(lambda x: Cell(x), r_df.values))
        rows.append(row)
    
    failing_df = df.iloc[len(df)-1]
    failing = toRow(map(lambda x: Cell(x), failing_df.values))   
    
    grid = Grid()
    grid.tableprefix = tableprefix
    grid.tablepostfix = tablepostfix
    grid.header = header
    grid.rows = rows
    grid.failing = failing

    applyConditionalFormating(grid)
    
    print grid.toLatex()

def toRow(cells):
    row = Row()
    row.var = cells[0]
    row.confs = cells[1:len(cells)]
    return row

def applyConditionalFormating(grid):
    badcolor = "radicalred!10"
    goodcolor = "green-yellow!20"
    failingcolor = "red"
        
    for row in grid.rows:
        for conf in row.confs[3:len(row.confs)]:
            cc1 = float(row.confs[0].text)
            cc2 = float(row.confs[1].text)
            cc3 = float(row.confs[2].text)
            if float(conf.text) > cc1 and float(conf.text) > cc2 and float(conf.text) > cc3:
                conf.backgroundcolor = "\\goodcolor"
            if float(conf.text) < cc1 and float(conf.text) < cc2 and float(conf.text) < cc3:
                conf.backgroundcolor = "\\badcolor"
                
    for row in grid.rows:
        for conf in row.confs:
            if float(conf.text) <= 0.05:
                conf.color = "\\failingcolor"  
            else:
                conf.color="\\passingcolor"      
                
    grid.failing.var.font = "bold"
                
    for conf in grid.failing.confs:
        conf.font = "bold"
    

def toLatex(df):
    csv = df.to_csv(index=False, sep="&")    
    
    lines = csv.split("\n")   
    
    for line in lines:
        line += "\\"

def renameCC(df):
    result = df.rename(columns = {"cc":"cc1", "cc1":"cc2", "cc2":"cc3"})
    return result

def getReducedDataframe(df, ch, test, configs, cols):
    result = evalgof.compareSideBySide(df, "cc", configs, test, ch)
    result = result.rename(columns = {"var":"variable"})
    result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1, inplace=True)
    
    return result