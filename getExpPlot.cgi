#!/usr/bin/python

###### getExpPlot.py #######

# Created By : Greg Hamilton 

###### Modules Required for the Scrip #######
import cgitb; cgitb.enable()
import os
import subprocess 
import cgi
import sqlite3
os.environ['MPLCONFIGDIR'] = '/tmp/gah324'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass
	
	
############## End of Modules ###################

############# Python Functions ##################

def Experesion_query(gene):
	'''
	This function accepts a gene name and searches
	the database for it in a MySql database and if 
	found it returns the expression values in a dictionary 
	by category
	'''
	connection = sqlite3.connect('ArabidopsisExpValues.db')
	cursor = connection.cursor()
	if 'T' in gene:
		gene = gene.replace('T','t')
	if 'G' in gene:
		gene = gene.replace('G','g')
	#print gene
	gene_db = (gene,)
	#print gene_db
	cursor.execute('SELECT * from geneexp WHERE gene=?',(gene_db))
	exp_values_vec = cursor.fetchall()
	connection.close()
	#print exp_values_
	return exp_values_vec[0]
	
def plot_exp_values(exp_values_vec):
	'''
	This function accepts an expression value dictionary
	and plots the values as a bar plot_exp_values
	'''
	exp_names = ('Control_1', 'Control_2', 'Nitrate_1', 'Nitrate_2', 'msx_1','msx_2','msxglu_1','msxglu_2')
	#print exp_names
	y_pos = np.arange(len(exp_values_vec[1:]))
	#print y_pos
	plt.barh(y_pos, np.array(exp_values_vec[1:]), align='center')
	plt.yticks(y_pos, exp_names)
	plt.xlabel('Expression Level')
	plt.title(exp_values_vec[0])
	plt.savefig('tmp.png')
	return
	
################## End of Python Functions ##########################

################# HTML Functions ##########################

def error():
	'''
	This function prints the page for when the gene
	is not found in the database.
	'''
	print '''
	<div align="center">
	<body>
	<h3>Gene Not Found</h3>
	'''
	print '''
	</div>
	</body>
	'''
	return
	
def print_plot():
	''' 
	This function prints the plot.
	'''
	print '<body>'
	print "<img src='tmp.png'>"
	print '</body>'
	return 
################ important Variables ##############
args = cgi.FieldStorage()
gene = args.getvalue('g')
exp_value_vec = Experesion_query(gene)
###########################################

print "Content-type:text/html\r\n\r\n"
 
print '<html>'
print '<head>'
print '<title> %s </title>' %(gene)
print '</head>'

if len(exp_value_vec) < 1:
	error_page()

if len(exp_value_vec) >= 1:
	plot_exp_values(exp_value_vec)
	print_plot()


print '</html>'
