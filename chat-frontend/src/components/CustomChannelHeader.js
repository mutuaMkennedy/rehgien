import React from "react";
import {
  withChannelContext,
} from "stream-chat-react";
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faUser} from '@fortawesome/free-regular-svg-icons';
import { faInfo,faPhone } from '@fortawesome/free-solid-svg-icons';
import { Accordion, Icon} from 'semantic-ui-react';
import { Popup as SemanticPopup} from 'semantic-ui-react';
import "./CustomChatSidebar.css";
import groupVideoCall from './groupVideoCall.svg';
import RemoveMember from './RemoveMember.js';
import AddMember from './AddMember.js';
import LeaveOrDeleteChannel from './DeleteChannel.js';
import EditGroupChannel from './UpdateChannel.js';


const ChHeaderWrapper = styled.div`
  padding:0px 10px;
  border-top:1px solid #ebf3ff;
  border-bottom:1px solid #ebf3ff;
  height: 70px;
  display:flex;
  align-items:center;
`

const ChHeadersContent = styled.div`
  margin-left:5px;
  width:70%;
  display:flex;
  justify-content:flex-start;
  align-items:center;
`
const ChHeaderAvatar = styled.img`
  width:55px;
  height:55px;
  object-fit:cover;
  margin-right:10px;
  border-radius:50%;
`

const ChHeaderName = styled.div`
  font-family:Ubuntu,Arial;
  color: #006cff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom:3px;
`
const ChHeaderDesc = styled.div`
  font-family:Noto Sans Jp,Roboto,Arial !important;
  color: #00000080;
  font-size: 13px;
  font-weight: 500;
  display:flex;
  align-items:baseline;
  margin-bottom:3px;

`

const SideBar = styled.div`
    height:calc(100vh - 60px);
    background:#ffffff;
    width:25%;
    position:fixed;
    top:60px;
    right:0;
    z-index:20;
    transition: 0.5s;
    display:none;
    margin-top:5px;
    overflow-y:scroll;
    overflow-x:hidden;
    border-left: 1px solid #ebf3ff;
    @media (max-width: 786px) {
       width:100%;
       position:absolute;
   }
`

const ChatActionButtonWrapper = styled.div`
  width:100%;
  display:flex;
  align-items:center;
  justify-content:space-around;
  margin:15px 15px;
`
const ChatActionButton= styled.button`
  width:35px;
  height:35px;
  background:#f0f2f5;
  border:none;
  border-radius:50%;
  margin-right:5px;
  margin-bottom:5px;
  outline:none;
  :hover{
    cursor:pointer;
  }
`



function openNav(){
  var sidBarInf = document.getElementById('ChatinfoSidenavi');
  var infoActionBtn = document.getElementById('infoAbTn');
  // sidBarInf.style.width='30%';
  sidBarInf.style.display='block';
  infoActionBtn.style.border='4px solid #a3caff'

  var root = document.getElementById('messageView');
  root.style.marginRight='25%';
  root.style.transition= 'margin-right 0.5s';
};

function closeNav(){
  var sidBarInf = document.getElementById('ChatinfoSidenavi');
  var infoActionBtn = document.getElementById('infoAbTn');
  sidBarInf.style.display='none';
  infoActionBtn.style.border='none'
  var root = document.getElementById('messageView');
  root.style.marginRight='0';
  root.style.transition= 'margin-right 0.5s';
};


const tokenUserId = localStorage.getItem("user_id");

