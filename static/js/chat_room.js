$(function() {
  // Reference to the chat messages area
  let $chatWindow = $("#messages");
  let $chatWindowInfo = $("#info-box");

  // Our interface to the Chat service
  let chatClient;

  // A handle to the room's chat channel
  let roomChannel;

  // The server will assign the client a random username - stored here
  let username;

  //get all public channels
  $.getJSON(
    "/chat/list_channels/",
    function(data) {
      // print out availlable Public channels
      var i;
      for (i = 0; i < data.length; ++i) {
          var chanelName = data[i].Name;
          $('#channelList').append(
            "<a>" +"<li>" + '# ' + chanelName + "</li>" +"</a>"
          )
      }
    }
  );

  //get all members
  $.getJSON(
    "/chat/list_members/",
    function(data) {
      var i;
      for (i = 0; i < data.length; ++i) {
          var memberName = data[i].Name;
          $('#roomMembers').append(
            "<a>" +"<li>" + '<i class="far fa-dot-circle"></i> ' + memberName + "</li>" +"</a>"
          )
      }
    }
  );

  // Helper function to print info messages to the chat window
  function print(infoMessage, asHtml) {
    let $msg = $('<div class="info">');
    if (asHtml) {
      $msg.html(infoMessage);
    } else {
      $msg.text(infoMessage);
    }
    $chatWindowInfo.append($msg);
  }

  // Helper function to print chat message to the chat window
  function printMessage(fromUser, message, timestamp) {
    var dtStr = String(timestamp);
    var sentDate = new Date(dtStr);
    var mins = ('0'+sentDate.getMinutes()).slice(-2);

    let $user = $('<div class="username">').append(
      '<div class="SnmDt">'+ '<img class="senderAvatar" src="https://images.unsplash.com/photo-1543762446-67600aab041f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=751&q=80" width="50px">'
      + '<div class="SndateF">' +'<h5>' + fromUser + '</h5>' +
      '<h6>' + sentDate + '</h6>' + '</div>' + '</div>'
      );
    if (fromUser === username) {
      $user.addClass("me");
    }
    if (message.match(/https:/)) {

      let $message = $('<img class="mediaMsg" onClick="loadPopUp()">').attr("src",message);
      let $container = $('<div class="message-container">');
      $user.append($message);
      $container.append($user);
      $chatWindow.append($container);
      $chatWindow.scrollTop($chatWindow[0].scrollHeight);
    }else {
      let $message = $('<span class="message">').text(message);
      let $container = $('<div class="message-container">');
      $user.append($message);
      $container.append($user);
      $chatWindow.append($container);
      $chatWindow.scrollTop($chatWindow[0].scrollHeight);
    }
  }

  // Get an access token for the current user, passing a device ID
  // for browser-based apps, we'll just use the value "browser"
  $.getJSON(
    "/chat/token",
    {
      device: "browser",
    },
    function(data) {
      // Alert the user they have been assigned a username
      username = data.identity;
      print(
        "You just joined as: " +
          '<span class="me">' +
          username +
          "</span>",
        true
      );

      // Initialize the Chat client
      Twilio.Chat.Client.create(data.token).then(client => {
        // Use client
        chatClient = client;
        chatClient.getSubscribedChannels().then(createOrJoinChannel);

        //Here we are accepting invitation and joining
        // Listen for new invitations to your Client
          chatClient.on('channelInvited', function(channel) {
            $('#notfCts-collapsible-body').append(
              '<div class="notifiMsg">'+'<p>'+ 'You have been added to ' +
              '<span>' + channel.uniqueName + '</span>' +' channel.'+
              '</p>'+'</div>'
            );
            // Join the channel that you were invited to
            channel.join();
          });

          // chatClient.on('joined', function(){
          //   // notifications count
          //     var notificationBody= $('#notfCts-collapsible-body');
          //     if (notificationBody.length > 0) {
          //       $('#notfCts-collapsible-header').append(
          //         '<span>' + notificationBody.length +'</span>'
          //       );
          //     } else{
          //       $('#notfCts-collapsible-body').append(
          //         '<div class="notifiMsg">'+'<p>'+ 'You have no new notifications' +
          //         '</p>'+'</div>'
          //       );
          // )};
      });
    }
  );

  // Set up channel after it has been found / created
  function setupChannel(name) {
    if(roomChannel.state.status !== "joined") {
      roomChannel.join().then(function(channel) {
        print(
          `Joined channel ${name} as <span class="me"> ${username} </span>.`,
          true
        );
      });
    }
    print(
      `Joined channel ${name} as <span class="me"> ${username} </span>.`,
      true
    );

    //creating room header
    $('.rmNm').append(
      '<h6>'+ (roomChannel.uniqueName) + '</h6>'
    )
    $('.rmMbrs').append(
      '<h6>'+ (roomChannel.members._c.size) + '</h6>'
    )
    $('.rmDescrption').append(
      '<p>'+ (roomChannel.friendlyName) + '</p>'
    )

    roomChannel.getMessages(30).then(processPage);
    // Listen for new messages sent to the channel
    roomChannel.on("messageAdded", function(message) {
      if (message.type === 'media') {
          message.media.getContentUrl().then(function(url) {
            printMessage(message.author, url, message.timestamp,);
        });
      }else {
            printMessage(message.author, message.body, message.timestamp,);
      }
    });
  }

  function processPage(page) {
    var messages = page.items;
    // console.log(page.items);
    messages.sort(function(a,b){
      // Turning strings into dates, and then subtracting them
      // to get a value that is either negative, positive, or zero.
      return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    });

    messages.forEach(message => {
        if (message.type === 'media') {
            message.media.getContentUrl().then(function(url) {
              printMessage(message.author, url,message.timestamp,);
          });
        }else {
              printMessage(message.author, message.body,message.timestamp,);
        }
    });
    if (page.hasPrevPage) {
      page.prevPage().then(processPage);
    } else {
      // console.log("Done loading messages");
    }
  }

  function createOrJoinChannel(channels) {
    // Extract the room's channel name from the page URL
    let channelName = window.location.pathname.split("/").slice(-2, -1)[0];

    print(`Attempting to join "${channelName}" chat channel...`);

    chatClient
      .getChannelByUniqueName(channelName)
      .then(function(channel) {
        roomChannel = channel;
        // console.log("Found channel:", channelName);
        setupChannel(channelName);
      })
      .catch(function() {
        // If it doesn't exist, let's create it
        chatClient
          .createChannel({
            uniqueName: channelName,
            friendlyName: `${channelName} Chat Channel`
          })
          .then(function(channel) {
            roomChannel = channel;
            setupChannel(channelName);
          });
      });

      //lists user member channels
        chatClient.getSubscribedChannels().then(function(paginator) {
          for (i = 0; i < paginator.items.length; i++) {
            const channel = paginator.items[i];
            // console.log('Channel: ' + channel.friendlyName);

          }
        });

  }



  //list all users
  $.getJSON(
    "/chat/list_users/",
    function(data) {
      var options = "";
      var i;
      var ch_usernameSelect=$("#ch_username");
      for (i = 0; i < data.length; ++i) {
          var userIDName = data[i].Name;

          ch_usernameSelect.append(buildOption(String(userIDName), String(userIDName)));

          function buildOption(value, text) {
            return $("<option/>", {
              value: value,
              text: text
            })
          }
      }

        // //initializing search select plugin
        //   $('#ch_username').selectstyle({
        //     onchange :function(val){}
        //   });

        //initializing search select2 plugin
        $('#ch_username').select2({
            placeholder: 'e.g mike'
        });
    }
  );



  // Add newly sent messages to the channel
  let $form = $("#message-form");
  let $input = $("#message-input");
  let $profileImg = $("#senderProfileImage").attr('src');
  $form.on("submit", function(e) {
    var files = $('#MsFile')[0].files;
    const formData = new FormData();
    formData.append('file', $('#MsFile')[0].files[0]);
    // formData.append('text', $input.val());
    e.preventDefault();
    if (roomChannel && $input.val().trim().length > 0 && files.length > 0){
      roomChannel.sendMessage($input.val());
      // send media with all FormData parsed atrtibutes
      roomChannel.sendMessage(formData);
      //clear input fields
      $input.val("");
      $('.emojionearea-editor').html('');
      $('.flsSelected').empty();
      $('#MsFile').val("");
    }else if (roomChannel && $input.val().trim().length > 0 && files.length === 0) {
      roomChannel.sendMessage($input.val());
      $input.val("");
    }else if (roomChannel && files.length > 0 && $input.val().trim().length === 0) {
      roomChannel.sendMessage(formData);
      $('#MsFile').val("");
      $('.flsSelected').empty();
    }
  });

//showing number of files selected
// 'use strict';
//
// ;( function ( document, window, index )
// {
// 	var inputs = document.querySelectorAll( '#MsFile' );
// 	Array.prototype.forEach.call( inputs, function( input )
// 	{
// 		var label	 = input.nextElementSibling,
// 			labelVal = label.innerHTML;
//
// 		input.addEventListener( 'change', function( e )
// 		{
//
// 			var fileName = '';
// 			if( this.files && this.files.length > 1 )
// 				fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
// 			else
// 				fileName = e.target.value.split( '\\' ).pop();
//
// 			if( fileName )
// 				label.querySelector( 'span' ).innerHTML = fileName;
// 			else
// 				label.innerHTML = labelVal;
// 		});
//
// 		// Firefox bug fix
// 		input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
// 		input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
// 	});
// }( document, window, 0 ));

    // emoji initializer
    $("#message-input").emojioneArea({
      pickerPosition: "top",
      tonesStyle: "bullet",
    });
});
// });
