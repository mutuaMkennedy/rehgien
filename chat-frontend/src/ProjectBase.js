import React from "react";
import { BrowserRouter as Router, Switch,Route,Link,NavLink  } from "react-router-dom";
import { Menu,Dropdown} from 'semantic-ui-react';
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
`
const LeadNavbarLogo = styled.div`
  width:160px;
  height:45px;
  margin-left:20px;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: contain !important;
`
const isAuthed = Boolean(localStorage.getItem("auth_token"));

const ProjectBase = () => (
  <Router>
  <Navbar>
      <Link to="/pro/home">
          <LeadNavbarLogo style={{'background':`url(${logo})`}}/>
      </Link>
      <Menu fluid secondary size='large' style={{'margin':'0','marginRight':'20px'}}>
          <Menu.Menu position='right' style={{'alignItems':'center'}}>
          {isAuthed ? (
              <>
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
                </>
              ):(
                  <NavLink  to="/pro/auth/login">
                    <Menu.Item name='Login'/>
                  </NavLink>
              )
              }
          </Menu.Menu>
        </Menu>
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
