import numpy as np
import tkinter as tk
from tkinter import ttk
DEFAULT_WIDTH = 7

def parse_matrix(matrix_string):
	"""
	Given inputs of the form a, b, c, ... ; x, y, z, ... ; ...
	Return np array
	"""
	rows = matrix_string.split(';')
	if len(rows) == 1:
		return parse_vector(rows[0])
	return np.array([[float(x) for x in row.split(',')] for row in rows])
	
def parse_vector(vector_string):
	"""
	Given inputs of the form a, b, c, ...
	Return np array
	"""
	return np.array([float(x) for x in vector_string.split(',')])

class VarWrapper:
	def __init__(self, name,  var, parent, **kwargs):
		self.var = var
		self.name = name
		self.parent = parent
		self.label = ttk.Label(self.parent, text=self.name)
		if 'val' in kwargs:
			self.set(kwargs['val'])
		if 'show' not in kwargs or kwargs['show']:
			self.show()
		print("Initalized ", name, "with params ", kwargs)
		
	def trace(self, mode, callback):
		self.var.trace(mode, callback)
	
	def set(self, val):
		self.var.set(val)
		
	def get(self):
		try:
			return self.var.get()
		except ValueError:
			print("error fetching: "+self.name)		
			
	def show(self):
		self.label.pack(side=tk.LEFT)
		self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		
	def hide(self):
		self.label.pack_forget()
		self.input_widget.pack_forget()
	
	def bind_command(self, command):
		self.input_widget.configure(command=command)
		
class EntryVar(VarWrapper):
	def __init__(self, name, var, parent, **kwargs):
		self.input_widget = ttk.Entry(parent, width=DEFAULT_WIDTH, textvariable=var)
		super().__init__(name, var, parent, **kwargs)

class BoolVar(VarWrapper):
	def __init__(self, name, var, parent, **kwargs):
		self.input_widget = ttk.Checkbutton(parent, width=DEFAULT_WIDTH, variable=var)
		super().__init__(name, var, parent, **kwargs)
		
			
class ComboboxVar(VarWrapper):
	def __init__(self, name, var, parent, **kwargs):
		assert 'opts' in kwargs, "Comboboxes need options"
		self.input_widget = ttk.Combobox(parent, textvariable=var, values=kwargs.pop('opts'))
		super().__init__(name, var, parent, **kwargs)

#Not subclass of VarWrapper, this will manage 2d arrays of vars (or 1d as a special case)
class MatrixEntryVar():
	def __init__(self, name, shape, parent, **kwargs):
		self.name = name
		self.parent = parent
		self.label = ttk.Label(parent, text=self.name)
		self.frame = ttk.Frame(parent)
		self.m, self.n = shape[0], shape[1]
		self.vars = [[tk.StringVar() for _ in range(self.n)] for _ in range(self.m)]
		self.entries = [[ttk.Entry(self.frame, width=DEFAULT_WIDTH//2, textvariable=self.vars[i][j]) for j in range(self.n)] for i in range(self.m)]
		if 'val' in kwargs:
			#[[self.vars[i][j].set(kwargs['val'][i][j]) for j in range(self.m)] for i in range(self.n)]
			self.set(kwargs['val'])
		if 'show' not in kwargs or kwargs['show']:
			self.show()
	
	def reshape(self, shape):
		self.hide()
		for i in range(self.m):
			for j in range(self.n):
				if i >= shape[0] or j >= shape[1]:
					self.entries[i][j].destroy()
		temp_vars, temp_entries = np.empty(shape, dtype=object), np.empty(shape, dtype=object)
		for i in range(shape[0]):
			for j in range(shape[1]):
				if i < self.m and j < self.n:
					temp_vars[i][j] = self.vars[i][j]
					temp_entries[i][j] = self.entries[i][j]
				else:
					temp_vars[i][j] = tk.StringVar()
					temp_entries[i][j] = ttk.Entry(self.frame, width=DEFAULT_WIDTH//2, textvariable=temp_vars[i][j])
					temp_vars[i][j].set("0")
		self.vars = temp_vars #[[tk.StringVar() for _ in range(self.m)] for _ in range(self.n)]
		self.entries = temp_entries #[[ttk.Entry(self.frame, width=DEFAULT_WIDTH//2, textvariable=self.vars[i][j]) for j in range(self.n)] for i in range(self.m)]
		self.m, self.n = shape[0], shape[1]
		self.show()

	def set(self, val):
		val = np.array(val)
		if val.shape[0] != self.m or val.shape[1] != self.n:
			print(val.shape)
			print(self.m, self.n)
			self.resize(val.shape)
		[[self.vars[i][j].set(val[i][j]) for j in range(self.n)] for i in range(self.m)]
		
	def get(self):
		try:
			if self.n == 1:
				return np.array([float(self.vars[i][0].get()) for i in range(self.m)])
			elif self.m == 1:
				return np.array([float(self.vars[0][j].get()) for i in range(self.n)])
			else:
				return np.array([[float(self.vars[i][j].get()) for j in range(self.m)] for i in range(self.n)])
		except ValueError:
			print("error fetching: "+self.name)		
			
	def show(self):
		self.label.pack(side=tk.LEFT)
		self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		[[self.entries[i][j].grid(row=i,column=j) for j in range(self.n)] for i in range(self.m)]
		
	def hide(self):
		self.label.pack_forget()
		[[self.entries[i][j].grid_forget() for j in range(self.n)] for i in range(self.m)]
		self.frame.pack_forget()
		