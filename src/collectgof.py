import json
import os
import argparse


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('-i', dest='input', help='Input', default="")
    parser.add_argument('-a', dest='append', help='Append to existing file if found', action="store_true")
    parser.add_argument('conf', nargs="*", help='Configurations', default=[])
    args = parser.parse_args()
    
    # base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017"
    base = "/afs/cern.ch/work/m/msajatov/private/cms3/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/out/{0}/gof/2017"

    if args.input != "":
        runNew(args, base)
        return
         

def runNew(args, base):    
    
    print "entering runNew..."

    if args.conf:
        print "confs from argument"
        configurations = args.conf
    
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
                
    if args.append:            
        path = "{0}_pvalues.json".format(args.channel)
        existing = load(path, "output")
        completepvalues = merge(existing, completepvalues)    
    
    saveAsJson(completepvalues, "{0}_pvalues".format(args.channel), "output")
    
def merge(existing, new):
        
    # print "Existing: {0}".format(existing)
    # print "New: {0}".format(new)
    # pvalues[dc_type][gof_mode][conf][var][test][channel]
    
    ignorevars = ["eta_1", "eta_2"]
    #ignorevars = []
    
    dc_types = ["emb_dc"]
    #gof_modes = ["results_w_emb", "results_wo_emb"]
    gof_modes = ["results_w_emb"]
    confs = []
    variables = []
    tests = ["saturated", "KS", "AD"]
    channels = ["et", "mt", "tt"]
    
    temp = next(new.itervalues())
    temp = next(temp.itervalues())
    
    for key, value in temp.items():
        confs.append(key)
        
    temp = next(temp.itervalues())
    for key, value in temp.items():
        variables.append(key)
    
    # for igv in ignorevars:
    #     variables.remove(igv)
    
    rows_list = []
    # iterate over new dict
    for dc_type_key, dc_type_val in new.items():
        for gof_mode_key, gof_mode_val in dc_type_val.items():            
            for confkey, confval in gof_mode_val.items():
                existing[dc_type_key][gof_mode_key][confkey] = confval
                    
            
    # print existing
    return existing

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

def load(path, outputbase):
    try:
        with open(os.path.join(outputbase, path), "r") as FSO:
            pvalues = json.load(FSO)
    except ValueError as e:
        print e
        print "ValueError while parsing pvalues"
        return
    except IOError as e:
        print "IOError while parsing pvalues"
        print e
        return
    return pvalues
    
if __name__ == '__main__':
    main()
