//carousel slider
$(document).ready(function(){
  $('.carousel.carousel-slider').carousel({
     fullWidth: true,
     indicators: true,
   });
   //function for next slide button
   $('.next').click(function(){
     $('.carousel').carousel('next');
   });
   //function for previous slide button
   $('.prev').click(function(){
     $('.carousel').carousel('prev');
   });
});

// document.addEventListener('DOMContentLoaded', function() {
//    var elems = document.querySelectorAll('.fixed-action-btn');
//    var instances = M.FloatingActionButton.init(elems, {
//      direction: 'left',
//      hoverEnabled: false,
//    });
//  });

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems, {
    coverTrigger:false,
    closeOnClick:false,
    inDuration:500,
    outDuration:500,
  });
});

//preloader

// window.onload=function(){
//   document.getElementById("preloader-animation").style.display="none";
// }
