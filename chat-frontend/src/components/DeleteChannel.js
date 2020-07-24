import React from "react";
import base from '../baseAddress.js';
import { StreamChat } from "stream-chat";
import { Popup as SemanticPopup} from 'semantic-ui-react';
import styled from 'styled-components';
import Popup from "reactjs-popup";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faTrashAlt} from '@fortawesome/free-regular-svg-icons';

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

const DeleteChannelModal = styled(Popup)`
    &-content {
      height:auto;
      border-radius:10px;
      width:500px !important;
    }
`
const DeleteChannelModalClose = styled.a`
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
const DeleteChannelForm= styled.form`
  margin:5px;
  padding:15px;
  height:auto;
  /* overflow-y:hidden; */
`
const DeleteChannelFormTitle= styled.h1`
  font-family:Noto Sans Jp, Roboto,Arial;
  font-size:15px;
  color:#141414;
  font-weight:700;
  width:100%;
`

const DeleteChannelFormParag= styled.p`
  font-family:Arial;
  font-size:14px;
  color:#141414;
  font-weight:300;
  width:100%;
`

const DeleteChannelSubmitButton= styled.button`
  border:1px solid #00ffd5;
  height:40px;
  border-radius:5px;
  margin-left:5px;
  font-family:Noto Sans Jp, Roboto, Arial;
  background-color:#ffffff;
  :hover{
      background-color:#db2828;
      cursor:pointer;
      border:none;
  }
`


const tokenUserName = localStorage.getItem("user_name");
const userToken = localStorage.getItem("token");
const tokenUserId = localStorage.getItem("user_id");
const userAvatar = localStorage.getItem("user_avatar");

class LeaveOrDeleteChannel extends React.Component {
  constructor(props){
    super(props);
    this.state= {
      errors:'',
      open: false,

    }

    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  openModal() {
  this.setState({ open: true });
  }
  closeModal() {
    this.setState({ open: false });
  }

  async handleSubmit(event){
    event.preventDefault();
    const client = new StreamChat("ke9puq24fsgq");
    await client.setUser(
      {
        id: tokenUserId,
        name: tokenUserName,
        image: base + userAvatar
      },
      userToken,
    );

      const channel = client.channel('team', this.props.channelID, {});
      const creator = this.props.creatorID;

      if ( creator.toString() === tokenUserId.toString() ){
        try{
            await channel.delete();

            this.setState({
              errors:'',
              open: false,
            });
        }
        catch(err){
          this.setState({
            errors:'Unable to delete channel. Try again later!',
          });
          //To do: send log report
        }
      } else{
        try{
          await channel.removeMembers([tokenUserId.toString()], { text: tokenUserName + ' left the channel'});
          this.setState({
            errors:'',
            open: false,
          });
        }
        catch (err){
          this.setState({errors: 'Unable to remove you from channel. Try again later!'});
        }
    }

  };

  render() {
    const creatorID = this.props.creatorID;
    return (
      <div>
            <SemanticPopup
              trigger={
                <ChatActionButton onClick={this.openModal}>
                    <FontAwesomeIcon icon={faTrashAlt} style={{
                        'color':'#006cff',
                        'fontSize':'15px',
                      }}/>
                </ChatActionButton>
              }
              inverted
              content='Delete conversation'
              position='top right'
              style={{'borderRadius': '10px','opacity': '0.7',}}
              />

              <DeleteChannelModal
                  open={this.state.open}
                  closeOnDocumentClick
                  onClose={this.closeModal}
                >
                <div className="DmModal">
                  <DeleteChannelModalClose className="close" onClick={this.closeModal}>
                    &times;
                  </DeleteChannelModalClose>
                      <DeleteChannelForm onSubmit={this.handleSubmit}>
                      {
                        creatorID !=null && (
                          creatorID.toString() === tokenUserId.toString() ? (
                            <DeleteChannelFormTitle>Delete channel</DeleteChannelFormTitle>
                          ) : (
                            <DeleteChannelFormTitle>Leave channel</DeleteChannelFormTitle>
                          )
                      )
                      }

                      { creatorID && (
                            creatorID.toString() === tokenUserId.toString() ? (
                            <DeleteChannelFormParag>
                            Are you sure you want to delete this channel? This action is permanent
                            and all data will be lost.
                            </DeleteChannelFormParag>
                            ) : (
                              <DeleteChannelFormParag>
                              Are you sure you want to leave this channel?
                              </DeleteChannelFormParag>
                            )
                      )
                      }

                      <div style={{'display':'flex','flexDirection':'column', 'justifyContent':'center'}}>

                      <span id="addError" style={{"color": "#db2828","fontFamily": "Arial","fontSize": "12px","textAlign": "center"}}>
                      {this.state.errors}
                      </span>

                      { creatorID && (
                            creatorID.toString() === tokenUserId.toString() ? (
                              <DeleteChannelSubmitButton type='submit'>Delete</DeleteChannelSubmitButton>
                            ) : (
                            <DeleteChannelSubmitButton type='submit'>Leave</DeleteChannelSubmitButton>
                          )
                        )
                      }
                      </div>
                  </DeleteChannelForm>
                </div>
              </DeleteChannelModal>
        </div>
    )
  }
}

export default LeaveOrDeleteChannel;
