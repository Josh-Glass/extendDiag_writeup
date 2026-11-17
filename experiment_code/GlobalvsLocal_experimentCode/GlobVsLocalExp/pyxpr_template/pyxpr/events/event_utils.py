## Python Standard Library
import sys
import os

## External Dependencies
from psychopy import core, gui, visual, event

def build_window(
	window_size = 'full',
	window_color = [1,1,1],
):

	if window_size == 'full':
		return visual.Window(fullscr=True, units='pix', color=window_color)
	else:
		return visual.Window(window_size, units='pix', color=window_color)



##__Wait for user response
def wait_for_btn_response(cursor, timer, buttons, quit_keys=['escape']):
	cursor.clickReset()
	event.clearEvents()
	timer.reset()

	while cursor.getPressed() == [False, False, False]:
		if event.getKeys(keyList=quit_keys):
			print('user terminated')
			core.quit()

	while True:
		if event.getKeys(keyList=quit_keys):
			print('user terminated')
			core.quit()
		for btn in buttons:
			if cursor.isPressedIn(buttons[btn]['box']) and buttons[btn]['box'].enabled == True:
				buttons[btn]['box'].setImage('./materials/btns/blank_btn_clicked.png')
				return([btn, timer.getTime()])

def reset_btn_response(buttons):
	for btn in buttons:
		if buttons[btn]['box'].enabled == True:
			buttons[btn]['box'].setImage('./materials/btns/blank_btn.png')

##__Wait for user response
def wait_for_click_response(cursor, timer, quit_keys=['escape']):
	cursor.clickReset()
	event.clearEvents()
	timer.reset()

	while cursor.getPressed() == [False, False, False]:
		if event.getKeys(keyList=quit_keys):
			print('user terminated')
			core.quit()
	return(timer.getTime())


##__Wait for user response



## this recursively draws everything in a dictionary of items/dictionaries
def draw_objects_in_bin(
		window,
		object_bin,
		object_list = None,
		flip = True,
	):

	if object_list == None:
		for obj in object_bin:
			if type(object_bin[obj]) == dict:
				draw_objects_in_bin(window, object_bin[obj], flip=False)
			else:
				object_bin[obj].draw()

	else:
		for obj in object_list:
			if type(object_bin[obj]) == dict:
				draw_objects_in_bin(window, object_bin[obj], flip=False)
			else:
				object_bin[obj].draw()

	if flip == True:
		window.flip()



## this makes a row of n numer of buttons that are evenly spaced
def make_button_row(
		window, 	# psychopy window object (required argument)
		labels = ['A', 'B'],
		btn_states = None,
		btn_disabled_color = [0.4,0.4,0.4],
		ypos = -100,
		padding = 0,	# this determines how far apart butons will be evenly placed
		btn_box_size = [200,75],
		btn_box_color = [0,0,0],
		btn_txt_size = 22,
		btn_txt_color = [-1,-1,-1],
		btn_txt_font = 'Arial',
	):

	btn_set = {}

	num_categories = len(labels)
	btn_row_len = btn_box_size[0] * num_categories + padding * 2 * num_categories
	btn_row_start = -btn_row_len / 2

	for index, item in enumerate(labels):
		btn_set[item] = {}
		btn_set[item]['box'] = visual.ImageStim(
				window,
				'./materials/btns/blank_btn.png',
				size = [btn_box_size[0], btn_box_size[1]],
				
				#fillColor = btn_box_color,
				#lineColor = [-1,-1,-1],
				pos = [btn_row_start + (btn_box_size[0] + padding * 2)/2 + (btn_box_size[0] + padding * 2) * index, ypos]
				# ^ that is just annoying trial+error math to get the buttons evenly spaced
			)
		btn_set[item]['txt'] = visual.TextStim(
				window,
				text = item,
				height = btn_txt_size,
				color = btn_txt_color,
				font = btn_txt_font,
				pos = btn_set[item]['box'].pos
			)

		# set if button is disabled or enabled
		if btn_states != None and len(btn_states) > index:
			btn_set[item]['box'].enabled = btn_states[index]
			if btn_states[index] == False:
				btn_set[item]['box'].setImage('./materials/btns/blank_btn_nonfunct.png')
				btn_set[item]['txt'].color = [1,1,1]
		else:
			btn_set[item]['box'].enabled = True

	# print('----\n' + str(type(btn_set)), btn_set, '\n----')
	return btn_set






## this makes a row of n numer of stims that are evenly spaced
def make_stim_row(
		window, 	# psychopy window object (required argument)
		num_stim,
		ypos = -100,
	): # returns a list of psychopy visual stimuli objects
	stim_set = {}

	for i in range(num_stim):
		stim_set[i] = visual.ImageStim(
			window,
			pos = [
				(i * window.size[0] / num_stim) + (window.size[0] / num_stim / 2) - (window.size[0] / 2),
				ypos,
			],
				# ^ that is just annoying trial+error math to get the buttons evenly spaced
			interpolate = True,
		)

	return stim_set
