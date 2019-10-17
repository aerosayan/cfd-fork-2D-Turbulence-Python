#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Marin Lauber"
__copyright__ = "Copyright 2019, Marin Lauber"
__license__ = "GPL"
__version__ = "1.0.1"
__email__  = "M.Lauber@soton.ac.uk"

import time as t
import numpy as np
from fluid import fluid

if __name__=="__main__":

    # build fluid and solver
    flow = fluid(128, 128, 1.)
    flow._init_field()
    flow._init_solver()

    print("Starting interating on field.\n")
    start_time = t.time()
    iterr = 0
    finish = 0.1

    # loop to solve
    while(flow.time<=finish):

        #  update using RK
        flow.update()
        iterr += 1

        #  print every 100 iterations
        if (iterr % 100 == 0):
            print("Iteration \t %d, time \t %f, time remaining \t %f" %(iterr, flow.time, finish-flow.time))

    end_time = t.time()
    print("\nExecution time for %d iterations is %f seconds." %(iterr, end_time-start_time))

    # get final results
    flow.wh_to_w()
    w_n = flow.w

    # exact solution
    flow._init_field("TG", t=flow.time)

    # L2-norm and exit 
    L2 = np.sqrt((flow.nx*flow.ny)**(-1)*np.einsum('ij->', (np.abs(flow.w - w_n))**2))
    Linf = np.max(np.abs(flow.w - w_n))
    print("The L2-norm of the Error in the Taylor-Green vortex on a %dx%d grid is %e." % (flow.nx, flow.ny, L2) )
    print("The Linf-norm of the Error in the Taylor-Green vortex on a %dx%d grid is %e." % (flow.nx, flow.ny, Linf) )