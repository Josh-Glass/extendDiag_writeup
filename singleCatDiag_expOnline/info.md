# Webrunner Template 

Here's a basic rundown of how this will work:

- when it's time for a subject to run in your experiment, the server will host the template `.html` file located in this folder
  - that template file is where you'll want to manage everything that happens in your experiment
- the server will load all the tools and resources needed to conduct the experiment
- the subject will engage in the experiment
- their data will be saved to a folder you specify
- when finished, the server will redirect the subject to the next experiment

The `static/utils.js` script has a number of functions for communicating with the flask server. You can pretty much ignore all those. The *only functions from that script that you need to worry* about are:

- `get_subject_id()` & `get_condition()` which do what they say they'll do
- `next(...)` which sends your data to the server

Both of those functions are imported into the template html file; so you dont have to worry about those until you add your experiment to the main webserver.

---

## Configuration Guidelines

*(you dont have to worry about this much until running live; for experiment building, move to the `Experiment Template` section)*

Because we're hosting experiments together via the same Flask webserver, you're experiment has to follow this configuration:

- there has to be a template `html` file that initializes your experiment (it's called `testExp.html` in this example)
- the rest of the materials for your experiment (including javascript code, images, stimuli, etc) have to be saved in their own separate folder inside the `static/` folder
  - ^ this is a Flask nuance we have to follow
- data *has* to be saved to your own project folder *outside* where your code is (if it's saved anywhere in the `static/ `folder, anyone on the internet has access to subject data)
  - for our purposes: make a separate folder in `data` folder with your experiment name
- when we add your experiment to the main webserver, you'll have to fill out some details in a `config` file (will contain info like the exp name, conditions, data location, etc). It will look something like this: 

```python
'testExp': {
    'template': 'testExp.html',
    'data': 'data/testExp/', # where datafiles get saved
    'conditions': ['1','2'],
}
```

---

## Experiment Template

Your experiment will be hosted through the template `html` file you provide (see `testExp.html` example script). In that script, you'll want to:

- load all the modules
- initialize your js code
- send data to server

All the modules and resources you import have to be through the `static/` folder. So, a lot of your imports are going to have a path like: `static/testExp/...`.

The experiment template has a number of important variables that make the workflow easier.

### <u>subject variable</u>

This is a javascript object (functionally similar to a python dictionary) that contains important info like:

- `id`: basically the pnum; this is determined by the server
- `condition`: also determined by the server
- `results`: this is where you'll save the data for each phase of the experiment (you dont have access to a csv or anything like that yet; that doesn't happen until the end)

I wouldn't mess with this variable too much

### <u>Experiment Functions</u>

Each type of task (sort, classification, connection learning, etc) is wrapped up in it's own script, containing a single object with all the needed functions. To run the experiment phase, you need to call the `experiment.start(...)` function, which takes 2 arguments:

- `params`: all the settings for the experiment phase
- `next`: the next experiment phase to run when that phase is complete

These arguments are necessary for the flow of this entire thing, and shouldn't be messed with much (although you can modify anything you want in the `params` argument; that's the point). 

### <u>Event Graph</u>

this is just a jsObject where each phase of the experiment can be called from. Makes things a lot easier to work with, and allowes you to quickly manipulate the order of events. The `setTimeout(...)` function is just a way to delay the onset of the next event.

The last event, `end` sends the message to server that the next experiment is ready to be started (along with the data from this experiment). The subjects data will be saved as a `.json`  file in whatever area you specificied in the `config` script.

There are other ways to organize the experiment phases besides this event object, but the previous ways i tried were messy and inefficient to modify.

---

## [oCanvas](http://ocanvas.org/) workflow

The experiment functions all use the oCanvas library. In html, you can either work with html objects (buttons, divs, etc), or "canvases" (which are just blank templates on which you can draw shapes and stuff). oCanvas allows you to *very easily* work inside the html canvas, and handles all the event logic you'd need to run an experiment.

By design, javascript isn't going to let you work with for loops like psychopy. Instead, all we can really do is define objects and events, and keep track of how many events have occurred. 

For example, for the classification phase, we have 5 objects:

- the stimulus image
- the response buttons
- the question text ("which category do you think...")
- the feedback text
- the continue button

At the start of each experiment, we'll first call a function to create  a randomize block order for stimulus presentation. Then, we'll initialize the stimulus and response buttons. That's it. No for loops. The recurrence of trials will have to be handled by the event logic:

- Stimulus is presented at a response button is clicked:
  - record reaction time & accuracy
  - show feedback about correct / incorrect
  - remove response buttons
  - wait n milliseconds and then show the "continue" button
- Continue button is clicked:
  - remove feedback and continue button
  - add trial data to data array
  - add +1 to trial counter
  - check if # trials == # of blocks; 
    - if True:
      - reset the trial counter and add +1 to blocks
      - check if # blocks == max blocks; 
        - if True: call `next` function (move on to next phase of the experiment)
        - if False: reset block order
  - wait n milliseconds and then:
    - load stimulus and response buttons
    - reset reaction timer

It might seem annoying / tricky to not have for loops, but it's actually pretty intuitive when you reduce an entire trial down to 2 events (response button click and continue button click), each triggering the subsequent phase of the trial

Once the experiment phase is finished, the `subject['results']` object will now have a full array of trial data for that phase of the experiment.

That's it. Everything you need to build an experiment is handled by objects and how subjects interact with those objects. oCanvas makes all this feasible (since working with a raw html canvas is a fucking nightmare)

This should be all you need to get started. Coding this all up really isn't that bad, and it's extremely flexible to design any kind of event logic.

---

## IMPORTANT DETAILS:

- because this is hosted as a website, *you dont have access to local folders like you would a normal program*; the webbrowser wont let you see what's happening in the subjects computer
  - because of that, all your tools/modules have to be in the `static/` folder that the web browser will host
- *ANYTHING IN THE STATIC FOLDER WILL BE ACCESSIBLE TO THE OUTSIDE WORLD!!!* 
  - do NOT store your data anywhere in the `static/` folder
- javascript doesn't have a rigid sense of time like python does. While javascript runs each line one at a time, it will not wait for one line to fully complete before running the next one
  - it's really annoying to deal with but apparently it makes webpages load faster
  - it will probably be your biggest source of bugs
- if you're just running a TACL variant, all you really need to do is update the template `.html` file and the `materials` folder and you're good to go
- fuck jsPsych 
- When displaying text (like for instructions or questionnaires), it assumes the text is html. If you want to do things like making things **bold** or *italics*, you'll need to follow html formatting.
  - websites like this one will automatically generate html for you to make things for you: https://html-cleaner.com/

### Side Note

You dont have to use any of these tools; you can code up whatever you want assuming its coded in html/javascript. In fact, there are tons of prebuild html/javascript experiments you can grab from websites like:

- https://expfactory.github.io/
- https://github.com/jspsych/jsPsych/tree/master/examples
- https://pavlovia.org/explore

The only requirements are:

- everything is called from the main `html` template
  - use the `get_condition()` and `get_subject_id()` when needed
- all your code is saved in it's own folder in the `static/` folder
- you send your data to the server using the `next(...)` function