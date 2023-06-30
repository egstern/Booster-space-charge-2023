# Notes

## RBARC?
First question is the RBARC setting. The FRS file sets the RBARC
option. Do I need to change something in my fixup scripts?

It appears Frank has taken the RBENDS and converted them back to SBENDS already.

```
fmag: sbend,l:= 2.889612000000000069377e+00,angle:= 7.074218219630160064959e-02,k1:= 5.442533684999999871179e-02,e1:= 3.537109109815080032480e-02,e2:= 3.537109109815080032480e-02,k2:=-2.859364530955530933620e-03;
dmag: sbend,l:= 2.889612000000000069377e+00,angle:= 6.015751184767671733145e-02,k1:=-5.772919635999999854459e-02,e1:= 3.007875592383835866572e-02,e2:= 3.007875592383835866572e-02,k2:=-3.633387859322498303349e-02;
```

Split `full_beam_machine.madx` back into `booster.ele` and `booster.seq`. Will have to extract fit values for the tunes and chromaticities into a new file `corrector_settings.madx`.

 File `booster_lattice.py` reads lattice. Length matches FRS output 4.742038440788001025794e+02
 
Create file `booster_synth.madx` which is the synthesis of `booster.ele`, `corrector_settings.madx`, and ` booster.seq` in one file.
