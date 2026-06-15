const langButton = document.getElementById("language");

function optionSelect() {
    langButton.classList.toggle('highlight')
}

/* const botaoTema = document.getElementById("data-theme");

if (botaoTema.classList.contains("light")) {
    botaoTema.textContent = "🌙";
} else {
    botaoTema.textContent = "☀️";
}

botaoTema.addEventListener("click", () => {
    if (botaoTema.classList.contains("light")) {
        botaoTema.classList.remove("light");
        botaoTema.classList.add("dark");
        botaoTema.textContent = "☀️";
    } else {
        botaoTema.classList.remove("dark");
        botaoTema.classList.add("light");
        botaoTema.textContent = "🌙";
    }
}) */