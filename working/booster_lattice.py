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

    a = synergia.simulation.Lattice_simulator.tune_circular_lattice(lattice)
    print('tcl: ', a)
    print('closed orbit length: ', a[4]*refpart.get_beta())
    return lattice

if __name__ == "__main__":
    lattice = get_booster_lattice()

    print('Read lattice, length: ', lattice.get_length(), ", number elements: ", len(lattice.get_elements()))

    refpart = lattice.get_reference_particle()
    etot = refpart.get_total_energy()
    pmom = refpart.get_momentum()
    gamma = refpart.get_gamma()
    beta = refpart.get_beta()
    print('Lattice energy: ', etot)
    print('Lattice momentum: ', pmom)
    print('Lattice gamma: ', gamma)
    print('Lattice beta: ', beta)

    print('RF cavities:')
    for elem in lattice.get_elements():
        if elem.get_type() == synergia.lattice.element_type.rfcavity:
            print(elem)

    L = lattice.get_length()
    c = synergia.foundation.pconstants.c
    h = 84
    f = h * beta * c/L
    print('frequency should be: ', f)

    closed_orbit = synergia.simulation.Lattice_simulator.calculate_closed_orbit(lattice)
    print('closed orbit: ', closed_orbit)
    
