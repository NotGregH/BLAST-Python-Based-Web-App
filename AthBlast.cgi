#!/usr/bin/python


### AthBlast.cgi ###

# Created By : Greg Hamilton 
# Current Version 0.0.1 

### All modules required for Script ###
import cgitb; cgitb.enable()
import os
import subprocess 
import cgi
from Bio.Blast import NCBIXML 
os.environ['MPLCONFIGDIR'] = '/tmp/gah324'
import matplotlib
matplotlib.use('Agg')
import pylab as plt
try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass

#########################


############## Start of Python Functions #############
### Functions for running the blast and parsing it for the table ###

###  Functions Tested Successfully :  YES - 12/11/14 
### Test Script - /home/gah324/Homework/Homework06/Test_pt_1_python.py



def run_blast(blast,input,db):
	'''
	This runs a BLAST using a FASTA file as the input.
	It returns the result in the form of a XML formatted file. 
	Options:
	The function assumes by default that input sequence is a protein sequence. 
	If entering nucleic acid sequence use option 'na' . 
	'''
	subprocess.call([blast,'-query',input,'-db',db,'-outfmt','5','-out','tmp.xml'])
	return

def read_xml(xml_file):
	'''
	This is intended for single query files!!!
	This opens a BLAST.xml data file and then parses the data
	into a columned pandas df. The columns will be 
	QueryName, SubjectName, PercentIdentity,E-value, QueryStart,
	QueryEnd, SubjectStart, and SubjectEnd. 
	'''
	QueryName = []
	SubjectName = []
	Percent_ID = []
	E_val = []
	QueryStart = []
	QueryEnd = []
	SubjectStart = []
	SubjectEnd = []
	BLAST = NCBIXML.parse(open(xml_file))
	all_records = []
	for i in BLAST:
		all_records.append(i)
	for record in all_records:
		for alignment in record.alignments:
			for hsp in alignment.hsps:
					SubjectName.append(str(alignment.hit_def))
					Percent_ID.append(hsp.identities)
					E_val.append(hsp.expect)
					QueryStart.append(hsp.query_start)
					QueryEnd.append(hsp.query_end)
					SubjectStart.append(hsp.sbjct_start)
					SubjectEnd.append(hsp.sbjct_end)
					QueryName.append((record.query))
	Data_list = zip(SubjectName,SubjectStart,SubjectEnd,QueryName,QueryStart,
		QueryEnd,E_val,Percent_ID)
	### Having issues turning dictionary into table ###
	#Data_dict = {'SubjectName':SubjectName,'QueryName':QueryName,'PercentIdentity':Percent_ID,
	#	'E-value':E_val,'QueryStart':QueryStart,'QueryEnd':QueryEnd,'SubjectStart':SubjectStart,
	#	'SubjectEnd':SubjectEnd}
	#return Data_dict
	return Data_list

def create_seq_file(seq):
	'''
	This function creates a temp text file for the fasta or seq 
	input variable.
	'''
	writer = open('tmp.txt','wb')
	writer.write(seq)
	writer.close()
	return 
	
def main(input,db,blast):
	'''
	This function combines the above functions to 
	run a create tmp sew file, run the blast and parse the 
	xml output
	'''
	create_seq_file(input)
	run_blast(blast,'tmp.txt',db)
	data_dict = read_xml('tmp.xml')
	return data_dict
######### End of Python Functions ############	


### I placed a lot of the heavier html into functions 
### this allowed for easier testing. 
######### Start of HTML Functions #############

def print_form():
	'''
	This function prints the form page which accepts 
	fasta and seq input and allows the user to select Blast type and 
	database type.
	'''
	print '''
	<body>
	<div align="center">	
	<h2>Welcome to the Hamilton BLAST Interface</h2>
	<p> Please fill in the information below to proceed </p>
	<form enctype="multipart/form-data" action="AthBlast.cgi" method="post">
	<br>
	<p> Paste Sequence here or upload a file below </p>
	<textarea name="sequence" rows='6' cols='60'></textarea>
	<br>
	<p>Fasta File: <input type="file" name="file"></p>
	<p> Select Database </p>
	<select name="database">
		<option value="Arabidopsis.nucl">Nucleic Acid</option>
		<option value="Arabidopsis.prot">Protein</option>
	</select>
	<p> Select BLAST Type </p>
		<select name="btype">
		<option value="blastn">BlastN</option>
		<option value="tblastn">TblastN</option>
		<option value="tblastx">TblastX</option>
		<option value="blastp">BlastP</option>
		<option value="blastx">BlastX</option>
	</select>
	<p><input type="submit" value="Submit"></p>
	</form>
	</div>
	</body>
	'''
	return

def error_page():
	'''
	This function prints the error page for improper Blast type
	and database combinations.
	'''
	print '''
	<div align="center">
	<body>
	<h3> ERROR </h3>
	<p> You have selected a blast type and database that are incompatible! </p>
	'''
	blast = None
	fasta = None
	seq = None
	db = None
	print '''
	<form action="AthBlast.cgi" method="post">
	<p> Press Continue to return to the form </p>
	<p><input type="submit" value="Continue"></p>
	</form>
	</div>
	</body>
	'''
	return
	
