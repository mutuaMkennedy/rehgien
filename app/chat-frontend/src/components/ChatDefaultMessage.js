import React, { Component } from "react";
import {
  withChannelContext,
} from "stream-chat-react";
import styled from 'styled-components';


const ChatDefaultMessage = withChannelContext(
  class ChatDefaultMessage extends React.PureComponent {
    render() {
      var dtStr = this.props.channel.data.created_at;
      const createdAt = new Date(dtStr);
      const newCreatedDate = String(createdAt)

      console.log(this.props);
      return (
        <div>
          <h1>{this.props.channel.data.name}</h1>
            <p>
              This is the begining of the <b>{this.props.channel.data.name}</b> channel.
              <span>{this.props.channel.data.created_by.name}</span> created this channel
               on {newCreatedDate}.

            </p>
        </div>
      );
    }
  },
);

export default ChatDefaultMessage;
