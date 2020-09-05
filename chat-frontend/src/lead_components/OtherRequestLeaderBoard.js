import React, { Component} from "react";
import axios from "axios";
import base from '../baseAddress.js';
import styled from 'styled-components';
import {List, Image,Statistic,Loader } from 'semantic-ui-react';
import avatar from '../static/avatar.png';

const ContentHeader = styled.h4`
  height: 35px;
  position: sticky;
  background-color: #fff;
  border-radius: 20px;
  z-index: 5;
  top: 0px;
  display: flex;
  justify-content: center;
  align-items: center;
  -webkit-box-shadow: 0 1px 3px 0 #63f1eb24, 0 0 0 1px #63f1eb24;
  box-shadow: 0 1px 3px 0 #63f1eb24, 0 0 0 1px #63f1eb24;
`
const LeaderBoard = styled.div`
  width:100%;
  height: 90%;
  border-radius:10px;
  background-color:#fff;
  margin-top:15px;
  padding: 0 10px;
  overflow-y:auto;
  -webkit-box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  @media (max-width: 786px){
    display:flex;
    flex-direction:column;
    justify-content:center;
  }
`

class LeaderPanel extends Component {
    constructor(props){
      super(props);
      this.state = {
      users:[],
      loading:false
      }
    }

    async componentDidMount(){
      this.setState({
        loading:true,
      });
      const usersArray = await axios.get(`${base}/apis/user/account/list/ `)
      await this.setState({
        users:usersArray.data,
        loading:false,
      })
    }
  render() {
    //Returning a new array from leads containing claimer field only
    let claimerArray = this.props.leads.map(a => a.claimer);
    //Returning a new array from leads containing referer field only
    let referalArray = this.props.leads.map(a => a.referrer);

    const users = this.state.users;
    var newUsersArray = [];
    //helper function for counting how many times a user id appears in claimers array
    function countClaims(array, value) {
      return array.reduce((s, a) => s + (Array.isArray(a) ? countClaims(a, value) : a === value), 0);
    }
    //helper function for counting how many times a user id appears in referals array
    function countReferals(array, value) {
      return array.reduce((s, a) => s + (Array.isArray(a) ? countReferals(a, value) : a === value), 0);
    }

    //constructing a new array with added fields
    for (let i = 0; i < users.length; i++ ){
        let array = {
          id:users[i].id,
          username:users[i].username,
          claims:countClaims(claimerArray, users[i].id),
          referals:countReferals(referalArray, users[i].id)
        }
          newUsersArray.push(array);
    }

    //sorting by descending order based on no. of claims
    newUsersArray.sort((a, b) => parseFloat(parseFloat(b.claims) - a.claims));
    //creating top 5 claimers
    var top5users = newUsersArray.slice(0, 10);

    var leaders = top5users.map((user) => {
        return(
          <List.Item key={user.id} >
              <Image avatar src={avatar} />
               <List.Content>
                <List.Header as='a'> {user.username}</List.Header>
                <List.Description>
                    <Statistic.Group size='mini'>
                          <Statistic color='green'>
                            <Statistic.Value style={{'fontSize':'10px'}}>{user.claims}</Statistic.Value>
                            <Statistic.Label style={{'fontSize':'10px'}}>Claims</Statistic.Label>
                          </Statistic>
                          <Statistic color='orange'>
                            <Statistic.Value style={{'fontSize':'10px'}}>{user.referals}</Statistic.Value>
                            <Statistic.Label style={{'fontSize':'10px'}}>Referals</Statistic.Label>
                          </Statistic>
                    </Statistic.Group>
                </List.Description>
              </List.Content>
            </List.Item>
        )

      });
    return (
          <LeaderBoard>
            <ContentHeader>LEADERBORD.</ContentHeader>
            {this.state.loading === true ? (
                <Loader active inline='centered' size='small' />
            ) : (
              <List relaxed='very' style={{"marginTop":'25px'}}>
                    {leaders}
              </List>
            )
            }
          </LeaderBoard>
    );
  }
}

export default LeaderPanel;
