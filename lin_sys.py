import numpy as np
from scipy.linalg import expm
from scipy import integrate

def disc_lin_sys(A,B,x0,T):
	"""
	Models x(t+l) = Ax(t) + B upto time step T
	"""
	n = x0.shape[0]
	assert A.shape[0] == n and A.shape[1] == n and B.shape[0] == n, "System dimensions incompatible"
	X, xt = [x0], x0
	for t in range(T):
		xt = A @ xt + B
		X.append(xt)
	X = np.stack(X,axis=1)
	return X
	
def contin_lin_sys(A,B,x0,T,s):
	"""
	Models x' = Ax(t) + B upto time step T, samples uniformly s times
	Solves by diagonalizing the system in new coordinates
	"""
	n = x0.shape[0]
	assert A.shape[0] == n and A.shape[1] == n and B.shape[0] == n, "System dimensions incompatible"
	L, V = np.linalg.eig(A)
	Vinv = np.linalg.inv(V)
	B, x0 = Vinv @ B, Vinv @ x0
	S = np.linspace(0,T,num=s)
	X = [[] for _ in range(len(S))]
	for t in range(len(S)):
		for i in range(n):
			if B[i] == 0:
				X[t].append(x0[i]*np.exp(L[i]*S[t]))
			else:
				X[t].append(-L[i] / B[i] + (L[i] / B[i] + x0[i])*np.exp(L[i]*S[t]))
		X[t] = V @ np.array(X[t])
	X = np.stack(np.array(X),axis=1)
	return X
	
def matrix_exp_sys(A,B,x0,T,s):
	"""
	Models x' = Ax(t) + B upto time step T, samples uniformly s times
	Solves by matrix exponential
	"""
	n = x0.shape[0]
	assert A.shape[0] == n and A.shape[1] == n and B.shape[0] == n, "System dimensions incompatible"
	step = T / s
	e_sA = expm(step*A)
	pts = np.linspace(0,step,20)
	vals = np.array([expm(-x*A) @ B for x in pts])
	W = np.array([integrate.simps(vals[0:20,i],pts) for i in range(n)])
	xt = x0
	X = [x0]
	for t in range(s-1):
		xt1 = np.array(e_sA @ (xt + W))
		X.append(xt1)
		xt = xt1
	X = np.stack(np.array(X),axis=1)
	return X
	
	
	
def pseudoinv_control(A,B,x0,xT,T):
	"""
	Finds the minimum norm or least squares solution to x(T) = xT for the system x(t+1) = Ax(t) + B u(t)
	"""
	C = np.concatenate([np.linalg.matrix_power(A,t) for t in range(T)], axis=1)
	return np.linalg.pinv(C) @ xT