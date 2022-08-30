import json
import pandas as pd
import pdfkit as pdf
import numpy as np
import argparse
import os

import evalgof as evalgof

import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['mathtext.fontset'] = 'dejavusans'
import matplotlib.pyplot as plt


defaultConfigs = ["cc", "cc1", "cc2", "nn1", "nn6", "nn13", "nn21", "nn5", "nn10", "nn18"]


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('--test', dest='test', nargs="*", help='Tests', default=[])
    parser.add_argument('--conf', dest='configs', nargs="*", help='Configurations', default=[])
    parser.add_argument('-m', dest='method', help='Method to use', default=[])
    parser.add_argument('-i', dest='input', help='Input dir to use', default="output")
    parser.add_argument('-tt', dest='tt_variant', help='tt Variant', choices = ['vanilla', 'a', 'a2', 'e'], default='vanilla')
    parser.add_argument('-fg', dest='fg', nargs="*", help='Foreground configurations', default=[])
    parser.add_argument('-bg', dest='bg', nargs="*", help='Background configurations', default=[])
    parser.add_argument('-err', dest='err', nargs="*", help='Errorbar configurations', default=[])
    parser.add_argument('-dummy', dest='dummy', nargs="*", help='Bg legend entry for plot', default=[])
    parser.add_argument('--vars', nargs="*", help='Variables', default=[])
    args = parser.parse_args()


    switcher = {
        "list": listFailing,
        "html": makeHtml,
        "pdf": makePdf,
        "csv": makeCsv,
        "print": printToConsole,
        "latex": makeLatex,
        "histo": makeHisto,
        "plot": makePlot,
        "seeds": evalSeeds
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
        df = loadRawDF(ch, args.input)
        completedf = completedf.append(df, ignore_index=True)   
        
    if "all" in args.channel:
        f = evalgof.compareFailingVarsNew(completedf, channels, configs)
    else:
        for ch in channels:
            df = loadRawDF(ch, args.input)
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
        df = loadRawDF(ch, args.input)
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
        df = loadRawDF(ch, args.input)
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
        df = loadRawDF(ch, args.input)
        completedf = completedf.append(df, ignore_index=True)   
        
    add_failing = False
    
#     if "all" in args.channel:
#         do something special
    
    for ch in channels:
        df = loadRawDF(ch, args.input)
        for test in ["saturated", "KS", "AD"]:
            if add_failing:
                result = getCompact(df, ch, test, configs)   
                print result 
                csv = result.to_csv(index=False, sep=",")
                print csv
                
                #add failing using evalgof.compareFailingVarsNew(in_df, channel)
            else:
                result = getCompact(df, ch, test, configs)
                print result
                csv = result.to_csv(index=False, sep=",")
                print csv              
        
def evalSeeds(args):

    if not args.vars:
        variables = ["pt_1", 
                    "pt_2", 
                    "jpt_1", 
                    "jpt_2", 
                    "bpt_1", 
                    "bpt_2", 
                    "njets", 
                    "nbtag",
                    "m_sv", 
                    "mt_1", 
                    "mt_2", 
                    "pt_vis", 
                    "pt_tt", 
                    "mjj", 
                    "jdeta",
                    "m_vis", 
                    "dijetpt", 
                    "met"]
    else:
        variables = args.vars

    ch = args.channel

    df = loadRawDF(ch, args.input, seeds=True)

    rows_list = []    

    for conf in args.configs:
        # print conf
        confdf = df.query("conf == '{0}'".format(conf)) \
            .query("test == '{0}'".format(args.test[0]))
        # print confdf
        for var in variables:
            print "{0} --- {1}".format(conf, var)
            vardf = confdf.query("var == '{0}'".format(var))
            aggregate = vardf.query("seed == 'aggregate'")["pvalue"]
            print "Aggregate: {0}".format(aggregate)

            mean = vardf.query("seed != 'aggregate'")["pvalue"].mean(axis=0)
            stddev = vardf.query("seed != 'aggregate'")["pvalue"].std(axis=0)
            # print "Mean: {0}".format(mean)
            # print "Sigma: {0}".format(stddev)

            print "{0} +- {1}".format(mean, stddev)
            nominal = vardf.query("seed == '1230:1249:1'")["pvalue"]
            print "Nominal: {0}".format(nominal)

            new_row = {'conf':conf, 'var':var, 'mean':mean}
            rows_list.append(new_row)

    newdf = pd.DataFrame(rows_list, columns=["conf", "var", "mean"])
    
    # only keep necessary columns (otherwise problems with merge)

    subset = newdf.loc[:, ["var"] + ["mean"] + ["conf"]]    
        
    subset = subset.sort_values(by=["var", "conf"])
    basedf = subset.query("conf == '{0}'".format(args.configs[0]))  
    basedf = basedf.rename(columns = {"mean":args.configs[0]})
    basedf = basedf.drop("conf", axis=1)   
    
    result = basedf
    
    for conf in args.configs[1:]: 
        confdf = subset.query("conf == '{0}'".format(conf))
        confdf = confdf.rename(columns = {"mean":conf})
        confdf = confdf.drop("conf", axis=1) 
        
        result = pd.merge(result, confdf, on="var")

    result.drop("var", axis=1, inplace=True)

    print result.to_csv(index=False)

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
        df = loadRawDF(ch, args.input)
        completedf = completedf.append(df, ignore_index=True)
        
    add_failing = False
    
    #     if "all" in args.channel:
#         do something special
    
    for ch in channels:
        df = loadRawDF(ch, args.input)
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
        df = loadRawDF(ch, args.input)
        completedf = completedf.append(df, ignore_index=True)
        
    add_failing = False
    
    #     if "all" in args.channel:
#         do something special
    
    tests = ["saturated", "KS", "AD"]
    
    for ch in channels:
        df = loadRawDF(ch, args.input)
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
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
    
    if args.fg or args.bg:
        configs = args.fg + args.bg
    elif args.err:  
        configs = args.err
    elif args.configs:  
        configs = args.configs
    else:
        configs = defaultConfigs
        
    completedf = pd.DataFrame()
        
    for ch in channels:
        df = loadRawDF(ch, args.input)
        completedf = completedf.append(df, ignore_index=True)
        
    add_failing = False
    
    for ch in channels:
        df = loadRawDF(ch, args.input)
        #for test in ["saturated", "KS", "AD"]:  
        for test in args.test:  
            result = getCompact(df, ch, test, configs)
            print result
            print "attempting to plot df: "

            fig = plt.figure(facecolor='w', figsize=(5,7))

            plt.xlim(-0.5, 17.5)  
            plt.ylim(0, 1)  

            ax = fig.add_subplot(1,1,1)   
            plt.subplots_adjust(top=0.85)     

            bg_handles = {}
            fg_handles = {}

            df = loadRawDF(ch, args.input, seeds=True)
            df = df.query("channel == '{0}'".format(ch)).query("test == '{0}'".format(test))

            for config in args.bg:
                confObj = Config(config)
                bg_handles[config] = plotBackgroundByType(ax, confObj, result, df)
                #ax.plot(xrange(len(result)), result[config], "o", color="lightgrey", markeredgecolor="lightgrey", label=config)

            if args.err:
                plt.gca().set_color_cycle(None)
                err_handles = {}
                # df = loadRawDF(ch, args.input, seeds=True)
                # df = df.query("channel == '{0}'".format(ch)).query("test == '{0}'".format(test))
                for i, config in enumerate(args.err):
                    co = Config(config)
                    err_handles[config] = plotErrorBars(ax, co, result, df, i, 3)

            plt.gca().set_color_cycle(None)
            for i, config in enumerate(args.fg):                
                confObj = Config(config)
                fg_handles[config] = plotForegroundByType(ax, confObj, result, i, 3)
                #ax.plot(xrange(len(result)), result[config], "_", markersize=12, markeredgewidth=2, label=config)

            plt.xticks(np.arange(len(result)), result["var"], rotation="vertical") 
            plt.yticks(np.arange(0, 1.1, step=0.1))  

            ax.grid(which='major', axis='both', linestyle='-', color='lightgrey')    
            ax.set_axisbelow(True) 

                    

            plt.hlines(0.05, -0.5, 17.5, colors='red')

            legend_handle_list = []
            legend_handle_label_list = []
            if fg_handles and len(fg_handles) > 0:
                for config in args.fg:
                    co = Config(config)
                    legend_handle_label_list.append(co.getName()) 
                legend_handle_list = [fg_handles[conf][0] for conf in args.fg]
            else:
                for config in args.err:
                    co = Config(config)
                    legend_handle_label_list.append(co.getName())    
                legend_handle_list = [err_handles[conf][0] for conf in args.err]            

            dummy_xrange = xrange(20, 20 + len(result))
            print dummy_xrange

            if args.dummy:
                for dum in args.dummy:
                    label = dum.split("-")[0]
                    if len(args.dummy) > 1:                        
                        marker = dum.split("-")[1]
                    else:
                        marker = "o"

                    # dummy, make invisible series
                    if marker == "_":
                        dummy_handle = ax.plot(dummy_xrange, [0] * len(result), marker, color="#e0e0e0", markeredgecolor="#e0e0e0", markersize=12, markeredgewidth=2, label=label)
                    else:
                        dummy_handle = ax.plot(dummy_xrange, [0] * len(result), marker, color="#e0e0e0", markeredgecolor="#e0e0e0", label=label)
                    legend_handle_list += dummy_handle   
                    legend_handle_label_list.append(label) 
            

            legendcols = len(args.err) + len(args.dummy)
            if legendcols == 5:
                legendfontsize = 10.5
            else:
                legendfontsize = 12

            #plt.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=2, borderaxespad=0, frameon=False, numpoints=1, fontsize=12) 
            plt.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01, 1.0, 0.2), ncol=legendcols, borderaxespad=0, frameon=False, numpoints=1, fontsize=legendfontsize, \
                handletextpad=0.1, handles=legend_handle_list, labels=legend_handle_label_list)     

            chtex_dict = {"et": r"$\mathrm{e}\tau_{\mathrm{h}}$", "mt": r"$\mu"r"\tau_{\mathrm{h}}$", "tt": r"$\tau_{\mathrm{h}}\tau_{\mathrm{h}}$"}
            chtex = chtex_dict.get(ch,ch)

            line = r"$-$"

            testtex = r"$\mathdefault{" + test + r"}$"
                    
            plt.title("p-values {2} {0} {2} {1}".format(chtex, testtex, line), y=1.1)    

            #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

            #plt.show()

            plt.tight_layout()

            path = "/eos/user/m/msajatov/wormhole/pvalue_plots"
            plt.savefig(os.path.join(path, "{0}_{1}.png".format(ch, test)))
            plt.savefig(os.path.join(path, "{0}_{1}.pdf".format(ch, test)))

    #print completedf

