$(document).ready(function(){
      M.AutoInit();
    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown({
      coverTrigger:false,
      closeOnClick:false,
      inDuration:500,
      outDuration:500,
      belowOrigin: true,
      alignment: 'left',
      // hover: true,
      onOpenStart:function setActive() {
        $("a[data-target='" + $(this).attr('id') + "']").addClass('active');
      },
      onCloseStart:function removeActive() {
        $("a[data-target='" + $(this).attr('id') + "']").removeClass('active');
      },
    });
    $('.modal').modal();
    $('.slider').slider({
    	indicators: false,
        height: 500,
        transition:500,
        interval:6000
    });
    $('.parallax').parallax();
    $('.materialboxed').materialbox();
    $('.fixed-action-btn').floatingActionButton();
    $('.datepicker').datepicker({
     format:'yyyy-mm-dd',
   });
    $('.collapsible').collapsible();
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
      $('.tabs').tabs();
  });
