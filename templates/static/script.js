

setTimeout(function displayFunc() {
    wordcount = document.querySelectorAll('.word').length
    wordsec = document.querySelector('.wordsec')
    
    wordsec.style.display = "grid";
    wordsec.style.gridTemplateColumns = "repeat(2, minmax(175px, 1fr))";
    wordsec.style.gridTemplateRows = "repeat("+Math.round(wordcount/2)+",50px)";
    wordsec.style.gridGap = "2rem";

    console.log("***Hello! There!***")
},25);

