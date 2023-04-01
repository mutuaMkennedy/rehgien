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

export default class AgentPropertyRequestModalContent extends Component {
  constructor(props){
    super(props);
    this.state = {
      show:false,
    }
    this.handleClaim = this.handleClaim.bind(this);
  }

  handleClaim (event){
    event.preventDefault();
    const pk = this.props.details.pk;
    try {
        const claimLead = axios({
          method: "PATCH",
          url: `${base}/apis/markets/agent_property_request/${pk}/cl_or_re/ `,
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
      { menuItem: 'Property Info', render: () =>(
        <Tab.Pane>
        {this.props.details.qualified === true ? (
          <Message
            size='tiny'
            success
            header='This lead has been Qualified.'
            content='We have confirmed the lead details.'
          />
        ) : (
          <Message
            size='tiny'
            warning
            header='This lead has not been Qualified.'
            content="We are yet to qualify this lead."
          />
        )
      }
          <h4>Basic Information</h4>
          <CustomItemGroup relaxed='very'>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Location</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyLoc' style={{'fontSize':'13px'}}>{this.props.details.location_name}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Property Type</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyType' style={{'fontSize':'14px'}}>{this.props.details.property_type}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>

                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Budget</Item.Header>
                    <Item.Meta>
                      <span className='rqplPrice' style={{'fontSize':'13px'}}>Ksh: {this.props.details.min_price} - {this.props.details.max_price}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Market Value</Item.Header>
                    <Item.Meta>
                      <span className='rqplmv' style={{'fontSize':'13px'}}>Ksh: {this.props.details.market_value}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
          </CustomItemGroup>
          <h4>Ownership & Timeline</h4>
          <CustomItemGroup relaxed='very'>
                 <Item>
                   <Item.Content>
                     <Item.Header style={{'fontSize':'14px'}}>Nature of ownership.</Item.Header>
                     <Item.Meta>
                       <span className='rqplPropertyownership' style={{'fontSize':'13px'}}>Looking to {this.props.details.ownership}</span>
                     </Item.Meta>
                   </Item.Content>
                 </Item>
                 <Item>
                   <Item.Content>
                     <Item.Header style={{'fontSize':'14px'}}>Property needed before.</Item.Header>
                     <Item.Meta>
                       <span className='rqplPropertyownership' style={{'fontSize':'13px'}}>{this.props.details.timeline} - {(this.props.timeRemaining === 0 ? 'Expired' : `${this.props.timeRemaining} days remaining.`)}</span>
                     </Item.Meta>
                   </Item.Content>
                 </Item>
         </CustomItemGroup>
         <h4>Property Features</h4>
          <CustomItemGroup relaxed='very'>
                  <Item>
                    <Item.Content>
                      <Item.Header style={{'fontSize':'14px'}}>Property Size</Item.Header>
                      <Item.Meta>
                        <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{this.props.details.property_size} sqm</span>
                      </Item.Meta>
                    </Item.Content>
                  </Item>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Beds</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{this.props.details.max_beds} - {this.props.details.min_beds}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
              <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>General Features</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyGfeatures' style={{'fontSize':'13px'}}>{this.props.details.general_features}</span>
                    </Item.Meta>
                  </Item.Content>
               </Item>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Parking options</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyPfeatures' style={{'fontSize':'13px'}}>{this.props.details.parking_choices}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Number of units needed.</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyNunits' style={{'fontSize':'13px'}}>{this.props.details.number_of_units}</span>
                    </Item.Meta>
                  </Item.Content>
                </Item>
          </CustomItemGroup>
          <h4>Extra Notes from this Agent.</h4>
          <Item.Group relaxed='very' style={{'backgroundColor':'#d0f3e969','padding':'10px'}}>
                <Item>
                  <Item.Content>
                    <Item.Header style={{'fontSize':'14px'}}>Additional details</Item.Header>
                    <Item.Meta>
                      <span className='rqplPropertyAdetails' style={{'fontSize':'13px'}}>{this.props.details.additional_details}</span>
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
              content="We are yet to qualify this lead."
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
                         <span className='rqplPropertyPfeatures' style={{'fontSize':'13px'}}>{this.props.details.email}</span>
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
