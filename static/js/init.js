(function($){
  $(function(){
    M.AutoInit();
    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown();
    $('.modal').modal();
    $('.slider').slider({
    	indicators: false,
        height: 500,
        transition:500,
        interval:6000
    });
    $('.parallax').parallax();
    $('.materialboxed').materialbox();


   // $('.autocomplete').autocomplete({
    	//data: {
    	//	"Juja": null;
    	//	"Kisumu": null;
    	//	"Machakos": null;
    	//	"Mombasa": null;
    	//	"Nairobi": null;
    	//}
   // });

  }); // end of document ready
})(jQuery); // end of jQuery name space
