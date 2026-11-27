#!/bin/sh
# poll for PROOF steps only (lower bounds / negations); anything that passes poll4's filter stops the loop for the orchestrator
cd /home/user/pvsnp/research/tools
python3 poll4.py
