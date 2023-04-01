import React from "react";
import { BrowserRouter as Router, Switch,Route,Link,NavLink  } from "react-router-dom";
import { Menu,Dropdown,Icon} from 'semantic-ui-react';
import styled from 'styled-components';
import base from './baseAddress.js';
import logo from './static/logo_pro.png';
import Logout from "./Logout";
import Chat from "./Chat";
import Login from "./Login";
import Home from "./ProHome.js";
import UnauthedRoute from "./UnauthedRoute";
import AuthedRoute from "./AuthedRoute";
import NotFound from "./PageNotFound";
import PropertyRequests from './lead_components/PropertyRequest.js';
import ProRequestList from './lead_components/ProRequestList.js';
import OtherRequestList from './lead_components/OtherRequestList.js';
import AgentLeadRequests from './lead_components/AgentLeadRequest.js';
import AgentPropertyRequest from './lead_components/AgentPropertyRequest.js';
import PropertyRequestLeadDetail from './lead_components/PropertyRequestLeadDetail.js';
import ProRequestLeadDetail from './lead_components/ProRequestLeadDetail.js';
import OtherRequestLeadDetail from './lead_components/OtherRequestLeadDetail.js';
import AgentLeadRequestDetail from './lead_components/AgentLeadRequestDetail.js';
import AgentPropertyRequestDetail from './lead_components/AgentPropertyRequestDetail.js';

const Navbar = styled.div`
  width:100%;
  height:60px;
  background-color:#fff;
  display:flex;
  align-items:center;
  position:sticky;
  top:0;
  z-index:999;
  border-bottom: 1px solid rgb(235, 243, 255);
`
const LogoLink = styled(Link)`
  @media (max-width: 786px){
    margin-left:50%;
    transform:translate(-50%,0);
  }
`
const LeadNavbarLogo = styled.div`
  width:160px;
  height:45px;
  margin-left:20px;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: contain !important;
`
const MobileNavbarWrapper = styled.div`
  z-index:999;
  display:block;
  position: relative;
  width:100%;
  background:#fff;
  height:60px;
  border-bottom: 1px solid rgb(235, 243, 255);
  @media (max-width: 768px){
    position: fixed;
    height:auto;
    top:0px;
    display:none;
    -webkit-box-shadow: 0 1px 3px 0 #00000033, 0 0 0 1px #00000033;
    box-shadow: 0 1px 3px 0 #00000033, 0 0 0 1px #00000033;
  }
`
const NavbarMenu = styled(Menu)`
  width:100%;
  text-transform:uppercase;
  justify-content:flex-end;
  @media (max-width: 768px){
    justify-content:center;
    align-items:center;
  }
`
const NavbarMenuItems = styled.div`
  display:flex;
  align-items:center;
  @media (max-width: 786px){
    flex-direction:row;
  }
`
const NavbarRevealButton = styled.button`
  width:auto;
  height:60px;
  border:none;
  display:none;
  position:absolute;
  left:0;
  background:#fff;
  @media (max-width: 786px){
    display:block;
  }
`
const NavbarCloseButton = styled.button`
  width:30px;
  height:30px;
  margin-top:5px;
  border:none;
  text-align:center;
  font-size:15px;
  line-height:10px;
  background:#00000033;
  color:#fff;
  position:relative;
  left:50%;
  border-radius:50%;
  transform:translate(-50%,0);
  display:none;
  @media (max-width: 786px){
    display:block;
  }
`

function openMobileMenu(){
  var navWrp = document.getElementById('proNavMenu');
  navWrp.style.display='block';
};

function closeMobileMenu(){
  var navWrp = document.getElementById('proNavMenu');
  navWrp.style.display='none';
};

const isAuthed = Boolean(localStorage.getItem("auth_token"));

const ProjectBase = () => (
  <Router>
  <Navbar>
      <LogoLink to="/pro/home">
          <LeadNavbarLogo style={{'background':`url(${logo})`}}/>
      </LogoLink>
      <NavbarRevealButton onClick={openMobileMenu}>
          <Icon name='bars' style={{'color':'#e2e2e4', 'fontSize':'24px'}}/>
      </NavbarRevealButton>
      <MobileNavbarWrapper id='proNavMenu'>
          <NavbarCloseButton onClick={closeMobileMenu}>
            x
          </NavbarCloseButton>
          <NavbarMenu fluid secondary size='large' style={{'margin':'0','marginRight':'20px','height':'100%'}}>
              <Menu.Menu >
              {isAuthed ? (
                  <NavbarMenuItems>
                        <NavLink  to="/pro/messaging">
                            <Menu.Item
                              name='Messaging'
                            />
                        </NavLink>
                          <Dropdown item text='Leads'>
                              <Dropdown.Menu>
                              <NavLink  to="/pro/markets/leads/property_requests">
                                <Dropdown.Item>Property Requests</Dropdown.Item>
                              </NavLink >
                              <NavLink  to="/pro/markets/leads/pro_requests">
                                <Dropdown.Item>Pro Requests</Dropdown.Item>
                              </NavLink >
                              <NavLink  to="/pro/markets/leads/other_requests">
                                <Dropdown.Item>Other requests</Dropdown.Item>
                              </NavLink >
                              <NavLink  to="/pro/markets/leads/agent_lead_requests">
                                <Dropdown.Item>Agent Lead Requests</Dropdown.Item>
                              </NavLink >
                              <NavLink  to="/pro/markets/leads/agent_property_requests">
                                <Dropdown.Item>Agent Property Requests</Dropdown.Item>
                              </NavLink >
                              </Dropdown.Menu>
                          </Dropdown>
                          <Menu.Item>
                            <Logout/>
                          </Menu.Item>
                    </NavbarMenuItems>
                  ):(
                      <NavLink  to="/pro/auth/login" style={{'alignSelf':'center'}}>
                        <Menu.Item name='Login'/>
                      </NavLink>
                  )
                  }
              </Menu.Menu>
          </NavbarMenu>
      </MobileNavbarWrapper>
  </Navbar>
    <Switch>
      <UnauthedRoute exact path="/pro/auth/login" component={Login} />
      <AuthedRoute exact path="/pro/messaging" component={Chat} />
      <Route exact path="/pro/home" component={Home} />
      <AuthedRoute exact path="/pro/markets/leads/property_requests" component={PropertyRequests} />
      <AuthedRoute exact path="/pro/markets/leads/pro_requests" component={ProRequestList} />
      <AuthedRoute exact path="/pro/markets/leads/other_requests" component={OtherRequestList} />
      <AuthedRoute exact path="/pro/markets/leads/agent_lead_requests" component={AgentLeadRequests} />
      <AuthedRoute exact path="/pro/markets/leads/agent_property_requests" component={AgentPropertyRequest} />
      <AuthedRoute exact path="/pro/markets/leads/property_requests/:id/detail" children={<PropertyRequestLeadDetail/>}/>
      <AuthedRoute exact path="/pro/markets/leads/pro_requests/:id/detail" children={<ProRequestLeadDetail/>}/>
      <AuthedRoute exact path="/pro/markets/leads/other_requests/:id/detail" children={<OtherRequestLeadDetail/>}/>
      <AuthedRoute exact path="/pro/markets/leads/agent_lead_requests/:id/detail" children={<AgentLeadRequestDetail/>}/>
      <AuthedRoute exact path="/pro/markets/leads/agent_property_requests/:id/detail" children={<AgentPropertyRequestDetail/>}/>
      <Route path="*">
        <NotFound/>
      </Route>
    </Switch>
  </Router>
);

export default ProjectBase;
