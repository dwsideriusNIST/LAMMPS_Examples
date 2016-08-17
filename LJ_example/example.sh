#!/bin/bash

ln -s ../LJ_initial_cfgs/in.nvt.dens_0.0400 ./
mpirun -np 8 lmp_mpi -in NVT.startfromrestart -var rho 0.4000 -var temp 1.50
