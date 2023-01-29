import React from "react";
import base from '../baseAddress.js';
import { StreamChat } from "stream-chat";
import { Popup as SemanticPopup,Dropdown} from 'semantic-ui-react';
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faUser} from '@fortawesome/free-regular-svg-icons';
import {faMinus } from '@fortawesome/free-solid-svg-icons';


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

const RemoveMemberModal = styled(Popup)`
    &-content {
      height:auto;
      border:1px solid red;
      width:500px !important;
    }
`
const RemoveMemberModalClose = styled.a`
  height:35px;
  width:35px;
  border-radius: 3px;
  font-size:40px;
  position:absolute;
  text-align:center;
  top:15px;
  right:15px;
  color:#d1d1d1;
  :hover{
    cursor:pointer;
    transform:scale(1.2);
    color:#d3d3d3;
  }
`
const RemoveMemberCreateForm= styled.form`
  margin:5px;
  padding:15px;
  height:auto;
  /* overflow-y:hidden; */
`
const RemoveMemberCreateFormTitle= styled.h1`
  font-family:Noto Sans Jp, Roboto,Arial;
  font-size:15px;
  color:#141414;
  font-weight:700;
  width:100%;
`

const RemoveMemberSubmitButton= styled.button`
  border:1px solid #00ffd5;
  height:40px;
  border-radius:5px;
  margin-left:5px;
  font-family:Noto Sans Jp, Roboto, Arial;
  background-color:#ffffff;
  :hover{
      background-color:#00ffd5;
      cursor:pointer;
  }
`

const renderLabel = (label) => ({
  color: 'blue',
  content: `${label.text}`,
  icon: 'check',
});

const channelMembers=[]; //storing channel members for dropdown

const tokenUserName = localStorage.getItem("user_name");
const userToken = localStorage.getItem("token");
const tokenUserId = localStorage.getItem("user_id");
const userAvatar = localStorage.getItem("user_avatar");

class RemoveMember extends React.Component {
  constructor(props){
    super(props);
    this.state= {
      errors:'',
      open: false,
      membersSelectedID:'',

    }

    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  openModal() {
  this.setState({ open: true });
  }
  closeModal() {
    this.setState({ open: false });
  }


  handleChange(event,data){
    const value = data.value;
    this.setState(
      {
        membersSelectedID:value,
      }
    );
  }

  async handleSubmit(event){
    event.preventDefault();
    const membersID = this.state.membersSelectedID;

    //stream client
    const client = new StreamChat("krfpqyntmyk8");

    await client.setUser(
      {
        id: tokenUserId,
        name: tokenUserName,
        image: base + userAvatar
      },
      userToken,
    );

      const channel = client.channel('team', this.props.channelID, {});
    if (membersID !== ''){
      try{
        await channel.removeMembers(membersID.map(String), { text: membersID.length + ' members left the channel'});
        this.setState({
          errors:'',
          open: false,
          membersSelectedID:'',
        });
      }
      catch (err){
        this.setState({errors: 'Something went wrong. Cannot remove user(s)'});
      }
    } else{
      this.setState({errors: 'Field cannot be empty. Select atleast one member!'});
    }

  };

  componentDidMount(){
    const members = this.props.channelMembers;
    const membersArray = Object.keys(members).map((key) => [ members[key]]);

    var i;
    for (i = 0; i < membersArray.length; i++) {
      var newMembersArray =
        {
          key: membersArray[i][0].user.name,
          text: membersArray[i][0].user.name,
          value: membersArray[i][0].user.id,
          image: { avatar: true, src: membersArray[i][0].user.image },
        };

      channelMembers.push(newMembersArray);
    }

  };

  render() {
    return (
      <div>
            <SemanticPopup
              trigger={
                <ChatActionButton onClick={this.openModal}>
                <FontAwesomeIcon icon={faUser} style={{
                    'color':'#006cff',
                    'fontSize':'15px',
                    'lineHeight':'19px',
                  }}/>
                  <FontAwesomeIcon icon={faMinus} style={{
                        'color':'#006cff',
                        'fontSize':'10px',
                        'position':'absolute',
                    }}/>
                </ChatActionButton>
              }
              inverted
              content='Remove member'
              position='top center'
              style={{'borderRadius': '10px','opacity': '0.7',}}
              />

              <RemoveMemberModal
                  open={this.state.open}
                  closeOnDocumentClick
                  onClose={this.closeModal}
                >
                <div className="DmModal">
                  <RemoveMemberModalClose className="close" onClick={this.closeModal}>
                    &times;
                  </RemoveMemberModalClose>
                  <RemoveMemberCreateForm onSubmit={this.handleSubmit}>
                      <RemoveMemberCreateFormTitle>Remove Member/s</RemoveMemberCreateFormTitle>
                      <div style={{'display':'flex'}}>
                          <Dropdown
                            placeholder='Remove member/s from this conversation'
                            fluid
                            search
                            selection
                            clearable
                            multiple
                            options={channelMembers}
                            scrolling
                            closeOnEscape
                            renderLabel={renderLabel}
                            value= {this.state.membersSelectedID}
                            onChange= {this.handleChange}
                          />
                          <RemoveMemberSubmitButton type='submit'>Remove</RemoveMemberSubmitButton>
                      </div>
                      <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "12px","textAlign": "center"}}>
                      {this.state.errors}
                      </span>
                  </RemoveMemberCreateForm>
                </div>
              </RemoveMemberModal>
        </div>
    )
  }
}

export default RemoveMember;
