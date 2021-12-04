
setTimeout(function filter_words() {

    document.querySelector(".allfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            elms[i].style.display = "initial";
        }; 
    }); 
    
    document.querySelector(".nounfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[1] != "noun") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 

    document.querySelector(".adjfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[1] != "adj") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 

    document.querySelector(".verbfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[1] != "verb") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 
    
    document.querySelector(".phrverbfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[1] != "phrverb") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    });     
    
    document.querySelector(".undeffilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[1] != "undef") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    });     

   

},25);


setTimeout(function length_words() {
    document.querySelector(".nounx").innerHTML = document.querySelectorAll(".noun").length;
    document.querySelector(".adjx").innerHTML = document.querySelectorAll(".adj").length;
    document.querySelector(".verbx").innerHTML = document.querySelectorAll(".verb").length;
    document.querySelector(".phrverbx").innerHTML = document.querySelectorAll(".phrverb").length;
    document.querySelector(".undefx").innerHTML = document.querySelectorAll(".undef").length;
},25)


setTimeout(function filter_oxford() {

    // document.querySelector(".allfilter").addEventListener("click", function(){
    //     elms = document.querySelectorAll("p");
    //     for (const i in elms) {
    //         elms[i].style.display = "initial";
    //     }; 
    // }); 
    
    document.querySelector(".a1filter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "a1") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 

    document.querySelector(".a2filter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "a2") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 

    document.querySelector(".b1filter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "b1") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    }); 
    
    document.querySelector(".b2filter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "b2") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    });     
    
    document.querySelector(".c1filter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "c1") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    });     

    document.querySelector(".ptherfilter").addEventListener("click", function(){
        elms = document.querySelectorAll(".word");
        for (const i in elms) {
            if (elms[i].classList[2] != "other") {
                elms[i].style.display = "none";
            }
            else{
                elms[i].style.display = "initial";
            }
        }; 
    });     

    document.querySelector(".alllevelfilter").addEventListener("click", function(){
        elms = document.querySelectorAll("p");
        for (const i in elms) {
            elms[i].style.display = "initial";
        }; 
    }); 



},25);


setTimeout(function length_oxford() {
    document.querySelector(".a1x").innerHTML = document.querySelectorAll(".a1").length;
    document.querySelector(".a2x").innerHTML = document.querySelectorAll(".a2").length;
    document.querySelector(".b1x").innerHTML = document.querySelectorAll(".b1").length;
    document.querySelector(".b2x").innerHTML = document.querySelectorAll(".b2").length;
    document.querySelector(".c1x").innerHTML = document.querySelectorAll(".c1").length;
    document.querySelector(".otherx").innerHTML = document.querySelectorAll(".other").length;
},25)

