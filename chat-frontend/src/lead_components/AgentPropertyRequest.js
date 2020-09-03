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
import AgentPropertyRequestStats from './AgentPropertyRequestStats.js';
import LeaderPanel from './AgentPropertyRequestLeaderBoard.js';
import AgentPropertyRequestStats2 from './PropertyRequestStats2.js';
import AgentPropertyRequestModalContent from './AgentPropertyRequestModalContent.js';

const LeadListWrapper = styled.div`
  width:100%;
  height:calc(100vh - 65px);
  background-color:#f1f9f1;
`
const LeftSidebar = styled.div`
  width:20%;
  padding:10px;
  height:90%;
  background-color:transparent;
  float:left;
  @media (max-width: 786px){
    display:none;
    position:absolute;
    top:0;
    z-index:1000;
    width:100%;
    height:100vh;
    background:#fff;
  }
`
const RevealLeftSidebarButton = styled.button`
  width:100px;
  height:30px;
  border:none;
  background:#ffff;
  color:blue;
  font-family:Lato,Arial;
  font-size:14px;
  display:none;
  border:1px solid #22242626;
  border-radius:.28571429rem;
  @media (max-width: 786px){
    display:block;
  }
`
const HideLeftSidebarButton = styled.button`
  width:30px;
  height:30px;
  line-height:12px;
  position:absolute;
  right:10px;
  top:10px;
  z-index:10;
  text-align:center;
  border:none;
  background:#00000066;
  color:#fff;
  font-family:Lato,Arial;
  font-size:12px;
  display:none;
  border-radius:50%;
  @media (max-width: 786px){
    display:block;
  }
`
const RightSidebar = styled.div`
  width:20%;
  padding:10px;
  height:90%;
  background-color:transparent;
  float:right;
  @media (max-width: 786px){
    display:none;
    position:absolute;
    top:0;
    z-index:1000;
    width:100%;
    height:100vh;
    background:#fff;
  }
`
const CardContainer = styled.div`
  padding:10px;
  width:60%;
  float:right;
  height:90%;
  overflow-y:auto;
  @media (max-width: 786px){
    width:100%;
    height:calc(100% - 90px);
  }
`
const RevealRightSidebarButton = styled.button`
  width:100px;
  height:30px;
  border:none;
  background:#ffff;
  color:blue;
  font-family:Lato,Arial;
  font-size:14px;
  display:none;
  border:1px solid #22242626;
  border-radius:.28571429rem;
  @media (max-width: 786px){
    display:block;
  }
`
const HideRightSidebarButton = styled.button`
  width:30px;
  height:30px;
  line-height:12px;
  position:absolute;
  right:10px;
  top:10px;
  z-index:10;
  text-align:center;
  border:none;
  background:#00000066;
  color:#fff;
  font-family:Lato,Arial;
  font-size:12px;
  display:none;
  border-radius:50%;
  @media (max-width: 786px){
    display:block;
  }
`
const StyledCard = styled(Card)`
  display:flex !important;
  flex-direction:row !important;
  @media (max-width: 786px){
    flex-direction:column !important;
  }
`
const SectionDivider = styled.div`
  height: 100%;
  width: 10px;
  border-left: 1px solid #2224261a;
  @media (max-width: 786px){
    display:none;
  }
`

const EmptyResults = styled.div`
  height: 100%;
  width: 100%;
  display:flex;
  justify-content:center;
  align-items:center;
`

const FilterBar = styled.div`
  width:100%;
  height:auto;
  background-color:#fff;
  padding: 10px;
  -webkit-box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
`
const RespFilterField = styled.div`
width:100%;
@media (max-width: 786px){
  display:none;
}
`
const RevealActionButtons = styled.div`
  display:none;
  @media (max-width: 786px){
    display:flex;
    align-items:center;
    justify-content:space-between;
  }
`
const FilterRevealButton = styled.button`
  width:100px;
  height:30px;
  border:none;
  background:#ffff;
  color:blue;
  font-family:Lato,Arial;
  font-size:14px;
  display:none;
  border:1px solid #22242626;
  border-radius:.28571429rem;
  @media (max-width: 786px){
    display:block;
  }
`
const FilterHideButton = styled.button`
  width:100px;
  height:30px;
  border:none;
  background:#ffff;
  color:#fb5f3d;
  font-family:Lato,Arial;
  font-size:14px;
  display:none;
  border:1px solid #22242626;
  border-radius:.28571429rem;
  @media (max-width: 786px){
    display:none;
  }
`
const FilterEmptyDiv = styled.div`
  display:none;
  margin-top:20px;
  margin-bottom:10px;
  @media (max-width: 786px){
    display:block;
  }
`
const StatsGroup = styled(Statistic.Group)`
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  width:100%;
`
const CustomModalActions = styled(Modal.Actions)`
  @media (max-width: 786px){
    display:flex;
    flex-direction:column;
    align-items:center;
    text-align:center !important;
    justify-content:center;
  }
`

