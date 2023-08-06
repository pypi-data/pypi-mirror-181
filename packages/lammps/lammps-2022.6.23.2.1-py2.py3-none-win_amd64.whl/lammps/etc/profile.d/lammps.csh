# set environment for LAMMPS and msi2lmp executables
# to find potential and force field files
if ( "$?LAMMPS_POTENTIALS" == 0 ) setenv LAMMPS_POTENTIALS C:/Users/runneradmin/LAMMPS/share/lammps/potentials
if ( "$?MSI2LMP_LIBRARY" == 0 ) setenv MSI2LMP_LIBRARY C:/Users/runneradmin/LAMMPS/share/lammps/frc_files
