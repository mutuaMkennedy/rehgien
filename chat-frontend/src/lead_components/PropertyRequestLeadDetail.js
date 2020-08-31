import React, { useState,useEffect } from 'react';
import {
  EmailShareButton,
  FacebookShareButton,
  LinkedinShareButton,
  TelegramShareButton,
  TwitterShareButton,
  ViberShareButton,
  WhatsappShareButton,
  WorkplaceShareButton
} from "react-share";
import {
  EmailIcon,
  FacebookIcon,
  LinkedinIcon,
  TelegramIcon,
  TwitterIcon,
  ViberIcon,
  WhatsappIcon,
  WorkplaceIcon
} from "react-share";
import {
  FacebookShareCount,
} from "react-share";
import { Tab,Item,Message,Statistic,Button,Modal } from 'semantic-ui-react'
import axios from "axios";
import styled from 'styled-components';
import base from '../baseAddress.js';
import {useParams} from "react-router-dom";
import LeadNotFound from './LeadDoesNotExist.js'


const LeadDetailWrapper = styled.div`
  width:100%;
  height:calc(100vh - 45px);
  padding:10px;
  background:#fff;
`
const LeadElementsBox = styled.div`
  width:70%;
  height:80%;
  background-color:#fff;
  margin-left:auto;
  margin-right:auto;
`

const LeadDetailContainer = styled.div`
  height:100%;
  background-color:#fff;
  overflow-y:auto;
  padding:10px;
`

const authToken = localStorage.getItem("auth_token");
const tokenUserId = localStorage.getItem("user_id");

