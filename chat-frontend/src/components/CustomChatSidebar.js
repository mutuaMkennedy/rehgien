import React, { Component } from "react";
import {withChatContext} from "stream-chat-react";
import styled from 'styled-components';
import DirectMessage from "./DirectMessaging";
import GroupChannel from "./GroupChannel";
import { Icon } from 'semantic-ui-react';
import { Popup as SemanticPopup} from 'semantic-ui-react';


const SidebarWrapper = styled.div`
  height:70px;
  width: 300px;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items:center;
  border-right: 1px solid rgb(235, 243, 255);
  border-bottom: 1px solid rgb(235, 243, 255);
`
const SidebarText = styled.h1`
  font-size:23px;
  width:60%;
  margin:0;
  font-family:Ubuntu,Arial;
  margin-left:10px;
  color:#141414;

`
const SidebarButtonsWrapper = styled.div`
  display:flex;
  width:40%;
  height:100%;
  align-items:center;
  justify-content: space-between;
  padding:0 10px;

`

const CustomChatSidePanel =  withChatContext(
  class CustomChatSidePanel extends Component {

    render() {
      return (
        <SidebarWrapper>
            <SidebarText>Chats</SidebarText>
            <SidebarButtonsWrapper>
                <GroupChannel/>
                <DirectMessage/>
            </SidebarButtonsWrapper>

        </SidebarWrapper>
      );
    }
  }

);


export default CustomChatSidePanel;
