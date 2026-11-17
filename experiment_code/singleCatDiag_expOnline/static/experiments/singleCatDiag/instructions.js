var instructions = {

    start: function(params, next) {
        // Use 'let' or 'var' to prevent overwriting global variables if this runs multiple times
        let instructions_div = document.createElement('div') 
        // Use a unique ID or class so they don't clash if multiple are on screen temporarily
        instructions_div.className = 'instructions_container' 
        document.getElementById('main').appendChild(instructions_div)

        // Generate Objects
        let continue_button = document.createElement('button')
        continue_button.id = 'continue'
        continue_button.appendChild(document.createTextNode('Next'))
        
        continue_button.addEventListener('click', function () {
            // FIX 1: Completely destroy the element instead of just emptying it
            instructions_div.remove() 
            next()
        })

        // add to DOM      
        let txt = document.createElement('p')
        txt.id = 'instructions'
        txt.innerHTML = params['text']

        instructions_div.appendChild(txt)
        instructions_div.appendChild(document.createElement('br'))
        instructions_div.appendChild(document.createElement('br'))
        instructions_div.appendChild(continue_button)

        // FIX 2: Force scroll to top immediately AFTER adding the new content.
        // We scroll both the window AND the main container just in case CSS is driving the scrollbar.
        window.scrollTo(0, 0);
        document.getElementById('main').scrollTop = 0;

        console.log('started instructions')
    }

}