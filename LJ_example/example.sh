#!/bin/bash

mpirun -np 12 lmp_mpi -in NVT.startfromrestart -var rho 0.4000 -var temp 1.50
