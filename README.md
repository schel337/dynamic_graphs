## Summary
Personal project for visualing discrete or continuous linear time invariant systems with tkinter and matplotlib. I find that the systems which are close to stable have interesting orbits, especially when plotted as a swarm with a heatmap to display the "compactified" dimensions outside of the 2d plane. I would add more controls things like LQR but the tkinter interface would make manual tweaking of controls very difficult. 
## Files
- gui.py: Runs tkinter gui and plots data
- lin_sys.py: Code for modeling linear time invariant systems.
- utils.py: Parsing tkinter string input into arrays.
## Examples
- Standard example of a 3D system which is very close to stable, giving a spiral shape: ![Ex1](examples/ex1.png)
- This is an example of the heatmap style I tried to use to "compactify" extra dimensions, albeit this shows the trajectory of one starting point: ![Ex2](examples/ex2.png)