function agPrShowFilters(){
  var filterField1 = document.getElementById('agPr-respFieldPt');
  var filterField2 = document.getElementById('agPr-respFieldMiP');
  var filterField3 = document.getElementById('agPr-respFieldMaP');
  var filterField4 = document.getElementById('agPr-respFieldRt');
  var revealButtons = document.getElementById('agPr-RevealButtons');
  var hideFilter = document.getElementById('agPr-hideFilter');

  filterField1.style.display='block';
  filterField2.style.display='block';
  filterField3.style.display='block';
  filterField4.style.display='block';
  revealButtons.style.display='none';
  hideFilter.style.display='block';
};

function agPrHideFilters(){
  var filterField1 = document.getElementById('agPr-respFieldPt');
  var filterField2 = document.getElementById('agPr-respFieldMiP');
  var filterField3 = document.getElementById('agPr-respFieldMaP');
  var filterField4 = document.getElementById('agPr-respFieldRt');
  var revealButtons = document.getElementById('agPr-RevealButtons');
  var hideFilter = document.getElementById('agPr-hideFilter');

  filterField1.style.display='none';
  filterField2.style.display='none';
  filterField3.style.display='none';
  filterField4.style.display='none';
  revealButtons.style.display='flex';
  hideFilter.style.display='none';
};

function agPrShowLeftSideBar(){
  var leftSideBar = document.getElementById('agPr-leftSideBar');
  leftSideBar.style.display='block';
};
function agPrHideLeftSideBar(){
  var leftSideBar = document.getElementById('agPr-leftSideBar');
  leftSideBar.style.display='none';
};

function agPrShowRightSideBar(){
  var rightSideBar = document.getElementById('agPr-rightSideBar');
  rightSideBar.style.display='block';
};
function agPrHideRightSideBar(){
  var rightSideBar = document.getElementById('agPr-rightSideBar');
  rightSideBar.style.display='none';
};

const authToken = localStorage.getItem("auth_token");
const tokenUserId = localStorage.getItem("user_id");

const options = [
  { key: 'b', text: 'Buy', value: 'Buy' },
  { key: 'r', text: 'Rent', value: 'Rent' },
  { key: 'l', text: 'Lease', value: 'Lease' },
]

const propertyTypeOptions = [
  {
    text: 'Apartment', key:'ap', value:'Apartment',
  },
  {
    text: 'Bungalow', key:'bu', value:'Bungalow',
  },
  {
    text: 'Condominium', key:'co', value:'Condominium',
  },
  {
    text: 'Dormitory', key:'do', value:'Dormitory',
  },
  {
    text: 'Duplex', key:'du', value:'Duplex',
  },
  {
    text: 'Duplex', key:'ma', value:'Duplex',
  },
  {
    text: 'Single-family', key:'si', value:'Single family',
  },
  {
    text: 'Terraced house', key:'te', value:'Terraced house',
  },
  {
    text: 'Townhouse', key:'to', value:'Townhouse',
  },
  {
    text: 'Land', key:'la', value:'Land',
  },
  {
    text: 'Other', key:'ot', value:'Other',
  },
]

