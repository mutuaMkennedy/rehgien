$(document).ready(function(){
  $(".formPhoneNumberField input").intlTelInput({
        // whether or not to allow the dropdown
        allowDropdown: true,
        // if there is just a dial code in the input: remove it on blur, and re-add it on focus
        autoHideDialCode: true,
        // add a placeholder in the input with an example number for the selected country
        autoPlaceholder: "polite",
        // modify the auto placeholder
        customPlaceholder: null,
        // append menu to specified element
        dropdownContainer: null,
        // don't display these countries
        excludeCountries: [],
        // format the input value during initialisation and on setNumber
        formatOnDisplay: true,
        // geoIp lookup function
        geoIpLookup: true,
        // inject a hidden input with this name, and on submit, populate it with the result of getNumber
        hiddenInput: "",
        // initial country
        initialCountry: "",
        // localized country names e.g. { 'de': 'Deutschland' }
        localizedCountries: null,
        // don't insert international dial codes
        nationalMode: false,
        // display only these countries
        onlyCountries: [],
        // number type to use for placeholders
        placeholderNumberType: "MOBILE",
        // the countries at the top of the list. defaults to united states and united kingdom
        preferredCountries: [],
        // display the country dial code next to the selected flag so it's not part of the typed number
        separateDialCode: false,
        // specify the path to the libphonenumber script to enable validation/formatting
        utilsScript: ""
  });
  //updates review message preview in rehgien_pro/templates/pro_reviewers
  $('.review_request_message').on('keyup', function() {
      $('#rvw_Rq_msg').html($(this).val());
  });

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
