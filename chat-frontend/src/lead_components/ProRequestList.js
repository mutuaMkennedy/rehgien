import React, { Component  } from "react";
import {
  Button,
  Card,
  Image,
  Statistic,
  Item,
  Modal,
  Loader,
  Form
} from 'semantic-ui-react';
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
import axios from "axios";
import styled from 'styled-components';
import base from '../baseAddress.js';
import avatar from '../static/avatar.jpg';
import shocked from '../static/shocked.svg';
import ProRequestStats from './ProRequestStats.js';
import LeaderPanel from './ProRequestLeaderBoard.js';
import ProRequestStats2 from './ProRequestStats2.js';
import ProRequestModalContent from './ProRequestLeadModalContent.js';

const LeadListWrapper = styled.div`
  width:100%;
  height:calc(100vh - 65px);
  background-color:#f1f9f1;
`
const LeftSidebar = styled.div`
  width:20%;
  padding:10px;
  height:100%;
  background-color:transparent;
  float:left;
`
const RightSidebar = styled.div`
  width:20%;
  padding:10px;
  height:100%;
  background-color:transparent;
  float:right;
`
const CardContainer = styled.div`
  padding:10px;
  width:60%;
  float:right;
  height:calc(90% - 15px);
  overflow-y:auto;
`
const StyledCard = styled(Card)`
  display:flex !important;
  flex-direction:row !important;
`
const SectionDivider = styled.div`
  height: 100%;
  width: 10px;
  border-left: 1px solid #2224261a;
`

const EmptyResults = styled.div`
  height: 100%;
  width: 100%;
  display:flex;
  justify-content:center;
  align-items:center;
`

const FilterBar = styled.div`
  width:60%;
  float:right;
  background-color:transparent;
  padding: 10px;
`

const authToken = localStorage.getItem("auth_token");
const tokenUserId = localStorage.getItem("user_id");

const proTypeOptions = [
  {
    text: 'Agent', key:'ag', value:'Agent',
  },
  {
    text: 'Property Manager', key:'pm', value:'PropertyManager',
  },
  {
    text: 'Interior Designer', key:'id', value:'InteriorDesigner',
  },
  {
    text: 'Architect', key:'ar', value:'Architect',
  },
  {
    text: 'Landscape architect', key:'la', value:'LandscapeArchitect',
  },
  {
    text: 'Home mover', key:'hm', value:'HomeMover',
  },
  {
    text: 'Plumbing', key:'pl', value:'Plumbing',
  },
  {
    text: 'Photographer', key:'ph', value:'Photographer',
  },
]

class ProRequests extends Component {
  constructor(props){
    super(props);
    this.state = {
    lead:[],
    open:false,
    setOpen:false,
    activeItem:'',
    secondOpen:false,
    secondsetOpen:false,
    loading:false,
    _activeItem:'',
    _secondOpen:false,
    _secondsetOpen:false,
    location:'',
    proType:'',
    }
    //activating claim modal
    this.openModal = (item) => {
       this.setState({activeItem:item}, ()=> this.setState({ open: true,setOpen:true }));
    };
    //activating refer modal inside claim modal
    this.secondOpenModal = (item) => {
       this.setState({secondOpen:true,secondsetOpen:true});
    };
    //activating refer modal on list page
    this._secondOpenModal = (item) => {
       this.setState({_activeItem:item}, ()=> this.setState({ _secondOpen: true,_secondsetOpen:true }));
    };
    this.secondCloseModal = () => {
       this.setState({secondOpen:false,secondsetOpen:false});
    };

    this.closeModal = this.closeModal.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSelectChange = this.handleSelectChange.bind(this);
    this.handleRefer = this.handleRefer.bind(this)
  }

  closeModal() {
    this.setState({
       open: false,
       setOpen:false,
       activeItem:''
     });
  }

  async componentDidMount(){
    this.setState({
      loading:true,
    });
    const rq_pro_leads = await axios.get(`${base}/apis/markets/pro_request/ `)
    await this.setState({
      lead:rq_pro_leads.data,
      loading:false,
    })
  }

