#!python
# -*- coding: utf-8 -*-
import sys
import nysol.util.margs as margs
import nysol.take as nt


args=margs.Margs(sys.argv,"ei=,ef=,ni=,nf=,-all,o=,l=,u=,log=,-rp","ei=,ef=")
nt.mclique(**(args.kvmap())).run(msg="on")

