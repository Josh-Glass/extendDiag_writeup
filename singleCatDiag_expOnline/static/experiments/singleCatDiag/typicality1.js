var typicality = {

    start: function(params, next) {
        params['results'].push(['trial','block','stimId','category','response','rt'])

        /*   initialize   */
        space = oCanvas.create({
            canvas: typicality.initCanvas(),
            background: 'rgba(190,190,190,1)',
            // origin: { x: "center", y: "center" },
        })
        typicality.initElements(params)
        typicality.initDebugWindow(params)
        space.scenes.load('debug')


        x = new Date().getTime()
        rt = 0
        response = null
        trial = 0
        block = 0
        block_order = typicality.generateBlockOrder(params['objects'], params['labels']) // <-- initialize the first block order (you'll do this every block)

        correctCategory = block_order[trial][1]
        typicality.initStim(block_order[trial][0])
        space.scenes.load('slider')
        space.scenes.load('continue')


        /*   define event logic   */
        continueBtn.bind('click tap', function () {
            rt = new Date().getTime() - x
            // response = typicality.getResponse()
     
            space.scenes.unload('slider')
            space.scenes.unload('continue')
            stimulus.remove()

            params['results'].push([trial, block, block_order[trial][0].split('/').slice(-1)[0].split('.')[0], correctCategory, response, rt])

            trial += 1
            if (trial == block_order.length) {
                trial = 0
                block += 1
                if (block == params['n_blocks']) {
                    space.destroy(space)
                    document.getElementById('main').innerHTML = ''
                    next()
                } else {
                    block_order = typicality.generateBlockOrder(params['objects'], params['labels'])
                }
            }

            setTimeout( function () {
                space.scenes.load('slider')
                space.scenes.load('continue')
                typicality.initStim(block_order[trial][0])
                correctCategory = block_order[trial][1]
                x = new Date().getTime()
            }, 200)

        })

        console.log('started typicality')
    },


    initElements: function (params) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        /*   Response Phase of Trial   */
        // typicality slider

        slider = space.display.rectangle({
            x: 600,
            y: 500,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 800,
            height: 4,
            fill: "#000000",
            stroke: "2px black",
            join: "round",
        })
        slider_min = - slider.width / 2
        slider_max = slider.width / 2

        // divider      
        ball = space.display.ellipse({
            x: 0,
            y: 0,
            radius: 30,
            origin: { x: "center", y: "center" }, align: 'center',
            fill: "#000000",
        })
        slider.addChild(ball)


        ball.dragAndDrop({
            changeZindex: true,
            move: function () {
                this.y = 0
                if (this.x < slider_min) {
                    this.x = slider_min
                } else if (this.x > slider_max) {
                    this.x = slider_max
                }
                if (params['sliderBins'] != null) {
                    this.x = (Math.round(((this.x + (slider.width / 2)) / slider.width) * params['sliderBins']) / params['sliderBins']) * slider.width - (slider.width/2)
                }
            },
        })

        for (bin of [...Array(params['sliderBins']+1).keys()]) {
            slider.addChild(
                space.display.text({
                    x: (bin / params['sliderBins']) * slider.width - (slider.width/2),
                    y: -45,
                    origin: { x: "center", y: "center" }, align: 'center',
                    align: "center",
                    font: "bold 25px sans-serif",
                    text: params['binLabels'][bin],
                    fill: "rgba(0,0,0,1)",
                    zIndex: "front",
                })
            )
        }



        instructionsTxt = space.display.text({
            x: centerX,
            y: centerY + 80,
            origin: { x: "center", y: "center" }, align: 'center',
            align: "center",
            font: "bold 25px sans-serif",
            text: "How typical is this item as a member of its category?",
            fill: "rgba(0,0,0,1)",
            zIndex: "front",
        })

        space.scenes.create('slider', function () {
            this.add(slider)
            this.add(instructionsTxt)
        })


        /*   Continue Button   */
        continueBtn = space.display.rectangle({
            x: cx,
            y: cy + 270,
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
                // zIndex: "front",
            })
        )
        space.scenes.create('continue', function () {
            this.add(continueBtn)
        })
    },


    initStim: function (image) {
        centerX = space.canvasElement.width / 2
        centerY = space.canvasElement.height / 2

        stimulus = space.display.image({
            x: centerX,
            y: centerY - 150,
            origin: { x: "center", y: "center" }, align: 'center',
            image: image,
        })
        space.addChild(stimulus)
    },


    generateBlockOrder: function (objects, labels) {
        let block = []
        idx = typicality.shuffle([...Array(labels.length).keys()]) // from ben @ https://stackoverflow.com/a/10050831

        for (let i of idx) {
            block.push([objects[i], labels[i]])
        }

        return block
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
                'slider val: '.concat(((ball.x + (slider.width / 2)) / slider.width) * params['sliderBins']),
                '\n',
                'data:',
                params['results'].join('\n'),
            ].join('\n')
        }).start()
    },

}