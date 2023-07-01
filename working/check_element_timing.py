#!/usr/bin/env python

import sys, os
import numpy as np
import booster_lattice
import synergia

def main():
    lattice = booster_lattice.get_booster_lattice()
    
    refpart = lattice.get_reference_particle()
    etot = refpart.get_total_energy()
    pmom = refpart.get_momentum()
    gamma = refpart.get_gamma()
    beta = refpart.get_beta()
    print('Lattice energy: ', etot)
    print('Lattice momentum: ', pmom)
    print('Lattice gamma: ', gamma)
    print('Lattice beta: ', beta)

    # Turn off RF cavities
    for elem in lattice.get_elements():
        if elem.get_type() == synergia.lattice.element_type.rfcavity:
            elem.set_double_attribute('volt', 0)
            elem.set_double_attribute('lag', 0)
            elem.set_double_attribute('harmon', 0)

    stepper = synergia.simulation.Independent_stepper_elements(1)

    propagator = synergia.simulation.Propagator(lattice, stepper)

    sim = synergia.simulation.Bunch_simulator.create_single_bunch_simulator(refpart, 8, 1.0e9)

    elements = list(lattice.get_elements())
    
    elem_lens = []
    # step_end_action(sim, lattice, turn, step)
    def step_end_action(sim, lattice, turn, step):
        bunch = sim.get_bunch()
        desref = bunch.get_design_reference_particle()
        elem_len = desref.get_state()[4]*desref.get_beta()
        elem_lens.append(elem_len)

    sim.reg_prop_action_step_end(step_end_action)

    simlog = synergia.utils.parallel_utils.Logger( 0,
        synergia.utils.parallel_utils.LoggerV.INFO_TURN)

    propagator.propagate(sim, simlog, 1)

    for i in range(len(elem_lens)):
        if ((elements[i].get_length() == 0.0) and
            (elem_lens[i] == 0.0)):
            continue

        if abs( 1 - elem_lens[i]/elements[i].get_length()  ) > 1.0e-7:
            print('step: ', i, ' length mismatch, lattice: ', elements[i].get_length(), ' <=> ', elem_lens[i], ' propagate')
            print(elements[i])
            print()

if __name__ == "__main__":
    main()