function PropertyRequestLeadDetail() {
  const [lead, setLead] = useState([]);
  const [isLoaded, setLoaded] = useState(false);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [show, setShow] = useState(false);


  let { id } = useParams();
  useEffect(() => {
    async function fetchData(){
      try {
        const rq_property_lead = await axios.get(`${base}/apis/markets/request_property/${id}/ `);
        setLead(rq_property_lead.data);
        setLoaded(true);
      }
      catch(err){
        setError('Item does not exist');
        setLoaded(true);
      }
    }
    fetchData();
  },[]);

  function openModal() {
    setOpen(true)
  };

  const handleClaim = (event) => {
    event.preventDefault();
    try {
        const claimLead = axios({
          method: "PATCH",
          url: `${base}/apis/markets/request_property/${id}/cl_or_re/ `,
          data: {
            claimer:[tokenUserId],
          },
          config: {
            headers: { "Content-Type": "application/json","Authorization":`Token ${authToken}` }
          }
        });
        setShow(true);
      }
      catch(e){
        console.log(e);
      }
  }

  const handleRefer = (event) => {
    event.preventDefault();
    const referLead = axios({
      method: "PATCH",
      url: `${base}/apis/markets/request_property/${id}/cl_or_re/ `,
      data: {
        referrer:[tokenUserId],
      },
      config: {
        headers: { "Content-Type": "application/json","Authorization":`Token ${authToken}` }
      }
    });
    setOpen(false);

  }

  function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [day, month, year].join('-');
  }
  //calculating no. of Days remaining before lead expires
    var date_today = new Date();
        date_today = formatDate(String(date_today).slice(0,15))
    var lead_timeline = lead.timeline;
        lead_timeline = formatDate(lead_timeline)

    var new_date = new Date(date_today.split('-')[2],date_today.split('-')[1]-1,date_today.split('-')[0]);
    var due_date = new Date(lead_timeline.split('-')[2],lead_timeline.split('-')[1]-1,lead_timeline.split('-')[0]);
    var timeDiff = Math.abs(due_date.getTime() - new_date.getTime());
    var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
    const panes = [
            { menuItem: 'Property Info', render: () =>(
              <Tab.Pane>
              {lead.qualified === true ? (
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
                  content="We are yet to qualify this client. However, that doesn't mean the client is not motivated."
                />
              )
            }
                <h4>Basic Information</h4>
                <Item.Group relaxed='very' style={{'display':'flex', 'justifyContent': 'flex-start',
                'alignItems':'top','backgroundColor':'#d0f3e969', 'padding':'10px'}}>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Location</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyLoc' style={{'fontSize':'13px'}}>{lead.location}</span>
                          </Item.Meta>
                        </Item.Content>
                      </Item>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Property Type</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyType' style={{'fontSize':'14px'}}>{lead.property_type}</span>
                          </Item.Meta>
                        </Item.Content>
                      </Item>

                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Budget</Item.Header>
                          <Item.Meta>
                            <span className='rqplPrice' style={{'fontSize':'13px'}}>Ksh: {lead.min_price} - {lead.max_price}</span>
                          </Item.Meta>
                        </Item.Content>
                      </Item>
                </Item.Group>
                <h4>Ownership & Timeline</h4>
                <Item.Group relaxed='very' style={{'display':'flex', 'justifyContent': 'flex-start',
                'alignItems':'top','backgroundColor':'#d0f3e969','padding':'10px'}}>
                       <Item>
                         <Item.Content>
                           <Item.Header style={{'fontSize':'14px'}}>Nature of ownership.</Item.Header>
                           <Item.Meta>
                             <span className='rqplPropertyownership' style={{'fontSize':'13px'}}>{lead.ownership}</span>
                           </Item.Meta>
                         </Item.Content>
                       </Item>
                       <Item>
                         <Item.Content>
                           <Item.Header style={{'fontSize':'14px'}}>Property needed before.</Item.Header>
                           <Item.Meta>
                             <span className='rqplPropertyownership' style={{'fontSize':'13px'}}>{lead.timeline} - {(diffDays === 0 ? 'Expired' : `${diffDays} days remaining.`)}</span>
                           </Item.Meta>
                         </Item.Content>
                       </Item>
               </Item.Group>
               <h4>Property Features</h4>
                <Item.Group relaxed='very' style={{'display':'flex', 'justifyContent': 'flex-start',
                'alignItems':'top','backgroundColor':'#d0f3e969','padding':'10px' }}>
                        <Item>
                          <Item.Content>
                            <Item.Header style={{'fontSize':'14px'}}>Property Size</Item.Header>
                            <Item.Meta>
                              <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{lead.property_size} sqm</span>
                            </Item.Meta>
                          </Item.Content>
                        </Item>
                        <Item>
                          <Item.Content>
                            <Item.Header style={{'fontSize':'14px'}}>Beds</Item.Header>
                            <Item.Meta>
                              <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{lead.min_beds} - {lead.max_beds}</span>
                            </Item.Meta>
                          </Item.Content>
                        </Item>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>General Features</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyGfeatures' style={{'fontSize':'13px'}}>{lead.general_features}</span>
                          </Item.Meta>
                        </Item.Content>
                     </Item>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Parking options</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyPfeatures' style={{'fontSize':'13px'}}>{lead.parking_choices}</span>
                          </Item.Meta>
                        </Item.Content>
                      </Item>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Number of units needed.</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyNunits' style={{'fontSize':'13px'}}>{lead.number_of_units}</span>
                          </Item.Meta>
                        </Item.Content>
                      </Item>
                </Item.Group>
                <h4>Extra Notes from the client.</h4>
                <Item.Group relaxed='very' style={{'backgroundColor':'#d0f3e969','padding':'10px'}}>
                      <Item>
                        <Item.Content>
                          <Item.Header style={{'fontSize':'14px'}}>Additional details</Item.Header>
                          <Item.Meta>
                            <span className='rqplPropertyAdetails' style={{'fontSize':'13px'}}>{lead.additional_details}</span>
                          </Item.Meta>
                        </Item.Content>
                    </Item>
                </Item.Group>
              </Tab.Pane>
            )
            },
            { menuItem: 'Contact Info', render: () => (
                <Tab.Pane>
                {lead.qualified === true ? (
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
                    content="We are yet to qualify this client. However, that doesn't mean the client is not motivated."
                  />
                )
              }
              { show === false ? (
                <form onSubmit={handleClaim}>
                  <Button
                    type='submit'
                    icon='check'
                    content='Show contact information.'
                  />
                </form>
                ) : (
                  <>
                    <h4>Client Names</h4>
                     <Item.Group relaxed='very' style={{'display':'flex', 'justifyContent': 'flex-start',
                     'alignItems':'top','backgroundColor':'#d0f3e969','padding':'10px' }}>
                             <Item>
                               <Item.Content>
                                 <Item.Header style={{'fontSize':'14px'}}>Name</Item.Header>
                                 <Item.Meta>
                                   <span className='rqplPropertySize' style={{'fontSize':'13px'}}>{lead.name}</span>
                                 </Item.Meta>
                               </Item.Content>
                             </Item>
                     </Item.Group>
                     <h4> Phone and Email</h4>
                     <Item.Group relaxed='very' style={{'display':'flex', 'justifyContent': 'flex-start',
                     'alignItems':'top','backgroundColor':'#d0f3e969','padding':'10px' }}>
                         <Item>
                           <Item.Content>
                             <Item.Header style={{'fontSize':'14px'}}>Phone</Item.Header>
                             <Item.Meta>
                               <span className='rqplPropertyGfeatures' style={{'fontSize':'13px'}}>{lead.phone}</span>
                             </Item.Meta>
                           </Item.Content>
                        </Item>
                         <Item>
                           <Item.Content>
                             <Item.Header style={{'fontSize':'14px'}}>Email</Item.Header>
                             <Item.Meta>
                               <span className='rqplPropertyPfeatures' style={{'fontSize':'13px'}}>{lead.email}</span>
                             </Item.Meta>
                           </Item.Content>
                         </Item>
                     </Item.Group>
                     </>
                   )
                 }
                </Tab.Pane>
            )
            },
          ]
    return (
      <LeadDetailWrapper>
            <LeadElementsBox>
            {
              isLoaded === true ? (
                error ==='' ? (
                    <>
                      <LeadDetailContainer>
                        <Tab menu={{ fluid: true,tabular: false, secondary:true }} panes={panes} defaultActiveIndex={0}/>
                      </LeadDetailContainer>
                      <div style={{'padding':'10px', 'display':'flex', 'justifyContent':'space-between', 'alignItems':'baseline'}}>

                          <div style={{'display':'flex', 'justifyContent':'start', 'alignItems':'baseline'}}>
                              <Statistic.Group size='mini' >
                                  <Statistic color='green'>
                                    <Statistic.Value>{lead.claimer.length}</Statistic.Value>
                                    <Statistic.Label style={{'fontSize':'10px',}}>Claims</Statistic.Label>
                                  </Statistic>
                                  <Statistic color='red' >
                                    <Statistic.Value>{lead.referrer.length}</Statistic.Value>
                                    <Statistic.Label style={{'fontSize':'10px',}}>Referals</Statistic.Label>
                                  </Statistic>
                                  <Statistic color='teal' >
                                    <Statistic.Value>{
                                      lead.qualified === true ? 'yes' : 'no'
                                    }</Statistic.Value>
                                    <Statistic.Label style={{'fontSize':'10px',}}>Qualified</Statistic.Label>
                                  </Statistic>
                              </Statistic.Group>
                          </div>
                        <div style={{'padding':'10px', 'display':'flex', 'justifyContent':'flex-end', 'alignItems':'baseline'}}>
                          <Button  negative icon='share' content='Refer' onClick={() => openModal()}/>
                        </div>
                      </div>
                      </>
                ):(
                  <LeadNotFound/>
                )
            ):''
            }
          </LeadElementsBox>
          <Modal open={open} size='small' dimmer='inverted'>
                <Modal.Header>Share on email or social.</Modal.Header>
                <Modal.Content>
                  <div style={{'display':'flex', 'justifyContent':'center', 'alignItems':'center'}}>
                    <EmailShareButton url={window.location.href + `/${id}`}>
                      <EmailIcon size={36} round={true}/>
                    </EmailShareButton>
                    <FacebookShareButton url={window.location.href + `/${id}`}>
                      <FacebookIcon size={36} round={true}/>
                      <FacebookShareCount url={window.location.href + `/${id}`}/>
                    </FacebookShareButton>
                    <LinkedinShareButton url={window.location.href + `/${id}`}>
                      <LinkedinIcon size={36} round={true}/>
                    </LinkedinShareButton>
                    <TelegramShareButton url={window.location.href + `/${id}`}>
                      <TelegramIcon size={36} round={true}/>
                    </TelegramShareButton>
                    <TwitterShareButton url={window.location.href + `/${id}`}>
                      <TwitterIcon size={36} round={true}/>
                    </TwitterShareButton>
                    <ViberShareButton url={window.location.href + `/${id}`}>
                      <ViberIcon size={36} round={true}/>
                    </ViberShareButton>
                    <WhatsappShareButton url={window.location.href + `/${id}`}>
                      <WhatsappIcon size={36} round={true}/>
                    </WhatsappShareButton>
                    <WorkplaceShareButton url={window.location.href + `/${id}`}>
                      <WorkplaceIcon size={36} round={true}/>
                    </WorkplaceShareButton>
                  </div>
                </Modal.Content>
                <Modal.Actions>
                  <form onSubmit={handleRefer}>
                  <Button
                    type='submit'
                    icon='check'
                    content='All done'
                  />
                </form>
                </Modal.Actions>
            </Modal>
      </LeadDetailWrapper>
    )
}

export default PropertyRequestLeadDetail;
