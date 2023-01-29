import React, { Component } from 'react'
import { Tab,Item,Message,Button } from 'semantic-ui-react'
import axios from "axios";
import base from '../baseAddress.js';
import styled from 'styled-components';

const CustomItemGroup = styled(Item.Group)`
  display:flex;
  justify-content: flex-start;
  align-items:top;
  background-color:#d0f3e969;
  padding:10px;
  @media (max-width: 786px){
    flex-direction: column;
  }
`

const authToken = localStorage.getItem("auth_token");
const tokenUserId = localStorage.getItem("user_id");

export default class OtherRequestModalContent extends Component {
  constructor(props){
    super(props);
    this.state = {
      show:false,
    }
    this.handleClaim = this.handleClaim.bind(this);
  }

  handleClaim (event){
    event.preventDefault();
    const pk = this.props.details.id;
    try {
        const claimLead = axios({
          method: "PATCH",
          url: `${base}/apis/markets/other_service_request/${pk}/cl_or_re/ `,
          data: {
            claimer:[tokenUserId],
          },
          config: {
            headers: { "Content-Type": "application/json","Authorization":`Token ${authToken}` }
          }
        });
        this.setState({
          show:true
        })
      }
      catch(e){
        console.log(e);
      }
  }

  render() {
    const panes = [
      { menuItem: 'Request Info', render: () =>(
        <Tab.Pane>
        {this.props.details.qualified === true ? (
          <Message
            size='tiny'
            success
            header='This lead has been Qualified.'
            content='We have confirmed the client details & motivation to convert.'
          />
        ) : (
          <Message
            size='tiny'
            warning
            header='This lead has not been Qualified.'
            content="We are yet to qualify this client."
          />
        )
      }
          <h4>Basic Information</h4>
          <CustomItemGroup relaxed='very'>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Location</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyLoc' style={{'fontSize':'13px'}}>{this.props.details.location}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
          </CustomItemGroup>
          <h4>Timeline</h4>
          <CustomItemGroup relaxed='very'>
                 <Item>
                   <Item.Content>
                     <Item.Header style={{'fontSize':'14px'}}>Pro needed before.</Item.Header>
                     <Item.Meta>
                       <span className='rqdlProTimeline' style={{'fontSize':'13px'}}>{this.props.details.timeline} - {(this.props.timeRemaining === 0 ? 'Expired' : `${this.props.timeRemaining} days remaining.`)}</span>
                     </Item.Meta>
                   </Item.Content>
                 </Item>
         </CustomItemGroup>
          <h4>Extra Notes from the client.</h4>
          <Item.Group relaxed='very' style={{'backgroundColor':'#d0f3e969','padding':'10px'}}>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Service details</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyAdetails' style={{'fontSize':'13px'}}>{this.props.details.service_details}</span>
                    </Item.Meta>
                  </Item.Content>
              </Item>
          </Item.Group>
        </Tab.Pane>
      )
      },
      { menuItem: 'Contact Info', render: () => (
          <Tab.Pane>
          {this.props.details.qualified === true ? (
            <Message
             size='tiny'
              success
              header='This lead has been Qualified.'
              content='We have confirmed the client details & motivation to convert.'
            />
          ) : (
            <Message
             size='tiny'
              warning
              header='This lead has not been Qualified.'
              content="We are yet to qualify this client."
            />
          )
        }
        { this.state.show === false ? (
          <form onSubmit={this.handleClaim}>
            <Button
              type='submit'
              icon='check'
              content='Show contact information.'
            />
          </form>
          ) : (
            <>
              <h4>Client Names</h4>
               <CustomItemGroup relaxed='very'>
                       <Item>
                         <Item.Content>
                           <Item.Header style={{'fontSize':'14px'}}>Name</Item.Header>
                           <Item.Meta>
                             <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{this.props.details.name}</span>
                           </Item.Meta>
                         </Item.Content>
                       </Item>
               </CustomItemGroup>
               <h4> Phone and Email</h4>
               <CustomItemGroup relaxed='very'>
                   <Item>
                     <Item.Content>
                       <Item.Header style={{'fontSize':'14px'}}>Phone</Item.Header>
                       <Item.Meta>
                         <span className='rqplPropertyGfeatures' style={{'fontSize':'13px'}}>{this.props.details.phone}</span>
                       </Item.Meta>
                     </Item.Content>
                  </Item>
                   <Item>
                     <Item.Content>
                       <Item.Header style={{'fontSize':'14px'}}>Email</Item.Header>
                       <Item.Meta>
                         <span className='rqplContactName' style={{'fontSize':'13px'}}>{this.props.details.email}</span>
                       </Item.Meta>
                     </Item.Content>
                   </Item>
               </CustomItemGroup>
               </>
             )
           }
          </Tab.Pane>
      )
      },
    ]
    return (
      <Tab menu={{ fluid: true,tabular: false, secondary:true }} panes={panes} defaultActiveIndex={0}/>
    )
  }
}
