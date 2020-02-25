#SAMI CHAABAN
#VERSION 1.1 2020-02-25

import optparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import sys
import os.path
from os import path

def setupParserOptions():
    parser = optparse.OptionParser(usage="Usage: %prog [options] filename",
                          version="%prog 1.01 2020-02-24")
    parser.add_option("-c", "--conductance",
                  action="store_true", dest="conductance", default=False,
                  help="Overlay conductance trace")
    parser.add_option("-b", "--percent_b",
                  action="store_true", dest="percentb", default=False,
                  help="Overlay % B")
    parser.add_option("-l", "--log",
                  action="store_true", dest="log", default=False,
                  help="Overlay the akta log (e.g. injection and elution)")
    parser.add_option("-f", "--akta_fracs",
                  action="store_true", dest="fracs", default=False,
                  help="Overlay the fractions generated by the Akta fraction collector")
    parser.add_option("-t", "--cetac_fracs",
                  action="store_true", dest="cetac", default=False,
                  help="Overlay the fractions generated by the Cetac fraction collector")
    parser.add_option("-o", "--only_fracs",
                  action="store_true", dest="only_fracs", default=False,
                  help="Only show region where fractions were collected. Use -e as well to only show the elution fractions")
    parser.add_option("-e", "--only_elution",
                  action="store_true", dest="only_elution", default=False,
                  help="Only show region where elution fractions were collected. This is based on where the 'Elution' akta log starts")
    parser.add_option("-n", "--hide_labels",
                  action="store_true", dest="hide_cetaclab", default=False,
                  help="Remove the Cetac fraction labels generated by this script.")
    parser.add_option("-m", "--uvmax",
                  action="store_true", dest="uvmax", default=False,
                  help="Draw a vertical line at the maximum UV value.")

    options,args = parser.parse_args()

    if len(args) > 1:
            parser.error("\nToo many filenames.")

    if len(args) == 0:
            parser.error("\nNo filename. Run plotakta.py -h to get the help text.")
            
    if len(sys.argv) < 2:
            parser.print_help()
            sys.exit()

    params={}

    for i in parser.option_list:
            if isinstance(i.dest,str):
                    params[i.dest] = getattr(options,i.dest)
                    
    params['file'] = args[0]
                    
    return(params)

def mainloop(params):
    
    
    doUV = True
    doCond = params["conductance"]
    doConcB = params["percentb"]
    doLog = params["log"]

    #FOR REGULAR AKTA FRACS
    doFracs = params["fracs"]

    #FOR CETAC SOFTWARE
    doDig1 = params["cetac"]
    doDig1Label = True
    hideDig1 = params["hide_cetaclab"]
    
    showOnlyFracs = params["only_fracs"] #only show region in between first and last fractions
    useElutionMark = params["only_elution"] #this is for when you also fractionated flow-through but only want to plot fractionated eluted protein

    showUVmax = params["uvmax"] #draw line at maximum uv
    
    if doDig1 and hideDig1:
        doDig1Label = False        

    aktafile = params["file"]

