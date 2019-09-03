import Reader
import evalgof as evalgof
import matplotlib.pyplot as plt
import pandas as pd
from math import pi



def main():
    df = evalgof.loadDF("../output/pvalues.json")
    base = "cc"
    configs = ["cc1", "nn1", "nn2", "nn3", "nn4", "nn5", "nn6", "nn7", "nn8", "nn9", "nn10", "nn11", "nn13", "nn15", "nn16"]

    cols = [base] + configs

    print df
    
    result = evalgof.compareSideBySide(df, "cc", configs, "saturated", "mt")
     
    filtered = result.drop(["dc_type", "gof_mode", "test", "channel"], axis=1)
    
    vars = [
                        "pt_1",
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
                        "met"
                        ]
    
    #drawRadioChartForVars(filtered, "m_vis")
    #drawRadioChartForConfs(filtered, ["cc", "cc1", "nn15"])
    drawRadioChartForConfs(filtered, ["nn13", "nn15", "nn16"])

def drawRadioChartForVars(input_df, vars):
    
#     print df_original
#     df = df_original.T
#     print df
#     
#     df.reset_index(inplace=True)
#     print df    

    print input_df
    df = input_df
    
    print df
    
    for v in vars:
    
        # ------- PART 1: Create background
     
        # number of variable
        categories=list(df)[1:]
        N = len(categories)
         
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
         
        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)
         
        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
         
        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories)
         
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([0.25,0.5,0.75], ["0.25","0.5","0.75"], color="grey", size=7)
        plt.ylim(0,1)
        
        # ------- PART 2: Add plots
     
        # Plot each individual = each line of the data
        # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
        
        index1 = df[df['var']==v].index.values.astype(int)[0]
        print index1
        
        # Ind1
        values=df.loc[index1].drop('var').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="var {0}".format(v))
        ax.fill(angles, values, 'b', alpha=0.1)
         
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        plt.show()
        
def drawRadioChartForConfs(input_df, confs):
    
#     print df_original
#     df = df_original.T
#     print df
#     
#     df.reset_index(inplace=True)
#     print df    

    print input_df
    input_df.set_index("var", inplace=True)
    df = input_df.T
    df.reset_index(inplace=True)
    
    print df
    
    # ------- PART 1: Create background
 
    # number of variable
    categories=list(df)[1:]
    N = len(categories)
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
     
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
     
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
     
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.25,0.5,0.75], ["0.25","0.5","0.75"], color="grey", size=7)
    plt.ylim(0,1)
    
    # ------- PART 2: Add plots
 
    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
    
    for conf in confs:  
        ind = df[df['index']==conf].index.values.astype(int)[0]
        print ind
        
        # Ind1
        values=df.loc[ind].drop('index').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="{0}".format(conf))
        ax.fill(angles, values, 'b', alpha=0.1)
     
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.show()

if __name__ == '__main__':
    main()