def plotErrorBars(ax, confObj, result, df, index, total):
    print "In plotErrorBars"
    print df
    
    config = confObj.getRawName()

    var_list = result["var"]
    print var_list

    # iterate over all distinct vars in df (containing seeds etc.)
    err_var_list = df["var"].unique()
    print err_var_list

    mean_list = [0] * len(result)
    err_list = [0] * len(result)

    x_list = list(xrange(len(result)))

    # use nominal values for all variables and selectively fill in non-zero error bars for variables in err_var_list
    for i, v in enumerate(var_list):
        if v in err_var_list:
            mean, stddev, stderr = getMeanAndStdDevFromSeeds(df, config, v)
            nominal = getFirstSeedFromSeeds(df, config, v)
            err_list[i] = stderr
            mean_list[i] = mean
        else:
            err_list[i] = 0
            mean_list[i] = 0

    if total == 3:
        diff = 0.1
        for i, x in enumerate(x_list):
            if index == 0:
                x_list[i] = x - diff
            elif index == 2:
                x_list[i] = x + diff
    elif total == 2:
        diff = 0.1
        for i, x in enumerate(x_list):
            if index == 0:
                x_list[i] = x - diff
            elif index == 1:
                x_list[i] = x + diff
     
    if config == "cc":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="black", markeredgecolor="black", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc1":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="red", markeredgecolor="red", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc2":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="orange", markeredgecolor="orange", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="black", markeredgecolor="black", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb1":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="red", markeredgecolor="red", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb2":
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="orange", markeredgecolor="orange", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "tt":
        #ax.plot(xrange(len(result)), result[config], "^", color="#9B98CC", markeredgecolor="#9B98CC", label=config)
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="#795A98", markeredgecolor="#795A98", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "w":
        #ax.plot(xrange(len(result)), result[config], "^", color="#DE5A6A", markeredgecolor="#DE5A6A", label=config)
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="#DE5A6A", markeredgecolor="#DE5A6A", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "xx":
        #ax.plot(xrange(len(result)), result[config], "^", color="#FACAFF", markeredgecolor="#FACAFF", label=config)
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", color="#f6a8f3", markeredgecolor="#f6a8f3", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    else:
        handle = ax.errorbar(x_list, mean_list, yerr=err_list, fmt="_", markersize=12, markeredgewidth=2, label=confObj.getName())

    return handle