#Test code from here

    aktafile_exists = path.exists(aktafile)

    if not aktafile_exists:

        print('\nERROR: ' + aktafile + ' does not exist.Run plotakta.py -h to get the help text.')

        sys.exit()

    #####################################################

    aktalst = []

    with open(aktafile, newline = '', encoding = 'utf16') as items:                                                                                          
        readme = csv.reader(items, delimiter='\t')
        for i in readme:
            aktalst.append(i)

    aktalst = list(map(list, zip(*aktalst)))

    #####################################################

    def clean(lst):
        lst[:] = [x for x in lst if x]
        return(lst)

    def floatize(lst):
        lst = [float(i) for i in lst]
        return(lst)

    def find_dig1_lab(dig1_x,dig1_signal):

        plate = ['A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12',
                'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12',
                'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12',
                'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12',
                'E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12',
                'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
                'G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12'
                'H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12']


        dig1lab_x = []
        dig1lab_frac = []

        p = 0

        peakflag = 0

        alreadydone = 0

        newpeak = 0

        for dx,ds in zip(dig1_x,dig1_signal):

            if ds == 1:

                if newpeak == 1:

                    dig1lab_x.append((dx+dxtemp)/2)

                    newpeak = 0

                peakflag = 1

                alreadydone = 0

            if ds == 0 and peakflag == 1 and alreadydone != 1:

                dxtemp = dx

                #dig1lab_x.append(dx)

                dig1lab_frac.append(plate[p])
                p += 1

                alreadydone = 1

                peakflag = 0

                newpeak = 1

        return(dig1lab_x, dig1lab_frac)


    ###########################################################

    uv_x = 0
    cond_x = 0
    concb_x = 0
    frac_x = 0
    log_x = 0
    dig1_x = 0

    for n,i in enumerate(aktalst):
        #print(i[1])
        if i[1] == 'UV 1_280':

            uv_x = i[3:]
            uv_x = floatize(clean(uv_x))

            uv_trace = aktalst[n+1][3:]
            uv_trace = floatize(clean(uv_trace))

        if i[1] == 'Cond':

            cond_x = i[3:]
            cond_x = floatize(clean(cond_x))

            cond_trace = aktalst[n+1][3:]
            cond_trace = floatize(clean(cond_trace))

        if i[1] == 'Conc B':

            concb_x = i[3:]
            concb_x = floatize(clean(concb_x))

            concb_trace = aktalst[n+1][3:]
            concb_trace = floatize(clean(concb_trace))

        if i[1] == 'Fraction':

            frac_x = i[3:]
            frac_x = floatize(clean(frac_x))

            fracs = clean(aktalst[n+1][3:])

            frac_x = frac_x[:len(fracs)]   

        if i[1] == 'Run Log':

            log_x = i[3:]
            log_x = floatize(clean(log_x))

            log_text = clean(aktalst[n+1][3:])
            
        if i[1] == 'Run Log':

            log_x = i[3:]
            log_x = floatize(clean(log_x))

            log_text = clean(aktalst[n+1][3:])

        if i[1] == 'Digital in 1':

            dig1_x = i[3:]
            dig1_x = floatize(clean(dig1_x))

            dig1_signal = aktalst[n+1][3:]
            dig1_signal = floatize(clean(dig1_signal))
            
    #######################################################################

    if uv_x == 0:

        print('\nERROR: No \'UV 1_280\' (UV trace) column in the CSV file.')
        sys.exit()
        
    if doCond and cond_x == 0:

        print('\nERROR: No \'Cond\' (conductance) column in the CSV file.')
        sys.exit()
        
    if doConcB and concb_x == 0:

        print('\nERROR: No \'Conc B\' (concentration B) column in the CSV file.')
        sys.exit()
        
    if doFracs and frac_x == 0:

        print('\nERROR: No \'Fraction\' column in the CSV file.')
        sys.exit()
        
    if doLog and log_x == 0:

        print('\nERROR: No \'Run Log\' column in the CSV file.')
        sys.exit()
        
    if doDig1 and dig1_x == 0:

        print('\nERROR: No \'Digial in 1\' Cetac column in the CSV file.')
        sys.exit()

    #####################################################

    xmin = uv_x[0]
    xmax = uv_x[-1]

    ymins = []
    ymaxs = []

    #####################################################        

    fig,ax = plt.subplots(figsize = (20,5))

    if useElutionMark:

        idx = np.searchsorted(uv_x, log_x[log_text.index('Elution')], side="left")

        uv_x = uv_x[idx:]
        uv_trace = uv_trace[idx:]

    if doUV:

        ax.plot(uv_x, uv_trace, linewidth = 2, color = 'darkblue')

    # MAIN PLOT

    plt.xlabel('Volume (mL)', fontsize = 20, fontname="Arial")
    plt.ylabel('Absorbance 280nm (mAU)', fontsize = 20, fontname="Arial", color = 'darkblue')
    plt.xticks(fontsize = 20, fontname="Arial")
    plt.yticks(fontsize = 20, fontname="Arial")

    ymins.append(ax.get_ylim()[0])
    ymaxs.append(ax.get_ylim()[1])

    if doConcB:

        ax4=ax.twinx()
        ax4.plot(concb_x, concb_trace, color = 'green', linewidth = 2)
        ax4.set_ylabel("Concentration B (%)",fontsize=20, color = 'green')
        ax4.yaxis.set_tick_params(labelsize=20)
        ax4.set_ylim(0, 100)

        if doCond:
            ax4.spines["right"].set_position(("axes", 1.1))
            
        ymins.append(ax4.get_ylim()[0])
        ymaxs.append(ax4.get_ylim()[1])

    if doCond:

        ax3=ax.twinx()
        ax3.plot(cond_x, cond_trace, color = 'brown', linewidth = 2)
        ax3.set_ylabel("Conductance (mS/cm)",fontsize=20, color = 'brown')
        ax3.yaxis.set_tick_params(labelsize=20)
        
        ymins.append(ax3.get_ylim()[0])
        ymaxs.append(ax3.get_ylim()[1])
        
    ##############

    ymin = np.amin(ymins)
    ymax = np.amax(ymaxs)

    if doLog:

        for lx, lt in zip(log_x, log_text):

            if showOnlyFracs and doDig1:

                if lx > np.amin(dig1lab_x) and lx < np.amax(dig1lab_x):

                    ax.text(lx, int(np.amax(uv_trace)*0.7), lt, fontsize=12, rotation = 90,
                             horizontalalignment='center', fontname="Arial", color = 'r', alpha = 0.6)

                    ax.plot([lx, lx], [ymin,np.amax(uv_trace)*0.66], '-',
                            color = 'r', alpha = 0.6, linewidth = 1)

            elif showOnlyFracs and doFracs and useElutionMark:

                if lx > log_x[log_text.index('Elution')] and lx < np.amax(frac_x):

                    ax.text(lx, int(np.amax(uv_trace)*0.7), lt, fontsize=12, rotation = 90,
                             horizontalalignment='center', fontname="Arial", color = 'r', alpha = 0.6)

                    ax.plot([lx, lx], [ymin,np.amax(uv_trace)*0.66], '-',
                            color = 'r', alpha = 0.6, linewidth = 1)

            elif showOnlyFracs and doFracs:

                if lx > np.amin(frac_x) and lx < np.amax(frac_x):

                    ax.text(lx, int(np.amax(uv_trace)*0.7), lt, fontsize=12, rotation = 90,
                             horizontalalignment='center', fontname="Arial", color = 'r', alpha = 0.6)

                    ax.plot([lx, lx], [ymin,np.amax(uv_trace)*0.66], '-',
                            color = 'r', alpha = 0.6, linewidth = 1)

            else:

                ax.text(lx, int(np.amax(uv_trace)*0.7), lt, fontsize=12, rotation = 90,
                         horizontalalignment='center', fontname="Arial", color = 'r', alpha = 0.6)

                ax.plot([lx, lx], [ymin,np.amax(uv_trace)*0.66], '-',
                        color = 'r', alpha = 0.6, linewidth = 1)

    if doDig1:

        try:

            ax2=ax.twinx()
            ax2.plot(dig1_x, dig1_signal, color = 'k', linewidth = 0.5, alpha = 0.25)
            ax2.tick_params(
                axis='y',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                right=False,      # ticks along the bottom edge are off
                labelright=False) # labels along the bottom edge are off
            ax2.yaxis.set_tick_params(labelsize=20)

            if doDig1Label:

                dig1lab_x, dig1lab_frac = find_dig1_lab(dig1_x, dig1_signal)

                dig1lab_x_frac = []

                for d in np.arange(0,len(dig1lab_x)-1):

                    dig1lab_x_frac.append((dig1lab_x[d] + dig1lab_x[d+1]) /2)

                for dx, df, dfx in zip(dig1lab_x, dig1lab_frac, dig1lab_x_frac):

                    if dx < uv_x[-1]:

                        ax2.text(dfx, 0.33, df, fontsize=15, rotation = 90,
                        horizontalalignment='center', fontname="Arial", color = 'k', alpha = 0.6)

                        ax2.plot([dx, dx], [0,1], '--', color = 'k', alpha = 0.6, linewidth = 1)


            if showOnlyFracs:

                xmin = np.amin(dig1lab_x)-0.5
                xmax = uv_x[-1]

            else:

                xmin = uv_x[0]
                xmax = uv_x[-1]

        except:

            print('\nERROR: Something went wrong parsing the Cetac data.')

            sys.exit()
            
    if showUVmax:

        maxpos = uv_trace.index(max(uv_trace))
        maxvol = uv_x[maxpos]

        ax.plot([maxvol, maxvol], [ymin, np.amax(uv_trace)], color = 'orange', linewidth = 1.5)

    if doFracs:

        frac_x_loc = []

        for d in np.arange(0,len(frac_x)-1):

            frac_x_loc.append((frac_x[d] + frac_x[d+1]) /2)

        for fx, ff, fxl in zip(frac_x, fracs, frac_x_loc):

            if useElutionMark:

                if fx > log_x[log_text.index('Elution')]:

                    ax.text(fxl, int(np.amax(uv_trace)/8), ff, fontsize=15, rotation = 90,
                             horizontalalignment='center', fontname="Arial", color = 'k', alpha = 0.6)

                    ax.plot([fx, fx], [ymin, ymax], '--', color = 'k', alpha = 0.6, linewidth = 1)

            else:

                ax.text(fxl, int(np.amax(uv_trace)/8), ff, fontsize=15, rotation = 90,
                         horizontalalignment='center', fontname="Arial", color = 'k', alpha = 0.6)

                ax.plot([fx, fx], [ymin, ymax], '--', color = 'k', alpha = 0.6, linewidth = 1)

        if showOnlyFracs:

            if useElutionMark:

                xmin = log_x[log_text.index('Elution')]
                xmax = np.amax(frac_x)

            else:

                xmin = np.amin(frac_x)
                xmax = np.amax(frac_x)

        else:

            xmin = uv_x[0]
            xmax = uv_x[-1]

    plt.xlim(xmin, xmax)

    spacing = (xmax - xmin)/10

    if spacing < 1:
        spacing = 0.5
    if spacing > 0.9 and spacing < 3:
        spacing = 1
    elif spacing > 1 and spacing < 5:
        spacing = 2.5
    elif spacing > 5 and spacing < 15:
        spacing = 10
    elif spacing > 10 and spacing < 50:
        spacing = 25
    elif spacing > 40 and spacing < 100:
        spacing = 50
    elif spacing > 60 and spacing < 150:
        spacing = 50
    elif spacing > 140:
        spacing = 100

    ax.xaxis.set_major_locator(ticker.MultipleLocator(spacing))

    plt.tight_layout()

    plt.savefig(aktafile[:-4]+'.pdf')
    plt.savefig(aktafile[:-4]+'.png', dpi=300)

    plt.show()

    plt.ion()

    print('\nOutput: ' + aktafile[:-4] + '.pdf and .png')

#Test code ends here
    
    sys.exit()
    
if __name__ == "__main__":
    params = setupParserOptions()
    mainloop(params)