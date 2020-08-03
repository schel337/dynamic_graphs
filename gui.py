import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import random
from scipy.integrate import solve_ivp
from lin_sys import *
from utils import *

root = tk.Tk()
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=2)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)

display_frame = ttk.Frame(root)
display_frame.grid(column=0, row=0, sticky="nsew")

fig_2d = plt.Figure(figsize=(6, 4), dpi=100)
axs_2d = fig_2d.add_subplot(111)
graph_2d = GraphWrapper(display_frame, fig_2d, axs_2d)

fig_polar = plt.Figure(figsize=(6, 4), dpi=100)
axs_polar = fig_polar.add_subplot(111, projection='polar')
graph_polar = GraphWrapper(display_frame, fig_polar, axs_polar)

fig_3d = plt.Figure(figsize=(6, 4), dpi=100)
axs_3d = fig_3d.add_subplot(111, projection = '3d')
graph_3d = GraphWrapper(display_frame, fig_3d, axs_3d)

graphs = {"2d":graph_2d, "polar":graph_polar, "3d":graph_3d}
graph_master = GraphMaster(display_frame, graphs, "2d")

def calculate():
	"""
	Calculates new dynamics of the system
	"""
	T = int(time_var.get())
	A = A_var.get()
	B = B_var.get()
	x0 = x0_var.get()
	if contin_var.get():
		s = int(sampling_var.get())
		return np.linspace(0,T,num=s), matrix_exp_sys(A,B,x0,T,s)
	else:	
		return np.array((range(T+1))), disc_lin_sys(A,B,x0,T)

def plot_static():
	graph_master.display("2d")
	try:
		Ts, X = calculate()
		graph_2d.axs.clear()
		graph_2d.axs.set_xlim(auto=True)
		graph_2d.axs.set_ylim(auto=True)
		for Xi in X:
			graph_2d.axs.plot(Ts, Xi)
		graph_2d.canvas.draw()
	except ValueError:
		pass
	
