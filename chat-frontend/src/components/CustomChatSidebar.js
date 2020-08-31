import React, { Component } from "react";
import {withChatContext} from "stream-chat-react";
import styled from 'styled-components';
import DirectMessage from "./DirectMessaging";
import GroupChannel from "./GroupChannel";
import { Icon } from 'semantic-ui-react';
import { Popup as SemanticPopup} from 'semantic-ui-react';


const SidebarWrapper = styled.div`
  float: left;
  height: 100vh;
  width: 55px;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  flex-direction: column;
  margin-left: 5px;
`

const SidebarButtonsWrapper = styled.div`
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content: center;
  background: #13031b;
  height: fit-content;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  padding: 15px;
`

const SidebarButton = styled.button`
  width:35px;
  height:35px;
  border:none;
  border-radius:50%;
  margin-bottom:25px;
  font-size:14px;
  background-color:transparent;
  position:relative;
  :hover {
    cursor:pointer;
    transform: scale(1.3);
  }
`

const CustomChatSidePanel =  withChatContext(
  class CustomChatSidePanel extends Component {

    render() {
      return (
        <SidebarWrapper>
            <SidebarButtonsWrapper>
            <SemanticPopup
              trigger={
                <SidebarButton>
                <a href='/'>
                  <Icon name='th large' style={{'color':'#ffffff', 'fontSize':'15px'}}/>
                  </a>
                </SidebarButton>
              }
              inverted
              content='Home'
              position='top left'
              style={{'borderRadius': '10px'}}
              />
              <SemanticPopup
                trigger={
                  <SidebarButton>
                    <a href='/profile/account/'>
                    <Icon name='user outline' style={{'color':'#ffffff', 'fontSize':'15px'}}/>
                    </a>
                  </SidebarButton>
                }
                inverted
                content='Profile'
                position='top left'
                style={{'borderRadius': '10px'}}
                />
                <GroupChannel/>
                <DirectMessage/>
                <SemanticPopup
                  trigger={
                    <SidebarButton>
                      <Icon name='bell outline' style={{'color':'#ffffff', 'fontSize':'15px'}}/>
                    </SidebarButton>
                  }
                  inverted
                  content='Notifications'
                  position='top left'
                  style={{'borderRadius': '10px'}}
                  />

                  <SemanticPopup
                    trigger={
                      <SidebarButton>
                        <Icon name='question circle outline' style={{'color':'#ffffff','fontSize':'15px'}}/>
                      </SidebarButton>
                    }
                    inverted
                    content='Help&Support'
                    position='top left'
                    style={{'borderRadius': '10px'}}
                    />
            </SidebarButtonsWrapper>

        </SidebarWrapper>
      );
    }
  }

);


export default CustomChatSidePanel;
