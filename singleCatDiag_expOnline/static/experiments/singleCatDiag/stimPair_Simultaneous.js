var stimPair_Simultaneous = {
    start: function(params, next) {
        params['results'].push(['pnum','condition','phase','trial','block','target','match_id','lure_id', 'randNum', 'category','response','acc','rt'])

    

        /*   initialize   */
        space = oCanvas.create({
            canvas: stimPair_Simultaneous.initCanvas(),
            background: 'rgba(255,255,255)',
        })

        // useful variables for stim creation
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        maxX = space.canvasElement.width
        maxY = space.canvasElement.height

        //viewing_time = 6000
        stimPair_Simultaneous.initElements(params)

        // progress tracking variables
        
        x = new Date().getTime()
        rt = null
        response = null
        acc = null
        trial = 0
        block =  0
        block_order = stimPair_Simultaneous.generateBlockOrder(params['objects'], params['labels'])
        state = 'viewing', // describe, select, or block_all_actions

        acc_array = []





        // - - - Event Logic - - -


        // category label
        correctCategory = block_order[trial][1]

        randNum = Math.random()

        if (randNum > .50) {
            stimPair_Simultaneous.initStim(block_order[trial][0], block_order[trial][2], block_order[trial][4])
            opt1Category = block_order[trial][3]
            opt2Category = block_order[trial][5]
            option1.bind('click tap', function () {startEvent(option1.image, option1)})
            option2.bind('click tap', function () {startEvent(option2.image, option2)})
        } else {
            stimPair_Simultaneous.initStim(block_order[trial][0], block_order[trial][4], block_order[trial][2])
            opt1Category = block_order[trial][5]
            opt2Category = block_order[trial][3]
            option1.bind('click tap', function () {startEvent(option1.image, option1)})
            option2.bind('click tap', function () {startEvent(option2.image, option2)})
        }

        targetTxt.text = `${correctCategory}`
        instructionsTxt.text = `Which of the two options is also a ${correctCategory}?`
        space.scenes.load('selection')

        function startEvent(selection, option) {
            state = 'block_all_actions'
            rt = new Date().getTime() - x
            // get label from selection
            option1Txt.text = option1.image.split('/')[4].slice(13,18)
            option2Txt.text = option2.image.split('/')[4].slice(13,18)

            response = selection.split('/')[4].slice(13,18)
            
            if (response == correctCategory) {
                acc = true
            } else {
                acc = false
            }
            //console.log(acc)

            if (params['feedback'] == false) {
                feedbackTxt.text = "Thanks for your response! You may continue."
                option.stroke = '10px orange'
                option.addChild(space.display.rectangle({
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, align: 'center',
                    width: 100,
                    height: 20,
                    fill: 'white',
                    join: "round",
                }))
                option.addChild(space.display.text({  
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, 
                    font: "bold 20px sans-serif",
                    text: `OPTION`,
                    fill: 'black',
                }))

            } else if (acc == true) {
                feedbackTxt.text = `Yep! You got it.\n\nThat option is a member of the ${correctCategory} category.`
                feedbackTxt.fill = 'rgb(128, 243, 64)'
                option.stroke = '10px #80F340'
                option.addChild(space.display.rectangle({
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, align: 'center',
                    width: 100,
                    height: 20,
                    fill: 'white',
                    join: "round",
                }))
                option.addChild(space.display.text({  
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, 
                    font: "bold 20px sans-serif",
                    text: `${response}`,
                    fill: 'rgb(128, 243, 64)',
                }))
            } else if (acc == false) {
                feedbackTxt.text = `Sorry, that\'s not it.\n\nThat option is a member of the ${response} category.`
                feedbackTxt.fill = 'rgb(249, 130, 130)'
                option.stroke = '10px rgb(249, 130, 130)'
                option.addChild(space.display.rectangle({
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, align: 'center',
                    width: 100,
                    height: 20,
                    fill: 'white',
                    join: "round",
                }))
                option.addChild(space.display.text({  
                    x: 0,
                    y: 110,
                    origin: { x: "center", y: "center" }, 
                    font: "bold 20px sans-serif",
                    text: `${response}`,
                    fill: 'rgb(249, 130, 130)',
                }))

            }

            acc = Number(acc)

            space.scenes.load('feedback')

            setTimeout( function () {
                space.scenes.load('continue')

                x = new Date().getTime()
            }, 1000)
    
        }

        continueBtn.bind('click tap', function () {
            space.scenes.unload('selection')
            space.scenes.unload('continue')
            space.scenes.unload('feedback')

            target.remove()
            option1.remove()
            option2.remove()

            targetTxt.text = ''
            option1Txt.text = ''
            option2Txt.text = ''

            console.log(block_order[trial][0])
            params['results'].push([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], block_order[trial][2].split('/').slice(-1)[0].split('.')[0], block_order[trial][4].split('/').slice(-1)[0].split('.')[0], randNum, correctCategory, response, acc, rt]) // pulled this variable from the main template
            console.log([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], block_order[trial][2].split('/').slice(-1)[0].split('.')[0], block_order[trial][4].split('/').slice(-1)[0].split('.')[0], randNum, correctCategory, response, acc, rt])

            acc_array.push(acc)

            trial += 1
            if (trial == block_order.length) {
                trial = 0
                block += 1
                if (block == params['num_blocks']) {
                    space.destroy(space)
                    document.getElementById('main').innerHTML = ''
                    next()
                } else {
                    block_order = stimPair_Simultaneous.generateBlockOrder(params['objects'], params['labels'])
                }
            }

            setTimeout( function () {
                //x = new Date().getTime()
                correctCategory = block_order[trial][1]

                randNum = Math.random()
        
                if (randNum > .50) {
                    stimPair_Simultaneous.initStim(block_order[trial][0], block_order[trial][2], block_order[trial][4])
                    opt1Category = block_order[trial][3]
                    opt2Category = block_order[trial][5]
                    option1.bind('click tap', function () {startEvent(option1.image, option1)})
                    option2.bind('click tap', function () {startEvent(option2.image, option2)})
                } else {
                    stimPair_Simultaneous.initStim(block_order[trial][0], block_order[trial][4], block_order[trial][2])
                    opt1Category = block_order[trial][5]
                    opt2Category = block_order[trial][3]
                    option1.bind('click tap', function () {startEvent(option1.image, option1)})
                    option2.bind('click tap', function () {startEvent(option2.image, option2)})
                }
        
                targetTxt.text = `${correctCategory}`
                instructionsTxt.text = `Which of the two options is also a ${correctCategory}?`
                space.scenes.load('selection')

            }, 200)


        })


    },


    initElements: function (params) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2
        maxX = space.canvasElement.width
        maxY = space.canvasElement.height
        
        


        instructionsTxt = space.display.text({
            x: centerX,
            y: 30,
            origin: { x: "center", y: "center" }, 
            align: "center",
            font: "bold 25px sans-serif",
            text: "instructs",
            fill: "black",
            zIndex: "front",
        })

        instructionsTxt.addChild(
            space.display.text({
                x: 0,
                y: 50,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 20px sans-serif",
                text: "< click on an image to make a selection >",
                fill: "#A6ACAF",
                zIndex: "front",
            })
        )

        space.scenes.create('selection', function () {
            this.add(instructionsTxt)
        })

        if (params['feedback'] == true) {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy ,
                origin: { x: "center", y: "center" },
                align: "center",
                font: "bold 25px sans-serif",
                text: "Feedback Message",
                fill: "black"
            });
        } else {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy ,
                origin: { x: "center", y: "center" },
                align: "center",
                font: "bold 25px sans-serif",
                text: "Thanks for your response! You may continue. ",
                fill: "black"
            });
        }
        space.scenes.create('feedback', function () {
            this.add(feedbackTxt)
        })

        /*   Continue Button   */
        continueBtn = space.display.rectangle({
            x: maxX - 200,
            y: maxY - 160,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#FF5D00",
            stroke: "#FF5D00",
            join: "round",

        })
        continueBtn.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Next Trial",
                fill: "rgba(255,255,255,1)",
                // zIndex: "front",
            })
        )
        space.scenes.create('continue', function () {
            this.add(continueBtn)
        })
    },




    initStim: function (image1, image2, image3, order) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        match_y_depth = 140
        match_x_depth = 200

        widthscale = .3
        heightscale = .3


        target = space.display.image({
            x: centerX,
            y: maxY - 160 ,
            origin: { x: "center", y: "center" }, align: 'center',
            height: maxY * .25,
            width:  maxY * .25,
            image: image1,
            stroke: "0px black"
        })
        target.addChild(
            targetTxt = space.display.text({
                x: 0,
                y: 110,
                origin: { x: "center", y: "center" }, 
                font: "bold 20px sans-serif",
                text: 'text',
                fill: "black",
            })
        )


        option1 = space.display.image({
            x: centerX - maxX/3,
            y: centerY - maxY/5,
            origin: { x: "center", y: "center" }, align: 'center',
            height: maxY * .25,
            width: maxY * .25,
            image: image2,
            stroke: "0px black"
        })

        option1.addChild(
            option1Txt =space.display.text({
                x: 0,
                y: 110,
                origin: { x: "center", y: "center" }, 
                font: "bold 20px sans-serif",
                text: 'OPTION',
                fill: "black",
            })
        )


        option2 = space.display.image({
            x: centerX + maxX/3,
            y: centerY - maxY/5,
            origin: { x: "center", y: "center" }, align: 'center',
            height: maxY * .25,
            width: maxY * .25,
            image: image3,
            stroke: "0px black"
        })

        option2.addChild(
            option2Txt = space.display.text({
                x: 0,
                y: 110,
                origin: { x: "center", y: "center" }, 
                font: "bold 20px sans-serif",
                text: 'OPTION',
                fill: "black",
            })
        )

        space.addChild(target)
        space.addChild(option1)
        space.addChild(option2)


        /* stim_pair_options = [item_rel, item_sup]
        stim_left_path = stim_pair_options[order[0]]
        stim_right_path = stim_pair_options[order[1]]

        height_ratio = 144 / 432

        standard = {
            obj: space.display.image({
                x: centerX,
                // y: centerY + maxY/4 + 50,
                y: maxY - 140,
                origin: { x: "center", y: "center" },
                image: item_standard,
                width: maxX * widthscale,
                height: maxX * widthscale * height_ratio,
            }),
            set_coords: function () {
                this.obj.x = centerX
                // this.obj.y = centerY + maxY/4
                this.obj.y = maxY - 100
                this.obj.width = maxX * widthscale
                this.obj.height = maxX * widthscale * height_ratio
            },
        }
        standard.obj.addChild(
            space.display.text({
                x: 0,
                y: 90,
                origin: { x: "center", y: "center" }, 
                font: "bold 25px sans-serif",
                text: "TARGET",
                fill: "rgba(0,0,0,1)",
            })
        )

        stim_left = { // order idx 0
            obj: space.display.image({
                x: centerX - maxX/4,
                y: centerY - maxY/4,
                origin: { x: "center", y: "center" },
                image: stim_left_path,
                width: maxX * widthscale,
                height: maxX * widthscale * height_ratio,
            }),
            set_coords: function () {
                this.obj.x = centerX - maxX/4 
                this.obj.y = centerY - maxY/4
                this.obj.width = maxX * widthscale
                this.obj.height = maxX * widthscale * height_ratio
            },
            match_type: lr[order[0]], match_type_id: order[0],
        }
        stim_left.obj.addChild(
            space.display.text({
                x: 0,
                y: 90,
                origin: { x: "center", y: "center" }, 
                font: "bold 25px sans-serif",
                text: "OPTION",
                fill: "rgba(0,0,0,1)",
            })
        )

        stim_right = { // order idx 1
            obj: space.display.image({
                x: centerX + maxX/4,
                y: centerY - maxY/4,
                origin: { x: "center", y: "center" },
                image: stim_right_path,
                width: maxX * widthscale,
                height: maxX * widthscale * height_ratio,
            }),
            set_coords: function () {
                this.obj.x = centerX + maxX/4
                this.obj.y = centerY - maxY/4
                this.obj.width = maxX * widthscale
                this.obj.height = maxX * widthscale * height_ratio
            },
            match_type: lr[order[1]], match_type_id: order[1],
        }
        stim_right.obj.addChild(
            space.display.text({
                x: 0,
                y: 90,
                origin: { x: "center", y: "center" }, 
                font: "bold 25px sans-serif",
                text: "OPTION",
                fill: "rgba(0,0,0,1)",
            })
        )



        space.scenes.create('standard', function () {
            this.add(standard.obj)
        })
        space.scenes.create('matches', function () {
            this.add(stim_left.obj)
            this.add(stim_right.obj)
        })
        
        stim_left.obj.bind('click tap', function () {
            if (state_information['state'] == 'select') {
                next_trial(stim_left.match_type, stim_left.match_type_id)
            }
        })
        stim_right.obj.bind('click tap', function () {
            if (state_information['state'] == 'select') {
                next_trial(stim_right.match_type, stim_right.match_type_id)
            }
        }) */

    },


    generateBlockOrder: function (objects, labels) {

        let block = [];
        let labelsD = [];
        let labelsG = [];
    
        // Separate the indices for each label
        for (let i = 0; i < labels.length; i++) {
            if (labels[i][0] == 'D') {
                labelsD.push(i);
            } else if (labels[i][0] == 'G') {
                labelsG.push(i);
            }
        }
    
        // Select an equal number of indices from each label group
        let numLabels = Math.floor(labels.length / 3);
        let numLabelsD = Math.floor(numLabels / 2);
        let numLabelsG = numLabels - numLabelsD;
    
        let idxD = stimPair_Simultaneous.shuffle(labelsD).slice(0, numLabelsD);
        let idxG = stimPair_Simultaneous.shuffle(labelsG).slice(0, numLabelsG);
        let idx = stimPair_Simultaneous.shuffle([...idxD, ...idxG]);
    
        console.log(idx)
    
        for (let i of idx) {
    
            console.log(labels[i][0])
    
            let bestMatch = null;
            let bestLure = null;
    
            for (let e of stimPair_Simultaneous.shuffle([...Array(labels.length).keys()])) {
                if ((labels[e][0] == labels[i][0]) && (e != i)) {
                    bestMatch = [objects[e], labels[e]];
                    break;
                }
            }
    
            for (let r of stimPair_Simultaneous.shuffle([...Array(labels.length).keys()])) {
                if (labels[r][0] != labels[i][0]) {
                    bestLure = [objects[r], labels[r]];
                    break;
                }
            }
    
            side_shuffle_idx = stimPair_Simultaneous.shuffle([...Array(2).keys()]);
    
            block.push([objects[i], labels[i], bestMatch[0], bestMatch[1], bestLure[0], bestLure[1]]);
        }
    
        return block;
    },


    shuffle: function (array) { // from mike bostok @ https://bost.ocks.org/mike/shuffle/
        var m = array.length, t, i;

        // While there remain elements to shuffle…
        while (m) {

            // Pick a remaining element…
            i = Math.floor(Math.random() * m--);

            // And swap it with the current element.
            t = array[m];
            array[m] = array[i];
            array[i] = t;
        }

        return array;
    
    },

    initCanvas: function () {
        canvas = document.createElement('canvas', {id: 'canvas', style: 'position:absolute;'})
        document.getElementById('main').appendChild(canvas)
        
        var ctx = canvas.getContext('2d');
        // ctx.lineWidth = 2;
        ctx.canvas.width  = window.innerWidth - 20;
        ctx.canvas.height = window.innerHeight - 20;

        window.addEventListener('resize', function () {
            space.width = window.innerWidth - 20;
            space.height = window.innerHeight - 20;
        }, false);

        return canvas
    },

/*     set_coords: function(elements) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2
        maxX = space.canvasElement.width
        maxY = space.canvasElement.height
        
        stim_left.set_coords()
        stim_right.set_coords()
        standard.set_coords()

        elements.rating_instructions.set_coords()
        elements.nextButton.set_coords()
        elements.selection_instructions.set_coords()
    },
 */
}