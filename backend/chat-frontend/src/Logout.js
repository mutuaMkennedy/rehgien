import React, { Component } from "react";
import base from './baseAddress.js';
import axios from "axios";
import styled from 'styled-components';

//

const ActionCard = styled.div`
  width:auto;
  height: 40px;
  border-bottom-right-radius: 30px;
  border-bottom-left-radius: 30px;
`

const LogOutButton = styled.button`
  height:40px;
  line-height:40px;
  display:flex;
  text-align:center;
  background-color:transparent;
  font-size:1.07142857rem;
  color:rgba(0,0,0,.87);
  font-family:Lato,Helvetica Neue,Arial,Helvetica,sans-serif;
  border:0;
  :hover {
    cursor:pointer;
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
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_avatar");

    this.props.history.push("/pro/home");
  }

  render() {
    return (
        <ActionCard>
          <div>
              <form onSubmit={this.logoutStream} >
              <LogOutButton type='submit'>
                 Logout
              </LogOutButton>
              </form>
          </div>
        </ActionCard>
    );
  }
}

export default Logout;
