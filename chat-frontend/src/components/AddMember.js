import React from "react";
import base from '../baseAddress.js';
import axios from "axios";
import { StreamChat } from "stream-chat";
import { Popup as SemanticPopup,Dropdown} from 'semantic-ui-react';
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faUser} from '@fortawesome/free-regular-svg-icons';
import {faPlus } from '@fortawesome/free-solid-svg-icons';


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
const AddMemberModal = styled(Popup)`
    &-content {
      height:auto;
      border-radius:10px;
      border:1px solid red;
      width:500px !important;
    }
`
const AddMemberModalClose = styled.a`
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
const AddMemberCreateForm= styled.form`
  margin:5px;
  padding:15px;
  height:auto;
  /* overflow-y:hidden; */
`
const AddMemberCreateFormTitle= styled.h1`
  font-family:Noto Sans Jp, Roboto,Arial;
  font-size:15px;
  color:#141414;
  font-weight:700;
  width:100%;
`

const AddMemberCreateFormParag= styled.p`
  font-family:Arial;
  font-size:13px;
  color:#141414;
  font-weight:300;
  width:100%;
`

const AddMemberSubmitButton= styled.button`
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

const tokenUserName = localStorage.getItem("user_name");

const renderLabel = (label) => ({
  color: 'blue',
  content: `${label.text}`,
  icon: 'check',
});

const usersList = []; //stores array of users to be used in dropdown

async function getUsers() { //fetches user from server and appends to usersList
  const users = await axios({
    method: "GET",
    url: `${base}/apis/user/account/list/	`,
    data: null,
    config: {
      headers: { "Content-Type": "application/json" }
    }
  });

  var i;
  for (i = 0; i < users.data.length; i++) {
    var userArray =
      {
        key: users.data[i].username,
        text: users.data[i].username,
        value: users.data[i].id,
        image: { avatar: true, src: 'https://images.unsplash.com/photo-1479936343636-73cdc5aae0c3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=80' },
      };

    usersList.push(userArray);
  }

};

getUsers();

const userToken = localStorage.getItem("token");
const tokenUserId = localStorage.getItem("user_id");
const userAvatar = localStorage.getItem("user_avatar");

class AddMember extends React.Component {
  constructor(props){
    super(props);
    this.state= {
      errors:'',
      open: false,
      usersSelected:'',

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
    this.setState({usersSelected:data.value});
  }

  async handleSubmit(event){
    event.preventDefault();
    const members = this.state.usersSelected;
    //stream client
    const client = new StreamChat("qk4nn7rpcn75");

    await client.setUser(
      {
        id: tokenUserId,
        name: tokenUserName,
        image: base + userAvatar
      },
      userToken,
    );

    const channel = client.channel('team', this.props.channelID, {});
    if (members !==''){
      try{
          await channel.addMembers(members.map(String), { text: members.length + ' members joined the channel.' });
          this.setState({
            errors:'',
            open: false,
            usersSelected:'',
          });
      }
      catch(err){
        this.setState({errors: 'Something went wrong. Cannot add user(s)'});
      }
    } else{
      this.setState({errors: 'Field cannot be empty. Select atleast one user!'});
    }


  };

  render() {
    const channelName = this.props.channelName;
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
                    <FontAwesomeIcon icon={faPlus} style={{
                          'color':'#006cff',
                          'fontSize':'10px',
                          'position':'absolute',
                      }}/>
                </ChatActionButton>
            }
            inverted
            content='Add member'
            position='top center'
            style={{'borderRadius': '10px','opacity': '0.7',}}
            />

            <AddMemberModal open={this.state.open} closeOnDocumentClick onClose={this.closeModal}>
              <div className="DmModal">
                <AddMemberModalClose className="close" onClick={this.closeModal}>
                  &times;
                </AddMemberModalClose>
                <AddMemberCreateForm onSubmit={this.handleSubmit}>
                    <AddMemberCreateFormTitle>Add people</AddMemberCreateFormTitle>
                    <AddMemberCreateFormParag>{channelName}</AddMemberCreateFormParag>
                    <div style={{'display':'flex'}}>
                        <Dropdown
                          placeholder='Add members, choose a contact'
                          fluid
                          search
                          selection
                          clearable
                          multiple
                          options={usersList}
                          scrolling
                          closeOnEscape
                          renderLabel={renderLabel}
                          value= {this.state.usersSelected}
                          onChange= {this.handleChange}
                        />
                        <AddMemberSubmitButton type='submit'>Add</AddMemberSubmitButton>
                    </div>
                    <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "12px","textAlign": "center"}}>
                    {this.state.errors}
                    </span>
                </AddMemberCreateForm>
              </div>
            </AddMemberModal>
        </div>
    )
  }
}

export default AddMember;
