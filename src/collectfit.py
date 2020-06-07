import json
import os
import argparse
import ROOT as R


defaultConfigs = ["cc"]

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('-i', dest='input', help='Input', default="")
    parser.add_argument('configs', nargs="*", help='Configurations', default=[])
    args = parser.parse_args()

    base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017"
    # base = "/afs/cern.ch/work/m/msajatov/private/cms3/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/out/{0}/gof/2017"
    
    if args.input != "":
        runNew(args, base)
        return
    

def runNew(args, base):        
    configurations = args.configs
    
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
    
    tests = ["saturated"]
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]  
    
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
                            
                            try:
                                path = "{0}/{1}/{2}/{3}/fitDiagnostics2017.root".format(basepath, var, test, channel)               
                                
                                tfile = R.TFile(path)
                                tree = tfile.tree_fit_sb                            
                                
                                leaf = tree.GetLeaf("fit_status")
                                leaf.GetBranch().GetEntry(0)
                                fit_status_value = leaf.GetValue()
                                
                                if fit_status_value != 0:
                                    print "{3}, var: {0}; channel: {1}; fit_status = {2}".format(var, channel, fit_status_value, conf)
                            except:
                                print "Exception for {2}, var: {0}; channel: {1}".format(var, channel, conf)
                            
#                             print "var: {0}; channel: {1}".format(var, channel)
#                             tree.Scan("fit_status:r")
                print ""
                print "----------------------------------------"
                print ""            
    
def saveAsJson(pvalues, filename, outputbase):
    dir = outputbase
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
