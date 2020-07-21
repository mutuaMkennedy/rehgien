//Chat client  setup
async function chatService(){

      // client initialization
      const client = new StreamChat("abwec7y2ujka");
      // setup user with a token
      await client.setUser(
          {
              id: 'jlahey',
              name: 'Jim Lahey',
              image: 'https://i.imgur.com/fR9Jz14.png',
          },
          "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiamxhaGV5In0.3N_V2lDQaFcFZUcGGMqCbQN9_uN_AjtwqwazB3a5w88",
      );

      $('.stMessages').append('<p>'+ 'you have been assigned the username ' + client.user.id +'</p>')

      // CREATING A CHANNEL
      const channel = client.channel('messaging', 'SalesTeam', {
          name: 'SalesTeam',
      });

      // fetch the channel state, subscribe to future updates
      const state = await channel.watch();
      console.log(state);
      $('.stMessages').append('<p>'+ 'you have been subscribed to ' + state.channel.id +'</p>')


      //sending a message
      const text = 'I’m mowing the air Rand, I’m mowing the air.';
      const response = await channel.sendMessage({
          text,
          customField: '123',
      });

      //listening on a channel
      channel.on('message.new', event => {
          console.log('received a new message', event.message.text);
          console.log(`Now have ${channel.state.messages.length} stored in local state`);
      });
};

chatService();
