import React, { Component } from "react";
import base from '../baseAddress.js';
import { StreamChat } from "stream-chat";
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { Popup as SemanticPopup} from 'semantic-ui-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faEdit} from '@fortawesome/free-regular-svg-icons';



const GcWrapper = styled.div`
  display:flex;
  align-items:center;
`

const GcCreateButton = styled.button`
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

const GcModal = styled(Popup)`
    &-content {
      height:auto;
      border-radius:10px;
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


const userToken = localStorage.getItem("token");
const tokenUserId = localStorage.getItem("user_id");
const tokenUserName = localStorage.getItem("user_name");
const userAvatar = localStorage.getItem("user_avatar");

class EditGroupChannel extends Component {
  constructor(props) {
    super(props);
    var cName = this.props.channelData.name;
    var cAbout = this.props.channelData.description;
    this.state = {
      errors:{
        channelName:'' ,
        channelAbout:'',
        stream:''
      },
      open: false,
      channelName: cName && cName.slice(1) ,
      channelAbout:cAbout
    };
    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
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
  }

  async handleSubmit(event){
    event.preventDefault();

    const channelName= this.state.channelName;
    const channelAbout = this.state.channelAbout;

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

    if (channelName !==""){
      if(channelAbout !==""){
            try{
                const channelID = this.props.channelData.id;
                const GroupChannel = await client.channel("team",channelID.toString(), {});

                 await GroupChannel.update({
                   name: "#"+channelName.toString(),
                   image:null,
                   description:channelAbout.toString(),
                 },
                 { text: tokenUserName.toString() + ' changed the channel information.'},
               );

                 //clear form inputs
                 this.setState({
                   channelName:'',
                   channelAbout:'',
                   open:false,

                 })
              }
              catch (err) {
                let errors = {...this.state.errors}
                errors.stream = 'Something went wrong. Cannot update channel, try again later!';
                this.setState({errors});
                //to do : send log report
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
            <FontAwesomeIcon icon={faEdit} style={{
                'color':'#006cff',
                'fontSize':'15px',
              }}/>
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
        >
          <div className="DmModal">
            <GcModalClose className="close" onClick={this.closeModal}>
              &times;
            </GcModalClose>
            <GcCreateForm onSubmit={this.handleSubmit}>
                <GcCreateFormTitle>Update Channel</GcCreateFormTitle>
                <GcCreateFormParag>Edit this channels info.</GcCreateFormParag>
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
                    <div style={{'width':'100%', 'display':'flex', 'justifyContent':'flex-end'}}>
                      <GcSubmitButton type='submit'>Update</GcSubmitButton>
                    </div>
                </div>
            </GcCreateForm>
          </div>
        </GcModal>
      </div>
    );
  }
}

export default EditGroupChannel;
