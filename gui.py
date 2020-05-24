import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import random
from lin_sys import *
from utils import *

root = tk.Tk()
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=2)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)

display_frame = ttk.Frame(root)
display_frame.grid(column=0, row=0, sticky="nsew")
fig = plt.Figure(figsize=(6, 4), dpi=100)
axs = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=display_frame)

def calculate():
	"""
	Calculates new dynamics of the system
	"""
	T = int(time_var.get())
	A = A_var.get()#parse_matrix(A_var.get())
	print(A)
	B = B_var.get()#parse_vector(B_var.get())
	print(B)
	x0 = x0_var.get()#parse_vector(x0_var.get())
	print(x0)
	if contin_var.get():
		s = int(sampling_var.get())
		return np.linspace(0,T,num=s), matrix_exp_sys(A,B,x0,T,s)#contin_lin_sys(A,B,x0,T,s)
	else:	
		return np.array((range(T+1))), disc_lin_sys(A,B,x0,T)

def plot_static():
	try:
		Ts, X = calculate()
		axs.clear()
		axs.set_xlim(auto=True)
		axs.set_ylim(auto=True)
		for Xi in X:
			axs.plot(Ts, Xi)
		canvas.draw()
	except ValueError:
		pass
	
def plot_animated():
	try:
		Ts, X = calculate()
		Tf = int(time_var.get())
		delay = min(int(2000 / Ts.shape[0]),5)
		axs.clear()
		axs.set_xlim(left=0,right=Tf)
		axs.set_ylim(bottom=np.min(X)*1.25,top=np.max(X)*1.25)
		lines = [axs.plot(Ts[0:1], X[i,0:1])[0] for i in range(X.shape[0])]
		canvas.draw()
		def updater(t):
			for j in range(X.shape[0]):
				lines[j].set_data(Ts[0:t],X[j,0:t])
			canvas.draw()
			if t < Ts.shape[0]:
				root.after(delay, updater, t+1)
		updater(0)
		#Unfortunately it looks like the matplotlib animation timer has problems while embedded in tkinter
		#animation.FuncAnimation(fig, updater,frames=Tf,interval=1000, blit=False)
	except ValueError:
		pass
		
def plot_animated_plane():
	"""
	Plots the graph in the 2d plane, by default selecting first two variables
	Probably need to have a faint, longer trail or something
	"""
	try:
		Ts, X = calculate()
		assert X.shape[0] >= 2, "plotting in the plane requires at least 2 dimensions"
		tail = 5
		delay = min(int(2000 / Ts.shape[0]),5)
		axs.clear()
		X1, X2 = X[0], X[1]
		axs.set_xlim(left=np.min(X1),right=np.max(X1))
		axs.set_ylim(bottom=np.min(X2),top=np.max(X2))
		line = axs.plot(X1[0:tail], X2[0:tail],marker='o',color=(0,0,0,1))[0]
		trail = axs.plot(X1[0:tail], X2[0:tail],color=(0,0,0,0.2))[0]
		canvas.draw()
		def updater(t):
			line.set_data(X1[t:t+tail],X2[t:t+tail])
			trail.set_data(X1[0:t+1],X2[0:t+1])
			canvas.draw()
			if t + tail < X1.shape[0]:
				root.after(delay, updater, t+1)
		updater(0)
	except ValueError:
		pass	

def plot_eigenvals():
	#TODO: changing projection for polar
	A = A_var.get()
	evals, evecs = np.linalg.eig(A)
	axs.clear()
	r = 1.414 * np.max(np.sqrt(evals.real**2 + evals.imag**2))
	axs.set_xlim(left=-r,right=r)
	axs.set_ylim(bottom=-r,top=r)
	axs.plot(evals.real, evals.imag, 'bo')
	canvas.draw()
	

def randomize():
	x0 = x0_var.get()
	n = x0.shape[0]
	A_var.set(np.array([[round(random.uniform(-1,1),3) for _ in range(n)] for _ in range(n)]))
	B_var.set(np.array([[round(random.uniform(-1,1),3)] for _ in range(n)]))
		
	
		
input_frame = ttk.Frame(root, borderwidth=5, relief="sunken")
input_frame.grid(column=0, row=1, sticky="nsew")

#TODO: add var for plot type and have that one handle plotting things
plot_type_var = ComboboxVar("Plot Type", tk.StringVar(), input_frame, opts=('static','animate','plane','eigenvalues'), val='static')
def plot():
	plotter = plot_type_var.get()
	if plotter == 'static':
		plot_static()
	elif plotter == 'animate':
		plot_animated()
	elif plotter == 'plane':
		plot_animated_plane()
	elif plotter == 'eigenvalues':
		plot_eigenvals()
ttk.Button(input_frame, text="Plot", command=plot).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
#ttk.Button(input_frame, text="Animate", command=plot_animated).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Button(input_frame, text="Randomize", command=randomize).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

sys_frame = ttk.Frame(input_frame)
sys_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
dim_var = EntryVar("Dim", tk.StringVar(), sys_frame, val="2")
A_var  = MatrixEntryVar("A", (2,2), sys_frame, val=[[0.5,-0.5],[0.5,0.5]]) #EntryVar("A",tk.StringVar(), input_frame, val="0.5,-0.5;\r 0.5,0.5")
B_var = MatrixEntryVar("B", (2,1), sys_frame, val=[[1],[1]]) #EntryVar("B",tk.StringVar(), input_frame, val = "1,1")
x0_var = MatrixEntryVar("x0", (2,1), sys_frame, val=[[1],[1]]) #EntryVar("x0",tk.StringVar(), input_frame, val = "1,1")
time_var = EntryVar("T",tk.StringVar(), input_frame, val = "20")
def dim_change(*args):
	n = dim_var.get()
	if n:
		n = int(n)
		A_var.reshape((n,n))
		B_var.reshape((n,1))
		x0_var.reshape((n,1))
dim_var.trace("w", dim_change)

contin_var = BoolVar("Continuous", tk.BooleanVar(), input_frame, val=False)
sampling_var = EntryVar("Samples", tk.StringVar(), input_frame, show=False, val="100")
#Possibly remove, use plot button as main method
def toggle_contin():
	if contin_var.get():
		sampling_var.show()
	else:
		sampling_var.hide()
contin_var.bind_command(toggle_contin)

plot_static()
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, display_frame)
toolbar.update()

root.mainloop()