// ====== BARD     =======

let results = [];
let currentDid = 0;
let buttons = document.querySelectorAll('button');
let sections = document.querySelectorAll('[id^="section_"]');

let button_back = buttons[0];
let button_vote1 = buttons[1];
let button_vote2 = buttons[2];
let button_skip = buttons[3];
let button_submit = buttons[4];

// =====buttons==========
if (currentDid < 1) {
    button_back.hidden = true;
}

if (currentDid < dids.length - 1) {
    button_submit.hidden = true;
}

button_back.hidden = true;  // simplify for now - hide back
button_skip.hidden = true;  // simplify for now - hide skip

// Handle the Vote 1 button click.
button_vote1.addEventListener('click', () => {vote_click(0)} );

// Handle the Vote 2 button click.
button_vote2.addEventListener('click', () => {vote_click(1)} );

// Handle the Skip button click.
button_skip.addEventListener('click', () => {vote_click(-1)});

// Handle the Back button click.
button_back.addEventListener('click', () => {
  currentDid--;
  showPreviousSection();
});

button_submit.addEventListener('click', () =>{
    submit_rlhf();
});
// =====end buttons======

function vote_click(who = 0) {
  if (who > -1){
      results.push(options_order[currentDid][who]);  // vote for option 1 or 2
  } else {
      results.push(who);  // skip
  }
  if (currentDid < dids.length - 1) {
      currentDid++;
      showNextSection();
  }
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
    button_skip.hidden = true;
    // Show submit button
    button_submit.hidden = false;
    button_vote1.hidden = button_vote2.hidden = true;
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
    button_back.hidden = true;
  }
  updateCounter();
}

function submit_rlhf() {
    // fetch('/vote', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(data)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.status === 'success') {
    //     console.log(data);
    //     }
    // });
    dids_used = get_dids_with_merge();
    console.log(dids_used);
    setCookie('dids_used', JSON.stringify(dids_used), 30);
    hide_all_sections();
    button_submit.hidden = true;
    const result = document.getElementById('result');
    result.innerHTML = `<h2>Thank for your time completing the RLHF!</h2>`;
    const form = document.getElementById('hor');
    form.hidden = true;
}

function get_dids_with_merge() {
    let dids_used = getCookie('dids_used') || '[]';
    dids_used = JSON.parse(dids_used);
    return dids_used.concat(dids);
}

function is_none(variable){
    // not in use
    return [null, undefined].includes(variable);
}

// --- chatGPT

// Function to update counter
function updateCounter() {
  // Get the counter element
  const counterDiv = document.getElementById('counterDiv');

  // Update the counter value
  counterDiv.innerHTML = `Screen ${currentDid+1} of: ${dids.length}`;
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
