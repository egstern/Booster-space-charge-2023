#!/usr/bin/env python

import sys, os
import numpy as np
import synergia

mp = synergia.foundation.pconstants.mp
etot = 1.353543422829672548957e+00

# Read and return the Booster lattice set up with the reference particle
def get_booster_lattice():
    # First read elements
    lattice_txt = ""
    mfile = open("booster.ele", "r")
    lattice_txt = lattice_txt + mfile.read()
    mfile.close()

    # Now get corrector settings
    mfile = open("corrector_settings.madx", "r")
    lattice_txt = lattice_txt + mfile.read()
    mfile.close()

    # Now get full sequence
    mfile = open("booster.seq", "r")
    lattice_txt = lattice_txt + mfile.read()
    mfile.close()

    reader = synergia.lattice.MadX_reader()
    reader.parse(lattice_txt)

    lattice = reader.get_lattice('machine')

    refpart = synergia.foundation.Reference_particle(1, mp, etot)

    lattice.set_reference_particle(refpart)

    return lattice

if __name__ == "__main__":
    lattice = get_booster_lattice()

    print('Read lattice, length: ', lattice.get_length(), ", number elements: ", len(lattice.get_elements()))
