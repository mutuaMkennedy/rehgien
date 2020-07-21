import React, { Component } from "react";
import base from './baseAddress.js';
import axios from "axios";
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPowerOff} from '@fortawesome/free-solid-svg-icons';
import { Popup as SemanticPopup} from 'semantic-ui-react';

//

const ActionCard = styled.div`
  display: flex;
  flex-direction: column;
  width:100%;
  height: 20vh;
  position:relative;
  justify-content: center;
  align-items: center;
  background: #13031b;
  border-bottom-right-radius: 30px;
  border-bottom-left-radius: 30px;
`

const LogOutButton = styled.button`
  width:40px;
  height:40px;
  text-align:center;
  background-color:transparent;
  font-size:15px;
  color:#ffffff;
  font-family:Arial;
  border:0;
  border-radius:50%;
  :hover {
    cursor:pointer;
    transform: scale(1.3);
      background-color:#006cff5c;
  }
`

//

class Logout extends Component {

  async logoutStream() {

    axios.post(base+'/apis/rest-auth/logout/',null)
    .then(function (response) {
      console.log('success');
    })
    .catch(function (error) {
      console.log(error);
    });
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_avatar");

    this.props.history.push("/auth/login");
  }

  render() {
    return (
        <ActionCard>
          <div>
              <form onSubmit={this.logoutStream} >
              <SemanticPopup
                trigger={
                  <LogOutButton type='submit'>
                    <FontAwesomeIcon icon={faPowerOff} style={{
                          'color':'#ffffff',
                        }}/>
                  </LogOutButton>
                }
                inverted
                content='Logout'
                position='top left'
                style={{'borderRadius': '10px', 'color':'red', 'fontWeight':'bold'}}
                />
              </form>
          </div>
        </ActionCard>
    );
  }
}

export default Logout;
