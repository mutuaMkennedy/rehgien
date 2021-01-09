$(document).ready(function(){
      _helperTextTrigger.addEventListener( 'click', function(){
         _helperTextTrigger.style.color='#1100ff';
         var helperText = document.getElementById('_helperText');
          helperText.style.display= 'flex';
          helperText.style.transform= 'translateY(5px)';
       });
       _helperTextHide.addEventListener( 'click', function(){
         _helperTextTrigger.style.color='#000';
          var helperText = document.getElementById('_helperText');
          helperText.style.display= "none";
          helperText.style.transform= 'translateY(0px)';
        });
});