def plot_animated():
	"""
	Line graph which is plotted over time
	"""
	graph_master.display("2d")
	try:
		Ts, X = calculate()
		Tf = int(time_var.get())
		delay = min(int(2000 / Ts.shape[0]),5)
		graph_2d.axs.clear()
		graph_2d.axs.set_xlim(left=0,right=Tf)
		graph_2d.axs.set_ylim(bottom=np.min(X)*1.25,top=np.max(X)*1.25)
		lines = [graph_2d.axs.plot(Ts[0:1], X[i,0:1])[0] for i in range(X.shape[0])]
		graph_2d.canvas.draw()
		def updater(t):
			for j in range(X.shape[0]):
				lines[j].set_data(Ts[0:t],X[j,0:t])
			graph_2d.canvas.draw()
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
	"""
	graph_master.display("2d")
	try:
		Ts, X = calculate()
		assert X.shape[0] >= 2, "plotting in the plane requires at least 2 dimensions"
		tail = 5
		delay = min(int(2000 / Ts.shape[0]),5)
		graph_2d.axs.clear()
		X1, X2 = X[0], X[1]
		graph_2d.axs.set_xlim(left=np.min(X1),right=np.max(X1))
		graph_2d.axs.set_ylim(bottom=np.min(X2),top=np.max(X2))
		line = graph_2d.axs.plot(X1[0:tail], X2[0:tail],marker='o',color=(0,0,0,1))[0]
		trail = graph_2d.axs.plot(X1[0:tail], X2[0:tail],color=(0,0,0,0.2))[0]
		graph_2d.canvas.draw()
		def updater(t):
			line.set_data(X1[t:t+tail],X2[t:t+tail])
			trail.set_data(X1[0:t+1],X2[0:t+1])
			graph_2d.canvas.draw()
			if t + tail < X1.shape[0]:
				root.after(delay, updater, t+1)
		updater(0)
	except ValueError:
		pass	

def plot_eigenvals():
	A = A_var.get()
	evals, evecs = np.linalg.eig(A)
	r, theta = np.sqrt(evals.real**2 + evals.imag**2), np.arctan2(evals.real, evals.imag)
	graph_polar.axs.clear()
	graph_polar.axs.fill_between(np.linspace(0,2*np.pi,100),0,1)
	graph_polar.axs.plot(theta, r, 'ro')
	graph_master.display("polar")
	

def animate_3D():
	graph_master.display("3d")
	try:
		Ts, X = calculate()
		assert X.shape[0] >= 3, "plotting in 3d requires at least 3 dimensions"
		tail = 5
		delay = min(int(2000 / Ts.shape[0]),5)
		graph_3d.axs.clear()
		X1, X2, X3 = X[0], X[1], X[2]
		graph_3d.axs.set_xlim(left=np.min(X1),right=np.max(X1))
		graph_3d.axs.set_ylim(bottom=np.min(X2),top=np.max(X2))
		graph_3d.axs.set_zlim(bottom=np.min(X3),top=np.max(X3))
		def updater(t):
			graph_3d.axs.clear()
			graph_3d.axs.plot3D(X1[t:t+tail], X2[t:t+tail], X3[t:t+tail], marker='o',color=(0,0,0,1))
			graph_3d.axs.plot3D(X1[0:t+1], X2[0:t+1], X3[0:t+1], color=(0,0,0,0.2))
			graph_3d.canvas.draw()
			if t + tail < X1.shape[0]:
				root.after(delay, updater, t+1)
		updater(0)
	except ValueError:
		pass	

def calculate_swarm(m):
	"""
	Calculates new dynamics of the system with m starting points
	"""
	T = int(time_var.get())
	A = A_var.get()
	B = B_var.get()
	x0 = x0_var.get()
	n = x0.shape[0]
	offsets = np.hstack((np.zeros((n,1)),2*np.random.random((n,m-1))))
	xs = offsets + (x0 - 1.0)[:,None]
	if contin_var.get():
		s = int(sampling_var.get())
		return np.linspace(0,T,num=s), matrix_exp_sys(A,B,xs,T,s)
	else:	
		return np.array((range(T+1))), disc_lin_sys(A,B,xs,T)

def plot_swarm(m):
	"""
	Plots m random starting points in hypercube around x0
	Uses heat map to respresent the portion of the point lying above the 2D plane
	Could improve memory usage by computing states one by one
	But this means the xy limits must change
	"""
	graph_master.display("2d")
	Ts, X = calculate_swarm(30)
	assert X.shape[0] >= 3, "plotting in the plane with a heat map requires at least 3 dimensions"
	tail = 5
	delay = 100
	X1, X2 = X[0], X[1]
	X3norms, Xnorms = np.linalg.norm(X[2:], axis=0), np.linalg.norm(X, axis=0)
	Xnorms[Xnorms==0] = 1
	Xratios = np.divide(X3norms, Xnorms)
	graph_2d.axs.clear()
	scatter = graph_2d.axs.scatter(X1[:,0],X2[:,0],c=Xratios[:,0],cmap="plasma")
	graph_2d.axs.set_xlim(left=np.min(X1),right=np.max(X1))
	graph_2d.axs.set_ylim(bottom=np.min(X2),top=np.max(X2))
	STEPS = 50
	def updater(t):
		X_delta = (1/STEPS)*np.dstack((X1[t]-X1[t-1],X2[t]-X2[t-1]))[0]
		Xr_delta = (1/STEPS)*(Xratios[t]-Xratios[t-1])
		def smooth_updater(s, Xs, Xrs):
			if s < STEPS:
				Xs, Xrs = Xs + X_delta, Xrs + Xr_delta
				scatter.set_array(Xrs)
				scatter.set_offsets(Xs)
				graph_2d.canvas.draw()
				root.after(delay//STEPS, lambda: smooth_updater(s+1, Xs, Xrs))
			else:
				scatter.set_array(Xratios[t])
				scatter.set_offsets(np.dstack((X1[t],X2[t]))[0])
				graph_2d.canvas.draw()
				if t + 1 < X1.shape[0]:
					root.after(delay//STEPS, updater, t+1)
		smooth_updater(0, np.dstack((X1[t-1],X2[t-1]))[0], Xratios[t-1])
	updater(1)
	
def plot_pendulum_hamiltonian(g=10,l=10):
	"""
	Plots a pendulum with gravity g and length l in phase space in angle and angular velocity
	Uses hamiltonian w^2/2 - g/l cos(theta) to provide 3d contour map of potential
	"""
	T = int(time_var.get())
	x0 = x0_var.get()
	E = lambda x,y : 0.5*x**2+ np.cos(y)
	X, Y  = np.meshgrid(np.linspace(-5,5,40),np.linspace(-5,5,40))
	Z = E(X,Y)
	graph_master.display("3d")
	graph_3d.axs.clear()
	graph_3d.axs.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='plasma')
	def fun(t,y):
		return np.array([y[1], -g*(1/l)*np.sin(y[0])])
	result = solve_ivp(fun, (0,T), x0, t_eval=np.linspace(0,T,100))
	Theta, Omega = result['y'][0], result['y'][1]
	Energy = E(Theta, Omega) + 0.01
	def update(t):
		graph_3d.axs.plot3D(Theta[t-1:t], Omega[t-1:t], Energy[t-1:t], marker='o',color=(0,0,0,1))
		graph_3d.canvas.draw()
		if t < Theta.shape[0]:
			root.after(20, update, t+1)
	update(1)
	

def randomize():
	x0 = x0_var.get()
	n = x0.shape[0]
	A_var.set(np.array([[round(random.uniform(-1,1),3) for _ in range(n)] for _ in range(n)]))
	B_var.set(np.array([[round(random.uniform(-1,1),3)] for _ in range(n)]))
		
	
input_frame = ttk.Frame(root, borderwidth=5, relief="sunken")
input_frame.grid(column=0, row=1, sticky="nsew")

plot_types = {
	'static': plot_static,
	'animate': plot_animated,
	'plane': plot_animated_plane,
	'eigenvalues': plot_eigenvals,
	'3D': animate_3D,
	'swarm': plot_swarm,
	'hamiltonian': plot_pendulum_hamiltonian
}
plot_type_var = ComboboxVar("Plot Type", tk.StringVar(), input_frame, opts=tuple(plot_types.keys()), val='static')
def plot():
	plot_types[plot_type_var.get()]()
ttk.Button(input_frame, text="Plot", command=plot).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Button(input_frame, text="Randomize", command=randomize).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

sys_frame = ttk.Frame(input_frame)
sys_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
dim_var = EntryVar("Dim", tk.StringVar(), sys_frame, val="2")
A_var  = MatrixEntryVar("A", (2,2), sys_frame, val=[[0.5,-0.5],[0.5,0.5]])
B_var = MatrixEntryVar("B", (2,1), sys_frame, val=[[1],[1]])
x0_var = MatrixEntryVar("x0", (2,1), sys_frame, val=[[1],[1]])
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
def toggle_contin():
	if contin_var.get():
		sampling_var.show()
	else:
		sampling_var.hide()
contin_var.bind_command(toggle_contin)

plot_static()
toolbar = NavigationToolbar2Tk(graph_2d.canvas, display_frame)
toolbar.update()

root.mainloop()