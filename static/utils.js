// ====== BARD     =======

let results = [];
let currentDid = 0;
let buttons = document.querySelectorAll('button');
let sections = document.querySelectorAll('[id^="section_"]');

function vote_click(who = 0) {
  if (who > -1){
      results.push(options_order[who]);  // vote for option 1 or 2
  } else {
      results.push(who);  // skip
  }
  currentDid++;
  showNextSection();
}

// Hide all sections.
function hide_all_sections() {
    for (const section of sections) {
      section.hidden = true;
    }
}

// Show the next section.
function showNextSection() {
  if (currentDid < dids.length - 1) {
    hide_all_sections()
    document.getElementById('section_' + dids[currentDid]).hidden = false;
  } else {
    // Hide the Skip button.
    buttons[3].hidden = true;
  }
  updateCounter();
}

// Show the previous section.
function showPreviousSection() {
  if (currentDid > 0) {
    hide_all_sections()
    document.getElementById('section_' + dids[currentDid]).hidden = false;
  } else {
    // Hide the Back button.
    buttons[0].hidden = true;
  }
  updateCounter();
}

function submit_rlhf(){
    fetch('/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
        console.log(data);
        }
    });
    dids_used = get_dids_with_merge();
    setCookie(JSON.stringify(dids_used));
}

function get_dids_with_merge() {
    let dids_used = getCookie('dids_used') || '[]';
    dids_used = JSON.parse(dids_used);
    return dids_used.concat(dids);
}

function is_none(variable){
    return [null, undefined].includes(variable);
}

// --- chatGPT

// Function to update counter
function updateCounter() {
  // Get the counter element
  const counterDiv = document.getElementById('counterDiv');

  // Update the counter value
  counterDiv.innerHTML = `Screen ${currentDid+1} of: ${dids.length]}`;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
// const username = getCookie('username');

// Setting a cookie for 7 days
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// setCookie('username', 'JohnDoe', 7);
