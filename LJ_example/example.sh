#!/bin/bash

set echo

ln -s ../LJ_initial_cfgs/in.nvt.dens_0.4000 ./
mpirun -np 8 lmp_mpi -in NVT.startfromrestart -var rho 0.4000 -var temp 1.50
../analysis/block_analysis.py -f ave.dens_0.4000.out -b 5 -m 100000
