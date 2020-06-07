import json
import os
import argparse


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel', choices = ['mt', 'et', 'tt', 'all'], default='all')
    parser.add_argument('--vars', dest='vars', nargs="*", help='Variable', default=[])
    parser.add_argument('--algos', dest='algos', nargs="*", help="Algorithm", default=["saturated", "KS", "AD"])
    parser.add_argument('-a', dest='append', help='Append to existing file if found', action="store_true")
    parser.add_argument('--conf', dest='conf', nargs="*", help='Configurations', default=[])
    args = parser.parse_args()
    
    # base = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017"
    base = "/afs/cern.ch/work/m/msajatov/private/cms3/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/out/{0}"

    runNew(args, base)
         

def runNew(args, base):    
    
    print "entering runNew..."
    
    configurations = args.conf
    
    # variables = ["pt_1", 
    #              "pt_2", 
    #              "jpt_1", 
    #              "jpt_2", 
    #              "bpt_1", 
    #              "bpt_2", 
    #              "njets", 
    #              "nbtag",
    #              "m_sv", 
    #              "mt_1", 
    #              "mt_2", 
    #              "pt_vis", 
    #              "pt_tt", 
    #              "mjj", 
    #              "jdeta",
    #              "m_vis", 
    #              "dijetpt", 
    #              "met",
    #              "eta_1",
    #              "eta_2"]

    variables = args.vars
    
    # tests = ["saturated", "KS", "AD"]
    tests = args.algos
    
    if args.channel == "all":
        channels = ["et", "mt", "tt"]
    else:
        channels = [args.channel]     

    seed_list = ["1230:1249:1", "1250:1269:1", "1270:1289:1", "1290:1309:1", "1310:1329:1", "1330:1349:1",
                "1350:1369:1", "1370:1389:1", "1390:1409:1", "1410:1429:1", "1430:1449:1",
                "1450:1469:1", "1470:1489:1", "1490:1509:1", "1510:1529:1", "1530:1549:1",
                "1550:1569:1", "1570:1589:1", "1590:1609:1", "1610:1629:1"]   
    
    
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
                for seed in seed_list:
                    pvalues[conf][seed] = {}
                    basepath = base.format(conf)                    
                    for var in variables:
                        pvalues[conf][seed][var] = {}
                        for test in tests:
                            pvalues[conf][seed][var][test] = {}
                            for channel in channels:                              

                                
                                path = "{0}/gof/{1}/2017/{2}/{3}/{4}/gof.json".format(basepath, seed, var, test, channel)
                                print path               
                                
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
                                
                                try:
                                    if test == "saturated":                                         
                                        pvalues[conf][seed][var][test][channel] = data["125.0"]["p"]
                                    else:                                        
                                        pvalues[conf][seed][var][test][channel] = data["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]                                
                                except:
                                    print "Exception"

                # for var in variables:
                #         for test in tests:
                #             for channel in channels:

                #                 pvalues[conf]["aggregate"] = {}
                #                 pvalues[conf]["aggregate"][var] = {}
                #                 pvalues[conf]["aggregate"][var][test] = {}


                #                 aggregate(basepath, channel, "2017", var, test, seed_list)

                #                 path = "{0}/gof/aggregate/2017/{2}/{3}/{4}/gof.json".format(basepath, seed, var, test, channel)               
                                
                #                 try:
                #                     with open(path, "r") as FSO:
                #                         data = json.load(FSO)
                #                 except ValueError as e:
                #                     print e
                #                     print "Check {0}. Probably a ',' ".format(ccpath)
                #                 except IOError as e:
                #                     print "Exception while parsing {0} {1} {2} for {3}".format(var, test, channel, conf)
                #                     print e
                #                     continue
                                
                #                 try:
                #                     if test == "saturated":                                          
                #                         pvalues[conf]["aggregate"][var][test][channel] = data["125.0"]["p"]
                #                     else:                                        
                #                         pvalues[conf]["aggregate"][var][test][channel] = data["125.0"]["htt_{0}_100_Run2017".format(channel)]["p"]
                #                 except:
                #                     print "Exception"

            completepvalues[dc_type][gof_mode] = pvalues
                
    if args.append:            
        path = "{0}_pvalues_seeds.json".format(args.channel)
        if os.path.exists(path):
            existing = load(path, "output_seeds")
            print existing
            if existing is not None:
                # completepvalues = merge(existing, completepvalues) 
                completepvalues = mergeDicts(existing, completepvalues)   
    
    saveAsJson(completepvalues, "{0}_pvalues_seeds".format(args.channel), "output_seeds")
    
def aggregate(basepath, channel, era, var, algo, seed_list):

    # cd into aggregate dir
    cwd = os.getcwd()
    os.chdir(basepath)

    seedstring = ""
    for seed in seed_list:
        seedstring += seed + " "

    cmd = "sh aggregate.sh {0} {1} {2} {3} {4}".format(channel, era, var, algo, seedstring) 

    # system call to aggregate.sh 
    os.system(cmd)

    # cd back
    os.chdir(cwd)

def mergeDicts(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergeDicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

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

    # seeds = True

    # for dc_type_key, dc_type_val in pvalues.items():
    #     for gof_mode_key, gof_mode_val in dc_type_val.items():            
    #         for confkey, confval in gof_mode_val.items():
    #             if seeds:
    #                 for seedkey, seedval in confval.items():
    #                     for varkey, varval in seedval.items():
    #                         for testkey, testval in varval.items():
    #                             for chkey, chval in testval.items():
    #                                 if existing[dc_type_key][gof_mode_key][confkey][seedkey][varkey][testkey] is None:

            
    # print existing
    return existing

def saveAsJson(pvalues, filename, outputbase):
    dir = outputbase
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, filename + ".json"), 'wb') as FSO:
            json.dump(pvalues, FSO)  
        
def saveOutput(filename, data):
    f = open("output_seeds/" + filename, "w")
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
