var study = {

    start: function(params, next) {
        study.params = params; 
        study.params['results'].push(['trial','block','targetCategory', 'aimedTargetSize', 'aimedTargetShade', 'chosenSize', 'chosenShade', 'acc','rt'])

        block_order = study.generateBlockOrder(study.params['objects'], study.params['labels']) 
        
        study.sizeLevels = [...new Set(block_order.map(item => item[0][0]))].sort((a,b)=>a-b);
        study.shadeLevels = [...new Set(block_order.map(item => item[0][1]))].sort((a,b)=>a-b);
        
        study.sizeRange = { min: study.sizeLevels[0], max: study.sizeLevels[study.sizeLevels.length-1] };
        study.shadeRange = { min: study.shadeLevels[0], max: study.shadeLevels[study.shadeLevels.length-1] };

        space = oCanvas.create({
            canvas: study.initCanvas(),
            background: '#F8F9FA',
        })

        cx = space.canvasElement.width / 2;
        cy = space.canvasElement.height / 2;

        study.initElements()

        x = new Date().getTime();
        rt = 0; trial = 0; block = 0;
        study.lastTargetIndex = -1; 
        correctCategory = block_order[trial][1];
        
        study.initStim();
        study.resetSlidersToNonMember();
        study.updateStim();

        space.scenes.load('selection');

        /* --------------------------------------------------------- */
        /* SUBMIT BUTTON LOGIC                                       */
        /* --------------------------------------------------------- */
        submitBtn.bind('click tap', function () {
            rt = new Date().getTime() - x;
            let chosenSize = study.currentSize;
            let chosenShade = study.currentShade;

            let closestTargetIndex = -1;
            let minTargetDist = 999;

            for (let i = 0; i < block_order.length; i++) {
                let tSize = block_order[i][0][0];
                let tShade = block_order[i][0][1];
                let dist = Math.sqrt(Math.pow(chosenSize - tSize, 2) + Math.pow(chosenShade - tShade, 2));
                if (dist < minTargetDist) {
                    minTargetDist = dist;
                    closestTargetIndex = i;
                }
            }

            let isExactTarget = (minTargetDist < 0.001); 

            if (isExactTarget) {
                if (closestTargetIndex === study.lastTargetIndex) {
                    acc = false; 
                    feedbackTxt.text = 'Valid member, but try a different one than your last discovery!';
                    feedbackBtnTxt.text = "Try Again";
                } else {
                    acc = true; 
                    study.lastTargetIndex = closestTargetIndex; 
                    feedbackTxt.text = 'Success! A new ' + study.params['btnLabels'][correctCategory] + ' member found.';
                    feedbackBtnTxt.text = "Next Discovery";
                    study.captureStimAnimation(); 
                }
            } else {
                acc = false;
                feedbackTxt.text = 'Not a member. Keep searching the active ranges!';
                feedbackBtnTxt.text = "Try Again";
            }

            study.params['results'].push([trial, block, correctCategory, block_order[closestTargetIndex][0][0], block_order[closestTargetIndex][0][1], chosenSize, chosenShade, acc, rt]);
            space.scenes.unload('selection');
            space.scenes.load('feedback');
        });

feedbackBtn.bind('click tap', function () {
            if (acc === true) {
                trial += 1;
                if (trial >= block_order.length) {
                    trial = 0; block += 1;
                    if (block == study.params['n_blocks']) { 
                        
                        space.destroy(space); // Stops oCanvas
                        
                        // BULLETPROOF REMOVAL:
                        // Delete the canvas using the direct reference we saved
                        if (study.canvasEl) {
                            study.canvasEl.remove();
                        }
                        
                        window.scrollTo(0, 0);
                        document.getElementById('main').scrollTop = 0;
                        
                        next(); 
                        return; 
                    }
                }
            }
            study.resetSlidersToNonMember();
            space.scenes.unload('feedback'); 
            space.scenes.load('selection');
            study.updateStim();
            x = new Date().getTime();
        });
    },

    initElements: function () {
        let scale = Math.min(space.canvasElement.height / 800, 1);
        sliderLen = 350 * scale; 
        
        instructionsTxt = space.display.text({
            x: cx, y: cy - (360 * scale), origin: { x: "center", y: "center" },
            font: "18px sans-serif", text: `Use the slider and the dial to create items, searching the highlighted zones for members of the category.`, fill: "#666"
        });

        categoryPrompt = space.display.text({
            x: cx, y: cy - (310 * scale), origin: { x: "center", y: "center" },
            font: "bold 32px sans-serif", text: `Target: `, fill: "#000"
        });

        /* --- 1. VERTICAL SLIDER GENERATOR (SIZE) --- */
        let createVerticalSlider = (xPos, yPos, label, levels, range) => {
            let container = space.display.rectangle({ x: xPos, y: yPos, width: 40, height: sliderLen, origin: {x:"center", y:"center"}})
            
            container.addChild(space.display.rectangle({ x: 0, y: 0, width: 2, height: sliderLen, fill: "#E0E0E0", origin: {x:"center", y:"center"}}));
            let activeSize = (range.max - range.min) * sliderLen;
            let activeOffset = (range.min * sliderLen) - (sliderLen/2) + (activeSize/2);
            container.addChild(space.display.rectangle({
                x: 0, y: -activeOffset, width: 6, height: activeSize, fill: "#079", origin: {x:"center", y:"center"}
            }));

            levels.forEach(lvl => {
                let pos = (lvl * sliderLen) - (sliderLen/2);
                container.addChild(space.display.rectangle({ 
                    x: 0, y: -pos, width: 16, height: 2, fill: "#079", origin: {x:"center", y:"center"}
                }));
            });

            let lbl = space.display.text({ 
                x: 0, y: sliderLen/2 + 25, origin: {x:"center", y:"center"}, font: "bold 14px sans-serif", text: label, fill: "#333"
            });
            
            let ball = space.display.ellipse({ x: 0, y: 0, radius: 15 * scale, fill: "#FFF", stroke: "3px #079", origin: {x:"center", y:"center"}, zIndex: "front"});
            
            container.addChild(lbl); container.addChild(ball);
            return { group: container, ball, levels, range };
        }

        /* --- 2. TEXTURED ROTATING DIAL GENERATOR (SHADE) --- */
        let createDial = (xPos, yPos, label, levels, range) => {
            let container = space.display.rectangle({ x: xPos, y: yPos, width: 200 * scale, height: 200 * scale, origin: {x:"center", y:"center"}});
            let R = 75 * scale; 
            let minAngle = 135; 
            let sweep = 270;    

            // Background Track
            container.addChild(space.display.arc({
                x: 0, y: 0, radius: R, start: minAngle, end: minAngle + sweep, stroke: "3px #E0E0E0", origin: {x:"center", y:"center"}
            }));
            
            // Highlighted Active Arc Zone
            let startActive = minAngle + (range.min * sweep);
            let endActive = minAngle + (range.max * sweep);
            container.addChild(space.display.arc({
                x: 0, y: 0, radius: R, start: startActive, end: endActive, stroke: "8px #079", origin: {x:"center", y:"center"}
            }));

            // Subtle Ticks (Small dots just outside the track)
            levels.forEach(lvl => {
                let a = (minAngle + lvl * sweep) * (Math.PI / 180);
                container.addChild(space.display.ellipse({
                    x: Math.cos(a) * (R + 15 * scale),
                    y: Math.sin(a) * (R + 15 * scale),
                    radius: 2.5 * scale,
                    fill: "#AAA",
                    origin: {x:"center", y:"center"}
                }));
            });

            // The physical knob group (this whole object will rotate)
            let knobOuter = space.display.ellipse({ x: 0, y: 0, radius: 55 * scale, fill: "#EAEAEA", stroke: "1px #BBB", shadow: "0 4px 6px rgba(0,0,0,0.15)", origin: {x:"center", y:"center"}, zIndex: "front"});
            let knobInner = space.display.ellipse({ x: 0, y: 0, radius: 45 * scale, fill: "#F8F9FA", stroke: "1px #DDD", origin: {x:"center", y:"center"}});
            knobOuter.addChild(knobInner);

            // Add Grip Texture (12 dimples around the edge)
            for (let i = 0; i < 360; i += 30) {
                let rad = i * (Math.PI / 180);
                let texDot = space.display.ellipse({
                    x: Math.cos(rad) * 38 * scale,
                    y: Math.sin(rad) * 38 * scale,
                    radius: 2 * scale,
                    fill: "#C8C8C8", // Subtle gray dimple
                    origin: {x: "center", y: "center"}
                });
                knobOuter.addChild(texDot);
            }
            
            // Pointer extending from center to edge
            let pointer = space.display.line({
                start: {x: 0, y: 0},
                end: {x: 45 * scale, y: 0}, // Pointing right (0 degrees) by default
                stroke: "4px #079",
                cap: "round"
            });
            
            // Main indicator dimple (matches the pointer color)
            let mainDimple = space.display.ellipse({ x: 38 * scale, y: 0, radius: 4 * scale, fill: "#079", origin: {x:"center", y:"center"}});

            knobOuter.addChild(pointer);
            knobOuter.addChild(mainDimple);

            let lbl = space.display.text({ x: 0, y: R + 35 * scale, origin: {x:"center", y:"center"}, font: "bold 14px sans-serif", text: label, fill: "#333"});

            container.addChild(knobOuter); container.addChild(lbl);
            return { group: container, knob: knobOuter, levels, range, minAngle, sweep, currentProp: 0 };
        }

        // Initialize Controls (Dial moved up to cy + 160)
        study.sizeObj = createVerticalSlider(cx - 300 * scale, cy - 80 * scale, "SIZE", study.sizeLevels, study.sizeRange);
        study.shadeObj = createDial(cx, cy + 160 * scale, "SHADING", study.shadeLevels, study.shadeRange);

        /* --- 3. SIZE SLIDER DRAG LOGIC --- */
        study.sizeObj.ball.dragAndDrop({
            move: function () {
                this.x = 0; 
                let half = sliderLen / 2;
                let mouseRelative = space.mouse.y - study.sizeObj.group.y;
                let prop = (half - mouseRelative) / sliderLen; 
                
                if (prop < study.sizeObj.range.min) prop = study.sizeObj.range.min;
                if (prop > study.sizeObj.range.max) prop = study.sizeObj.range.max;

                let closest = study.sizeObj.levels.reduce((prev, curr) => Math.abs(curr - prop) < Math.abs(prev - prop) ? curr : prev);
                this.y = -((closest * sliderLen) - half);
                study.updateStim();
            }
        });

        /* --- 4. SHADE DIAL DRAG LOGIC (Rotates the Knob) --- */
        study.shadeObj.knob.dragAndDrop({
            move: function () {
                this.x = 0; this.y = 0; // Lock the knob position, allow only rotation
                
                let dx = space.mouse.x - study.shadeObj.group.x;
                let dy = space.mouse.y - study.shadeObj.group.y;
                
                // Calculate angle from center of dial
                let ang = Math.atan2(dy, dx) * (180 / Math.PI);
                if (ang < 90) ang += 360; // Normalize 135 to 405 range
                
                let prop = (ang - study.shadeObj.minAngle) / study.shadeObj.sweep;
                
                // Clamp to active range
                if (prop < study.shadeObj.range.min) prop = study.shadeObj.range.min;
                if (prop > study.shadeObj.range.max) prop = study.shadeObj.range.max;

                // Snap to correct level
                let closest = study.shadeObj.levels.reduce((prev, curr) => Math.abs(curr - prop) < Math.abs(prev - prop) ? curr : prev);
                study.shadeObj.currentProp = closest;
                
                // Rotate the entire physical knob
                this.rotation = study.shadeObj.minAngle + (closest * study.shadeObj.sweep);

                study.updateStim();
            }
        });

        submitBtn = space.display.rectangle({ x: cx, y: cy + 340 * scale, width: 160, height: 50, fill: "#079", radius: 5, origin: {x:"center", y:"center"}})
        submitBtn.addChild(space.display.text({ x: 0, y: 0, font: "bold 18px sans-serif", text: "CHECK", fill: "white", origin: {x:"center", y:"center"}}))

        feedbackBtn = space.display.rectangle({ x: cx, y: cy + 280 * scale, width: 200, height: 50, fill: "#28a745", radius: 5, origin: {x:"center", y:"center"}})
        feedbackBtnTxt = space.display.text({ x: 0, y: 0, font: "bold 18px sans-serif", text: "NEXT", fill: "white", origin: {x:"center", y:"center"}})
        feedbackBtn.addChild(feedbackBtnTxt);

        ghostContainer = space.display.rectangle({ x: cx + 380 * scale, y: cy - 80 * scale, width: 120, height: 160, fill: "white", stroke: "1px #DDD", radius: 8, origin: {x:"center", y:"center"}});
        ghostContainer.addChild(space.display.text({ x: 0, y: -65, font: "bold 11px sans-serif", text: "LAST DISCOVERY", fill: "#AAA", origin: {x:"center", y:"center"}}));
        ghostStim = space.display.rectangle({ x: 0, y: 10, width: 40, height: 40, fill: "rgba(0,0,0,0)", stroke: "1px #EEE", origin: {x:"center", y:"center"}});
        ghostContainer.addChild(ghostStim);

        space.scenes.create('selection', function () { 
            this.add(instructionsTxt);
            this.add(categoryPrompt); this.add(study.sizeObj.group); this.add(study.shadeObj.group); this.add(submitBtn);
            if (study.lastTargetIndex !== -1) { this.add(ghostContainer); }
        });

        feedbackTxt = space.display.text({ x: cx, y: cy + 50 * scale, font: "italic 20px Georgia, serif", text: "", fill: "#333", origin: {x:"center", y:"top"}, align: "center"});
        space.scenes.create('feedback', function () { 
            this.add(feedbackTxt); this.add(feedbackBtn); 
            if (study.lastTargetIndex !== -1) { this.add(ghostContainer); }
        });
    },

    initStim: function () {
        dynamicStim = space.display.rectangle({ x: cx, y: cy - 80, width: 80, height: 80, fill: "#888", stroke: "2px #333", origin: {x:"center", y:"center"}, zIndex: "back"});
        space.addChild(dynamicStim);
    },

    updateStim: function() {
        study.currentSize = ((-study.sizeObj.ball.y + (sliderLen/2)) / sliderLen);
        study.currentShade = study.shadeObj.currentProp;

        let d = (study.currentSize * (7.1 - 2.5) + 2.5) * (1440 / 41);
        let s = Math.round((study.currentShade * (230 - 25)) + 25);
        dynamicStim.width = d; dynamicStim.height = d;
        dynamicStim.fill = `rgb(${s}, ${s}, ${s})`;
        
        if (typeof correctCategory !== 'undefined') {
            categoryPrompt.text = `Find: ${study.params['btnLabels'][correctCategory]}`;
        }
        space.redraw();
    },

    resetSlidersToNonMember: function() {
        let valid = false;
        let s, h;
        while (!valid) {
            s = study.sizeLevels[Math.floor(Math.random() * study.sizeLevels.length)];
            h = study.shadeLevels[Math.floor(Math.random() * study.shadeLevels.length)];
            let isMember = block_order.some(item => Math.abs(item[0][0] - s) < 0.001 && Math.abs(item[0][1] - h) < 0.001);
            if (!isMember) valid = true;
        }
        
        // Reset Size Ball
        study.sizeObj.ball.y = -((s * sliderLen) - (sliderLen/2));
        
        // Reset Shade Dial 
        study.shadeObj.currentProp = h;
        study.shadeObj.knob.rotation = study.shadeObj.minAngle + (h * study.shadeObj.sweep);
    },

    captureStimAnimation: function() {
        let startWidth = dynamicStim.width;
        let endGlobalX = ghostContainer.x + ghostStim.x;
        let endGlobalY = ghostContainer.y + ghostStim.y;
        let endWidth = startWidth * 0.45;

        let flyingClone = space.display.rectangle({
            x: dynamicStim.x, y: dynamicStim.y, width: startWidth, height: startWidth, 
            fill: dynamicStim.fill, stroke: dynamicStim.stroke, origin: dynamicStim.origin, 
            opacity: 0.8, zIndex: "front"
        });
        space.addChild(flyingClone);

        flyingClone.animate({
            x: endGlobalX, y: endGlobalY, width: endWidth, height: endWidth
        }, {
            duration: 1500,
            easing: "ease-out-quint",
            callback: function() {
                this.remove(); 
                study.updateGhost(flyingClone.width, flyingClone.fill); 
            }
        });
    },

    updateGhost: function(w, f) {
        ghostStim.width = w; ghostStim.height = w; ghostStim.fill = f;
    },

    generateBlockOrder: function (o, l) {
        let b = []; let idx = study.shuffle([...Array(l.length).keys()]);
        for (let i of idx) b.push([o[i], l[i]]);
        return b;
    },

    shuffle: function (a) { 
        var m = a.length, t, i; while (m) { i = Math.floor(Math.random() * m--); t = a[m]; a[m] = a[i]; a[i] = t; } return a;
    },

initCanvas: function () {
        let canvas = document.createElement('canvas');
        canvas.id = 'canvas'; // Set ID properly
        canvas.style.position = 'absolute'; // Set style properly
        canvas.style.top = '0px';
        canvas.style.left = '0px';
        
        document.getElementById('main').appendChild(canvas);
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // Save a direct reference so we can easily delete it later
        study.canvasEl = canvas; 
        
        return canvas;
    }
};