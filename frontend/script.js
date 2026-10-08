console.log("Javascript ce stamo?");

let nome = "Alessandro";
const eta = 21;

const titolo = document.getElementById("titolo");
titolo.textContent = "Titolo modificato con JavaScript!"

const bottone = document.getElementById("bottone");

bottone.addEventListener("click", function () {

    if (titolo.textContent === "Hai premuto il bottone") {
        titolo.textContent = "Benvenuto nel mio sito";
        bottone.style.background = "orange";
    } else {
        titolo.textContent = "Hai premuto il bottone";
        bottone.style.background = "blue";
    }
});

const inputNome = document.getElementById("nome");
const inputEta = document.getElementById("eta")
const bottoneinvio = document.getElementById("invio")
const paragrafo = document.getElementById("paragrafo");
bottoneinvio.addEventListener("click", function () {

    if (inputNome.value === "") {
        paragrafo.textContent = "INSERISCI IL NOME";
    }

    else if (inputEta.value >= 18) {
        paragrafo.textContent =
            "Ciao " + inputNome.value + ", sei maggiorenne e hai: " + inputEta.value + " anni";
    }

    else {
        paragrafo.textContent =
            "Ciao " + inputNome.value + ", sei minorenne e hai: " + inputEta.value + " anni";
    }

});
