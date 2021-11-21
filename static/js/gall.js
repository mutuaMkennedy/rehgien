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

  // show/hide helper text in business profile detail page connection list
  $('#_helperTextTrigger').on('click', function(){
    $(this).css('color','#1100ff')
    $('#_helperText').css({'display':'flex', 'transform':'translateY(5px)'});
  });

  $('#_helperTextHide').on('click', function(){
    $('#_helperTextTrigger').css('color','#000');
    $('#_helperText').css({'display':'none', 'transform':'translateY(0px)'});
  });

  const canvas = document.getElementsByClassName('HomeHerocanvas');
  if (canvas.length > 0) {
    const context = canvas[0].getContext('2d');
    let time = 0;

    const color = function (x, y, r, g, b) {
        context.fillStyle = `rgb(${r}, ${g}, ${b})`
        context.fillRect(x, y, 10, 10);
    }
    const R = function (x, y, time) {
        return (Math.floor(179 + 64 * Math.cos((x * x - y * y) / 300 + time)));
    }

    const G = function (x, y, time) {
        return (Math.floor(20 + 64 * Math.sin((x * x * Math.cos(time / 4) + y * y * Math.sin(time / 3)) / 300)));
    }

    const B = function (x, y, time) {
        return (Math.floor(185 + 64 * Math.sin(5 * Math.sin(time / 9) + ((x - 100) * (x - 100) + (y - 100) * (y - 100)) / 1100)));
    }

    const startAnimation = function () {
        for (x = 0; x <= 30; x++) {
            for (y = 0; y <= 30; y++) {
                color(x, y, R(x, y, time), G(x, y, time), B(x, y, time));
            }
        }
        time = time + 0.03;
        window.requestAnimationFrame(startAnimation);
    }

    startAnimation();
  }



});
