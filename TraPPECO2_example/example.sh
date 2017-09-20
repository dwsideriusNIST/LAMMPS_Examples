#!/bin/bash

set echo

ln -s ../TraPPECO2_initial_cfgs/TraPPECO2_N1000_config.dens_18.0molL.cfg.lammps
mpirun -np 8 lmp_mpi -in in.TraPPECO2 -var infile TraPPECO2_N1000_config.dens_18.0molL.cfg.lammps -var temp 300.0
../analysis/block_analysis.py -f ave.dens_18.0molL.out -b 5 -m 10000
