var study = {

    start: function(params, next) {
        params['results'].push(['trial','block','stimId','category','response','rt'])

        /*   initialize   */
        space = oCanvas.create({
            canvas: study.initCanvas(),
            background: 'rgba(255,255,255)',
            // origin: { x: "center", y: "center" },
        })

        cx = space.canvasElement.width / 2
        cy = space.canvasElement.height / 2

        study.initElements(params)
        //study.initDebugWindow(params)
        //space.scenes.load('debug')

        x = new Date().getTime()
        rt = 0
        response = null
        acc = null
        trial = 0
        block = 0
        block_order = study.generateBlockOrder(params['objects'], params['labels']) // <-- initialize the first block order (you'll do this every block)
        acc_history = []

        correctCategory = block_order[trial][1]
        study.initStim(block_order[trial][0])

        space.scenes.load('selection')


        /*   define event logic   */
        for (category of params['categories']) {
            responseBtns[category].btn.bind('click tap', function () {
                rt = new Date().getTime() - x

                response = this.category

                acc = response == correctCategory

                if (params['feedback'] == true) {
                    if (acc == true) {
                        feedbackTxt.text = 'Yep! You got it. This is a member of category '.concat(params['btnLabels'][correctCategory])
                    } else {
                        feedbackTxt.text = 'Sorry, that\'s not it. This is a member of category '.concat(params['btnLabels'][correctCategory])
                    }
                }

                space.scenes.unload('selection')
                space.scenes.load('feedback')
                stimulus.remove()

                params['results'].push([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], correctCategory, response, rt]) // pulled this variable from the main template

                trial += 1
                if (trial == block_order.length) {
                trial = 0
                block += 1
                if (block == params['n_blocks']) {
                    space.destroy(space)
                    document.getElementById('main').innerHTML = ''
                    next()
                } else {
                    block_order = study.generateBlockOrder(params['objects'], params['labels'])
                }
                }


                setTimeout( function () {
                    space.scenes.load('selection')
                    study.initStim(block_order[trial][0])
                    correctCategory = block_order[trial][1]
                    x = new Date().getTime()
                }, 200)
                

                //setTimeout(function () {
                  //  space.scenes.load('continue')
                //}, 200)
            })
        }


        continueBtn.bind('click tap', function () {
            space.scenes.unload('continue')
            space.scenes.unload('feedback')
            stimulus.remove()

            params['results'].push([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], correctCategory, response, acc, rt]) // pulled this variable from the main template
            
            if (params['finish_early'] == true) {
                acc_history.push(acc)
                if (acc_history.length >= params['lookback']) {
                    if (block >= params['min_blocks']) {
                        if ( study.mean(acc_history.slice(-params['lookback']))  >= params['finish_early_criterion']) { // <-- the reduce thing calculates the mean (because apparently a sum function didnt make the cut in javascripts standard lib (despite other bs making the cut; sigh))
                            space.destroy()
                            document.getElementById('main').innerHTML = ''
                            next()
                        }
                    }
                } 
                if (trial == block_order.length) {
                    trial = 0
                    block += 1
                    if (block == params['n_blocks']) {
                        space.destroy(space)
                        document.getElementById('main').innerHTML = ''
                        next()
                    } else {
                        block_order = study.generateBlockOrder(params['objects'], params['labels'])
                    }
                }
            }


            trial += 1
            if (trial == block_order.length) {
                trial = 0
                block += 1
                if (block == params['n_blocks']) {
                    space.destroy(space)
                    document.getElementById('main').innerHTML = ''
                    next()
                } else {
                    block_order = study.generateBlockOrder(params['objects'], params['labels'])
                }
            }

            setTimeout( function () {
                space.scenes.load('selection')
                study.initStim(block_order[trial][0])
                correctCategory = block_order[trial][1]
                x = new Date().getTime()
            }, 200)

        })

        console.log('started study')
    },


    initElements: function (params) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        /*   Response Phase of Trial   */

        // Calculate how much to shrink elements if the screen is shorter than 900px
        let scale = Math.min(space.canvasElement.height / 800, 1)

        responseBtns = {}
        btnCompression = .4
        for (let [index, category] of params['categories'].entries()) {
            let xpos = ((space.canvasElement.width / params['categories'].length) * index)  +  ((space.canvasElement.width / params['categories'].length) / 2)
            responseBtns[category] = {
                'category': category,
                'btnLabel': params['btnLabels'][category],
            }

            responseBtns[category].btn = space.display.rectangle({
                x: xpos + (((space.canvasElement.width / 2) - xpos) * btnCompression),
                y: centerY + (250 * scale), // <-- Scaled Y position
                origin: { x: "center", y: "center" },// align: 'center',
                width: 190,
                height: 60,
                fill: "#079",
                stroke: "10px #079",
                join: "round",
                category: category, // <-- CAREFUL! This is a custom added property to the oCanvas Base object; if they decide to ever include it, this will overwrite whatever function they decide the 'category' property should have (though low odds of that happening)
            })
            responseBtns[category].btn.addChild(
                space.display.text({
                    x: 0,
                    y: 0,
                    origin: { x: "center", y: "center" },// align: 'center',
                    font: "bold 25px sans-serif",
                    text: 'Next',
                    fill: "rgba(255,255,255,1)",
                    zIndex: "front",
                })
            )
        

        instructionsTxt = space.display.text({
            x: centerX,
            y: centerY + (170 * scale),
            origin: { x: "center", y: "center" }, align: 'center',
            align: "center",
            font: "bold 20px sans-serif",
            text: `Study this item\nfrom the\n${responseBtns[category]['btnLabel']} category`,
            fill: "rgba(0,0,0,1)",
            zIndex: "front",
        })}

        space.scenes.create('selection', function () {
            for (category of params['categories']) {
                this.add(responseBtns[category].btn)
            }
            this.add(instructionsTxt)
        })


        /*   Feedback   */
        if (params['feedback'] == true) {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy + (120 * scale),
                origin: { x: "center", y: "top" }, align: 'center',
                align: "center",
                font: "bold 30px sans-serif",
                text: "Feedback Message",
                fill: "#000000",
                zIndex: "front"
            });
        } else if (params['feedback'] == false) {
            feedbackTxt = space.display.text({
                x: cx,
                y: cy,
                origin: { x: "center", y: "top" }, align: 'center',
                align: 'center',
                font: "bold 30px sans-serif",
                text: " ",
                fill: "#000000",
                zIndex: "front"
            });
        }
        space.scenes.create('feedback', function () {
            this.add(feedbackTxt)
        })



        /*   Continue Button   */
        continueBtn = space.display.rectangle({
            x: cx,
            y: cy + (250 * scale),
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
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
                zIndex: "front",
            })
        )
        space.scenes.create('continue', function () {
            this.add(continueBtn)
        })
    },

    initStim: function (image) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2
        
        let scale = Math.min(space.canvasElement.height / 800, 1)

        stimulus = space.display.image({
            x: centerX,
            y: centerY - (150 * scale), // <-- Scaled Y position
            origin: { x: "center", y: "center" }, align: 'center',
            image: image,
            height: 500 * scale, // <-- Scaled dimensions
            width: 500 * scale,  // <-- Scaled dimensions
            zIndex: "back", // set z index to back
        })

        space.addChild(stimulus)
    },



    generateBlockOrder: function (objects, labels) {
        let block = []
        idx = study.shuffle([...Array(labels.length).keys()]) // from ben @ https://stackoverflow.com/a/10050831

        for (let i of idx) {
            block.push([objects[i], labels[i]])
        }

        return block
    },

    mean: function(numbers) {
        return study.sum(numbers) / numbers.length;
    },

    sum: function(numbers) {
        var total = 0;
        for(var i = 0; i < numbers.length; i++) {
            total += numbers[i];
        }
        return total;
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

    initDebugWindow: function (params) {
        lastBtnClick = ''

        debugWindow = space.display.rectangle({
            x: 10,
            y: 10,
            // origin: { x: "center", y: "center" }, align: 'center',
            width: 200,
            height:300,
            fill: "rgb(255,255,255)",
            stroke: "3px black",
            join: "round",
        })

        debugInfo = space.display.text({
            x: 30,
            y: 30,
            // origin: { x: "center", y: "center" },
            font: "bold 12px sans-serif",
            text: "debug",
            fill: "black",
            zIndex: "front",
        })

        debugWindow.addChild(debugInfo)

        close = space.display.rectangle({
            x: 12,
            y: 12,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 20,
            height:20,
            fill: "rgb(190,190,190)",
            stroke: "2px black",
            join: "round",
        })
        close.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: "center",
                font: "bold 14px sans-serif",
                text: "x",
                fill: "white",
                zIndex: "front",
            }) 
        )
        debugWindow.addChild(close)
        close.bind('click tap', function () {
            space.scenes.unload('debug')
        })

        space.scenes.create('debug', function () {
            this.add(debugWindow)
        })

        space.setLoop(function () {
            debugInfo.text = [
                'x: '.concat(space.mouse.x),
                'y: '.concat(space.mouse.y),
                'correctCategory: '. concat(correctCategory),
                'response: '. concat(response),
                'rt: '.concat(rt),
                '\n',
                'data:',
                params['results'].join('\n')
            ].join('\n')
        }).start()
    },

}