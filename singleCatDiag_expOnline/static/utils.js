// redirects user to the next template that's provided in the message response
async function start(name) {
    localStorage.setItem('name', name)

    // Send participant data from initial survey
    const  options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'message': 'start',
            'name': name,
        })
    }

    const resp = await fetch('/start', options)
    const data = await resp.json()
    localStorage.setItem('subject_id', data['subject_id'])
    localStorage.setItem('condition', data['condition'])
    window.location = data['message']
}



// redirects user to the next template that's provided in the message response
async function next(experiment, subject_id, condition, results) {
    console.log('experiment complete')

    // v-- ignore all that --v

    // // Send participant data from initial survey
    // const  options = {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         'message': 'next',
    //         'subject_id': localStorage.getItem('subject_id'),
    //         'condition': condition,
    //         'experiment': experiment,
    //         'results': results,
    //         'name': localStorage.getItem('name')
    //     })
    // }

    // const resp = await fetch('/next', options)
    // const data = await resp.json()
    // console.log(data['condition'])
    // localStorage.setItem('subject_id', data['subject_id'])
    // localStorage.setItem('condition', data['condition'])
    // localStorage.setItem('check',data['check'])
    // window.location = data['message']
}



// You'll need these in your experiment script
function get_subject_id() {
    return 123 // <-- this is a test
}
function get_condition() {
    return 1 // <-- this is also just a test
}



// return debriefing forms for relevant experiment
async function debriefing() {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'message': 'debrief',
            'subject_id': localStorage.getItem('subject_id'),
            'check': localStorage.getItem('check'),
        })
    }
    const resp = await fetch('/debriefing', options)
    const data = await resp.json()
    // console.log(data)
    // data = {'message': 'recieved', 'debriefing_forms': {'basicExp2': 'This is the <b>briefing</b> form for a project', 'transl1': 'This is the other debriefing form for a project', 'transl2': 'This is the other debriefing form for a project', 'basicExp': 'This is the other debriefing form for a project'}}
    return data
}




function viewData(data, filename = 'experiment_data.json') {
    // 1. Check if the data is already a string, if not, stringify it nicely
    const jsonString = typeof data === 'string' ? data : JSON.stringify(data, null, 2); 
    
    // 2. Create a Blob (Binary Large Object) to hold the data
    const blob = new Blob([jsonString], { type: "application/json" });
    
    // 3. Create a temporary URL for the Blob
    const url = URL.createObjectURL(blob);
    
    // 4. Create an invisible anchor tag to trigger the download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    
    // 5. Append it to the document, click it, and clean up
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}








function structureData(rawResults) {
    let structuredResults = {};
    
    // Loop through study, trainPhase, testPhase, typicality
    for (let phase in rawResults) {
        let data = rawResults[phase];
        
        // If the phase is empty (like your trainPhase), just pass an empty array
        if (data.length === 0) {
            structuredResults[phase] = [];
            continue;
        }
        
        // Grab the first row to use as our keys (e.g., "trial", "block", "stimId")
        let keys = data[0];
        let formattedPhase = [];
        
        // Loop through the actual data rows (starting at index 1)
        for (let i = 1; i < data.length; i++) {
            let trialObj = {};
            for (let j = 0; j < keys.length; j++) {
                trialObj[keys[j]] = data[i][j];
            }
            formattedPhase.push(trialObj);
        }
        
        structuredResults[phase] = formattedPhase;
    }
    
    return structuredResults;
}