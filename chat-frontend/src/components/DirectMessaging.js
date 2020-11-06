import React, { Component } from "react";
import base from '../baseAddress.js';
import { StreamChat } from "stream-chat";
import axios from "axios";
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { Dropdown,Icon } from 'semantic-ui-react';
import { Popup as SemanticPopup} from 'semantic-ui-react';
import "./DirectMessaging.css";


const DmWrapper = styled.div`
  display:flex;
  align-items:center;
`

const DmCreateButton = styled.button`
  width:40px;
  height:40px;
  border:none;
  border-radius:50%;
  font-size:14px;
  position:relative;
  background:transparent;
  border:none;
  :hover {
    cursor:pointer;
}
`

const DmModal = styled(Popup)`
    z-index:1002 !important;
    @media (max-width:768px) {
      width:100% !important;
      height:auto !important;
    };
    &-content {
      height:auto;
      border-radius:10px;
    }

`
const DmModalClose = styled.a`
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
const DmCreateForm= styled.form`
  margin:5px;
  padding:15px;
  height:350px;
  overflow-y:hidden;
`
const DmCreateFormTitle= styled.h1`
  font-family:Noto Sans Jp, Roboto,Arial;
  font-size:25px;
  color:#141414;
  font-weight:500;
  width:100%;
`

const DmSubmitButton= styled.button`
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
const tokenUserName = localStorage.getItem("user_name");
const userAvatar = localStorage.getItem("user_avatar");

class DirectMessage extends Component {
  constructor(props) {
    super(props);
    //modal state
    this.state = {
      errors:'',
      open: false,
      value:'',
      };

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
    this.setState({value:data.value});
  }

  async handleSubmit(event){
    event.preventDefault();
    const contactId = this.state.value;

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
    //Private chat Initialization
    if (contactId !== ''){
      try{
          const PrivateMessage = client.channel('team', {
          members: [contactId.toString(),tokenUserId.toString()],
          });
          await PrivateMessage.create();
           //clear input and modal
           this.setState({
             errors:'',
             open: false,
             value:'',
           });
      }catch(err){
        this.setState({
          errors:'Something went wrong. Cannot create converstion,try again later!',
        })
      }

    } else{
      this.setState({
        errors:'Field cannot be empty. Select a user!',
      })
    }

  };

  render() {
    return (
      <div>
        <DmWrapper>
        <SemanticPopup
          trigger={
            <DmCreateButton onClick={this.openModal}>
              <Icon name='edit outline' style={{'color':'#fff','fontSize':'13px','margin':'0'}}/>
            </DmCreateButton>
          }
          inverted
          content='Direct message'
          position='top left'
          style={{'borderRadius': '10px',}}
          />

        </DmWrapper>

        <DmModal
          open={this.state.open}
          closeOnDocumentClick
          onClose={this.closeModal}
          className='DmChModal'
        >
          <div className="DmModal">
            <DmModalClose className="close" onClick={this.closeModal}>
              &times;
            </DmModalClose>
            <DmCreateForm onSubmit={this.handleSubmit}>
                <DmCreateFormTitle>Direct Messages</DmCreateFormTitle>
                <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px","textAlign": "center"}}>
                {this.state.errors}
                </span>
                <div style={{'display':'flex'}}>
                    <Dropdown
                      placeholder='Start a converstion, choose a contact'
                      fluid
                      search
                      selection
                      clearable
                      options={usersList}
                      open
                      scrolling
                      closeOnEscape
                      renderLabel={renderLabel}
                      value= {this.state.value}
                      onChange= {this.handleChange}
                    />
                    <DmSubmitButton type='submit'>Create</DmSubmitButton>
                </div>
            </DmCreateForm>
          </div>
        </DmModal>
      </div>
    );
  }
}

export default DirectMessage;
