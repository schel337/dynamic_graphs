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
	
class var_wrapper:
	def __init__(self, name, var, frame, default=None):
		self.var = var
		self.name = name
		self.frame = frame
		self.label = ttk.Label(self.frame, text=self.name)
		if default != None:
			self.set(default)
		print("Initalized ", name, " with val ", default)
		
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
		
class entry_var(var_wrapper):
	def __init__(self, name, var, frame, show=True, default=None):
		super().__init__(name, var, frame, default=default)
		self.input_widget = ttk.Entry(self.frame, width=DEFAULT_WIDTH, textvariable=var)
		if show:
			self.show()
	

class bool_var(var_wrapper):
	def __init__(self, name, var, frame, show=True, default=None):
		super().__init__(name, var, frame, default=default)
		self.input_widget = ttk.Checkbutton(self.frame, width=DEFAULT_WIDTH, variable=self.var)
		if show:
			self.show()