def set_color_cycle(self, clist=None):
    if clist is None:
        clist = rcParams['axes.color_cycle']
    self.color_cycle = itertools.cycle(clist)

def set_color_cycle(self, clist):
    """
    Set the color cycle for any future plot commands on this Axes.

    *clist* is a list of mpl color specifiers.
    """
    self._get_lines.set_color_cycle(clist)
    self._get_patches_for_fill.set_color_cycle(clist)

def getMeanAndStdDevFromSeeds(df, conf, var):            
    confdf = df.query("conf == '{0}'".format(conf))
    print "{0} --- {1}".format(conf, var)
    vardf = confdf.query("var == '{0}'".format(var))
    # aggregate = vardf.query("seed == 'aggregate'")["pvalue"]
    # print "Aggregate: {0}".format(aggregate)

    print vardf

    mean = vardf.query("seed != 'aggregate'")["pvalue"].mean(axis=0)
    stddev = vardf.query("seed != 'aggregate'")["pvalue"].std(axis=0)
    stderr = vardf.query("seed != 'aggregate'")["pvalue"].sem(axis=0)
    # print "Mean: {0}".format(mean)
    # print "Sigma: {0}".format(stddev)

    print "{0} +- {1}".format(mean, stddev)
    nominal = vardf.query("seed == '1230:1249:1'")["pvalue"]
    print "Nominal: {0}".format(nominal)

    return mean, stddev, stderr

