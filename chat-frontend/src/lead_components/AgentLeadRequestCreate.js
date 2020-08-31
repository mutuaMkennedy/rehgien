import React, { Component } from "react";
import axios from "axios";
import styled from 'styled-components';
import base from '../baseAddress.js';
import { Button, Header, Image, Modal } from 'semantic-ui-react';


class AgentLeadRequestCreate extends Component {
  constructor(props) {
    super(props);

    this.state = {
      open:false,
      setOpen:false,
      loading: false,
      u_errors: '',
      p_error:'',
      auth_error:''
    };
    this.openModal = () => {
      this.setState({open:true,setOpen:true})
    }

    this.closeModal = () => {
      this.setState({open:false,setOpen:false,})
    }
  }

  render() {
    return (
      <div>
      <Modal
          open={this.state.open}

          trigger={<Button onClick={() => this.openModal()}>Create</Button>}
        >
          <Modal.Header>Select a Photo</Modal.Header>
          <Modal.Content image scrolling>
            <Modal.Description>
              <Header>Default Profile Image</Header>
              <p>
                We've found the following gravatar image associated with your e-mail
                address.
              </p>
              <p>Is it okay to use this photo?</p>
            </Modal.Description>
          </Modal.Content>
          <Modal.Actions>
            <Button color='black' onClick={() => this.closeModal()}>
              Cancel
            </Button>
            <Button
              content="Submit"
              labelPosition='right'
              icon='Submit'
              onClick={() => this.closeModal()}
              positive
            />
          </Modal.Actions>
        </Modal>
      </div>
    );
  }
}

export default AgentLeadRequestCreate;
