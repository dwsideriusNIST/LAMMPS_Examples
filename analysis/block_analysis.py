#!/usr/bin/env python

#------------SOFTWARE DISCLAIMER AND REDISTRIBUTION CONDITIONS----------------
#   This software was developed at the National Institute of Standards and
#   Technology by employees of the Federal Government in the course of their
#   official duties. Pursuant to Title 17 Section 105 of the United States 
#   Code this software is not subject to copyright protection and is in the 
#   public domain. block_analysis.py is an experimental system. NIST assumes no
#   responsibility whatsoever for its use by other parties, and makes no
#   guarantees, expressed or implied, about its quality, reliability, or any
#   other characteristic. We would appreciate acknowledgement if the software
#   is used.
#
#   This software can be redistributed and/or modified freely provided that 
#   any derivative works bear some notice that they are derived from it, and 
#   any modified versions bear some notice that they have been modified.
#
#-----------------------------------------------------------------------------
#   Software Name: block_analysis.py
#   Brief Description: Script to compute the averages and uncertainty
#    of column-organized output from LAMMPS. Uses the standard block
#    averaging technique outlined in:
#      "Understanding Molecular Simulation: From Algorithms to Applications",
#        by D. Frenkel and B. Smit (Second Edition, pages 529-532)
#      "Computer Simulation of Liquids", by M.P. Allen and D. J. Tildesley
#        (pages 191-195)
#
#   Author: Daniel W. Siderius, PhD
#   Contact Information: daniel.siderius@nist.gov
#
#   Version History: Consult Git Log (> git log)
#-----------------------------------------------------------------------------

import math
import numpy as np
import sys
import optparse

class LAMMPS_Thermo(object):
    def __init__(self):
        self.timeseries = []
    def ensemble_avg(self):
        return np.mean(self.timeseries)
    def block_avg(self,blocks):
        block_size = int( float(len(self.timeseries)) / float(blocks) )
        #print(block_size)
        sumsq = 0.0; sum = 0.0; bsum = 0.0; count = 0
        for (i,entry) in enumerate(self.timeseries):
            bsum = bsum + entry
            if ( (i+1) % block_size ) == 0:
                bsum = bsum / float(block_size)
                sum = sum + bsum ; sumsq = sumsq + (bsum**2) ; count = count + 1
                bsum = 0.0
        avg = sum / float(count) ; sq_avg = sumsq / float(count)
        if np.abs(sq_avg - avg**2)/sq_avg < 1.0e-10:
            #This handles cases where the column is invariant
            return avg, 0.0 
        else:
            return avg, np.sqrt((sq_avg-(avg**2))/float(count))

def main():
    #Parse Command-line Arguments
    opts = parse_commandline_opts()
    filename = opts.file
    min_timestep = opts.minsteps
    blocks = opts.blocks

    #Read in the data
    data_file = open(filename,mode='r')
    for (i,line) in enumerate(data_file):
        #Do not read first line
        if i == 1:
            #Second line contains column headers
            columns = line.replace("#","").replace("v_","").split()
            columns = columns[1:] #Get rid of the timestep column
            #Create time-series data objects
            timestep = []
            LAMMPS_data = [ LAMMPS_Thermo() for x in columns ]
        elif i > 1:
            #Add the current line of data to the time-series data objects
            if int(line.split()[0]) > min_timestep:
                timestep.append(int(line.split()[0]))
                for j in range(len(columns)):
                    LAMMPS_data[j].timeseries.append(float(line.split()[j+1]))
    data_file.close()
    delta_timestep = timestep[1] - timestep[0]

    #Output Thermodynamic Averages and Statistical Uncertain
    print('Thermodynamic Ensemble Averages from: '+filename)
    print('  Discarded Timesteps:    '+str(min_timestep))
    print('  Number of Blocks:       '+str(blocks))
    print('  Block size (timesteps): '+str(len(timestep)/blocks*delta_timestep))
    print('  Stated uncertainty is the standard error of the thermodynamic property')
    print('')
    for (i,column) in enumerate(columns): 
        print(format(column, "<15"), format(LAMMPS_data[i].ensemble_avg(), "+8.4E"), ' +/- ', \
            format(LAMMPS_data[i].block_avg(blocks)[1], "+8.4E") )
        
def parse_commandline_opts():
    op = optparse.OptionParser()
    op.add_option("-f", "--file",     help="Specify the file containing LAMMPS time-series data")
    op.add_option("-b", "--blocks",   help="Specify the number of blocks for estimating error")
    op.add_option("-m", "--minsteps", help="Specify the number of timesteps for equilibration")
    opts,args = op.parse_args()
    if not opts.file or not opts.blocks or not opts.minsteps:
        sys.exit("Please specify:\n"+
                 "   1) Data filename '-f filename'\n" +
                 "   2) Number of blocks '-b #'\n" +
                 "   3) Number of steps for equilibration '-m #'\n" +
                 "Use -h flag to view options")
    #Ensure blocks and minsteps are integers
    opts.blocks = int(opts.blocks)
    opts.minsteps = int(opts.minsteps)
    return opts

# Execute main function if this file is the starting point
if __name__ == '__main__':
    main()

