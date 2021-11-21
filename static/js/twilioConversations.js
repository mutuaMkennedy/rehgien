$(document).ready(function() {

  // $('#creatChatThread').click(function(){
  //   // createConversation();
  //   // deleteConversation('CHa8560d44e20947008c52e0693fba974c');
  //
  // });


  let conversationClient;
  let activeConversation;


  async function getToken(){
     const auth = await axios({
        method: 'get',
        url:'/chat/twilio/get_token/',
      });

       conversationClient = await Twilio.Conversations.Client.create(auth.data.token);
       getSubscribedChannels(conversationClient);
  };


  // Helper function for formating time to am/pm
  function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  };
  // Helper function for checking last modfied date for chat items
  function lastModifiedDate(lastUpdatedDate, lastUpdatedHours){
    var today = new Date();
    var yesterday = ( d => new Date(d.setDate(d.getDate()-1)) )(new Date); //today.setDate(today.getDate() - 1)

    var dateToday = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var dateYesterday = yesterday.getFullYear()+'-'+(yesterday.getMonth()+1)+'-'+(yesterday.getDate());
    var showDate = '';
    if (lastUpdatedDate) {
      if (dateToday === lastUpdatedDate) {
        showDate = 'Today at ' + lastUpdatedHours;
      }else if (dateYesterday === lastUpdatedDate) {
        showDate = 'Yesterday at ' + lastUpdatedHours;
      }else {
        showDate = lastUpdatedDate +' at '+ lastUpdatedHours;
      };
    };

    return showDate;

  };

  async function getSubscribedChannels(conversationClient){
      let conversations = await conversationClient.getSubscribedConversations().then(list_conversations);
  };



  //
  // We will handle how the chat threads and messages will be created and displayed in the DOM
  //



  let threadContainer = $('#thrdIntContainer'); // Div that shows an expanded view of a conversation
  let threadList = $('#msgItems');  // Div that shows all the user's conversations
  let loader = $('.msgThreadsLoading');
      // show loader
      loader.css('display','flex')

  // html markup when no messages are found
  let emptyMailBox = (
    "<div class='cnoConversationsYet'>"+
    "<img src='/static/img/mailbox.svg'>" +
    "<div class='emptyMailboxTxt'>"+
      "<h3>No Messages yet!</h3>"+
      "<p>Messages or conversations you have will appear here.</p>" +
    "</div>"+
  "</div>"
)

  // Helper funtion for iterating through the items of a conversation and returning values/data
  // So that other functions can easily get and use that data
  async function getConversationData(conversation){
    // console.log(conversation);
    let convID = conversation.sid;
    let convoCreatedBy = conversation.createdBy;

    //conversation created date
    let convoCreatedOnHours = conversation.dateCreated ? formatAMPM(conversation.dateCreated) : '';
    let convoCreatedOnDate = conversation.dateCreated ? conversation.dateCreated.getFullYear()+'-'+(conversation.dateCreated.getMonth()+1)+'-'+conversation.dateCreated.getDate() : '';
    let convoCreatedOn = lastModifiedDate(convoCreatedOnDate, convoCreatedOnHours);

    // Last sent message time
    let lastUpdatedhours = conversation.lastMessage ? formatAMPM(conversation.lastMessage.dateCreated) : '';
    let lastUpdatedDate = conversation.lastMessage ? conversation.lastMessage.dateCreated.getFullYear()+'-'+(conversation.lastMessage.dateCreated.getMonth()+1)+'-'+conversation.lastMessage.dateCreated.getDate() : '';

    let showDate = lastModifiedDate(lastUpdatedDate, lastUpdatedhours);

    // Getting conversations particpants. Also this will filter out conversations that don't have particpants
    let participantsArray = await conversation.getParticipants();
    // Get the unread message count for current participant.
    let totalMessages = await conversation.getMessagesCount();

    let unreadMessageCount;
    for (var a = 0; a < participantsArray.length; a++) {
      if (participantsArray[a].lastReadMessageIndex === null) {
        // Means all messages are unread so get the message count
         unreadMessageCount = totalMessages;
      }else{
        // Get only the unread messages count
         unreadMessageCount = await conversation.getUnreadMessagesCount();
      };
    };
    // find the participant who we are talking to so we can display their info on the conversation list items
    // NOTE: AUTH_USER_ID is a global js variable we defined in the base template to get the current authenticated user id so we can use it here easily
    let userP = participantsArray.find(el => el.identity != AUTH_USER_ID );
    let userAtrributes = await userP.getUser();

    let userCategory = userAtrributes.attributes.user_type =='PRO' ?  'Pro > ' + userAtrributes.attributes.pro_category : 'Client';

    return {
      convID,
      convoCreatedOn,
      convoCreatedBy,
      unreadMessageCount,
      userAtrributes,
      userCategory
    }
  };

  // Helper function for creating list of conversations dom elements
  async function createThreadListDomElement(conversationData) {
      // Get the data we are going to use to build/show in the dom elements
      let convID = conversationData.convID;
      let convoCreatedOn = conversationData.convoCreatedOn;
      let convoCreatedBy = conversationData.convoCreatedBy;
      let unreadMessageCount = conversationData.unreadMessageCount;
      let userAtrributes = conversationData.userAtrributes;
      let userCategory = conversationData.userCategory;

      // Create the dom elements
      let threadListItem = (
        " <div id='azMsgThread-"+ convID +"' class='msg-item azMsgThread' data-threadid='" + convID + "'>" +
          "<div class='msg-item-avatar'>" +
             "<img id='msg-item-avtrImg' src=' " + (userAtrributes.attributes.profile_image != undefined ? userAtrributes.attributes.profile_image : '') + " ' alt=''>" +
             "<div class='"+userAtrributes.identity +"-onlineState isOnlineIndicator "+(userAtrributes.isOnline ? "true" :'') +"'></div>" +
           "</div>" +
           "<div class='msg-item-scD'>" +
             "<div class='msg-item-userD'>" +
               "<div class='msg-item-userD-id'>" +
                 "<h5 id='msg-item-userDsname'>" + (userAtrributes.attributes.username ? userAtrributes.attributes.username : '') + "</h5>" +
                 "<h6>" + userCategory + "</h6>" +
               "</div>" +
            "</div>" +
            "<div class='msg-item-msgSnippet'>" +
               "<p id='latestMessage-"+ convID +"'><span class='noMessagesvS'>No messages yet. Be the first to send a message.</span></p>" +
               "<div class='msg-item-unreadCount'>" +
                 "<span class='"+ (unreadMessageCount ? '' : 'none')+ "'>"+ unreadMessageCount +"</span>" +
               "</div>"+
             "</div>" +
             "<div class='msg-item-msgTime'>" +
               "<span id='latestMessageDate-"+ convID +"'></span>" +
             "</div>" +
           "</div>" +
        "</div>"
      );


      return threadListItem
    };

  // Helper function for creating open thread chat window dom elements
  async function createThreadOpenDomElement(conversationData) {
    // Get the data we are going to use to build/show in the dom elements
    let convID = conversationData.convID;
    let convoCreatedOn = conversationData.convoCreatedOn;
    let convoCreatedBy = conversationData.convoCreatedBy;
    let unreadMessageCount = conversationData.unreadMessageCount;
    let userAtrributes = conversationData.userAtrributes;
    let userCategory = conversationData.userCategory;

    // Create the dom elements
    let threadInfo = (
      "<div class='openThreadInfoSct'>" +
            "<div class='openThreadInfoSct-hdr'>" +
              "<h2>Thread Info</h2>" +
              "<button class='closeThrdInfoXVC' data-sid='"+convID+"' type='button' name='button' class='closeThreadInfoCt'><i class='iconify' data-icon='eva:close-fill'></i></button>" +
            "</div>" +
            "<div class='openThreadInfoSct-body'>" +
                "<div class='openThreadInfoSct-pcpnt'>" +
                    "<div class='openThreadInfoSct-pcpnt-usrs'>" +
                      "<div class='openThreadInfoSct-pcpnt-img'>" +
                        "<img src='" + (userAtrributes.attributes.profile_image != undefined ? userAtrributes.attributes.profile_image : '') +"'>" +
                      "</div>" +
                      "<div class='openThreadInfoSct-pcpnt-name'>" +
                        "<h5>"+ (userAtrributes.attributes.username ? userAtrributes.attributes.username : '') +"</h5>" +
                      "</div>" +
                    "</div>" +
                    "<div class='openThreadInfoSct-pcpnt-ActBtn'>" +
                      "<button type='button' name='button'><i class='iconify' data-icon='fluent:call-28-filled'></i><div class='chatActLocked'><i class='iconify' data-icon='carbon:locked'></i></div></button>" +
                      "<button type='button' name='button'><i class='iconify' data-icon='wpf:video-call'></i><div class='chatActLocked'><i class='iconify' data-icon='carbon:locked'></i></div></button>" +
                    "</div>" +
                "</div>" +
                "<div class='openThreadInfoSct-ExtraInfo'>" +
                  "<div class='openThreadInfoSct-ExtraInfo-Sc'>" +
                    "<h5>User Info</h5>" +
                    "<ul>" +
                      "<li>" +
                        "<i class='iconify' data-icon='ant-design:user-outlined'></i>" +
                        "<div class='oTis-eXsc-bd'>" +
                          "<h6>Username</h6>" +
                          "<p>" + (userAtrributes.attributes.username ? userAtrributes.attributes.username : '') + "</p>" +
                        "</div>" +
                      "</li>" +
                      "<li>" +
                        "<i class='iconify' data-icon='carbon:user-profile'></i>" +
                        "<div class='oTis-eXsc-bd'>" +
                          "<h6>User Type</h6>" +
                          "<p>"+userCategory+"</p>" +
                        "</div>" +
                      "</li>" +
                    "</ul>" +
                  "</div>" +
                  "<div class='openThreadInfoSct-ExtraInfo-Sc'>" +
                    "<h5>Chat Info</h5>" +
                    "<ul>" +
                      "<li>" +
                        "<i class='iconify' data-icon='healthicons:i-schedule-school-date-time-outline'></i>" +
                        "<div class='oTis-eXsc-bd'>" +
                          "<h6>Created On</h6>" +
                          "<p>" + convoCreatedOn + "</p>" +
                        "</div>" +
                      "</li>" +
                      "<li>" +
                        "<i class='iconify' data-icon='fluent:chat-multiple-20-regular'></i>" +
                        "<div class='oTis-eXsc-bd'>" +
                          "<h6>Messages</h6>" +
                          "<p class='convoTMessagesCount'>0</p>" +
                        "</div>" +
                      "</li>" +
                      "<li>" +
                        "<i class='iconify' data-icon='carbon:media-library'></i>" +
                        "<div class='oTis-eXsc-bd'>" +
                          "<h6>Media Files</h6>" +
                          "<p class='convoMediaFileCount'>0</p>" +
                        "</div>" +
                      "</li>" +
                    "</ul>" +
                  "</div>" +
                "</div>" +
            "</div>" +
      "</div>"
    );

    let thread = (
      "<div id='trdhAcnTop-bar' class='proDash-msg-thread-top-bar'>" +
        "<div id='trdhAcctUsr-bar' class='proDash-msg-thread-top-bar-item'>" +
          "<div class='tUsr-item-avatar'>" +
            "<img src='" + (userAtrributes.attributes.profile_image != undefined ? userAtrributes.attributes.profile_image : '') + "' alt=''>" +
          "</div>" +
          "<div class='tUsr-item-dvdr'></div>" +
          "<div class='tUsr-item-info'>" +
            "<h2>" + (userAtrributes.attributes.username ? userAtrributes.attributes.username : '') + "</h2>" +
            "<div class='tUsr-item-info-st'> <h5>"+ userCategory + "</h5>"+
                "<div class='"+userAtrributes.identity +"-onlineState isOnlineIndicator "+(userAtrributes.isOnline ? "true" :'') +"'>" +
                "<div class='tUsr-item-info-stDvdr'></div><span>Online</span></div>"+
            "</div>" +
          "</div>" +
        "</div>" +
        "<div class='proDash-msg-thread-top-bar-btns'>" +
         "<div class='proDash-thread-top-bar-btns-properties'>" +
            "<button class='openThrdInfoXVC' data-sid='"+convID+"' type='button' name='button'><i class='iconify' data-icon='bi:three-dots-vertical'></i></button>" +
         "</div>" +
        "</div>" +
      "</div>" +

      "<div id='threadMessages-" + convID + "' class='proDash-msg-thread-messages'>"+
          "<div id='isTypingInd-"+ convID +"' class='userStypingInd'>" +
                "<div class='userStyping-avatar'>" +
                  "<img src='/static/img/avatar.png' alt=''>" +
                "</div>" +
                "<div class='typingBody'>" +
                  "<div class='isTypingIndicator'>" +
                    "<img src='/static/img/chat-typing-indicator_2.gif'/>" +
                  "</div>" +
                  "<div class='isTyping-bdy-ft'>" +
                     "<p><span>User</span> is typing..</p>" +
                  "</div>" +
                "</div>" +
          "</div>"+
      "</div>" +

      "<div class='proDash-msg-thread-inpBox'>" +
        "<div id='cSendFiles-"+convID+"' class='chatSendFilesSelected'>"+
            "<div class='chatSendFilesSelectedBox'>"+
                  // Display selected files here
            "</div>"+
            "<div class='seeMoreScrollFlS'><div class='slctDmrIco'><i class='iconify' data-icon='bi:chevron-double-right'></i></div></div>"+
        "</div>" +
        "<form class='proDash-msg-thread-inpBox-form' action='' method='post' enctype='multipart/form-data'>" +
          "<input type='hidden' name='csrfmiddlewaretoken' value='" + CSRF_TOKEN +"'>"+
          "<input hidden type='text' name='threadID' value='"+ convID +"'>" +
          "<div class='proDash-msg-thread-inpBox-input'>" +
            "<textarea id='chattxtmsgInputBox' data-csid='"+convID+"' name='message' rows='8' cols='80' placeholder='Your Message'></textarea>" +
          "</div>" +
          "<div class='proDash-msg-thread-inpBox-btns'>" +
            "<div class='proDash-thread-inpBox-btns-Act'>" +
                "<div class='proDash-thread-inpBox-btns-attach'>" +
                  "<input id='filesSelectTchat-"+ convID+"' class='filesSelectTchat' data-sid='"+convID+"' type='file' multiple accept='image/x-png,image/jpeg' name='photos'>" +
                   "<button class='selectFilesTChat' data-sid='"+convID+"' type='button' name='button'><i class='iconify' data-icon='icomoon-free:attachment'></i></button>" +
                "</div>" +
                 "<div class='proDash-thread-inpBox-btns-audio'>" +
                    "<button type='button' name='button'><i class='iconify' data-icon='ant-design:audio-filled'></i></button>" +
                 "</div>" +
             "</div>" +
             "<div class='proDash-thread-inpBox-btns-send'>" +
                "<button type='submit' name='button'><i class='iconify' data-icon='ic:sharp-send'></i>Send</button>" +
             "</div>" +
          "</div>" +
        "</form>" +
      "</div>"
    );

    let threadOpenItem = (
      "<div id='threadId-" + convID + "'class='proDash-msg-threadBox' data-active='false' >" +
          "<div class='proDash-msg-threadBox-thread'>" +
            thread +
          "</div>" +
          "<div id='threadInfo-"+convID+"' class='proDash-msg-threadBox-thrdInfo' data-active='false'>" +
            threadInfo +
          "</div>" +
      "</div>"
    );


    return threadOpenItem
  };

  // Create the thread list and chat window then append them to the DOM
  async function list_conversations(conversations){
    // console.log(conversationClient);
    let conversationsArray = conversations.items;
    // sorting array by last message date in ascending format
    conversationsArray.sort(function (a, b) {
      if (a.lastMessage && b.lastMessage) {
        	var dateA = new Date(a.lastMessage.dateCreated), dateB = new Date(b.lastMessage.dateCreated)
      }else {
          var dateA = new Date(a.dateUpdated), dateB = new Date(b.dateUpdated)
      }
    	return dateB - dateA
    });

    let totalUnreadCount = 0;
    if (conversationsArray.length > 0) {
      for (var i = 0; i < conversationsArray.length; i++) {

          // Get the conversation object data
          let conversationData = await getConversationData(conversationsArray[i]);

          // list conversations in thread list
          let threadListItem = await createThreadListDomElement(conversationData);
          threadList.append(threadListItem);

          // Append corresponding conversations windows to dom for quick switching between conversations
          let threadItem = await createThreadOpenDomElement(conversationData)
          threadContainer.append(threadItem);

          // Get all messages for this conversation
          let messagePages = await conversationsArray[i].getMessages(pageSize=30);
          processPage(messagePages);

          totalUnreadCount = totalUnreadCount + conversationData.unreadMessageCount;

        };

      // hide the all open thread message boxes & mark them as inactive
      $('.proDash-msg-threadBox').css('display','none').attr('data-active',false);
      //remove the empty mailbox message
      $('.cnoConversationsYet').remove();

      // update unread message count badges
      let msgUnreadBadge = $('.unreadMessageCountUnread');
      let innitialUnreadCount = parseInt(msgUnreadBadge.text());

      // if totalUnreadCount is not 0 display the total unread badge
      // else hide it
      if (totalUnreadCount != 0) {

        // if innitialUnreadCount is not NaN add it to the totalUnreadCount
        // else show the totalUnreadCount only
        if (innitialUnreadCount) {
          msgUnreadBadge.text(parseInt(innitialUnreadCount) + totalUnreadCount);
        }else{
          msgUnreadBadge.text(totalUnreadCount);
        };

        msgUnreadBadge.css('display','flex');

      }else{

          msgUnreadBadge.css('display','none');

      };

    }else {
      threadList.html(emptyMailBox);
    };
    // hide loader
    loader.css('display','none');

    // When client joins a conversation add it to the dom.
    // Fired when a user is added to a conversation
    conversationClient.on('conversationJoined', async function(conversation){
      if (conversation.status == 'joined') {
        //remove the empty mailbox message if it exists
        $('.cnoConversationsYet').remove();

        // Get the conversation object data
        let conversationData = await getConversationData(conversation);

        // list conversations in thread list
        let threadListItem = await createThreadListDomElement(conversationData);
        threadList.append(threadListItem);

        // Append corresponding conversations windows to dom for quick switching between conversations
        let threadItem = await createThreadOpenDomElement(conversationData)
        threadContainer.append(threadItem);

        // Move thread to top of conversation list
        moveConversationToTop(conversationData.convID);

        // Get all messages for this conversation
        let messagePages = await conversation.getMessages(pageSize=30);
        processPage(messagePages);
      };
    });

    // When client leaves a conversation remove it from the DOM
    conversationClient.on('conversationLeft', async function(conversation){
      // remove conversation from thread list
      $("#azMsgThread-"+conversation.sid).remove();

      // remove conversation from then open thread interaction window
      let openThreadView = $("#threadId-"+conversation.sid);
      let threadIsOpen = openThreadView.attr("data-active");
      openThreadView.remove();

      // show the default intro/welcome message if the user currently has this thread open
      if (threadIsOpen == 'true') {
          $('#clickThMsg').css('display','flex');
      };

      // show empty conversation message
      if (!$('.msg-item').length) {
        threadList.html(emptyMailBox);
      };

    });
    // on user Updated event
    conversationClient.on('userUpdated',function(data){
      if (data.user.isOnline === true) {
        // find all elements that show online status for this user show the user is online
        $('.'+data.user.identity+'-onlineState').addClass('true');
      }else {
        // find all elements that show online status for this user show the user is offline
        $('.'+data.user.identity+'-onlineState').removeClass('true');
      }
    });

    // on message add event listener
    conversationClient.on('messageAdded',async function(message) {
      //remove the message sending indicator
      $('#sendingThread-Msg-'+message.conversation.sid).remove();

      // dispaly the sent message
      printMessage(message);

      // Move thread to top of conversation list
      moveConversationToTop(message.conversation.sid);

      // Handling the read status indicator
      let threadBox = $('#threadId-'+message.conversation.sid).attr('data-active');
      if (threadBox === 'true') {
        let activeConversation = await conversationClient.getConversationBySid(conversationSid=message.conversation.sid);
        // Move the read horizon for pertcipant to current sent message index
        await activeConversation.updateLastReadMessageIndex(message.index);
      }else{
        // Update the unread message count
        let currentUnreadMessagesEl = $('#azMsgThread-'+message.conversation.sid).find('.msg-item-unreadCount span');
        let currentUnreadMessagesCount = parseInt(currentUnreadMessagesEl.html());
            currentUnreadMessagesEl.text(currentUnreadMessagesCount + 1);
            currentUnreadMessagesEl.removeClass('none');
      };

    });

  };

  // helper function to process messages pages
  function processPage(page) {
    // console.log(page);
    page.items.forEach(message => {
      printMessage(message);
    });
    if (page.hasNextPage) {
          page.nextPage().then(processPage);
    } else {
      // console.log("Done loading messages");
    };
  };

  // Helper function to print messages in conversation window
  let latestMessageTxt; //We are going to use this later as a reference when updating the typing indicator on the thread list
  async function printMessage(message) {

    let participant = await message.getParticipant();

    let authorAtrr = await participant.getUser();

    let latestMessage;
    if (message.body) {
      latestMessage = message.body.length > 85 ? (message.body.substring(0,85) + '...') : (message.body);
    }else if (message.attachedMedia) {
      latestMessage= "<div class='mediaFileSnip'><i class='iconify' data-icon='clarity:image-line'></i>File</div>";
    };

    let threadMessageBox = $('#threadMessages-'+message.conversation.sid);
        latestMessageTxt = latestMessage; //We are going to use this later as a reference when updating the typing indicator on the thread list

    // get the typing indicator so we can control its styling and position
    let typingIndicator = $('#isTypingInd-'+message.conversation.sid);

    // lets handle how the messages will be styled on the conversation window
    let messageClassName = message.author.toString() === AUTH_USER_ID.toString() ? 'dRight' : 'dLeft'; // if author is the current authenticated user show message on right side else show on left side
    let senderDisplay = message.author.toString() === AUTH_USER_ID.toString() ? 'You' : authorAtrr.attributes.username; // if author is the current authenticated user show you else show full name

    // lets get the last modified in well formated way
    let lastUpdatedhours = message ? formatAMPM(message.dateCreated) : '';
    let lastUpdatedDate = message ? message.dateCreated.getFullYear()+'-'+(message.dateCreated.getMonth()+1)+'-'+message.dateCreated.getDate() : '';
    let showDate = lastModifiedDate(lastUpdatedDate, lastUpdatedhours)
    let recentMessageSnippet = $('#latestMessage-'+message.conversation.sid);
    let latestMessageSnippetDate = $('#latestMessageDate-'+message.conversation.sid);

    let msgFooter = messageClassName === 'dRight' ?  ("<p>" + showDate + "<span> "+ senderDisplay +"</span></p>") : "<p><span>" + senderDisplay +"</span> " + showDate + "</p>";

    // handling messages with media file
    let mediaContent;
    let textContent;

    if (message.attachedMedia && message.attachedMedia[0]) {
        //show media sent count
        let mediaFilesCount = parseInt($('#threadId-'+message.conversation.sid).find('.convoMediaFileCount').text());

        $('#threadId-'+message.conversation.sid).find('.convoMediaFileCount').text( mediaFilesCount + message.attachedMedia.length );

        let moreFilesSection;
        let firstMediaFileUrl = await message.attachedMedia[0].getContentTemporaryUrl();
        if (message.attachedMedia.length > 1) {
          moreFilesSection = (
            "<div class='Md-items-count'>" +
              "<button type='button' name='button'>" +
                "<i class='iconify' data-icon='ion:images-outline'></i>" +
                "+"+ message.attachedMedia.length +
              "</button>" +
            "</div>"
          );
        };

        mediaContent = (
          "<div class='tUsr-msg-bdy-Md-ct'>" +
            "<div class='MdType-Img'>" +
              "<img src='"+firstMediaFileUrl +"'>" +
            "</div>" +
            (moreFilesSection ? moreFilesSection : '' )+
          "</div>"
        );
    };

    if(message.body) {
      textContent =(
        "<div class='tUsr-msg-bdy-ct'>" +
          "<p>" + message.body + "</p>" +
        "</div>"
      );
    };

    threadMessageBox.append(
      "<div class='thread-msg " + messageClassName  + " msgIndex-" + message.index + "'>" +
            "<div class='tUsr-msg-avatar'>" +
              "<img src=' " + authorAtrr.attributes.profile_image + " ' alt=''>" +
            "</div>" +
            "<div class='tUsr-msg-bdy'>" +
              // Insert media message
                (mediaContent ? mediaContent : '') +
              // Insert text message
                (textContent ?  textContent : '')+
              "<div class='tUsr-msg-bdy-ft'>" +
                 msgFooter +
                 (messageClassName === 'dRight' ? "<button type='button' name='button'><i class='iconify' data-icon='bi:check-circle-fill' style='color:#00AD56'></i></button>" : '') +
              "</div>" +
            "</div>" +
      "</div>"
    );

    recentMessageSnippet.html(latestMessage);
    latestMessageSnippetDate.text(showDate);

    // update total messages count in thread info
    let messagesCount = parseInt($('#threadId-'+message.conversation.sid).find('.convoTMessagesCount').text());

    $('#threadId-'+message.conversation.sid).find('.convoTMessagesCount').text( messagesCount + 1 );

    // we want the typing indicator to always be last element in the div
    typingIndicator.appendTo(threadMessageBox);

    threadMessageBox.animate({
        scrollTop: threadMessageBox[0].scrollHeight
      }, 0);

  };

  // Switching/hopping between conversations
  $(document).on('click', '.azMsgThread', async function(){
      let id = $(this).attr('data-threadid');

      // this will be our active conversation
      let activeConversation = await conversationClient.getConversationBySid(conversationSid=id);

      // hide the all open thread message boxes & mark them as inactive
      $('.proDash-msg-threadBox').css('display','none').attr('data-active',false);
      // remove active className that controls styling of threads in thread list
      $('.azMsgThread').removeClass('thread_active');

      // hide default intro/welcome div
      $('#clickThMsg').css('display','none');

      // display the thread we clicked & mark it as active
      $('#threadId-'+id).css('display','flex').attr('data-active',true);
      // Add the active className to control styling of thread in thread list
      $(this).addClass('thread_active');


      let threadMessageBox = $('#threadMessages-'+id);

      // get the innitial unread count for this thread
      // We will use this to update the global total unread message badges later
      let innitialUnreadCountForThread = $('#azMsgThread-'+id).find('.msg-item-unreadCount span').text();

      // Get the last message read index
      let lastReadMessageIndex = activeConversation.lastReadMessageIndex;

      // Set the position where to scroll the user when they open a conversation
      if (lastReadMessageIndex === null) {
        // scroll to top where the first message of the conversation will be
        threadMessageBox.animate({
            scrollTop: threadMessageBox.offset().top
          }, 0);

        // then mark all messages as read
        await activeConversation.setAllMessagesRead();

        // Hide the unread messages indicator
        $('#azMsgThread-'+id).find('.msg-item-unreadCount span').text('0').addClass('none');

      }else {
        // scroll view to the last read message index position
        let messageIndex = threadMessageBox.find('.msgIndex-'+ lastReadMessageIndex)

        threadMessageBox.animate({
            scrollTop: messageIndex.offset().top - threadMessageBox.offset().top + threadMessageBox.scrollTop()
          }, 500);

        // then set all messages as read
        await activeConversation.setAllMessagesRead();
        // console.log(activeConversation);

        // Hide the unread messages indicator
        $('#azMsgThread-'+id).find('.msg-item-unreadCount span').text('0').addClass('none');

      };

      // // NOTE: Buggy fix later
      // update the global total unread messages badges on nav bars
      let innitialUnreadCountForThreadInt = parseInt(innitialUnreadCountForThread);
      let totalMsgUnreadBadge = $('.unreadMessageCountUnread');
      let innitialTotalUnreadCount = parseInt(totalMsgUnreadBadge.text());

      if (innitialUnreadCountForThreadInt && innitialTotalUnreadCount) {

          totalMsgUnreadBadge.text(innitialTotalUnreadCount - innitialUnreadCountForThreadInt);

          let updatedMsgTotalUnread = $('.unreadMessageCountUnread');
          let updatedMsgTotalUnreadCount = parseInt(updatedMsgTotalUnread.text());

          // if updatedMsgTotalUnreadCount is not NaN or updatedMsgTotalUnreadCount is not 0 show badge
          // else hide the badge
          if (updatedMsgTotalUnreadCount || updatedMsgTotalUnreadCount != 0) {
            updatedMsgTotalUnread.css('display','flex');
          }else{
            updatedMsgTotalUnread.css('display','none');
          };

      }else{
        totalMsgUnreadBadge.css('display','none');
      };

  });


  // Move the conversation to top of conversations list
  // triggered by the messageAdded event;
  function moveConversationToTop(convoSID) {
      $('#azMsgThread-'+convoSID).prependTo('#msgItems');
  }

  // Fire typing started event when user starts typing on input bar
  $(document).on('keydown', '#chattxtmsgInputBox', async function() {
      let cSid = $(this).attr('data-csid');
    // console.log('sese');
    activeConversation = await conversationClient.getConversationBySid(conversationSid=cSid);
    activeConversation.typing();

    conversationClient.on('typingStarted',function(participant) {
      updateTypingIndicator(participant,true)
    });
    conversationClient.on('typingEnded',function(participant) {
      updateTypingIndicator(participant,false)
    });

  });
  // Helper funtion for displaying typing indicator
  async function updateTypingIndicator(participant, isTyping) {

      let authorAtrr = await participant.getUser();
      let threadMessageBox = $('#threadMessages-'+participant.conversation.sid);

      let convoListTypingIndicator = $('#latestMessage-'+participant.conversation.sid);

      let typingIndicator = $('#isTypingInd-'+participant.conversation.sid);
          typingIndicator.find('.userStyping-avatar img').attr('src',authorAtrr.attributes.profile_image);
          typingIndicator.find('.isTyping-bdy-ft span').text(authorAtrr.attributes.username);

          if (isTyping == true) {
              typingIndicator.css('display', 'flex');
              convoListTypingIndicator.html(authorAtrr.attributes.username + ' is typing').css('color','#00ad56');
          }else {
              typingIndicator.css('display', 'none');
              convoListTypingIndicator.html(latestMessageTxt ? latestMessageTxt :"<span class='noMessagesvS'>No messages yet. Be the first to send a message.</span></p>" ).css('color','#000');
          }

      threadMessageBox.animate({
          scrollTop: threadMessageBox[0].scrollHeight
        }, 1000);
    };



  //
  // CRUD operations on chat client
  //



  // A Conversation is a unique thread of a conversation.
  // Each Conversation includes a list of current Participants and the Messages that they have sent amongst each other.
  function createConversation() {
    conversationClient.createConversation({
           friendlyName: 'Service Request'
         })
        .then(function(conversation) {
          // We now have access to the conversation object
          let identityIds = ['1','65']
          addPartcipant(conversation,identityIds)
          // console.log(conversation);

        });
    };

  // twilio does not have a js sdk delete conversation method so at the moment
  // we will delete from backend using the python sdk
  function deleteConversation(sid) {
    axios({
        method: 'get',
        url:'/chat/twilio/delete/conversation/',
        params:{
            "sid":sid
          },
      }).then(function (response){
        // do nothing. The conversation left event listener will handle the rest of the functionality
      }).catch(function (error) {
        console.log(error);
      });
    };

  //add participant to conversation
  async function addPartcipant(conversation, ids){

      // We dont need to get the conversation again so ignore this : let convo = await conversationClient.getConversationBySid(conversationSid=sid);

      // TODO: Catch duplicate error. When user is already a participant join the in the conversation instead.
      for (var i = 0; i < ids.length; i++) {
        // array[i]
        let newPartcipant = await conversation.add(identity=ids[i]);
      }
  }

  // Helper function for sending message to thread
  async function sendMessage(txtMessage, photos, sid){

    let convo = await conversationClient.getConversationBySid(conversationSid=sid);
    // await convo.sendMessage(message=formData);
    let prepMessage = await convo.prepareMessage();
    if (photos.length > 0) {
      for (var i = 0; i < photos.length; i++) {
        // check if photo uploaded is of supported type
        if (photos[i].type == "image/png" || photos[i].type == "image/jpeg" ) {
          let mediaBuffer = await photos[i].arrayBuffer();
          prepMessage.addMedia({contentType:photos[i].type, filename:photos[i].name, media:mediaBuffer });
        };
      };
    };
    prepMessage.setBody(txtMessage);
    prepMessage.build();
    prepMessage.message.send();
  };



  //
  // Handling message input experience and behaviour on the  before sending message
  //



  // triger file select
  $(document).on('click', '.selectFilesTChat', function(e){
    let convoSID = $(this).attr('data-sid');
    $('#filesSelectTchat-'+convoSID).click();
  });

  // display selected files
  $(document).on('change', '.filesSelectTchat', function () {
      let convoSID = $(this).attr('data-sid');
      let filesSelected = $('#cSendFiles-'+convoSID);
      let filesSelectedBox = filesSelected.find('.chatSendFilesSelectedBox');
      // remove existing selections
        filesSelectedBox.html('');
      let filesArray = this.files;
      // console.log(filesArray);
      if (filesArray && filesArray[0]) {
        for (var i = 0; i < filesArray.length; i++) {
          let index = i;
          var reader = new FileReader();
          reader.onload = function (e) {
            filesSelectedBox.append(
              "<div class='chatFileSelected'>"+
                "<img src='"+e.target.result+"'/>"+
                "<button class='rmvSelectedFile' data-fileIndex='"+ index +"' data-sid='"+ convoSID +"'type='button'><i class='iconify' data-icon='eva:close-outline'></i></button>" +
              "</div>"
            );
          };
          reader.readAsDataURL(filesArray[i]);
        };
        filesSelected.css('display','flex');
      }else {
        filesSelected.css('display','none');
      };

      // NOTE: This is not working - filesSelectedBox scrollWidth & filesSelectedBox clientWidth are always equal, fix later!
      // Show more button when content overflows
      if (filesSelectedBox.prop('scrollWidth') > filesSelectedBox.prop('clientWidth')){
          //if 'true', the content overflows the tab: we show the hidden link
          filesSelectedBox.find('seeMoreScrollFlS').css('display','flex');
      }else {
          filesSelectedBox.find('seeMoreScrollFlS').css('display','none');
      };

    });

  //remove a file from selected files
  $(document).on('click', '.rmvSelectedFile', function(){
      let fileIndex = $(this).attr('data-fileIndex');
      // console.log(fileIndex);
      let convoSID = $(this).attr('data-sid');
      // console.log(convoSID);
      let fileInput = $("#filesSelectTchat-"+convoSID);
      let files = fileInput[0].files;
      let fileBuffer = new DataTransfer();
      // console.log(files);
      // append the file list to an array iteratively
      for (let i = 0; i < files.length; i++) {
          // Exclude file in specified index
          if (parseInt(fileIndex) !== i) {
              fileBuffer.items.add(files[i]);
          };

      };

      // Assign buffer to file input replacing the innitial
      let newFileInput = $("#filesSelectTchat-"+convoSID);
      newFileInput[0].files = fileBuffer.files;
      // console.log(fileBuffer.files);
      // Trigger change event that will update the file selected preview
      newFileInput.trigger('change');
  });

  // listen for user send message action
  $(document).on('submit','.proDash-msg-thread-inpBox-form', function functionName(event) {
       event.preventDefault();
       var formData = new FormData(this);
       let elem = $(this)
       let txtMessage = formData.get('message');
       let photos = formData.getAll('photos');

       let threadSID = elem.find("input[name='threadID']").val();
       let msgBox = $('#threadMessages-'+threadSID);

       let messageInput = elem.find("textarea[name='message']");
       let photosInput = elem.find("input[name='photos']");

       sendMessage(txtMessage, photos, threadSID);

       //show sending indicator
       // We will hide indicator when listening to the onMessagAdded event
       let sendingMessageLoader = (
         "<div id='sendingThread-Msg-"+threadSID+"' class='thread-msg dRight'>" +
               "<div class='tUsr-msg-avatar'>" +
                 // Will be dispalyed after message is sucessfully sent
               "</div>" +
               "<div class='tUsr-msg-bdy'>" +
                 "<div class='tUsr-msg-bdy-ft'>" +
                     "<p>Sending message</p>" +
                     "<button type='button' name='button'><img src='/static/img/Preloader_2_sm.gif'/></button>" +
                 "</div>" +
               "</div>" +
         "</div>"
       )

       msgBox.append(sendingMessageLoader);

       msgBox.animate({
           scrollTop: msgBox[0].scrollHeight
         }, 0);

       //reset input fields
       messageInput.val('');
       photosInput.val('');
       photosInput.trigger('change');
  });



  //
  // Initilize this functions on load
  //



  getToken();



  //
  // UI interaction controls
  //

  $(document).on('click','.openThrdInfoXVC', function(e){
    showOrHideThreadInfo($(this));
  });

  $(document).on('click','.closeThrdInfoXVC', function(e){
    showOrHideThreadInfo($(this));
  });

  function showOrHideThreadInfo(button){
    let triggerBtn = button;
    let conversationSID = triggerBtn.attr('data-sid');

    let threadInfoSc = $('#threadInfo-'+conversationSID);
    let allThreadInfoSc = $('.proDash-msg-threadBox-thrdInfo');

    let threadInfoIsActive = threadInfoSc.attr('data-active');

    let allThreadMsgBox = $('.proDash-msg-threadBox-thread');

    if (threadInfoIsActive == 'false') {
      // open the thread info tab
      allThreadInfoSc.css({
        'width':'40%',
        'display':'block'
      });
      allThreadMsgBox.css({
        'width':'60%',
      });

      // change active to True
      threadInfoSc.attr('data-active', true);

      // change the colot of button
      triggerBtn.find('svg').css('color','#2ba2ca')
    }else {
      // close the thread info tab
      allThreadInfoSc.css({
        'width':'0%',
        'display':'none'
      });
      allThreadMsgBox.css({
        'width':'100%',
      });

      // change active to False
      threadInfoSc.attr('data-active', false);

      // change the colot of button
      console.log(  triggerBtn.find('svg'));
      triggerBtn.find('svg').css('color','#000')
    };
  };

})
