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
    
    if args.input != "":
        runNew(args, args.input)
        return
    

def runNew(args, boundary):    
    
    print "entering runNew..."
    
    if args.configs:            
        common = args.configs
        conf_a = []
        conf_a2 = []
        conf_e = []
    else:
        if boundary == "":
            common = ["cc", "cc1", "cc2", "nn1", "nn6", "nn13", "nn21"] + ["nn5", "nn10", "nn18"]
            conf_a = ["nn1a", "nn5a", "nn6a", "nn10a", "nn13a", "nn18a"]
            conf_a2 = []
            conf_e = []
        else:
            common = ["cc", "cc1", "cc2"] + ["nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10"]
            conf_a = []
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
    
    tests = ["saturated"]
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]
        
    if boundary == "":
    #gof_modes = ["results_w_emb", "results_wo_emb"]
        base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest/{0}/gof/2017"
    elif boundary == "original":
        base = "/afs/cern.ch/work/m/msajatov/private/cms/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/emb_dc/results_w_emb/{0}/gof/2017"
    elif boundary == "10":
        base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest2/{0}/gof/2017"
    elif boundary == "20":
        base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest3/{0}/gof/2017"
    else:
        base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest{1}/{0}/gof/2017"
    
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
                if not boundary:
                    basepath = base.format(conf)
                elif not "original" in boundary:
                    basepath = base.format(conf, boundary)
                else:
                    basepath = base.format(conf)
                for var in variables:
                    pvalues[conf][var] = {}
                    for test in tests:
                        pvalues[conf][var][test] = {}
                        for channel in channels:
                            path = "{0}/{1}/{2}/{3}/fitDiagnostics2017.root".format(basepath, var, test, channel)               
                            
                            tfile = R.TFile(path)
                            tree = tfile.tree_fit_sb
                            
                            print "var: {0}; channel: {1}".format(var, channel)
                            tree.Scan("fit_status:r")
                            
    
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
