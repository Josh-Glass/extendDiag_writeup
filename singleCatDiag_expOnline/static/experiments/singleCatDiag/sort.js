var sort = {

    start: function(params, next) {
        
        params['results'].push(['stim','x','y','assignment','div'])

        /*   initialize   */
        var space = oCanvas.create({
            canvas: sort.initCanvas(),
            background: 'rgba(190,190,190,1)',
        })
        sort.initListeners(space)

        x = new Date().getTime()


        /*   make objects   */
        cx = space.canvasElement.width / 2
        cy = space.canvasElement.height / 2
        divX = cx + 180

        stim = sort.initStim(space, params)
        continue_box = sort.initContinueBox(space)
        warning_box = sort.initWarningBox(space)

        sortMess = space.display.text({
            x: cx,
            y: cy + 150,
            origin: { x: "center", y: "top" }, align: 'center',
            font: "bold 30px sans-serif",
            text: 'Sort these objects into 2 groups.\nClick finished when done',
            fill: "black",
        })
        space.addChild(sortMess)

        finished = space.display.rectangle({
            x: cx + 200,
            y: cy + 280,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })
        finished.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Finished",
                fill: "rgba(255,255,255,1)",
                zIndex: "front",
            })
        )
        space.addChild(finished)


        reset = space.display.rectangle({
            x: cx - 200,
            y: cy + 280,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })
        reset.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Reset",
                fill: "rgba(255,255,255,1)",
                zIndex: "front",
            })
        )
        space.addChild(reset)


        background = space.display.rectangle({
            x: divX,
            y: cy - 80,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 800,
            height: 450,
            fill: "white",
            stroke: "2px black",
            join: "round",
        })

        // divider      
        background.addChild(
            space.display.rectangle({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                width: 4,
                height: 450,
                fill: "#000000",
                // stroke: "10px #079",
                // join: "round",
                // zIndex: 1
            })
        )

        space.addChild(background)


        /*   Event Logic   */
        finished.bind('click tap', function () {
            
            // nudge away from center line
            for (s of stim) {
                if ((s.x < divX + 100) && (s.x > divX)) {
                    s.move(100,0)
                } else if ((s.x > divX - 100) && (s.x < divX)) {
                    s.move(-100,0)
                }
            }

            // check to make sure in box
            bad_stim = 0
            for (s of stim) {
                if ( (s.x < (background.x-(background.width/2))) || (s.x > (background.x+(background.width/2))) || (s.y > (background.y+(background.height/2))) || (s.y < (background.y-(background.height/2)))) {
                    bad_stim += 1
                } 
            }

            if (bad_stim > 0) {
                space.scenes.load('warning')
            } else {
                space.scenes.load('continue_check')
            }
            // space.redraw()
        })

        reset.bind('click tap', function () {
            space.scenes.unload('continue_check')
            space.scenes.unload('warning')
            sort.reinitStim(space, params, stim)
        })

        continue_box.yes.bind('click tap', function () {
            for (s of stim) {
                if (s.x > divX) {
                    assignment = 1
                } else {
                    assignment = 0
                }
                params['results'].push(
                    [s.image, s.x, s.y, assignment, divX]
                )
            }

            space.destroy(space)
            document.getElementById('main').innerHTML = ''
            next()
        })

        continue_box.no.bind('click tap', function () {
            space.scenes.unload('continue_check')
        })

        warning_box.ok.bind('click tap', function () {
            space.scenes.unload('warning')
        })

        console.log('started sort')
    },


    initCanvas: function () {
        canvas = document.createElement('canvas', {id: 'canvas', style: 'position:absolute;'})
        document.getElementById('main').appendChild(canvas)
        
        var ctx = canvas.getContext('2d');
        // ctx.lineWidth = 2;
        ctx.canvas.width  = window.innerWidth - 20;
        ctx.canvas.height = window.innerHeight - 20;

        return canvas
    },


    initStim: function (space, params) {
        cx = space.canvasElement.width / 2
        cy = space.canvasElement.height / 2

        stim = []

        yv = -200
        xv = -300
        flip = 1
        for (im of sort.shuffle(params['objects'])) {
            ob = space.display.image({
                x: cx + xv,
                y: cy + yv,
                origin: { x: "center", y: "center" }, align: 'center',
                image: im,
                width: 150, height: 150,
            })
            ob.dragAndDrop({
                changeZindex: true,
                start: function () {
                    space.scenes.unload('continue_check'); space.scenes.unload('warning')
                },
            })
            space.addChild(ob)
            stim.push(ob)
            yv += 150
            xv -= flip * 200
            flip *= -1
        }

        return stim
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

    reinitStim: function (space, params) {
        cx = space.canvasElement.width / 2
        cy = space.canvasElement.height / 2

        for (stim of stim) {
            space.removeChild(stim)
        }

        stim = []

        yv = -200
        xv = -300
        flip = 1
        for (im of sort.shuffle(params['objects'])) {
            ob = space.display.image({
                x: cx + xv,
                y: cy + yv,
                origin: { x: "center", y: "center" }, align: 'center',
                image: im,
                width: 150, height: 150,
            })
            ob.dragAndDrop({
                changeZindex: true,
                start: function () {
                    space.scenes.unload('continue_check'); space.scenes.unload('warning')
                },
            })
            space.addChild(ob)
            stim.push(ob)
            yv += 150
            xv -= flip * 200
            flip *= -1
        }

        return stim
    },


    initListeners: function (space) {
        window.addEventListener('resize', function () {
            space.width = window.innerWidth - 20;
            space.height = window.innerHeight - 20;
        }, false);
    },

    initContinueBox: function (space) {
        box = {}

        box.frame = space.display.rectangle({
            x: cx,
            y: cy,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 800,
            height:400,
            fill: "rgb(190,190,190)",
            stroke: "10px #079",
            join: "round",
        })

        box.yes = space.display.rectangle({
            x: 100,
            y: 50,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#000000",
            stroke: "10px #000000",
            join: "round",
        })
        box.yes.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Yes",
                fill: "#ffffff",
                zIndex: "front",
            })
        )
        box.frame.addChild(box.yes)

        box.no = space.display.rectangle({
            x: -100,
            y: 50,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#000000",
            stroke: "10px #000000",
            join: "round",
        })
        box.no.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "No",
                fill: "#ffffff",
                zIndex: "front",
            })
        )
        box.frame.addChild(box.no)

        box.frame.addChild(
            space.display.text({
                x: 0,
                y: -100,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Are you happy with your selection? Click Yes to Continue...",
                fill: "#000000",
                zIndex: "front",
            }) 
        )

        space.scenes.create('continue_check', function () {
            this.add(box.frame)
        })

        return box
    },


    initWarningBox: function (space) {
        box = {}

        box.frame = space.display.rectangle({
            x: cx,
            y: cy,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 800,
            height:400,
            fill: "rgb(190,190,190)",
            stroke: "10px #079",
            join: "round",
        })

        box.ok = space.display.rectangle({
            x: 0,
            y: 50,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#000000",
            stroke: "10px #000000",
            join: "round",
        })
        box.ok.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Ok",
                fill: "#ffffff",
                zIndex: "front",
            })
        )
        box.frame.addChild(box.ok)

        box.frame.addChild(
            space.display.text({
                x: 0,
                y: -100,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Make sure you've grouped all of the objects to continue.\n\n\nHint: they have to be inside the white box :)",
                fill: "#000000",
                zIndex: "front",
            }) 
        )

        space.scenes.create('warning', function () {
            this.add(box.frame)
        })

        return box
    }

}