class AgentPropertyRequest extends Component {
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
    locationName:'',
    propertyType:'',
    maxPrice:'',
    minPrice:'',
    requestType:''
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
    const agent_property_rq_leads = await axios.get(`${base}/apis/markets/agent_property_request/ `)
    await this.setState({
      lead:agent_property_rq_leads.data,
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
      url: `${base}/apis/markets/agent_property_request/${pk}/cl_or_re/ `,
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
    var locationName = this.state.locationName.toLowerCase();
    var propertyType = this.state.propertyType;
    var maxPrice = this.state.maxPrice;
    var minPrice = this.state.minPrice;
    var requestType = this.state.requestType;

    if (locationName){
      leads =  leads.filter(function(request) {
          return String(request.location_name.toLowerCase()).includes(locationName.toString());
      });
    }
    if (propertyType){
      leads =  leads.filter(function(request) {
          return request.property_type.toLowerCase() === propertyType.toLowerCase();
      });
    }
    if (maxPrice){
      leads =  leads.filter(function(request) {
          return request.max_price.toString() === maxPrice.toString();
      });
    }
    if (minPrice){
      leads =  leads.filter(function(request) {
          return request.min_price.toString() === minPrice.toString();
      });
    }
    if (requestType){
      leads =  leads.filter(function(request) {
          return request.ownership.toLowerCase() === requestType.toLowerCase();
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
                        Looking to {item.ownership}
                      </Card.Description>
                </Card.Content>
                <Card.Content extra textAlign='left' style={{'display':'flex', 'justifyContent': 'flex-start','alignItems':'top','flex-grow':'1' }}>
                    <SectionDivider/>
                    <div style={{'width':'100%'}}>
                        <Item.Group relaxed style={{'display':'flex', 'justifyContent': 'flex-start','alignItems':'top', }}>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content  style={{'fontSize':'10px'}} verticalAlign='top'  header='Location' meta={item.location_name} />
                            </Item>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content  style={{'fontSize':'10px'}}verticalAlign='top' header='Property Type' meta={item.property_type} />
                            </Item>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content  style={{'fontSize':'10px'}}verticalAlign='top' header='Units' meta={item.number_of_units} />
                            </Item>
                        </Item.Group>
                        <Item.Group style={{'display':'flex', 'justifyContent': 'flex-start', 'alignItems':'top'}}>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content style={{'fontSize':'10px'}} verticalAlign='top' header='Price Range'>
                                  <Item.Header>
                                    <span className='price'>Price Range</span>
                                  </Item.Header>
                                    <Item.Meta>
                                      <span className='price'>Ksh {item.min_price} - {item.max_price}</span>
                                    </Item.Meta>
                                  </Item.Content>
                            </Item>
                            <Item style={{'margin':'0', 'marginLeft':'5px'}}>
                                  <Item.Content style={{'fontSize':'10px'}} verticalAlign='top' header='Price Range'>
                                  <Item.Header>
                                    <span className='mv'>MV</span>
                                  </Item.Header>
                                    <Item.Meta>
                                      <span className='mv'>Ksh {item.market_value}</span>
                                    </Item.Meta>
                                  </Item.Content>
                            </Item>
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
                          <StatsGroup size='mini'>
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
                          </StatsGroup>
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
              <AgentPropertyRequestModalContent details={this.state.activeItem} timeRemaining={diffDays}/>
            </Modal.Content>
            <CustomModalActions>
              Dont have this property? Perhaps you know an agent who does.
              <Button negative icon='share' content='Refer' onClick={() => this.secondOpenModal()} style={{'marginTop':'5px'}}/>
              <Button icon='check' content='All Done' onClick={() => this.closeModal()} style={{'marginTop':'5px'}}/>
            </CustomModalActions>
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
                        <form onSubmit={this.handleRefer} style={{'margin':'5px'}}>
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
                  <form onSubmit={this.handleRefer} style={{'margin':'5px'}}>
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
      <FilterBar>
        <Form size='tiny'>
            <Form.Group inline widths='equal'>
            <div style={{'width':'100%'}}>
              <Form.Input fluid placeholder='Enter an address, city or neighborhood'
              name='location' onChange={this.handleInputChange} value={this.state.location}/>
            </div>
            <RespFilterField id='agPr-respFieldPt'>
              <FilterEmptyDiv></FilterEmptyDiv>
              <Form.Select fluid options={propertyTypeOptions} placeholder=' property type'
              name='propertyType' onChange={this.handleSelectChange} value={this.state.propertyType}/>
            </RespFilterField>
            <RespFilterField id='agPr-respFieldMiP'>
              <FilterEmptyDiv></FilterEmptyDiv>
              <Form.Input fluid  placeholder='Enter Minimum price'
              name='minPrice' onChange={this.handleInputChange} value={this.state.minPrice}/>
            </RespFilterField>
            <RespFilterField id='agPr-respFieldMaP'>
              <FilterEmptyDiv></FilterEmptyDiv>
              <Form.Input fluid  placeholder='Enter Maximum price'
              name='maxPrice' onChange={this.handleInputChange} value={this.state.maxPrice}/>
            </RespFilterField>
            <RespFilterField id='agPr-respFieldRt'>
              <FilterEmptyDiv></FilterEmptyDiv>
              <Form.Select fluid options={options} placeholder='Request Type'
              name='requestType' onChange={this.handleSelectChange} value={this.state.requestType}/>
            </RespFilterField>
            </Form.Group>
        </Form>
        <RevealActionButtons id='agPr-RevealButtons' >
            <FilterRevealButton onClick={agPrShowFilters}>
              Show Filters
            </FilterRevealButton>
            <RevealLeftSidebarButton onClick={agPrShowLeftSideBar}>
              Statistics
            </RevealLeftSidebarButton>
            <RevealRightSidebarButton onClick={agPrShowRightSideBar}>
              Activity
            </RevealRightSidebarButton>
        </RevealActionButtons>
        <FilterHideButton id='agPr-hideFilter' onClick={agPrHideFilters}>
          Hide Filters
        </FilterHideButton>
      </FilterBar>
          <LeftSidebar id='agPr-leftSideBar'>
          <HideLeftSidebarButton onClick={agPrHideLeftSideBar}>x</HideLeftSidebarButton>
          {this.state.loading === true ? (
            <EmptyResults>
               <Loader active inline='centered' size='small' />
            </EmptyResults>
          ) : (
              <AgentPropertyRequestStats leads={leads}/>
            )
          }
          </LeftSidebar>
          <RightSidebar id='agPr-rightSideBar'>
          <HideRightSidebarButton onClick={agPrHideRightSideBar}>x</HideRightSidebarButton>
            {this.state.loading === true ? (
              <EmptyResults>
                 <Loader active inline='centered' size='small' />
              </EmptyResults>
            ) : (
              <>
                <AgentPropertyRequestStats2 leads={leads}/>
                <LeaderPanel leads={leads}/>
              </>
            )
          }
          </RightSidebar>
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

export default AgentPropertyRequest;
