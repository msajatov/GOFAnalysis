import json
import os
import argparse


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('-i', dest='input', help='Input', default="")
    args = parser.parse_args()
    
    if args.input == "new":
        runNew(args)
        return
    
    #configurations = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
    
    configurations = ["cc", "cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", 
                     "nn11", "nn12", "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn21", "nn22", "nn23"]     
    
    #configurations = ["nn1", "nn1_alternative"] 
    
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
                 "met",
                 "eta_1",
                 "eta_2"]
    
    tests = ["saturated", "KS", "AD"]
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
        
    if args.channel == "tt":
        configurations = ["cc", "cc1", "cc2", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", 
                          "nn11", "nn12", "nn13", "nn14", "nn15", "nn16", "nn17", "nn18", "nn19", "nn20", "nn21",                         
                          "nn1a2", "nn2a2", "nn3a2", "nn4a2", "nn5a2", "nn6a2", "nn7a2", "nn8a2", "nn9a2", "nn10a2", 
                          "nn11a2", "nn12a2", "nn13a2", "nn14a2", "nn15a2", "nn16a2", "nn17a2", "nn18a2",
                          "nn11e", "nn12e", "nn14e", "nn16e", "nn18e",
                          "nn1a", "nn2a", "nn3a", "nn4a", "nn5a", "nn6a", "nn7a", "nn8a", "nn9a", "nn10a",
                          "nn11a", "nn12a", "nn13a", "nn14a", "nn15a", "nn16a", "nn17a", "nn18a", "nn22a", "nn23a", "xx"]
    
    dc_types = ["emb_dc"]
    #dc_types = ["mc_dc", "emb_dc"]
    gof_modes = ["results_w_emb"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    base = "/afs/cern.ch/work/m/msajatov/private/cms/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/{0}/{1}/{2}/gof/2017"
    
    completepvalues = {}
    
    
    for dc_type in dc_types:
        completepvalues[dc_type] = {}
        for gof_mode in gof_modes:
            pvalues = {}
            for conf in configurations:  
                print conf              
                pvalues[conf] = {}
                basepath = base.format(dc_type, gof_mode, conf)
                for var in variables:
                    pvalues[conf][var] = {}
                    for test in tests:
                        pvalues[conf][var][test] = {}
                        for channel in channels:
                            path = "{0}/{1}/{2}/{3}/gof.json".format(basepath, var, test, channel)               
                            
                            try:
                                with open(path, "r") as FSO:
                                    data = json.load(FSO)
                            except ValueError as e:
                                print e
                                print "Check {0}. Probably a ',' ".format(ccpath)
                            except IOError as e:
                                print "Exception while parsing {0} {1} {2} for {3}".format(var, test, channel, conf)
                                print e
                                continue
                            
            #                 pvalues["cc"][var][test][channel] = cc["125.0"]["p"]
            #                 pvalues["nn"][var][test][channel] = nn["125.0"]["p"]
                            
                            try:
                                if test == "saturated":                
            #                         print cc["125.0"]["p"]
            #                         print nn["125.0"]["p"]
            #                         print nn1["125.0"]["p"]
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]["p"]
                                else:
            #                         print cc["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn1["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                            except:
                                print "Exception"
            completepvalues[dc_type][gof_mode] = pvalues
                
    
    
    
    #saveAsJson(pvalues, "pvalues")
    
    saveAsJson(completepvalues, "{0}_pvalues".format(args.channel))
    

def runNew(args):    
    
    print "entering runNew..."
    
    common = ["cc", "cc1", "cc2", "nn1", "nn6", "nn13", "nn21"] + ["nn5", "nn10", "nn18"]
    
    conf_a = ["nn1a", "nn5a", "nn6a", "nn10a", "nn13a", "nn18a"]
    conf_a2 = []
    conf_e = []
    
    if args.channel == "tt":
        configurations = common + conf_a
    elif args.channel == "et" or args.channel == "mt":
        configurations = common 
#     configurations = ["nn1", "nn6", "nn13", "nn21"] 
    
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
                 "met",
                 "eta_1",
                 "eta_2"]
    
    tests = ["saturated", "KS", "AD"]
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
        
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest/{0}/gof/2017"
    
    completepvalues = {}
    
    dc_types = ["emb_dc"]
    #dc_types = ["mc_dc", "emb_dc"]
    gof_modes = ["results_w_emb"]
    
    
    for dc_type in dc_types:
        completepvalues[dc_type] = {}
        for gof_mode in gof_modes:
            pvalues = {}
            for conf in configurations:  
                print conf              
                pvalues[conf] = {}
                basepath = base.format(conf)
                for var in variables:
                    pvalues[conf][var] = {}
                    for test in tests:
                        pvalues[conf][var][test] = {}
                        for channel in channels:
                            path = "{0}/{1}/{2}/{3}/gof.json".format(basepath, var, test, channel)               
                            
                            try:
                                with open(path, "r") as FSO:
                                    data = json.load(FSO)
                            except ValueError as e:
                                print e
                                print "Check {0}. Probably a ',' ".format(ccpath)
                            except IOError as e:
                                print "Exception while parsing {0} {1} {2} for {3}".format(var, test, channel, conf)
                                print e
                                continue
                            
            #                 pvalues["cc"][var][test][channel] = cc["125.0"]["p"]
            #                 pvalues["nn"][var][test][channel] = nn["125.0"]["p"]
                            
                            try:
                                if test == "saturated":                
            #                         print cc["125.0"]["p"]
            #                         print nn["125.0"]["p"]
            #                         print nn1["125.0"]["p"]
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]["p"]
                                else:
            #                         print cc["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn1["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                            except:
                                print "Exception"
            completepvalues[dc_type][gof_mode] = pvalues
                
    
    
    
    #saveAsJson(pvalues, "pvalues")
    
    saveAsJson(completepvalues, "{0}_pvalues".format(args.channel))
    
def saveAsJson(pvalues, filename):
    dir = "output"
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, filename + ".json"), 'wb') as FSO:
            json.dump(pvalues, FSO)  
        
def saveOutput(filename, data):
    f = open("output/" + filename, "w")
    f.write(data)
    f.close()
    
if __name__ == '__main__':
    main()
