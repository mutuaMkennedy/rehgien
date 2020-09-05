import React, { Component } from "react";
import base from './baseAddress.js';
import {
  Chat,
  Channel,
  ChannelList,
  ChannelPreviewLastMessage,
  Thread,
  Window,
  // ChannelListTeam,
  ChannelListMessenger,
  MessageTeam,
  MessageSimple,
} from "stream-chat-react";
import { MessageList, MessageInputLarge } from "stream-chat-react";
import { StreamChat } from "stream-chat";
import "stream-chat-react/dist/css/index.css";
import CustomChatSidePanel from "./components/CustomChatSidebar";
import CustomChannelHeader from "./components/CustomChannelHeader";
import ChatSearchBar from "./components/ChatSearchBar";
import "./Chat.css";
import {Icon } from 'semantic-ui-react';




let userID = localStorage.getItem("user_id");
const sort = {
  last_message_at: -1,
  cid: 1,
};

const options = {
  member: true,
  watch: true,
  // limit: 5
};

const filter = {
  members: { $in: [userID] } //dont change
};

function openSideBar(){
  var sidBarWrp = document.getElementById('ChListSideBarWrapper');
  sidBarWrp.style.display='block';
};

function closeSideBar(){
  var sidBarWrp = document.getElementById('ChListSideBarWrapper');
  sidBarWrp.style.display='none';
};


class App extends Component {
  constructor(props) {
    super(props);
    this.client = new StreamChat("qk4nn7rpcn75");

    const userToken = localStorage.getItem("token");
    const tokenUserId = localStorage.getItem("user_id");
    const tokenUserName = localStorage.getItem("user_name");
    const userAvatar = localStorage.getItem("user_avatar");

    this.client.setUser(
      {
        id: tokenUserId,
        name: tokenUserName,
        image: base + userAvatar
      },
      userToken,
    );

    // innitialize default channells
    const GeneralChannel = this.client.channel("team", "general", {
      name: "#general",
      image:null,
      description:'General topic, conversations & announcements. Every user is added here by default',
      members: [tokenUserId],
    });

    const RandomChannel = this.client.channel("team", "Random", {
      name: "#random",
      image:null,
      description:'No specifics just random topics and conversations. Every user is added here by default',
      members: [tokenUserId],
    });

    // create the channel and add members
    GeneralChannel.create();
    GeneralChannel.addMembers([tokenUserId]);
    RandomChannel.create();
    RandomChannel.addMembers([tokenUserId]);

  };


  render() {
    return (
      <div id="messageView">
        <Chat client={this.client} theme={"team light"}>

              <div id='ChListSideBarWrapper'>
                  <CustomChatSidePanel/>
                    <ChannelList
                        Preview={ ChannelPreviewLastMessage} options={options}
                        sort={sort}
                        List={ChannelListMessenger}
                        customActiveChannel='general'
                    />
                    <button  type='button' className="navclosebtn" onClick={closeSideBar}>x</button>

              </div>

              <Channel>
                <Window>
                <div style={{ 'display':'flex', 'alignItems':'center', 'width':'100%'}}>
                <button id="navBtnA" onClick={openSideBar}><Icon id='ChannelListReveal' name='chevron right' style={{'color':'blue', 'fontSize':'24px'}}/></button>
                  <ChatSearchBar style={{'margin':'5px 0px', 'width':'100%'}}/>
                </div>
                  <CustomChannelHeader/>
                  <MessageList Message={MessageTeam} />
                  <MessageInputLarge/>
                </Window>
                <Thread  Message={MessageTeam} />
              </Channel>

        </Chat>
      </div>
    );
  }
}


export default App;