const CustomChannelHeader = withChannelContext(
  class CustomChannelHeader extends React.PureComponent {

    constructor(props) {
      super(props);
      //modal state
      this.state = {
        activeIndex: 0,
        };

      this.handleClick = this.handleClick.bind(this);

    }

    handleClick = (e, titleProps) => {
      const { index } = titleProps
      const { activeIndex } = this.state
      const newIndex = activeIndex === index ? -1 : index

      this.setState({ activeIndex: newIndex })
    }

    render() {
      const { activeIndex } = this.state;

      const members = this.props.members;
      var membersArray = Object.keys(members).map((key) => [ members[key]]);

      var dtStr = this.props.channel.data.created_at;
      const createdAt = new Date(dtStr);
      const newCreatedDate = String(createdAt)

      const messagesArray = this.props.messages;

      var newMembersArray = Object.keys(members).map((key) => members[key]);

      //getting array object for the other user in a 2 member conversation
      var othUserObject;
      if (newMembersArray.length < 3 ){
        othUserObject = newMembersArray.find(o => o.user.id !== tokenUserId);
        console.log(othUserObject);
      }

console.log(this.props);
      return (

        <div>
            <ChHeaderWrapper>
                <ChHeadersContent>
                { this.props.channel.data.image && <ChHeaderAvatar src={this.props.channel.data.image}/>}
                  <div>
                      <ChHeaderName>
                        {
                          this.props.channel.data.name ? (
                            this.props.channel.data.name
                          ) : othUserObject ? (
                            othUserObject.user.name
                          ) : ''
                        }
                      </ChHeaderName>
                      <ChHeaderDesc>
                        <FontAwesomeIcon icon={faUser} style={{
                              'color':'#00000080',
                              'fontSize':'12px',
                              'lineHeight':'19px',
                            }}/>
                            <div style={{ 'marginLeft':'4px'}}>
                                {this.props.channel.data.member_count}
                            </div>
                          {this.props.channel.data.description && (
                            <>
                              <span style={{ 'margin':'0 5px','fontSize': '13px'}}>|</span>
                             <div>this.props.channel.data.description.slice(0,43) + '...' </div>
                            </>
                           )
                         }

                      </ChHeaderDesc>
                  </div>
                </ChHeadersContent>
                <div style={{'width': '30%', 'display':'flex','alignItems':'center','justifyContent':'flex-end', 'marginRight':'20px'}}>
                    <SemanticPopup
                      trigger={
                        <ChatActionButton>
                              <FontAwesomeIcon icon={faPhone} style={{
                                  'color':'#006cff',
                                  'fontSize':'15px',
                                }}/>
                          </ChatActionButton>
                      }
                      hoverable
                      wide
                      position='top right'
                      >
                      <div className='GroupVideoPopup'>
                        <h2>Premium feature</h2>
                        <div className='GroupVideoPopupCt'>
                          <img src={groupVideoCall} alt="Group video call"/>
                          <p>Experience seemless group video calls with other members.
                            <span>Feature coming soon!</span>
                          </p>

                        </div>
                      </div>
                    </SemanticPopup>
                    <SemanticPopup
                      trigger={
                        <ChatActionButton id='infoAbTn' onClick={openNav}>
                        <FontAwesomeIcon icon={faInfo} style={{
                          'color':'#006cff',
                          'fontSize':'15px',
                            }}/>
                        </ChatActionButton>
                      }
                      inverted
                      content='Details'
                      position='top left'
                      style={{'borderRadius': '10px','opacity': '0.7',}}
                      />
                </div>

            </ChHeaderWrapper>
            <SideBar id='ChatinfoSidenavi'>
                  <div style={{ 'padding':'0px 10px','borderBottom':'1px solid #ebf3ff', 'height':'50px'}}>
                    <ChHeaderName>Details</ChHeaderName> {/*reusing styled component here*/}
                    <ChHeaderDesc>{this.props.channel.data.name ? (
                        this.props.channel.data.name
                      ) :  othUserObject ? (
                        othUserObject.user.name
                      ) : ''
                    }
                    </ChHeaderDesc>  {/*reusing styled component here*/}

                    <a style={{'color':'#006cff','margin':'10px','fontSize':'13px',
                      'position':'absolute', 'top':'0', 'right':'0', 'width':'25px', 'height':'25px',
                      'borderRadius':'5px', 'background':'#0000001a', 'textAlign':'center', 'padding':'2px'
                      }}
                    href="javascript:void(0)" className="closebtn" onClick={closeNav}>x</a>
                  </div>
                      {
                        othUserObject && (
                          <div className='ChtinfoSVAvatarWrapper'>
                              <div className='ChtinfoSVImgWrapper'>
                                <img src={othUserObject.user.image} className='ChtinfoSVImg' alt={othUserObject.user.name}/>
                              </div>
                          </div>
                        )
                    }

                  <ChatActionButtonWrapper>
                    {this.props.channel.data.name && <AddMember channelID={this.props.channel.id} channelName={this.props.channel.data.name}/> }
                    {this.props.channel.data.name && <RemoveMember channelID={this.props.channel.id} channelMembers={this.props.members}/>}
                    {this.props.channel.data.name && <EditGroupChannel channelData={this.props.channel.data}/>}
                    <LeaveOrDeleteChannel channelID={this.props.channel.id} creatorID={this.props.channel.data.created_by.id}/>

                  </ChatActionButtonWrapper>

                  <Accordion fluid styled>
                      <Accordion.Title
                      active={activeIndex === 0}
                      index={0}
                      onClick={this.handleClick}
                      >
                    <Icon name='dropdown'/>
                            About
                      </Accordion.Title>
                      <Accordion.Content active={activeIndex === 0}>
                          {this.props.channel.data.description && <p style={{'fontSize':'13px', 'background':'#ebf3ff','display':'flex', 'alignItems':'center', 'justifyContent':'start',
                           'borderRadius':'10px', 'padding':'5px'}}>
                          {this.props.channel.data.description && this.props.channel.data.description}
                          </p>}
                          <div style={{'fontFamily':'Arial','fontSize':'12px', 'display':'flex', 'flexDirection':'column'}}>Created on:
                            <span style={{'fontSize':'10px', 'background':'#ebf3ff','display':'flex', 'alignItems':'center', 'justifyContent':'center',
                             'borderRadius':'10px', 'padding':'0 5px', 'height':'50px'}}>
                             {newCreatedDate.slice(0,15)}
                             </span>
                          </div>
                      </Accordion.Content>

                      <Accordion.Title
                      active={activeIndex === 1}
                      index={1}
                      onClick={this.handleClick}
                      >
                            <Icon name='dropdown'/>
                            Members {this.props.channel.data.member_count}
                      </Accordion.Title>
                      <Accordion.Content active={activeIndex === 1}>
                        <div id='chatMembersList' style={{'display':'flex','flexDirection':'column'}}>
                          {membersArray.map((member) => (

                              <div key={member[0].user.id} style ={{'display':'flex','alignItems':'center','flexWrap':'no-wrap'}}>
                                  <div style={{'width':'auto','position':'relative','margin':'5px 10px'}}>
                                  <img src={member[0].user.image} style={{'width':'30px',
                                  'height':'30px', 'borderRadius':'5px','objectFit': 'cover'}}
                                  alt={member[0].user.name}
                                  />
                                  {member[0].user.online === true ? (
                                      <span style={{'position':'absolute', 'top':'-2px',
                                           'right':'-2px','border':'4px solid #ffffff', 'background':'green',
                                           'height':'15px', 'width':'15px', 'borderRadius':'50%'}}
                                       >
                                      </span>
                                      ) : (
                                        <span style={{'position':'absolute', 'top':'-2px',
                                           'right':'-2px','border':'4px solid #ffffff', 'background':'#bababc',
                                           'height':'15px', 'width':'15px', 'borderRadius':'50%'}}
                                         >
                                        </span>
                                      )
                                    }
                                  </div>
                                  <div style={{'display':'flex','flexDirection':'column','fontFamily':'Roboto, Arial', 'fontWeight':'700', 'fontSize':'13px'}}>
                                    {member[0].user.name}
                                    <span style={{'fontSize':'8px'}}> joined on { String(new Date(member[0].user.created_at)).slice(0,15)}</span>
                                  </div>
                              </div>
                          ))}
                        </div>
                      </Accordion.Content>
                      <Accordion.Title
                      active={activeIndex === 2}
                      index={2}
                      onClick={this.handleClick}
                      >
                            <Icon name='dropdown'/>
                            Files
                      </Accordion.Title>
                      <Accordion.Content active={activeIndex === 2}>
                          <div id='chatFilesList'>
                          {messagesArray.map((message) => (

                              message.attachments.length !== 0 ? (
                                  message.attachments[0].type ==='image' ? (

                                    <div key={message.id} style={{'display':'flex','width':'100%' ,
                                    'height':'80px', 'borderRadius':'5px', 'margin':'5px',
                                    'border':'1px solid #0000001a', 'alignItems':'center', 'position':'relative'
                                    }}>
                                        <img src= {message.attachments[0].image_url } style={{'width':'90px','borderRadius':'5px','height':'70px','margin':'5px','objectFit': 'cover'}} download alt='attachment'/>

                                        <div style={{'fontFamily':'Noto Sans Jp, Arial','fontWeight':'700',
                                        'marginLeft':'10px','color':'#767676', 'display':'flex', 'flexDirection':'column'}}>
                                          {message.attachments[0].fallback && '..' + message.attachments[0].fallback.slice(-10)}
                                          <span style={{'fontFamily':'Arial', 'fontSize':'11px', 'fontWeight':'200','color':'#00000066'}}>
                                            {message.user.name } {String(message.created_at).slice(0, 24)}
                                          </span>
                                        </div>
                                        <a href= {message.attachments[0].image_url } style={{
                                          'color':'#141414',
                                          'position':'absolute',
                                          'right':'0',
                                          'marginRight':'5px'
                                        }} download>
                                          <Icon name='long arrow alternate down' style={{'color':'#9a9a9a','fontSize':'17px'}}/>
                                        </a>

                                    </div>

                                  ) : message.attachments[0].type ==='giphy' ? (

                                    <div key={message.id} style={{'display':'flex','width':'100%' ,
                                    'height':'80px', 'borderRadius':'5px', 'margin':'5px',
                                    'border':'1px solid #0000001a', 'alignItems':'center', 'position':'relative'
                                    }}>
                                        <img src= {message.attachments[0].thumb_url } style={{'borderRadius':'5px','margin':'5px','width':'90px',
                                          'height':'70px','flexBasis': '70px','objectFit': 'cover'}} alt='attachment'/>

                                        <div style={{'fontFamily':'Noto Sans Jp, Arial','marginLeft':'10px',
                                        'fontWeight':'700','color':'#767676', 'display':'flex', 'flexDirection':'column'}}>
                                         gif
                                           <span style={{'fontFamily':'Arial', 'fontSize':'10px', 'fontWeight':'200','color':'#00000066'}}>
                                            {message.user.name } {String(message.created_at).slice(0, 24)}
                                           </span>
                                        </div>

                                        <a href= {message.attachments[0].thumb_url } style={{
                                          'color':'#141414',
                                          'position':'absolute',
                                          'right':'0',
                                          'marginRight':'5px'
                                        }} download>
                                          <Icon name='long arrow alternate down' style={{'color':'#9a9a9a','fontSize':'17px'}}/>
                                        </a>
                                    </div>

                                  ) :  message.attachments[0].type ==='file' ? (

                                    <div key={message.id} style={{'display':'flex','width':'100%' ,
                                    'height':'80px', 'borderRadius':'5px', 'margin':'5px',
                                    'border':'1px solid #0000001a', 'alignItems':'center', 'position':'relative'
                                    }}>
                                        <Icon name='file text outline' size='huge' style={{'color':'#13031b',}}/>
                                          <div style={{'color':'#141414','display':'flex', 'flexDirection':'column'}}>
                                             {'..' + message.attachments[0].title.slice(-10) }
                                             <span style={{'fontFamily':'Arial', 'fontSize':'11px', 'fontWeight':'200','color':'#00000066'}}>
                                              {message.user.name } {String(message.created_at).slice(0, 24)}
                                             </span>
                                          </div>
                                          <a href={message.attachments[0].asset_url } style={{
                                            'color':'#141414',
                                            'position':'absolute',
                                            'right':'0',
                                            'marginRight':'5px'
                                          }}>
                                            <Icon name='cloud download' style={{'color':'#9a9a9a','fontSize':'15px'}}/>
                                          </a>
                                    </div>
                                  ) : message.attachments[0].type ==='media' ? (
                                    <div key={message.id} style={{'display':'flex','width':'100%' ,
                                    'height':'80px', 'borderRadius':'5px', 'margin':'5px',
                                    'border':'1px solid #0000001a', 'alignItems':'center', 'position':'relative'
                                    }}>
                                      <video  src= {message.attachments[0].asset_url } style={{'width':'80px','borderRadius':'5px','height':'70px','margin':'5px'}} controls></video>
                                        <div style={{'color':'#141414','display':'flex', 'flexDirection':'column'}}>
                                           {'..' + message.attachments[0].title.slice(-10) }
                                           <span style={{'fontFamily':'Arial', 'fontSize':'11px', 'fontWeight':'200','color':'#00000066'}}>
                                            {message.user.name } {String(message.created_at).slice(0, 24)}
                                           </span>
                                        </div>
                                        <a key={message.id} href={message.attachments[0].asset_url } style={{
                                          'color':'#141414',
                                          'position':'absolute',
                                          'right':'0',
                                          'marginRight':'5px'
                                        }}>
                                          <Icon name='cloud download' style={{'color':'#9a9a9a','fontSize':'15px'}}/>
                                        </a>
                                    </div>
                                  ) : (
                                    <div key={message.id} style={{'display':'flex', 'flexDirection':'column','width':'100%' ,
                                    'height':'80px', 'borderRadius':'5px', 'margin':'5px',
                                    'border':'1px solid #0000001a', 'alignItems':'center', 'position':'relative'
                                    }}>
                                      <div style={{'color':'#141414','display':'flex', 'flexDirection':'column'}}>
                                         {message.attachments[0].title && '..' + message.attachments[0].title.slice(-10) }
                                         <span style={{'fontFamily':'Arial', 'fontSize':'11px', 'fontWeight':'200','color':'#00000066'}}>
                                          {message.user.name } {String(message.created_at).slice(0, 24)}
                                         </span>
                                      </div>
                                      <audio src= {message.attachments[0].asset_url } style={{'width':'100%','borderRadius':'5px','height':'50px','margin':'5px'}} controls />
                                        <a href={message.attachments[0].asset_url } style={{
                                          'color':'#141414',
                                          'position':'absolute',
                                          'right':'0',
                                          'marginRight':'5px'
                                        }}>
                                          <Icon name='cloud download' style={{'color':'#9a9a9a','fontSize':'15px'}}/>
                                        </a>
                                    </div>
                                  )
                                ) : ''

                            ))}

                          </div>
                      </Accordion.Content>
                  </Accordion>
            </SideBar>
        </div>
      );
    }
  },
);

export default CustomChannelHeader;
