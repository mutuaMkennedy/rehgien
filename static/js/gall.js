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
   //tooltip initialization
     $('.tooltipped').tooltip();

    //custome helper text initialization
    _helperTextTrigger.addEventListener( 'click', function(){
       document.getElementById("_helperTextTrigger").style.color='#1100ff';
       var helperText = document.getElementById('_helperText');
        helperText.style.display= 'block';
        helperText.style.transform= 'translateY(5px)';
     });
     _helperTextHide.addEventListener( 'click', function(){
       document.getElementById("_helperTextTrigger").style.color='#000';
        var helperText = document.getElementById('_helperText');
        helperText.style.display= "none";
        helperText.style.transform= 'translateY(0px)';
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
