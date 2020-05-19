## Summary
Personal project for visualing discrete or continuous linear time invariant systems with tkinter and matplotlib. 
## Files
- gui.py: Runs tkinter gui.
- lin_sys.py: Code for modeling linear time invariant systems.
- utils.py: Parsing tkinter string input into arrays.
## Todo
- Plotting 2d and 3d systems as animations on plane
- Finish implementation of basic controls module
- For diagonalizing systems, need to group complex eigenvals to take real part
- Make input of matrices easier
- Planning on messing with Jordan Canonical form, even though every matrix is diagonalizable within floating point precision (for instance numpy claims to find 2 eigenvectors for [[2,1][0,2]]).
- Other extensions: LQR controls, plotting hamiltonians or lyaponuv functions.

