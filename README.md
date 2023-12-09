# SIMON_DS-MITM
These tools are part of the paper Automatic Demirci-Selcuk meet-in-the-middle attack on SIMON.

#DSMITM_SIMON_Dist.py
This python file generates the .lp file including MILP constraints in the distinguisher and the command file(.cmd).  We first run this file to find out the maximum number of distinguisher rounds, and set the number in the key recovery phase searching. 

#DSMITM_SIMON_Key.py
This python file generates the .lp file including MILP constraints in the dinstinguisher combined with key recovery phase.

#feasible solutions
This folder includes the feasible DS-MITM solutions for all versions of SIMON.
