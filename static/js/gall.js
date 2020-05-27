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

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems, {
    coverTrigger:false,
    closeOnClick:false,
    inDuration:500,
    outDuration:500,
  });
});

$(document).ready(function(){
   $('.fixed-action-btn').floatingActionButton();
 });

 $(document).ready(function(){
    $('.datepicker').datepicker({
      format:'yyyy-mm-dd',
    });
  });

  $(document).ready(function(){
    $('.collapsible').collapsible();
  });
