var ready = {

    start: function(params, next) {
        var space = oCanvas.create({
            canvas: ready.initCanvas(),
            background: 'rgba(190,190,190,1)',
        })

        cx = space.canvasElement.width / 2
        cy = space.canvasElement.height / 2

        // Continue Button
        go = space.display.rectangle({
            x: cx + 100,
            y: cy + 50,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })

        go.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Start",
                fill: "rgba(255,255,255,1)",
                // zIndex: "front",
            })
        )
        space.addChild(go)


        // Back Button
        back = space.display.rectangle({
            x: cx - 100,
            y: cy + 50,
            origin: { x: "center", y: "center" }, align: 'center',
            width: 160,
            height: 60,
            fill: "#079",
            stroke: "10px #079",
            join: "round",
        })

        back.addChild(
            space.display.text({
                x: 0,
                y: 0,
                origin: { x: "center", y: "center" }, align: 'center',
                align: "center",
                font: "bold 25px sans-serif",
                text: "Go Back",
                fill: "rgba(255,255,255,1)",
                // zIndex: "front",
            })
        )
        space.addChild(back)

        readytxt = space.display.text({
            x: cx,
            y: cy - 150,
            origin: { x: "center", y: "top" },
            font: "bold 30px sans-serif",
            text: "Ready?",
            fill: "#000000"
        })
        space.addChild(readytxt)


        // Event Logic
        go.bind('click tap', function () {
            space.destroy(space)
            document.getElementById('main').innerHTML = ''
            next()
        })

        back.bind('click tap', function () {
            // document.getElementById('main').removeChild(canvas)
            space.destroy(space)
            document.getElementById('main').innerHTML = ''
            params['previous_event']()
        })

        console.log('started ready')
    },

    initCanvas: function () {
        canvas = document.createElement('canvas')// , {id: 'canvas', style: 'position:absolute;'})
        canvas.id = 'c'
        canvas.style = 'position:absolute;'
        document.getElementById('main').appendChild(canvas)
        
        var ctx = canvas.getContext('2d');
        ctx.canvas.width  = window.innerWidth - 20;
        ctx.canvas.height = window.innerHeight - 20;

        return canvas
    },

}