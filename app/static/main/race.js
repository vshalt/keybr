import words from './words.js';

// variable definitions
const WORD_LEN = words.length;
var text = [];
var seconds = 60;
var counter = 60;
var len = 100;
var correctWords = 0;
var wrongWords = 0;
var wpm = 0;
var accuracy = 0;
var typingSpeed = 0;
var i = -1;
var j = 0;
var allchars = 0;
let typer = document.getElementById('typer');
let timer = document.getElementById('timer');
let retry_btn = document.getElementById('retry');
let content = document.getElementById('content');

// variable configs
typer.value = "";
retry_btn.setAttribute('disabled', true)
content.value = "";

if (time == 1){
    seconds = 60;
    counter = 60;
    len=100;
}else if (time == 2){
    seconds = 120;
    counter = 120;
    len = 200;
}

// functions
for (let z=0; z < len; z += 1) {
    text.push(words[Math.floor(Math.random() * WORD_LEN)])
}
for (let z=0; z < text.length; z += 1){
    content.innerHTML += `<span id="w${z}">${text[z]} </span>`;
}

typer.addEventListener('keyup', function(event) {
    retry_btn.removeAttribute('disabled');
    decrementTime();
}, {once: true});

typer.addEventListener('keypress', (event) => {
    if (event.keyCode == 13 || event.keyCode == 32) {
        event.preventDefault();
        ++i;
        let word = typer.value;
        typer.value = "";
        if (text[i] === word) {
            document.getElementById('w'+ i).style.color = '#00c606';
            correctWords += 1;
            allchars += word.length;
        } else {
            document.getElementById('w' + i).style.color = '#e50000';
            wrongWords += 1;
        }
    }});

retry_btn.addEventListener('click', () => {window.location.reload('true')});

function decrementTime() {
    seconds --;
    timer.innerHTML = seconds.toString();
    if (seconds > 0) {
        setTimeout(decrementTime, 1000);
    }
    if (seconds === 0) {
        typer.setAttribute('disabled', true);
        typer.remove();
        if (wrongWords === 0) {
            accuracy = 100;
        } else {
            accuracy = Math.round(
                (correctWords / (correctWords + wrongWords)) * 10000)/ 100;
        }
        wpm = allchars/5; 
        typingSpeed = Math.ceil(wpm) + wrongWords / (counter/60);
        content.innerHTML = `
<h3>Correct Words: ${correctWords}</h3>
<h3>Accuracy: ${Math.round(accuracy, 2)}</h3>
<h3>WPM: ${wpm}</h3>
<h3>Typing Speed: ${typingSpeed}`;
    let points = correctWords * 2;
    if (is_user == 1) {
        const POST_URL = '/post-race';
        const xhr = new XMLHttpRequest();
        const data = new FormData();
        data.append('points', points);
        data.append('username', username.toString());
        xhr.open('POST', POST_URL);
        xhr.send(data);
    // TODO: send data from js to backend 
    }
    }
}

