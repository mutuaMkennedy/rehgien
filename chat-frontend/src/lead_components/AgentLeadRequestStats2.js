import React, { PureComponent } from 'react';
import { Statistic } from 'semantic-ui-react';
import styled from 'styled-components';

const StatsBoard = styled.div`
  width:100%;
  height: 20%;
  border-radius:10px;
  background-color:#fff;
  padding: 0 10px;
  overflow-y:auto;
  -webkit-box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  display:flex;
  flex-direction:column;
  justify-content:center;
`

const tokenUserId = localStorage.getItem("user_id");

class AgentRequestStats2 extends PureComponent {

  render(){
    // Helper function to count claims array for current auth.. user
    var claimsArray =  this.props.leads.filter(function(request) {
        return request.claimer.toString() === tokenUserId.toString();
    });
    // Helper function to count referals array for current auth.. user
    var referrersArray =  this.props.leads.filter(function(request) {
        return request.referrer.toString() === tokenUserId.toString();
    });

    return(
          <StatsBoard>
              <Statistic.Group widths='two'>
                  <Statistic color='green'>
                    <Statistic.Value>{claimsArray.length}</Statistic.Value>
                    <Statistic.Label>CLAIMS</Statistic.Label>
                  </Statistic>
                  <Statistic color='orange'>
                    <Statistic.Value>{referrersArray.length}</Statistic.Value>
                    <Statistic.Label>REFERALS</Statistic.Label>
                  </Statistic>
              </Statistic.Group>
          </StatsBoard>
        );
  }
}

export default AgentRequestStats2;