def getFirstSeedFromSeeds(df, conf, var):            
    confdf = df.query("conf == '{0}'".format(conf))
    print "{0} --- {1}".format(conf, var)
    vardf = confdf.query("var == '{0}'".format(var))
    nominal = vardf.query("seed == '1230:1249:1'").reset_index(drop=True)
    # print "Nominal:"
    # print nominal
    # nominal = nominal.reset_index(drop=True)
    # print "Nominal:"
    # print nominal

    val = nominal["pvalue"][0]
    print val

    return val

def plotForegroundByType(ax, confObj, result, index, total):
    config = confObj.getRawName()

    x_list = list(xrange(len(result)))

    if total == 3:
        diff = 0.2
        for i, x in enumerate(x_list):
            if index == 0:
                x_list[i] = x - diff
            elif index == 2:
                x_list[i] = x + diff
    elif total == 2:
        diff = 0.1
        for i, x in enumerate(x_list):
            if index == 0:
                x_list[i] = x - diff
            elif index == 1:
                x_list[i] = x + diff


    if config == "cc":
        handle = ax.plot(x_list, result[config], "_", color="black", markeredgecolor="black", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc1":
        handle = ax.plot(x_list, result[config], "_", color="red", markeredgecolor="red", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc2":
        handle = ax.plot(x_list, result[config], "_", color="orange", markeredgecolor="orange", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb":
        handle = ax.plot(x_list, result[config], "_", color="black", markeredgecolor="black", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb1":
        handle = ax.plot(x_list, result[config], "_", color="red", markeredgecolor="red", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb2":
        handle = ax.plot(x_list, result[config], "_", color="orange", markeredgecolor="orange", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "tt":
        #ax.plot(xrange(len(result)), result[config], "^", color="#9B98CC", markeredgecolor="#9B98CC", label=config)
        handle = ax.plot(x_list, result[config], "_", color="#795A98", markeredgecolor="#795A98", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "w":
        #ax.plot(xrange(len(result)), result[config], "^", color="#DE5A6A", markeredgecolor="#DE5A6A", label=config)
        handle = ax.plot(x_list, result[config], "_", color="#DE5A6A", markeredgecolor="#DE5A6A", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "xx":
        #ax.plot(xrange(len(result)), result[config], "^", color="#FACAFF", markeredgecolor="#FACAFF", label=config)
        handle = ax.plot(x_list, result[config], "_", color="#f6a8f3", markeredgecolor="#f6a8f3", markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    else:
        handle = ax.plot(x_list, result[config], "|", markersize=12, markeredgewidth=2, label=confObj.getName())

    return handle


def plotBackgroundByType(ax, confObj, result, df):
    config = confObj.getRawName()
    y_list = result[config]

    highres = True

    var_list = result["var"]

    mean_list = [0] * len(result)

    # use nominal values for all variables and selectively fill in non-zero error bars for variables in err_var_list
    if highres:
        for i, v in enumerate(var_list):
            mean, stddev, stderr = getMeanAndStdDevFromSeeds(df, config, v)
            nominal = getFirstSeedFromSeeds(df, config, v)
            mean_list[i] = mean

        y_list = mean_list

    if config == "cc":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0, markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc1":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0,markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "cc2":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0, markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0, markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb1":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0,markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    elif config == "ccemb2":
        handle = ax.plot(xrange(len(result)), y_list, "_", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0, markersize=12, markeredgewidth=2, label=confObj.getName())
        pass
    else:
        handle = ax.plot(xrange(len(result)), y_list, "o", color="#e0e0e0", markeredgecolor="#e0e0e0", zorder=0, label=confObj.getName())

    return handle

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

def loadRawDF(ch, dir, seeds=False):

    path = "{0}/{1}_pvalues.json".format(dir, ch)
    if seeds:
        path = path.replace(".json", "_seeds.json")

    df = evalgof.loadDF(path, seeds=seeds)
    return df

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

class Config:
    def __init__(self, rawname):
        self.rawname = rawname
        self.namedict = {}
        self.namedict["tt"] = "TT"
        self.namedict["w"] = "W"
        self.namedict["xx"] = "QCD"
        self.namedict["cc"] = "MC1"
        self.namedict["cc1"] = "MC2"
        self.namedict["cc2"] = "MC3"
        self.namedict["ccemb"] = "EMB1"
        self.namedict["ccemb1"] = "EMB2"
        self.namedict["ccemb2"] = "EMB3"

    def getName(self):
        if self.rawname in self.namedict:
            return self.namedict[self.rawname]
        else:
            return self.rawname

    def getRawName(self):
        return self.rawname

if __name__ == '__main__':
    main()