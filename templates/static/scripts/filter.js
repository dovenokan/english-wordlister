


function filter_words() {
    let oxford = document.querySelector("#oxfordfilter").value
    let type = document.querySelector("#typefilter").value
    let words = document.querySelectorAll(".word")
    
    words.forEach((w)=>{
        if (w.classList.contains(oxford) && w.classList.contains(type)) {
            w.style.display="initial"
        }else{
            w.style.display="none"
        }
    })
}

setTimeout(function length_oxford() {
    document.querySelector(".a1x").innerHTML = document.querySelectorAll(".a1").length;
    document.querySelector(".a2x").innerHTML = document.querySelectorAll(".a2").length;
    document.querySelector(".b1x").innerHTML = document.querySelectorAll(".b1").length;
    document.querySelector(".b2x").innerHTML = document.querySelectorAll(".b2").length;
    document.querySelector(".c1x").innerHTML = document.querySelectorAll(".c1").length;
    document.querySelector(".otherx").innerHTML = document.querySelectorAll(".other").length;
},25)

setTimeout(function length_type() {
    document.querySelector(".nounx").innerHTML = document.querySelectorAll(".noun").length;
    document.querySelector(".adjx").innerHTML = document.querySelectorAll(".adj").length;
    document.querySelector(".verbx").innerHTML = document.querySelectorAll(".verb").length;
    document.querySelector(".phrverbx").innerHTML = document.querySelectorAll(".phrverb").length;
    document.querySelector(".undefx").innerHTML = document.querySelectorAll(".undef").length;
},25)