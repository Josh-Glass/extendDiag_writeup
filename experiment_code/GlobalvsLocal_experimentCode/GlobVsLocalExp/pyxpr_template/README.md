# PYthon eXPeRiments

This repo contains the general skeleton of a TACL experiment. The main file you'll want to focus on is the `experiment.py` file. 

## `experiment.py` organization

Here's a walkthrough of what's going on in the `experiment.py` file

### Imports
```python
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
```

Here's where we import all the tools we'll be using. We obviously need psychopy installed; that's the core tool we'll use for designing experiments. You'll have to download it.

The `pxypr` import contains a bunch of wrappers to make the design even easier (arguably). The `pyxpr` module contains a bunch of "event" scripts with functions for each type of task you might want to run. 


### Settings Variable

Next, we initialize a python dictionary object to store some global settings that we may want to tweak at any point.

```python
settings = {
    'experiment_id': 'exp',

	'save_data': True,
    'data_folder': './subject_data',
	'show_initial_dialogue': False,

	'subject_data_folder': './subject_data',
    'window_color': [1,1,1],
}
```

### Setup

```python
# # # # # # # # # # # # # # # # # 
# 
#  SETUP
# 
# # # # # # # # # # # # # # # # # 

settings['experiment_time'] = '-'.join([str(d) for d in datetime.datetime.now().timetuple()][:6])

# Show initial dialogue window if True
if settings['show_initial_dialogue'] == True:
	initial_info = initializer.run()
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
```

Here we do a few things. First, we initialize a dialogue window, where RAs will type in subjects id_number and condition info (which they get from the experiment log). Then, we create a dictionary called `subject` to store some important info about the subject. Next, we create an empty file where we'll eventually store their data. Finally, we make a psychopy `window` object.

### Running the Experiment

Next, we'll actually run each phase of our experiment; this is what we use `pyxpr` for. Each `pxypr` event can be called using the `.run(...)` function <-- the parameters of that function can be tweaked to fit your particular needs. 

#### Running the Instructions
```python
instructions.run(
	window = win,
	text_file = 'materials/instructions/training.txt',	
)
```
^ Running the instructions is pretty easy. We just call the `instructions.run(...)` function, and provide the psychopy window object along with the path to the textfile containing our instructions. I have the textfile stored in `materials/instructions` for convenience.

#### Supervised Classification Phase
```python
stimuli_train = [
    'materials/stimuli/stim1.png',
    'materials/stimuli/stim2.png',
]

labels_train = [
	'A',
	'B'
]

# classification phase function
classification.run(
	stimuli_train,
	labels = labels_train,

    phase_id = 'training_phase_1',
    supervised = True, # <-- this means there will be feedback
    randomize_presentation = True,
    num_blocks = 3,

	window = win,
	experiment_id = settings['experiment_id'],
	subject_info = subject,
	save_data = True,
	debug_mode = False,
)
```
To run a classification phase, first we need 2 variables:
- a list of images (specifically, the path to image files)
- a list of category labels

After we make those variables, we'll call the `classification.run(...)` function. If we set `supervised = True`, participants will be given feedback after each trial. This is typically what we do for the training phase of an experiment.

#### Unsupervised Test Phase
```python
# instructions function
instructions.run(
    text_file = './materials/instructions/test.txt',

	window = win,
	debug_mode = settings['debug_mode'],
    window_color = settings['window_color'],
    continue_option = 'click',
)


stimuli_test = [
    'materials/stimuli/stim1.png',
    'materials/stimuli/stim2.png',
    'materials/stimuli/stim3.png',
]

labels_test = ['A','B','test']

# classification phase function
classification.run(
	stimuli_test,
	labels = labels_test,
    response_btn_labels = ['A','B'],

    phase_id = 'test_phase',
    supervised = False, # <-- no feedback
    randomize_presentation = True,
    num_blocks = 1,

	window = win,
	experiment_id = settings['experiment_id'],
	subject_info = subject,
	save_data = True,
	debug_mode = settings['debug_mode'],
)

```
^ This time, we pretty much to exactly the same thing as we did for the training phase, with 2 changes:
- number of blocks was set to 1
- we set `supervised = False`; meaning: there won't be any feedback

If you have critical test items that weren't observed during training, you'll want to include them in your stimulus and label list. For critical test items, I like to label them "test" so I know in my datafile which items were unseen.


---

And that's about it. Subject data will be stored in the `subject_data` folder.