def error_page_2():
	'''
	This function prints the error page for when a user inserts both
	a seq and a fasta_file.
	'''
	print '''
	<div align="center">
	<body>
	<h3> ERROR </h3>
	<p> You have entered both a sequence and a fasta file. </p>
	'''
	blast = None
	fasta = None
	seq = None
	db = None
	print '''
	<form action="AthBlast.cgi" method="post">
	<p> Press Continue to return to the form </p>
	<p><input type="submit" value="Continue"></p>
	</form>
	</div>
	</body>
	'''
	return
	
def error_page_3():
	'''
	This function prints the error page for when a user has not
	provided a seq or a fasta file.
	'''
	print '''
	<div align="center">
	<body>
	<h3> ERROR </h3>
	<p>Please enter a fasta or sequence for analysis </p>
	'''
	blast = None
	fasta = None
	seq = None
	db = None
	print '''
	<form action="AthBlast.cgi" method="post">
	<p> Press Continue to return to the form </p>
	<p><input type="submit" value="Continue"></p>
	</form>
	</div>
	</body>
	'''
	return

def error_page_4():
	'''
	This function prints the error page for when a user has not
	picks an input seq that is not compatible with the BLAST they choose.
	'''
	print '''
	<div align="center">
	<body>
	<h3> ERROR </h3>
	<p>The Sequence you have enterred is not compatible with the BLAST Type</p>
	'''
	blast = None
	fasta = None
	seq = None
	db = None
	print '''
	<form action="AthBlast.cgi" method="post">
	<p> Press Continue to return to the form </p>
	<p><input type="submit" value="Continue"></p>
	</form>
	</div>
	</body>
	'''
	return

def no_hits():
	'''
	This function prints the page for when no hits
	are found by the BLAST.
	'''
	print '''
	<div align="center">
	<body>
	<h3>No Hits Found</h3>
	'''
	blast = None
	fasta = None
	seq = None
	db = None
	print '''
	<form action="AthBlast.cgi" method="post">
	<p> Press Continue to return to the form </p>
	<p><input type="submit" value="Continue"></p>
	</form>
	</div>
	</body>
	'''
	return

def create_table(data):
	'''
	This function creates an html function from 
	the dictionary created from parsing the BLAST 
	XML output. It accepts only the dictionary as 
	an argument. 
	'''
	Headers = ['SubjectName','SubjectStart','SubjectEnd','QueryName','QueryStart',
		'QueryEnd','E_val','Percent_ID']
	print '''
	<body>
	<style>
	thead {color:teal;}
	table, th, td {
		border: 1px solid black;
	}
	a:link    {color:#0000FF}
	a:visited {color:8A2BE2}
	</style>
	<table>
	'''
	print '<thead>'
	print '<tr>'
	for colnm in Headers:
		print '<th> %s </th>' %(colnm)
	print '</tr>'
	print '</thead>'
	print '<tbody>'
	for i in data:
		print '<tr>'
		print '<td><a href=getExpPlot.cgi?g=%s> %s </a></td>' %(i[0], i[0])
		for ind in range(1,len(i)):
			print '<td> %s </td>' %(i[ind])
		print '</tr>'
	print '</tbody>'
	print '''
	</table>
	</div>
	</body>
	'''
	return
	
	
######## End of HTML Functions ###############

######## Important Variables ##################

args = cgi.FieldStorage()
blast = args.getvalue('btype')
fasta = args.getvalue('file')
seq = args.getvalue('sequence')
db = args.getvalue('database')

######## Start of HTML ###################
#### NOTE: Error messages and the results pages are located above the form 
#### because cgi scripts are read from the top down by the processor so 
#### the form is only created while the input variables are None. 
#### I structure all my loops based on this as well. 

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Hamilton BLAST Interface</title>'
print '</head>'
if blast == 'blastn' and db == 'Arabidopsis.prot':
	error_page()
if blast == 'blastp' and db == 'Arabidopsis.nucl':
	error_page()
if blast == 'blastx' and db == 'Arabidopsis.nucl':
	error_page()
if blast == 'tblastn' and db == 'Arabidopsis.prot':
	error_page()
if blast == 'tblastx' and db == 'Arabidopsis.prot':
	error_page()
if fasta is not None and seq is not None:
	if seq is '' and fasta is '':
		error_page_3()
	if seq is not '' and fasta is not '':
		error_page_2()
	else:
		if seq is not '' :
			if 'M' in seq and blast == 'blastn': 
				error_page_4()
			if 'M' in seq and blast == 'blastx': 
				error_page_4()
			if 'M' in seq and blast == 'tblastx': 
				error_page_4()
			if 'M' not in seq and blast == 'blastp': 
				error_page_4()
			if 'M' not in seq and blast == 'tblastn': 
				error_page_4()
			else:
				data = main(seq,db,blast)
				if len(data) < 1:    
					no_hits()
				else:
					create_table(data)
		if fasta is not '':
			if 'M' in fasta.split('\n')[1] and blast == 'blastn': 
				error_page_4()
			if 'M' in fasta.split('\n')[1] and blast == 'blastx': 
				error_page_4()
			if 'M' in fasta.split('\n')[1] and blast == 'tblastx': 
				error_page_4()
			if 'M' not in fasta.split('\n')[1] and blast == 'blastp': 
				error_page_4()
			if 'M' not in fasta.split('\n')[1] and blast == 'tblastn': 
				error_page_4()
			else:
				data = main(fasta,db,blast)
				if len(data) < 1:
					no_hits()
				else:
					create_table(data)
if fasta is None and seq is None: 
	print_form()
print '</html>'
