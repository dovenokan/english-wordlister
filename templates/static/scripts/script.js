

// setTimeout(function displayFunc() {
//     wordcount = document.querySelectorAll('.word').length
//     wordsec = document.querySelector('.wordsec')
    
//     wordsec.style.display = "grid";
//     wordsec.style.gridTemplateColumns = "repeat(2, minmax(175px, 1fr))";
//     wordsec.style.gridTemplateRows = "repeat("+Math.round(wordcount/2)+",50px)";
//     wordsec.style.gridGap = "2rem";

//     console.log("***Hello! There!***")
// },25);


// var ps = document.querySelectorAll('.word')
// for (const p in ps) {
//     const x = ps[p]
//     x.addEventListener('click', function pron(e) {
//         // var audio = new Audio('https://cdn.yourdictionary.com/audio/en/'+x.outerText.trim()+'.mp3');
//         var audio = new Audio('https://d1qx7pbj0dvboc.cloudfront.net/'+x.outerText.trim()+'.mp3');
//         audio.play();
//     })
// }