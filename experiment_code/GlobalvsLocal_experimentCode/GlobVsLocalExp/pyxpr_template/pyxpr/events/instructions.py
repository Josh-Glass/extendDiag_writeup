## Python Standard Library
import sys
import os

## External Dependencies
from psychopy import core, gui, visual, event


'''
- - - instructions - - -
~ shows instructions on the screen; awaits response
-> parameters:
	*
	**
'''
def run(
		window = None,
		window_size = 'full', 
		window_color = [1,1,1], 
		text_file = None, 
		text_color = [-1,-1,-1], 
		continue_option = 'button', # options: [button, any, space, click]
		continue_txt = 'Click to continue...', 
		continue_txt_size = 22,
		continue_txt_font = 'Consolas',
		continue_txt_color = [-1,-1,-1],
		continue_button_color = [.7, 0, 0], 
		continue_obj_pos = [0, -300],
		wait_time = 3,
		quit_keys = ['escape'],
		debug_mode = False,
		text_align = 'left',
		wrap_width = 1000
	):

	## Setup
	if window == None:
		if window_size == 'full':
			window = visual.Window(fullscr=True, units='pix', color=window_color)
		else:
			window = visual.Window(window_size, units='pix', color=window_color)

	if debug_mode == True:
		wait_time = 0

	cursor = event.Mouse() # set initial cursor

	# Setup Instructions Text Object
	instructions = visual.TextStim(window, pos=[0,30], color=text_color, alignText = text_align, wrapWidth = wrap_width) # create Text Stim Object
	
	if text_file == None:
		instructions.setText('Ready?')
	else:
		with open(text_file, 'r') as text_file_object:
			instructions.setText(text_file_object.read())


	# Setup Continue Option
	if continue_option == 'button':
		continue_obj = {}
		continue_obj['box'] = visual.Rect(
				window,
				width = 200,
				height = 75,
				fillColor = continue_button_color,
				lineColor = [-1,-1,-1],
				pos = continue_obj_pos,
			)
		continue_obj['txt'] = visual.TextStim(
				window,
				text = continue_txt,
				height = continue_txt_size,
				font = continue_txt_font,
				color = continue_txt_color,
				pos = continue_obj['box'].pos
			)
	
	elif continue_option == 'any':
		continue_obj = {'txt': visual.TextStim(
				window,
				text = 'Press any key to continue...',
				height = continue_txt_size,
				font = continue_txt_font,
				color = continue_txt_color,
				pos = continue_obj_pos,
			)
		}
	
	elif continue_option == 'space':
		continue_obj = {'txt': visual.TextStim(
				window,
				text = 'Press the spacebar to continue...',
				height = continue_txt_size,
				font = continue_txt_font,
				color = continue_txt_color,
				pos = continue_obj_pos,
			)
		}

	elif continue_option == 'click':
		continue_obj = {'txt': visual.TextStim(
				window,
				text = 'Click anywhere to continue...',
				height = continue_txt_size,
				font = continue_txt_font,
				color = continue_txt_color,
				pos = continue_obj_pos,
			)
		}


	## Run Phase

	instructions.draw()
	window.flip()
	core.wait(wait_time)
	instructions.draw()
	for key, val in continue_obj.items():
		val.draw()
	window.flip()



	# Wait for user response
	cursor.clickReset()
	event.clearEvents()
	
	if continue_option == 'button':
		# Wait for first click
		while cursor.getPressed() == [False, False, False]:
			if event.getKeys(keyList = quit_keys): # quit check
				print('user terminated'); core.quit()

		# Now that user has made a response, check to see where they clicked
		while True:
			if event.getKeys(keyList = quit_keys):
				print('user terminated'); core.quit()

			# Return to main script once user clicks continue
			if cursor.isPressedIn(continue_obj['box']):
				return

	if continue_option == 'any':
		# wait for spacebar keypress
		event.waitKeys()
		if event.getKeys(keyList = quit_keys):
			print('user terminated'); core.quit()
		return


	if continue_option == 'space':
		# wait for spacebar keypress
		event.waitKeys(keyList = ['space'] + quit_keys)
		if event.getKeys(keyList = quit_keys):
			print('user terminated'); core.quit()
		return


	if continue_option == 'click':
		# wait for first click
		while cursor.getPressed() == [False, False, False]:
			# quit check
			if event.getKeys(keyList = quit_keys) == True:
				print('user terminated'); core.quit()
		return









