# EQeq

Charge equilibration method for crystal structures.

Modified version, which allows specifying additional parameters:

- `lambda` (default: 1.2) The dielectric screening parameter. Corresponds to eps_eff = 1.67
- `hI0` (default: -2.0) The electron affinity of hydrogen
- `chargePrecision` (default: 3) Number of digits to use for point charges
- `method` (default: "ewald", alternative: "nonperiodic") Method to compute the Coulombic interaction
- `mR` (default: 2) Number of "expansion" unit cells to consider in periodic calculation ("real space"). 2 => 5x5x5
- `mK` (default: 2) Number of "expansion" unit cells to consider in periodic calculation ("frequency space"). 2 => 5x5x5
- `eta` (default: 50) Ewald splitting parameter
- `ionizationdata` (default: [ionizationdata.dat](data/ionizationdata.dat)) File with ionization potentials and electron affinities. Default data are
  EA: experimental, [T.Andersen et al., 1999](http://aip.scitation.org/doi/10.1063/1.556047)
  IP: experimental, [C.E.Moore, 1970](https://nvlpubs.nist.gov/nistpubs/Legacy/NSRDS/nbsnsrds34.pdf)
- `chargecenters` (default: [chargecenters.dat](data/chargecenters.dat)) File with common oxidation states (lowered, if missing ionizationdata)

## Installation

```bash
pip install pyeqeq
```

## Usage

### Command line interface

To run the HKUST-1 example:

```bash
eqeq examples/HKUST1/HKUST1.cif -o examples/HKUST1/HKUST1_w_charge.cif
```

### Python interface

```python
from pyeqeq import run_on_cif
run_on_cif("examples/HKUST1/HKUST1.cif")
```

## Summary

The source code in this program demonstrates the charge equilibration method described
in the accompanying paper. The purpose of the source code provided is to be
minimalistic and do "just the job" described. In practice, you may wish to add various
features to the source code to fit the particular needs of your project.

### Major highlights of program:

- Obtains charges for atoms in periodic systems without iteration
- Can use non-neutral charge centers for more accurate point charges
- Designed for speed (but without significant code optimizations)

### Features not implemented but that you may want to consider adding:

- Spherical cut-offs (for both real-space and reciprocal-space sums)
- An iterative loop that guesses the appropriate charge center (so the user does not have to guess)
- Ewald parameter auto-optimization
- Various code optimizations


## Authors 

[Original implementation by  Christopher E. Wilmer, Randall Q. Snurr (advisor), Hansung Kim (car output), Patrick Fuller (streaming functionality), Louis Knapp (json output)](https://github.com/numat/EQeq). [Updated by Daniele Ongari](https://github.com/danieleongari/EQeq).