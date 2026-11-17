## Python Standard Library
import sys
import os

## External Dependencies
from psychopy import gui

'''
- - - initializer - - -
~ runs an initial dialogue window to collect participant data
-> parameters:
	** conditions: list of condition labels/numbers
	** queries: dictionary of labels & lists of options (for making queries besides condition number)
		^ you don't really have to worry about this one
'''
def run(conditions=[0], queries={}):
	dlg = gui.Dlg(title='Experiment Initializer') # initialize dialogue box

	dlg.addField('ID:', tip='#') # add subject_id textbox
	dlg.addField('Condition', choices=conditions) # add 'condition' dropdown menu (which is why the 'conditions' argument needs to be a list)

	for query in queries.keys():
		if type(queries[query]==list):
			dlg.addField(str(query), choices=queries[query])

	dlg.show() # show window (will return a list with all the information when done)


	if dlg.OK == False:
		print('User Terminated')
		sys.exit()

	return(dlg.data)

## Example
if __name__ == '__main__':
	info = run(conditions=[0])
	print(info)

