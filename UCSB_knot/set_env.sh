#!/bin/bash
#Makefile for building / running gem5
#Assume the directory above contains all of the dependencies in a predictable file structure

#Set python path dependencies (require version 2.6.9 for our build)
#export LD_LIBRARY_PATH :=$(deps_path)/python-2.6/Python-2.6.9/lib:${LD_LIBRARY_PATH}
export PATH=../python-2.6/Python-2.6.9/bin:$PATH
