let words = document.getElementById('text').innerText.split(" ")
let typing = document.getElementById('typing')
counter = 0
typing.addEventListener('change', checkIfCorrect(event))

if (counter == words.length) {
    // TODO: send the word count as score to the backend
}

function checkIfCorrect(event) {
    let value = event.target.value
    if (value == words[counter]) {
        counter+= 1
        event.target.value = "";
    }
}
