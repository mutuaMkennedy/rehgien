import React, { Component } from "react";
import base from '../baseAddress.js';
import { v4 as uuidv4 } from 'uuid';
import { StreamChat } from "stream-chat";
import axios from "axios";
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { Dropdown,Icon } from 'semantic-ui-react';
import { Popup as SemanticPopup} from 'semantic-ui-react';



const GcWrapper = styled.div`
  display:flex;
  align-items:center;
`

const GcCreateButton = styled.button`
  width:40px;
  height:40px;
  border:none;
  border-radius:50%;
  font-size:14px;
  position:relative;
  background:transparent;
  display:flex;
  justify-content:center;
  align-items:center;
  border:none;
  :hover {
    cursor:pointer;
    color:blue;
}
`

const GcModal = styled(Popup)`
    z-index:1002 !important;
    @media (max-width:768px) {
      width:100% !important;
      height:auto !important;
    };
    &-content {
      /* border-radius:10px; */
      width:500px !important;
      height:auto !important;
    }
`
const GcModalClose = styled.a`
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
const GcCreateForm= styled.form`
  margin:5px;
  padding:15px;
  height:auto;
`
const GcCreateFormTitle= styled.h1`
  font-family:Noto Sans Jp, Roboto,Arial;
  font-size:25px;
  color:#141414;
  font-weight:500;
  width:100%;
`
const GcCreateFormParag= styled.p`
  font-family:Arial;
  font-size:14px;
  color:#141414;
  font-weight:300;
  width:100%;
`

const GcInputWrapper= styled.div`
  border:2px solid #00ffd5;
  height:50px;
  width:100%;
  border-radius:5px;
  background-color:#ffffff;
  padding:5px;
  margin-bottom:10px;
  :hover{
      cursor:pointer;
  }
`
const GcInputLabel= styled.label`
  color:#141414;
  font-family:Roboto, Arial;
  font-weight:200;
  font-size:15px;
`

const GcInput= styled.input`
  height:40px;
  width:100%;
  border:none;
  background-color:#ffffff;
  :hover{
    cursor:pointer;
  }
  outline:none;
`

const GcSubmitButton= styled.button`
  border:1px solid #00ffd5;
  border-radius:5px;
  width:100px;
  height:45px;
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
})

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

class GroupChannel extends Component {
  constructor(props) {
    super(props);
    //modal state
    this.state = {
      errors:{
        channelName:'',
        channelAbout:'',
        membersSelected:'',
        stream:''
      },
      open: false,
      channelName:'',
      channelAbout:'',
      membersSelected:''
    };
    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleDropdownChange = this.handleDropdownChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  openModal() {
  this.setState({ open: true });
  }
  closeModal() {
    this.setState({ open: false });
  }

  handleInputChange(event){
    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]:value,
    });
    // console.log(this.state.channelName + ' ' + this.state.channelAbout );
  }
  handleDropdownChange(event,data){
    var options = data.value;
              var value = [];
              for (var i = 0; i < options.length; i++) {
                if (options[i]) {
                  value.push(options[i]);
                }
              }
              this.setState({membersSelected: value});
  }
  async handleSubmit(event){
    event.preventDefault();
    const members = this.state.membersSelected;

    if (members !==''){
      members.push(tokenUserId); //apending session user id to members
    }

    const channelName= this.state.channelName;
    const channelAbout = this.state.channelAbout;

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

    if (channelName !==""){
      if(channelAbout !==""){
          if(members !==''){
            try{
                const uchannelID = uuidv4();
                const GroupChannel = await client.channel("team",uchannelID.toString(), {
                  name: "#"+channelName.toString(),
                  image:null,
                  description:channelAbout.toString(),
                  members: members.map(String),
                });

                 await GroupChannel.create();
                 await GroupChannel.watch();

                 //clear form inputs
                 this.setState({
                   channelName:'',
                   channelAbout:'',
                   membersSelected:'',
                   open:false,

                 })
              }
              catch (err) {
                let errors = {...this.state.errors}
                errors.stream = 'Something went wrong. Cannot create channel, try again later!';
                this.setState({errors});
                //to do : send log report
              };

          } else{
            let errors = {...this.state.errors}
            errors.membersSelected = 'Add atleast one member!';
            this.setState({errors});
          };
      }else{
        let errors = {...this.state.errors}
        errors.channelAbout = 'Field cannot be empty. Add a description of your channel!';
        this.setState({errors});
      };
    } else{
      let errors = {...this.state.errors}
      errors.channelName = 'Field cannot be empty. Add a name to your channel!';
      this.setState({errors});
    };

  };

  render() {
    return (
      <div>
        <GcWrapper>
        <SemanticPopup
          trigger={
            <GcCreateButton onClick={this.openModal}>
              <Icon name='comments outline' style={{'color':'#fff','fontSize':'13px', 'margin':'0'}}/>
            </GcCreateButton>
          }
          inverted
          content='Group conversation'
          position='top left'
          style={{'borderRadius': '10px',}}
          />
        </GcWrapper>

        <GcModal
          open={this.state.open}
          closeOnDocumentClick
          onClose={this.closeModal}
          className='GchannelModal'
        >
          <div className="DmModal">
            <GcModalClose className="close" onClick={this.closeModal}>
              &times;
            </GcModalClose>
            <GcCreateForm onSubmit={this.handleSubmit}>
                <GcCreateFormTitle>Create a Channel</GcCreateFormTitle>
                <GcCreateFormParag>Channels are where you communicate with other members. Channels
                are ussually based on groups, discussions or even trends.</GcCreateFormParag>
                <div style={{'display':'flex', 'flexDirection':'column'}}>
                    <GcInputLabel htmlFor='channelName'>Name</GcInputLabel>
                    <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px","textAlign": "center"}}>
                    {this.state.errors.channelName}
                    </span>
                    <GcInputWrapper>
                      <GcInput id='channelName' name='channelName' value={this.state.channelName} onChange={this.handleInputChange} type='text' placeholder='e.g share-leads, nicNacs...'/>
                    </GcInputWrapper>
                    <GcInputLabel htmlFor='channelAbout'>Description</GcInputLabel>
                    <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px","textAlign": "center"}}>
                    {this.state.errors.channelAbout}
                    </span>
                    <GcInputWrapper>
                      <GcInput id='channelAbout' name='channelAbout' value={this.state.channelAbout} onChange={this.handleInputChange} type='text' placeholder='What this channel is about?'/>
                    </GcInputWrapper>
                    <div style={{'width':'100%','height':'100px'}}>
                      <p style={{'fontFamily':'Roboto,Arial', 'fontWeight':'200'}}>Add some members</p>
                      <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px","textAlign": "center"}}>
                      {this.state.errors.membersSelected}
                      </span>
                      <Dropdown
                        placeholder='Search for members'
                        fluid
                        search
                        multiple
                        name='membersSelected'
                        selection
                        clearable
                        options={usersList}
                        scrolling
                        closeOnEscape
                        renderLabel={renderLabel}
                        value={this.state.membersSelected}
                        onChange= {this.handleDropdownChange}
                      />
                    </div>
                    <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "12px","textAlign": "center"}}>
                    {this.state.errors.stream}
                    </span>
                    <div style={{'width':'100%', 'display':'flex', 'justifyContent':'flex-end'}}>
                      <GcSubmitButton type='submit'>Create</GcSubmitButton>
                    </div>
                </div>
            </GcCreateForm>
          </div>
        </GcModal>
      </div>
    );
  }
}

export default GroupChannel;
