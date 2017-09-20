#!/bin/bash

set echo

ln -s ../TraPPEN2_initial_cfgs/TraPPEN2_N1000_config.dens_22.0molL.cfg.lammps
mpirun -np 8 lmp_mpi -in in.TraPPEN2 -var infile TraPPEN2_N1000_config.dens_22.0molL.cfg.lammps -var temp 110.0
../analysis/block_analysis.py -f ave.dens_22.0molL.out -b 5 -m 10000
