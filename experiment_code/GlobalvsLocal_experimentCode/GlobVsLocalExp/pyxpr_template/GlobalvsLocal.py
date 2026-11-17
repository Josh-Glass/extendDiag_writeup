'''
Experiment
'''

## Python Standard Library
import sys
import os
import datetime
import time

## external dependencies
from psychopy import visual

## Internal Dependencies
import pyxpr.utils
from pyxpr.events import initializer, instructions, classification

settings = {
    'experiment_id': 'exp',

	'save_data': True,
    'data_folder': './subject_data',
	'show_initial_dialogue': True,

	'subject_data_folder': './subject_data',
    'window_color': [1,1,1],
    'debug_mode': False,
}


# # # # # # # # # # # # # # # # # 
# 
#  SETUP
# 
# # # # # # # # # # # # # # # # # 

settings['experiment_time'] = '-'.join([str(d) for d in datetime.datetime.now().timetuple()][:6])

# Show initial dialogue window if True
if settings['show_initial_dialogue'] == True:
	initial_info = initializer.run(conditions=list([1,2]))
else:
	initial_info = ['debug', 1]

# Define Subject Dictionary (this is where we'll store all the information about the subject)
subject = {
	'id': str(initial_info[0]),
	'condition': int(initial_info[1]),
	'datafile_path': os.path.join(settings['data_folder'], str(initial_info[0]) + '_' + settings['experiment_time'] + '.csv')
}

if settings['save_data'] == True:
	with open(subject['datafile_path'], 'w'):
		pass

if subject['id'] == 'debug':
	settings['debug_mode'] = True

## build experiment window (little bit faster to pass the window as an argument to each event rather than making a new one on the fly each time an event changes)
if settings.get('window_size', 'full') == 'full':
	win = visual.Window(fullscr = True, units = 'pix', color = settings.get('window_color', [1,1,1]))
else:
	win = visual.Window(settings['window_size'], units = 'pix', color = settings.get('window_color', [1,1,1]))






# # # # # # # # # # # # # # # # # 
# 
#  Run Experiment
# 
# # # # # # # # # # # # # # # # # 




# - - - Phase 1 - Training (with feedback) - - - 

#condition 1
if int(initial_info[1]) == 1:
    # instructions function
    instructions.run(
        text_file = 'materials/instructions/C1_Train1.txt',	
        
        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )


    stimuli_train = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
    ]

    labels_train = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        ]

    # classification phase function
    classification.run(
        stimuli_train,
        labels = labels_train,
        response_btn_labels = ['Alpha','Beta'],

        phase_id = 'training_phase_1',
        supervised = True, # <-- this means there will be feedback
        randomize_presentation = True,
        criterian = 11,
        max_attempts = 8,
        num_stim = 12,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = False,
        
        feedback_txt_position = [0, 250],
        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200]
    )




    # - - - Phase 2 - Test (no feedback) - - -

    # instructions function
    instructions.run(
        text_file = './materials/instructions/C1_Test.txt',

        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
        
        
    
    )


    stimuli_test = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
        'materials/images/yGen1.png',
        'materials/images/yGen2.png',
        'materials/images/yGen3.png',
        'materials/images/yGen4.png',
        'materials/images/yGen5.png',
    ]

    labels_test = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'test',
        'test',
        'test',
        'test',
        'test']

    # classification phase function
    classification.run(
        stimuli_test,
        labels = labels_test,
        response_btn_labels = ['Alpha','Beta'],

        phase_id = 'test_phase',
        supervised = False, # <-- no feedback
        randomize_presentation = True,
        criterian = 1,
        max_attempts = 1,
        num_stim = 17,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = settings['debug_mode'],
        
        
        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200]
    )
    
    #   Phase 3<--training_phase_2
        # instructions function
    instructions.run(
        text_file = 'materials/instructions/C1_Train2.txt',	
        
        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )


    stimuli_train = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
        'materials/images/blackG1.png',
        'materials/images/blackG2.png',
        'materials/images/blackG3.png',
        'materials/images/blackG4.png',
        'materials/images/blackG5.png',
        'materials/images/blackG6.png',
        'materials/images/greenD1.png',
        'materials/images/greenD2.png',
        'materials/images/greenD3.png',
        'materials/images/greenD4.png',
        'materials/images/greenD5.png',
        'materials/images/greenD6.png',
        
    ]

    labels_train = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        ]

    # classification phase function
    classification.run(
        stimuli_train,
        labels = labels_train,
        response_btn_labels = ['Alpha','Beta', 'Gamma', 'Delta'],

        phase_id = 'training_phase_2',
        supervised = True, # <-- this means there will be feedback
        randomize_presentation = True,
        criterian = 30,
        max_attempts = 2,
        num_stim = 24,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = False,
        
        feedback_txt_position = [0, 250],
        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200]
    )

    # - - - Exit Page - - -
    instructions.run(
        text_file = './materials/instructions/exit.txt',

        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )
#  # # # # # # # # # # #################################################################################
#Condition 2  
#   # ##################################################################################################

# #####################################################################################################
else:
    instructions.run(
        text_file = 'materials/instructions/C2_Train1.txt',	
        
        
        
        
        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )


    stimuli_train = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
    ]

    labels_train = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        ]

    # classification phase function
    classification.run(
        stimuli_train,
        labels = labels_train,
        response_btn_labels = ['Alpha','Beta','Gamma', 'Delta'],
        
        response_btn_states = [True, True, False, False],

        phase_id = 'training_phase_1',
        supervised = True, # <-- this means there will be feedback
        randomize_presentation = True,
        criterian = 11,
        max_attempts = 8,
        num_stim = 12,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = False,
        
        feedback_txt_position = [0, 250],
        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200],
        
        
        
        
        
        
    )




    # - - - Phase 2 - Test (no feedback) - - -

    # instructions function
    instructions.run(
        text_file = './materials/instructions/C2_Test.txt',

        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
        
        
        
    )


    stimuli_test = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
        'materials/images/yGen1.png',
        'materials/images/yGen2.png',
        'materials/images/yGen3.png',
        'materials/images/yGen4.png',
        'materials/images/yGen5.png',
    ]

    labels_test = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'test',
        'test',
        'test',
        'test',
        'test',
    ]

    # classification phase function
    classification.run(
        stimuli_test,
        labels = labels_test,
        response_btn_labels = ['Alpha','Beta','Gamma', 'Delta'],
        response_btn_states = [True, True, False, False],

        phase_id = 'test_phase',
        supervised = False, # <-- no feedback
        randomize_presentation = True,
        criterian = 1,
        max_attempts = 1,
        num_stim = 17,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = settings['debug_mode'],
        

        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200]
    )

        #   Phase 3<--training_phase_2
        # instructions function
    instructions.run(
        text_file = 'materials/instructions/C2_Train2.txt',	
        
        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )


    stimuli_train = [
        'materials/images/redA1.png',
        'materials/images/redA2.png',
        'materials/images/redA3.png',
        'materials/images/redA4.png',
        'materials/images/redA5.png',
        'materials/images/redA6.png',
        'materials/images/blueB1.png',
        'materials/images/blueB2.png',
        'materials/images/blueB3.png',
        'materials/images/blueB4.png',
        'materials/images/blueB5.png',
        'materials/images/blueB6.png',
        'materials/images/blackG1.png',
        'materials/images/blackG2.png',
        'materials/images/blackG3.png',
        'materials/images/blackG4.png',
        'materials/images/blackG5.png',
        'materials/images/blackG6.png',
        'materials/images/greenD1.png',
        'materials/images/greenD2.png',
        'materials/images/greenD3.png',
        'materials/images/greenD4.png',
        'materials/images/greenD5.png',
        'materials/images/greenD6.png',
        
    ]

    labels_train = [
        'Alpha', 
        'Alpha', 
        'Alpha',
        'Alpha',
        'Alpha',
        'Alpha',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Beta',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Gamma',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        'Delta',
        ]

    # classification phase function
    classification.run(
        stimuli_train,
        labels = labels_train,
        response_btn_labels = ['Alpha','Beta', 'Gamma', 'Delta'],

        phase_id = 'training_phase_2',
        supervised = True, # <-- this means there will be feedback
        randomize_presentation = True,
        criterian = 30,
        max_attempts = 2,
        num_stim = 24,

        window = win,
        experiment_id = settings['experiment_id'],
        subject_info = subject,
        save_data = True,
        debug_mode = False,
        
        feedback_txt_position = [0, 250],
        click_instructions_position = [0, 200],
        continue_txt_position = [0, 200]
    )

    # - - - Exit Page - - -
    instructions.run(
        text_file = './materials/instructions/exit.txt',

        window = win,
        debug_mode = settings['debug_mode'],
        window_color = settings['window_color'],
        continue_option = 'click',
    )
