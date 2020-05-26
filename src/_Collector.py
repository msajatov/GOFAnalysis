import json
import os

def main():
    
    configurations = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
    #configurations = ["cc", "cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"] 
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
    
    channels = ["et", "mt", "tt"]
    
    dc_types = ["mc_dc", "emb_dc"]
    #dc_types = ["mc_dc", "emb_dc"]
    #gof_modes = ["results_w_emb"]
    gof_modes = ["results_w_emb", "results_wo_emb"]
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
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]
                                else:
            #                         print cc["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
            #                         print nn1["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                                    
                                    pvalues[conf][var][test][channel] = data["125.0"]["htt_{0}_100_Run2017".format(channel)]
                            except:
                                print "Exception"
            completepvalues[dc_type][gof_mode] = pvalues
                
    
    
    
    #saveAsJson(pvalues, "pvalues")
    
    saveAsJson(completepvalues, "gof")
    
    
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