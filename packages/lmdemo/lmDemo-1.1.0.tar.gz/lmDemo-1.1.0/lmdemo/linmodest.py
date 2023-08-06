import numpy as np
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

def linmodest(x:np.matrix, y:np.array) -> dict:
	"""Solve simple linear models

	Take a n by p matrix x and a p x 1 array and compute coefficients, vcov, 
	sigma squared and degrees of freedom for a standard linear model

	Args:
		x (np.matrix): an n x p matrix where n are the observations and p are the number of predictors
		y (np.array): an n x 1 response vector

	Raises:
		ValueError: raised when number of rows of x do not match number of rows of y

	Returns:
		dict: A dictionary with keys coef (coefficients), 
		vcov (variance covariance matrix), 
	"""


	# first, check that the dimensions are correct
	logging.debug("shape of x: %s; shape of y: %s" %(str(x.shape),str(y.shape))) #pylint: disable=C0209,W1201
	if not x.shape[0] == y.shape[0]:
		raise ValueError(f"Number of rows in x is {x.shape[1]}, "\
			f"number of rows in y is {y.shape[0]}. These are not equal. "
			f"They should be.")

	# compute the coefficients
	q,r = np.linalg.qr(x)
	coef = np.dot(np.linalg.inv(r),np.dot(q.T,y))

	# get degrees of freedom, rows-columns
	df = x.shape[0] - x.shape[1]

	# compute sigma squared
	sigma2 = np.sum((y-np.matmul(x,coef))**2) / df

	# compute variance covariance matrix
	vcov = sigma2 * np.linalg.inv(np.dot(r.T,r))

	# return a named dict
	return {k:v for k,v in zip(['coef','vcov','sigma','df'],
	                           [coef,vcov,np.sqrt(sigma2),df])}