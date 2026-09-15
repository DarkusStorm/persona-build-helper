const text = {
    'en-us': {
        'welcome': "Welcome to Persona Build Helper Tool!",
        'instructions': "Choose one of the games in the menu above or click the cover of the game below to check the skills, equipment and Personas (including how to obtain them) of their respective party members."
    },
    'pt-br': {
        'welcome': "Bem-vindo ao Persona Build Helper Tool!",
        'instructions': "Escolha um dos jogos no menu acima ou clique na capa do jogo abaixo para checar as habilidades, equipamentos e Personas (incluindo como obtê-los) de seus respectivos membros de equipe."
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const langSelect = document.getElementById('language');

    const savedLang = localStorage.getItem('userLanguage') || 'en-us';
    langSelect.value = savedLang;

    function translatePage() {
        const lang = langSelect.value;
        localStorage.setItem('userLanguage', lang);

        if (typeof text !== 'undefined' && text[lang]) {
            Object.keys(text[lang]).forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = text[lang][id];
                }
            });
        }
    }

    langSelect.addEventListener('change', translatePage);
    translatePage();
});