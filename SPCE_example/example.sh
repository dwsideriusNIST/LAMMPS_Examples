#!/bin/bash

set echo

ln -s ../SPCE_initial_cfgs/spce_N1500_config.dens_1000kgm3.lammps ./
mpirun -np 8 lmp_mpi -in in.spce -var infile spce_N1500_config.dens_1000kgm3.lammps -var temp 300.0
../analysis/block_analysis.py -f ave.dens_1000kgm3.out -b 5 -m 10000
