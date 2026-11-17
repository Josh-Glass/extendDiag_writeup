## Python Standard Library
import sys
import os
import random
import csv

## External Dependencies
from psychopy import core, gui, visual, event

## Internal Dependencies
sys.path.append(os.path.abspath(os.path.join(__file__, '..')))
import event_utils



##__Forced Choice Phase
def run(
	stimuli,
	labels = None,
	randomize_presentation = True,

	supervised = True, # this determines whether participants recieve feedback
	criterian = 11,
	max_attempts = 1,
	num_stim = 12,

	experiment_id = 'experiment',
	phase_id = 'forced_choice',
	subject_info = None,
	save_data = False,

	window = None,

	stim_position = [0,0],

	fixation_symbol = '',

	click_instructions_txt = 'Click a button to select the correct category.',
	click_instructions_txt_color = [-1,-1,-1], 
	click_instructions_position = [0, -120],

	feedback_txt_position = [0, -90],
	feedback_txt_color = [-1,-1,-1],
	
	continue_txt_position = [0, -145],
	continue_txt_color = [-1,-1,-1],

	response_btn_labels = None,
	response_btn_states = None,
	response_btn_disabled_color = [0.4, 0.4, 0.4],
	response_btn_ypos = -310,
	response_btn_padding = 150,
	response_btn_box_size = [290, 130],
	response_btn_box_color = [.5, .8, .5],
	response_btn_txt_size = 22,
	response_btn_txt_font = 'Consolas',
	response_btn_txt_color = [-1,-1,-1],
    
    
	

	quit_keys = ['escape'],
	debug_mode = False,
):

	# Initialize Main Psychopy win if one isn't included
	if window == None:
		window = event_utils.build_window()

	cursor = event.Mouse() # set initial cursor
	timer = core.Clock()

	if subject_info == None:
		subject_info = {
			'id': '0000',
			'condition': 0,
			'datafile_path': './subject_data.csv'
		}

	headerList = [
				    'pnum', 
				    'phase_id',
				    'condition',
				    'block_data',
				    'trial_num',
				    'stim',
				    'correct_category',
				    'response',
				    'hit',
				    'rt',
				    'criterian',
				    'met_criterian',
				    'num_correct_in_block',]
				    	
	with open(subject_info['datafile_path'], 'a') as file:
		dw = csv.DictWriter(file, delimiter=',', fieldnames=headerList)
		dw.writeheader()	

	if (labels == None) & (supervised == True):
		print(phase_id + ' is set to "supeprvised", but no labels were provided. quitting experiment.')
		sys.exit()

	if response_btn_labels == None:
		if labels != None:
			response_btn_labels = list(set(labels))
		else:
			response_btn_labels = ['no', 'labels', 'provided']


	## Prepare Stimuli and Text Objects
	object_bin = {} 
	
	object_bin['stim'] = visual.ImageStim(
		window,
		pos = stim_position,
		name = 'image_stim',
		interpolate = True,
	)

	
	
	object_bin['response_btns'] = event_utils.make_button_row(
		window,    # psychopy win object (required argument)
		labels = response_btn_labels,
		btn_states = response_btn_states,
		btn_disabled_color = response_btn_disabled_color,
		ypos = response_btn_ypos, 
		padding = 20,  # this determines how far apart butons will be evenly placed
		btn_box_size = response_btn_box_size, 
		btn_box_color = response_btn_box_color, 
		btn_txt_size = response_btn_txt_size,
		btn_txt_color = response_btn_txt_color,
		btn_txt_font = response_btn_txt_font,
	)


	
	object_bin['click_msg'] = visual.TextStim(
		window,
		text = click_instructions_txt,
		pos = click_instructions_position,
		color = click_instructions_txt_color
	)

	object_bin['feedback_msg'] = visual.TextStim(
		window,
		pos = feedback_txt_position,
		color = feedback_txt_color,
	)

	object_bin['click_anywhere_msg'] = visual.TextStim(
		window,
		text = 'Click anywhere to continue...',
		pos = continue_txt_position, 
		color = continue_txt_color,
	)

	object_bin['color_response'] = visual.Rect(
		window,
		width = window.size[0],
		height = window.size[1],
		lineWidth = 30
	)


	##__ Start Phase
	trial_num = 1
	accuracy = []
	presentation_order = list(range(len(stimuli)))

	attempts = 0
	block_data = 0 
	num_correct_in_block = 0
	num_incorrect_in_block = 0
	while num_correct_in_block < criterian:
		print( 'current_num_correct = ' + str(num_correct_in_block))
		print('attempts = ' + str(attempts))
		print('max_attempts ' + str(max_attempts))
		print('criterian ' + str(criterian))
		print('num_incorrect_in_block ' + str(num_incorrect_in_block))
		if randomize_presentation == True:
			random.shuffle(presentation_order)

		if attempts == max_attempts:
			print('break')
			break

		attempts += 1
		#track the which block we are in
		block_data += 1
		if (num_incorrect_in_block + num_correct_in_block) >= num_stim:
				num_correct_in_block = 0
				num_incorrect_in_block = 0

		#num_correct_in_block = 0 #set number of correct to 0 at the beginning of each block
		#num_incorrect_in_block = 0 #set number of incorrect to 0 at the beginning of each block
		#while num_correct_in_block < num_stim:
		for i in presentation_order:
			
			# set stimulus image
			object_bin['stim'].setImage(stimuli[i])
            
			# reset clicked buttons
			event_utils.reset_btn_response(object_bin['response_btns'])

			# initially draw stimulus and response buttons
			event_utils.draw_objects_in_bin(
				window,
				object_bin, 
				object_list = ['stim', 'response_btns'],
			)           
			# wait some time
			if debug_mode == False: core.wait(.77)
			# draw click message
			event_utils.draw_objects_in_bin(
				window,
				object_bin, 
				object_list = ['stim', 'response_btns', 'click_msg'],
			)

			# wait some time
			if debug_mode == False: core.wait(.35)

			# wait for user to click a response button
			response, rt = event_utils.wait_for_btn_response(cursor, timer, object_bin['response_btns'], quit_keys=quit_keys)
			# check accuracy of subject's response
			correct_category = labels[i]
			if (supervised == True) & (correct_category != 'gen'):
				hit = response == correct_category
			else:
				hit = 'gen'
			accuracy.append(hit)
			#if (hit):
			#	num_correct_in_block += 1
			#else:
			#	num_incorrect_in_block += 1
			#keep track of whether the criteran has been met    
			#if num_correct_in_block >= criterian:
			#	met_criterian = True
			#else:
			#	met_criterian = False
			#get rid of the number correct for unsupervised so the data file is not confusing
			#if supervised == False:
			##	num_correct_in_block = 404
			#if all the stim have been run through, break out of this loop to move on to the next block
			#if (num_incorrect_in_block + num_correct_in_block) >= num_stim:
			#	break

           
			# keep track of total number of hits (increment if hit, preserve total if not hit)
			if (hit):
				num_correct_in_block += 1
			else:
			    num_incorrect_in_block += 1
			
			#keep track of whether the criteran has been met    
			if num_correct_in_block >= criterian:
				met_criterian = True
			else:
				met_criterian = False

            #get rid of the number correct for unsupervised so the data file is not confusing
			if supervised == False:
				current_num_correct = 404
 	
	
			if supervised == True:
				if response == correct_category:
					object_bin['feedback_msg'].setText('Correct! This is a member of category: ' + correct_category)
					object_bin['color_response'].setLineRGB("green")
				else:
					object_bin['feedback_msg'].setText('Incorrect... This is a member of category: ' + correct_category)
					object_bin['color_response'].setLineRGB("red")
				# draw feedback message
				event_utils.draw_objects_in_bin(
						window,
						object_bin, 
						object_list = ['stim', 'response_btns', 'feedback_msg', 'color_response'],
					)
			else:
				event_utils.draw_objects_in_bin(
					window,
					object_bin, 
					object_list = ['stim', 'response_btns'],
					)
	
	
			if debug_mode == False: core.wait(1)
			
			# draw continue message
			if supervised == True:
				event_utils.draw_objects_in_bin(
					window,
					object_bin, 
					object_list = ['stim', 'response_btns', 'feedback_msg', 'click_anywhere_msg'],
					)
	
			else:
				event_utils.draw_objects_in_bin(
					window,
					object_bin, 
					object_list = ['stim', 'response_btns', 'click_anywhere_msg'],
					)
	
			if debug_mode == False: core.wait(.35)
	
			event_utils.wait_for_click_response(cursor, timer, quit_keys=quit_keys)
	
			event_utils.draw_objects_in_bin(
				window,
				object_bin,
				object_list = ['response_btns'],
				)
            

			if save_data == True:
			
				subject_data = [
					subject_info['id'],
					phase_id,
					subject_info['condition'],
					block_data,
					trial_num,
					stimuli[i],
					correct_category,
					response,
					hit,
					rt,
					criterian,
					met_criterian,
					num_correct_in_block,
					]
				with open(subject_info['datafile_path'], 'a') as file:
					csv_object = csv.writer(file)
					csv_object.writerow(subject_data)
						
	
	
	
				# if early_finish_accuracy_criterion != None:
				# 	if trial_num > minimum_trials:
				# 		if sum(accuracy[-early_finish_lookback:]) / len(accuracy[-early_finish_lookback:]) >= early_finish_accuracy_criterion:
				# 			return

			
			trial_num = trial_num + 1