  handleInputChange(event){
    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]:value,
    });
   }
  handleSelectChange(event,data){
    const value = data.value;
    const name = data.name;
    this.setState({
      [name]:value,
    });
  }

  handleRefer(event){
    event.preventDefault();
    var pk;

    //setting item pk based on what modal is active
    if(this.state.activeItem !==''){ //if claim modal is active
      pk = this.state.activeItem.pk
    }
    if(this.state._activeItem !==''){ //if list page refer modal is active
      pk = this.state._activeItem.pk
    }
    const referLead = axios({
      method: "PATCH",
      url: `${base}/apis/markets/pro_request/${pk}/cl_or_re/ `,
      data: {
        referrer:[tokenUserId],
      },
      config: {
        headers: { "Content-Type": "application/json","Authorization":`Token ${authToken}` }
      }
    });

    //closing refer modal inside claim modal
    if(this.state.activeItem !==''){
      this.setState({secondOpen: false,secondsetOpen:false });
    }
    //closing refer modal on list page
    if(this.state._activeItem !==''){
      this.setState({_activeItem:'',_secondOpen: false,_secondsetOpen:false });
    }
  }

  render() {
    let leads = this.state.lead.slice();
    var location = this.state.location.toLowerCase();
    var proType = this.state.proType;

    if (location){
      leads =  leads.filter(function(request) {
          return String(request.location.toLowerCase()).includes(location.toString());
      });
    }
    if (proType){
      leads =  leads.filter(function(request) {
          return request.type_of_proffesional.toLowerCase() === proType.toLowerCase();
      });
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
    var lead_items = leads.map((item) => {
          //calculating no. of Days remaining before lead expires
            var date_today = new Date();
                date_today = formatDate(String(date_today).slice(0,15))
            var lead_timeline = item.timeline;
                lead_timeline = formatDate(lead_timeline)

            var new_date = new Date(date_today.split('-')[2],date_today.split('-')[1]-1,date_today.split('-')[0]);
            var due_date = new Date(lead_timeline.split('-')[2],lead_timeline.split('-')[1]-1,lead_timeline.split('-')[0]);
            var timeDiff = Math.abs(due_date.getTime() - new_date.getTime());
            var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));

          return(
            <>
            <StyledCard centered key={item.pk}>
                <Card.Content>
                      <Image floated='left' size='mini' src={avatar}/>
                      <Card.Header>{item.name}</Card.Header>
                      <Card.Description>
                        {
                          item.service_details.slice(0,20) + '...'
                        }
                      </Card.Description>
                </Card.Content>
                <Card.Content extra textAlign='left' style={{'display':'flex', 'justifyContent': 'flex-start','alignItems':'top','flex-grow':'1' }}>
                    <SectionDivider/>
                    <div style={{'width':'100%'}}>
                        <Item.Group relaxed style={{'display':'flex', 'justifyContent': 'flex-start','alignItems':'top', }}>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content  style={{'fontSize':'10px'}} verticalAlign='top'  header='Location' meta={item.location} />
                            </Item>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content  style={{'fontSize':'10px'}}verticalAlign='top' header='Pro Needed' meta={item.type_of_proffesional} />
                            </Item>
                        </Item.Group>
                        <Item.Group style={{'display':'flex', 'justifyContent': 'flex-start', 'alignItems':'top'}}>
                            <Item style={{'margin':'0','marginLeft':'5px'}}>
                                  <Item.Content style={{'fontSize':'10px'}} verticalAlign='top' header='Timeline' meta={
                                    diffDays === 0 ? 'Expired' : `${diffDays} days remaining.`
                                  } />
                            </Item>
                        </Item.Group>
                    </div>
                </Card.Content>
                <Card.Content extra textAlign='left' style={{'display':'flex', 'justifyContent': 'flex-start','alignItems':'center', }}>
                      <SectionDivider/>
                      <div style={{'width':'100%'}}>
                          <Statistic.Group size='mini' widths='two'>
                              <Statistic color='green'>
                                <Statistic.Value>{item.claimer.length}</Statistic.Value>
                                <Statistic.Label style={{'fontSize':'10px',}}>Claims</Statistic.Label>
                              </Statistic>
                              <Statistic color='red' >
                                <Statistic.Value>{item.referrer.length}</Statistic.Value>
                                <Statistic.Label style={{'fontSize':'10px',}}>Referals</Statistic.Label>
                              </Statistic>
                              <Statistic color='teal' >
                                <Statistic.Value>{
                                  item.qualified === true ? 'yes' : 'no'
                                }</Statistic.Value>
                                <Statistic.Label style={{'fontSize':'10px',}}>Qualified</Statistic.Label>
                              </Statistic>
                          </Statistic.Group>
                      </div>
                </Card.Content>
                <Card.Content extra textAlign='left' style={{'display':'flex', 'justifyContent': 'center','alignItems':'center', }}>
                      <SectionDivider/>
                      <div className='ui two buttons' style={{'flexDirection':'column'}}>
                        <Button basic color='green' style={{'width':'100%','margin':'5px', 'borderRadius':'5px'}}
                        onClick={()=> this.openModal(item)}
                        >
                          Claim
                        </Button>
                        <Button basic color='red' style={{'width':'100%','margin':'5px', 'borderRadius':'5px'}}
                        onClick={()=> this._secondOpenModal(item)}
                        >
                          Refer
                        </Button>
                      </div>
                </Card.Content>
          </StyledCard>
          <Modal open={this.state.open} dimmer='inverted'>
            <Modal.Header>Lead Details</Modal.Header>
            <Modal.Content scrolling>
              <ProRequestModalContent details={this.state.activeItem} timeRemaining={diffDays}/>
            </Modal.Content>
            <Modal.Actions>
              No interested? Perhaps you can refer someone.
              <Button negative icon='share' content='Refer' onClick={() => this.secondOpenModal()}/>
                OR
              <Button icon='check' content='All Done' onClick={() => this.closeModal()}/>
            </Modal.Actions>
                <Modal open={this.state.secondOpen} size='small' dimmer='inverted'>
                      <Modal.Header>Share on email or social.</Modal.Header>
                      <Modal.Content>
                        <div style={{'display':'flex', 'justifyContent':'center', 'alignItems':'center'}}>
                          <EmailShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <EmailIcon size={36} round={true}/>
                          </EmailShareButton>
                          <FacebookShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <FacebookIcon size={36} round={true}/>
                            <FacebookShareCount url={window.location.href + `/${this.state.activeItem.pk}`}/>
                          </FacebookShareButton>
                          <LinkedinShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <LinkedinIcon size={36} round={true}/>
                          </LinkedinShareButton>
                          <TelegramShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <TelegramIcon size={36} round={true}/>
                          </TelegramShareButton>
                          <TwitterShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <TwitterIcon size={36} round={true}/>
                          </TwitterShareButton>
                          <ViberShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <ViberIcon size={36} round={true}/>
                          </ViberShareButton>
                          <WhatsappShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <WhatsappIcon size={36} round={true}/>
                          </WhatsappShareButton>
                          <WorkplaceShareButton url={window.location.href + `/${this.state.activeItem.pk}`}>
                            <WorkplaceIcon size={36} round={true}/>
                          </WorkplaceShareButton>
                        </div>
                      </Modal.Content>
                      <Modal.Actions>
                        <form onSubmit={this.handleRefer}>
                          <Button
                            type='submit'
                            icon='check'
                            content='All Done'
                          />
                        </form>
                      </Modal.Actions>
                  </Modal>
          </Modal>
          <Modal open={this.state._secondOpen} size='small' dimmer='inverted'>
                <Modal.Header>Share on email or social.</Modal.Header>
                <Modal.Content>
                  <div style={{'display':'flex', 'justifyContent':'center', 'alignItems':'center'}}>
                    <EmailShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <EmailIcon size={36} round={true}/>
                    </EmailShareButton>
                    <FacebookShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <FacebookIcon size={36} round={true}/>
                      <FacebookShareCount url={window.location.href + `/${this.state._activeItem.pk}`}/>
                    </FacebookShareButton>
                    <LinkedinShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <LinkedinIcon size={36} round={true}/>
                    </LinkedinShareButton>
                    <TelegramShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <TelegramIcon size={36} round={true}/>
                    </TelegramShareButton>
                    <TwitterShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <TwitterIcon size={36} round={true}/>
                    </TwitterShareButton>
                    <ViberShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <ViberIcon size={36} round={true}/>
                    </ViberShareButton>
                    <WhatsappShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <WhatsappIcon size={36} round={true}/>
                    </WhatsappShareButton>
                    <WorkplaceShareButton url={window.location.href + `/${this.state._activeItem.pk}`}>
                      <WorkplaceIcon size={36} round={true}/>
                    </WorkplaceShareButton>
                  </div>
                </Modal.Content>
                <Modal.Actions>
                  <form onSubmit={this.handleRefer}>
                    <Button
                      type='submit'
                      icon='check'
                      content='All Done'
                    />
                  </form>
                </Modal.Actions>
            </Modal>
          </>
        );
    })

    return (
      <LeadListWrapper>
          <LeftSidebar>
          {this.state.loading === true ? (
            <EmptyResults>
               <Loader active inline='centered' size='small' />
            </EmptyResults>
          ) : (
              <ProRequestStats leads={leads}/>
            )
          }
          </LeftSidebar>
          <RightSidebar>
            {this.state.loading === true ? (
              <EmptyResults>
                 <Loader active inline='centered' size='small' />
              </EmptyResults>
            ) : (
              <>
                <ProRequestStats2 leads={leads}/>
                <LeaderPanel leads={leads}/>
              </>
            )
          }
          </RightSidebar>
          <FilterBar>
            <Form size='tiny' style={{'padding':'5px'}}>
                <Form.Group inline widths='equal' >
                <Form.Input fluid placeholder='Enter an address, city or neighborhood'
                name='location' onChange={this.handleInputChange} value={this.state.location}/>
                <Form.Select fluid options={proTypeOptions} placeholder='Pro type'
                name='proType' onChange={this.handleSelectChange} value={this.state.propertyType}/>
                </Form.Group>
            </Form>
          </FilterBar>
          <CardContainer>
              {leads.length > 0 ? (
                  <Card.Group itemsPerRow={1}>
                    {lead_items}
                  </Card.Group>
              ): this.state.loading === true ? (
                <EmptyResults>
                   <Loader active inline='centered' size='large' />
                </EmptyResults>
              ) : (
                <EmptyResults>
                  <div style={{'display':'flex', 'justifyContent':'center', 'alignItems':'center', 'flexDirection':'column'}}>
                    <Image size='small' src={shocked}/>
                    <h4>No results found. Try again later</h4>
                    <p>Leads published will appear here.</p>
                  </div>
                </EmptyResults>
                )
              }
          </CardContainer>
      </LeadListWrapper>
    );
  }
}

export default ProRequests;
