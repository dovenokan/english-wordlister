


window.onload = function () {
  document.getElementById("download")
      .addEventListener("click", () => {
          const sectopdf = this.document.querySelector(".wordsec");
          console.log(sectopdf);
          console.log(window);
          var opt = {
              margin: 0.2,
              filename: 'myfile.pdf',
              image: { type: 'png', quality: 0.98 },
              html2canvas: { scale: 2 },
              jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
          };
          html2pdf().from(sectopdf).set(opt).save();
      })
}




// function getPDF() {
//     var doc = new jsPDF();
   
//     // We'll make our own renderer to skip this editor
//     var specialElementHandlers = {
//       '#download': function(element, renderer){
//         return true;
//       },
//       '.controls': function(element, renderer){
//         return true;
//       }
//     };
  
//     // All units are in the set measurement for the document
//     // This can be changed to "pt" (points), "mm" (Default), "cm", "in"
//     doc.fromHTML($('.wordsec').get(0), 0, 0, {
//       'width': 170, 
//       'elementHandlers': specialElementHandlers
//     });
  
//     doc.save('wordlist_ready.pdf');
//   }
  
// setTimeout(function generate_pdf() {
//     document.querySelector("#download").addEventListener("click", function(){
//       getPDF();
//   });  
// },25);









// function stephanraab() {
//     var doc = new jsPDF();
    
//     // We'll make our own renderer to skip this editor
//     var specialElementHandlers = {
//         '#hidden': function(element, renderer){
//             return true;
//         }
//     };
    
//     // All units are in the set measurement for the document
//     // This can be changed to "pt" (points), "mm" (Default), "cm", "in"
//     doc.fromHTML($('.wordsec').get(0), 15, 15, {
//         'width': 170, 
//         'elementHandlers': specialElementHandlers
//     });
//       doc.save('v3_wordlist.pdf');
//     }
    

// setTimeout(function v3() {
//     document.querySelector("#download").addEventListener("click", function(){
//         stephanraab();
//   });  
// },25);


