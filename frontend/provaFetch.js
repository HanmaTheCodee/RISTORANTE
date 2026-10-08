const piatti = [

    {
        nome: "Carbonara",
        prezzo: 12
    },
    {
        nome: "Margherita",
        prezzo: 8
    },
    {
        nome: "Hamburger",
        prezzo: 15
    },
    {
        nome: "Amatriciana",
        prezzo: 11
    }
]


const piattiEconomici = piatti.filter(function (piatto) {
    return piatto.prezzo <= 11
})

const hamburger = piatti.find(function (piatto) {
    return piatto.nome === "hamburger"
})

const nomiPiatti = piatti.map(function (piatto) {
    return piatto.nome
})

console.log(piattiEconomici)
console.log(hamburger)
console.log(nomiPiatti)


const piattiJson = JSON.stringify(piatti)

console.log("I piatti json: " + piattiJson)


const nome = document.getElementById("nome")
const eta = document.getElementById("eta")
const bottoneInvio = document.getElementById("bottone")
const colonnaNome = document.getElementById("colonnaNome")
const colonnaEta = document.getElementById("colonnaEta")




async function caricaDati() {
    try {
        //const risposta = await fetch(`http://127.0.0.1:8000/informazioni?nome=${nome.value}&eta=${eta.value}`);
        const risposta = await fetch(`http://127.0.0.1:8000/persone/1`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: nome.value,
                eta: Number(eta.value)
            })
        });
        if (!risposta.ok) {
            throw new Error("Errore HTTP: " + risposta.status);
        }

        const dato = await risposta.json();
        /*console.log(dato);
        console.log(risposta.status);
    
        console.log(dato);
        console.log("nome:", dato.nome);
        console.log("eta:", dato.eta);
        colonnaNome.textContent = dato.nome
        colonnaEta.textContent = dato.eta*/
        console.log(dato);
        console.log(risposta.status);

    } catch (errore) {
        console.log("Errore:", errore);
    }
}
bottoneInvio.addEventListener("click", function () {
    caricaDati();

})






