

// WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE 
// WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE 
// WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE 
// WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE 
// WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE // WORDTYPE 

setTimeout(function filter() {

    var filbuts = document.querySelectorAll(".filterButton");
    var words = document.querySelectorAll(".word")

    for (const key in filbuts) {
        listener = filbuts[key]
        listener.addEventListener("click",function f(e) {
            var seen = []
            let clicked = e.target.innerText.toLowerCase()
            seen.push(clicked)

            for (const key in filbuts) {
                let item = filbuts[key]
                try {
                    if (item.classList.contains("active") && seen.includes(item.innerText.toLowerCase())==false )  {
                        seen.push(item.innerText.toLowerCase())
                    }
                } catch (error) {
                    null
                }

                for (const key in words) {
                    let wording = words[key]
                    
                    if (seen.length===2) {
                        if ( wording.classList.contains(seen[0]) && wording.classList.contains(seen[1]) ) {
                            wording.style.display = "initial"
                        }
                        else{
                            wording.style.display = "none"
                        }
                    }

                }
    
            }

        })
    }





}, 1000);





// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 
// tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js // tabs.js 




$(function() {
    $('.tabs-nav a').click(function() {
  
      // Check for active
      $('.tabs-nav a').removeClass('active');
      $(this).parent().addClass('active');
  
      // Display active tab
      let currentTab = $(this).attr('href');
      $('.tabs-content div').hide();
      $(currentTab).show();
  
      return false;
    });
  });
  
  
  setTimeout(function upload_tabs() {
    textarea = document.querySelector(".textarea");
    uploadfile = document.querySelector(".uploadfile");
    
    document.querySelector(".textarea").addEventListener("click", function(){
        textarea.classList.add("active");
        uploadfile.classList.remove("active");
    }); 
    
    document.querySelector(".uploadfile").addEventListener("click", function(){
        textarea.classList.remove("active");
        uploadfile.classList.add("active");
    }); 
  },25);


  setTimeout(function oxford_tabs() {
    a1 = document.querySelector(".a1filter");
    a2 = document.querySelector(".a2filter");
    b1 = document.querySelector(".b1filter");
    b2 = document.querySelector(".b2filter");
    c1 = document.querySelector(".c1filter");
    other = document.querySelector(".otherfilter");
    allev = document.querySelector(".alllevelfilter");
    
    document.querySelector(".a1filter").addEventListener("click", function(){
      a1.classList.add("active");
      a2.classList.remove("active");
      b1.classList.remove("active");
      b2.classList.remove("active");
      c1.classList.remove("active");
      other.classList.remove("active");
      allev.classList.remove("active");
    }); 
    
    document.querySelector(".a2filter").addEventListener("click", function(){
      a1.classList.remove("active");
      a2.classList.add("active");
      b1.classList.remove("active");
      b2.classList.remove("active");
      c1.classList.remove("active");
      other.classList.remove("active");
      allev.classList.remove("active");
    }); 
  
    document.querySelector(".b1filter").addEventListener("click", function(){
      a1.classList.remove("active");
      a2.classList.remove("active");
      b1.classList.add("active");
      b2.classList.remove("active");
      c1.classList.remove("active");
      other.classList.remove("active");
      allev.classList.remove("active");
    }); 
  
    document.querySelector(".b2filter").addEventListener("click", function(){
      a1.classList.remove("active");
      a2.classList.remove("active");
      b1.classList.remove("active");
      b2.classList.add("active");
      c1.classList.remove("active");
      other.classList.remove("active");
      allev.classList.remove("active");
    }); 
  
    document.querySelector(".c1filter").addEventListener("click", function(){
      a1.classList.remove("active");
      a2.classList.remove("active");
      b1.classList.remove("active");
      b2.classList.remove("active");
      c1.classList.add("active");
      other.classList.remove("active");
      allev.classList.remove("active");
    });   

    document.querySelector(".otherfilter").addEventListener("click", function(){
        a1.classList.remove("active");
        a2.classList.remove("active");
        b1.classList.remove("active");
        b2.classList.remove("active");
        c1.classList.remove("active");
        other.classList.add("active");
        allev.classList.remove("active");
    });      
    
    document.querySelector(".alllevelfilter").addEventListener("click", function(){
      a1.classList.remove("active");
      a2.classList.remove("active");
      b1.classList.remove("active");
      b2.classList.remove("active");
      c1.classList.remove("active");
      other.classList.remove("active");
      allev.classList.add("active");
    });   
          
  },25);
  
  
setTimeout(function wordtype_tabs() {
    a1x = document.querySelector(".allfilter");
    a2x = document.querySelector(".nounfilter");
    b1x = document.querySelector(".adjfilter");
    b2x = document.querySelector(".verbfilter");
    c1x = document.querySelector(".phrverbfilter");
    c2x = document.querySelector(".undeffilter");


    document.querySelector(".allfilter").addEventListener("click", function(){
        a1x.classList.add("active");
        a2x.classList.remove("active");
        b1x.classList.remove("active");
        b2x.classList.remove("active");
        c1x.classList.remove("active");
        c2x.classList.remove("active");
    }); 


    document.querySelector(".nounfilter").addEventListener("click", function(){
        a1x.classList.remove("active");
        a2x.classList.add("active");
        b1x.classList.remove("active");
        b2x.classList.remove("active");
        c1x.classList.remove("active");
        c2x.classList.remove("active");
    }); 

    document.querySelector(".adjfilter").addEventListener("click", function(){
        a1x.classList.remove("active");
        a2x.classList.remove("active");
        b1x.classList.add("active");
        b2x.classList.remove("active");
        c1x.classList.remove("active");
        c2x.classList.remove("active");
    }); 

    document.querySelector(".verbfilter").addEventListener("click", function(){
        a1x.classList.remove("active");
        a2x.classList.remove("active");
        b1x.classList.remove("active");
        b2x.classList.add("active");
        c1x.classList.remove("active");
        c2x.classList.remove("active");
    }); 

    document.querySelector(".phrverbfilter").addEventListener("click", function(){
        a1x.classList.remove("active");
        a2x.classList.remove("active");
        b1x.classList.remove("active");
        b2x.classList.remove("active");
        c1x.classList.add("active");
        c2x.classList.remove("active");
    }); 

    document.querySelector(".undeffilter").addEventListener("click", function(){
        a1x.classList.remove("active");
        a2x.classList.remove("active");
        b1x.classList.remove("active");
        b2x.classList.remove("active");
        c1x.classList.remove("active");
        c2x.classList.add("active");
    });   
    
},25);