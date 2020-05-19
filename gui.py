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
	try:
		T = int(time_var.get())
		A = parse_matrix(A_var.get())
		B = parse_vector(B_var.get())
		x0 = parse_vector(x0_var.get())
		if contin_var.get():
			s = int(sampling_var.get())
			return np.linspace(0,T,num=s), matrix_exp_sys(A,B,x0,T,s)#contin_lin_sys(A,B,x0,T,s)
		else:	
			return np.array((range(T+1))), disc_lin_sys(A,B,x0,T)
	except ValueError:
		pass

def plot_static(*args):
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
		
def plot_animated(*args):
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
	
def randomize(*args):
	try:
		x0 = parse_vector(x0_var.get())
		n = x0.shape[0]
		A = ""
		for i in range(n):
			for j in range(n):
				A += str(round(random.uniform(-1,1),3))
				if j + 1 < n:
					A += ','
			if i + 1 < n:
				A += ';'
		A_var.set(A)
		B = ""
		for i in range(n):
			B += str(round(random.uniform(-1,1),3))
			if i + 1 < n:
				B += ','
		B_var.set(B)
	except ValueError:
		pass
		
	
	

def toggle_contin(*args):
	if contin_var.get():
		n = parse_vector(x0_var.get()).shape[0]
		sampling_label.pack(side=tk.LEFT)
		sampling_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
	else:
		sampling_label.pack_forget()
		sampling_entry.pack_forget()
		
	

input_frame = ttk.Frame(root, borderwidth=5, relief="sunken")
input_frame.grid(column=0, row=1, sticky="nsew")
ttk.Button(input_frame, text="Plot", command=plot_static).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Button(input_frame, text="Animate", command=plot_animated).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Button(input_frame, text="Randomize", command=randomize).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
A_var, B_var, time_var, x0_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
A_var.set("0.5,-0.5;\r 0.5,0.5")
B_var.set("1,1")
time_var.set('20')
x0_var.set('1,1')
ttk.Label(input_frame, text="A").pack(side=tk.LEFT)
ttk.Entry(input_frame, width=7, textvariable=A_var).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Label(input_frame, text="B").pack(side=tk.LEFT)
ttk.Entry(input_frame, width=7, textvariable=B_var).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Label(input_frame, text="x0").pack(side=tk.LEFT)
ttk.Entry(input_frame, width=7, textvariable=x0_var).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
ttk.Label(input_frame, text="T").pack(side=tk.LEFT)
ttk.Entry(input_frame, width=7, textvariable=time_var).pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

contin_var, sampling_var = tk.BooleanVar(), tk.StringVar()
contin_var.set(False)
sampling_var.set("100")
ttk.Label(input_frame, text="Continous Time").pack(side=tk.LEFT)
ttk.Checkbutton(input_frame, width=7, variable=contin_var, command=toggle_contin).pack(side=tk.LEFT)
sampling_label = ttk.Label(input_frame, text="samples")
sampling_entry = ttk.Entry(input_frame, width=7, textvariable=sampling_var)


plot_static()
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, display_frame)
toolbar.update()

root.mainloop()