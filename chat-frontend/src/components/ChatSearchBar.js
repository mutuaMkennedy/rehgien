import React, { Component } from "react";
import base from '../baseAddress.js';
import _ from 'lodash';
import {Search, Grid} from 'semantic-ui-react';
import { StreamChat } from "stream-chat";

const userToken = localStorage.getItem("token");
const tokenUserId = localStorage.getItem("user_id");
const tokenUserName = localStorage.getItem("user_name");
const userAvatar = localStorage.getItem("user_avatar");

const initialState = { isLoading: false, results: [], value: '' }

class ChatSearchBar extends Component{

    state = initialState

    handleResultSelect = (e, { result }) => this.setState({ value: result.title })

    handleSearchChange =(e, { value }) => {
      this.setState({ isLoading: true, value })

      setTimeout(async () => {
        if (this.state.value.length < 1) return this.setState(initialState)

        const client = new StreamChat("qk4nn7rpcn75");

        const filters = { type: 'team', members: { $in: [tokenUserId] } };

        await client.setUser(
          {
            id: tokenUserId,
            name: tokenUserName,
            image: base + userAvatar
          },
          userToken,
        );

        if (this.state.value.length > 1){
         const search = await client.search(
            filters,
            this.state.value,
            { limit: 0, offset: 0 },
         );

         const sourceArray = [];

         if (search.results.length > 0) {
           for(var i =0; i < search.results.length; i++){
             const name =search.results[i].message.channel.name
             const searchArray = {
                 'title': name ? 'gp: '+ search.results[i].message.channel.name: 'pv: #privateChat',
                 'description':search.results[i].message.text,
                 'price': String(new Date(search.results[i].message.created_at)).slice(0,21) + ' ~ ' +search.results[i].message.user.name,
                 'image':search.results[i].message.user.image

               }
                sourceArray.push(searchArray);
            }
         }

        const re = new RegExp(_.escapeRegExp(this.state.value), 'i')
        const isMatch = (result) => re.test(result.description)

          this.setState({
            isLoading: false,
            results: _.filter(sourceArray, isMatch),
        })
       }
      }, 300)
    }

  render(){
    const { isLoading, value, results } = this.state
    return(
            <Grid style={{'width':'100%'}}>
              <Grid.Column width={16} textAlign='center'>
                  <Search
                    className='ChatClientSearchBar'
                    fluid
                    input={{ icon: 'search', iconPosition: 'left' }}
                    loading={isLoading}
                    onResultSelect={this.handleResultSelect}
                    onSearchChange={_.debounce(this.handleSearchChange, 500, {
                      leading: true,

                  })}
                    placeholder='Search in messages and channels'
                    results={results}
                    value={value}
                    {...this.props}
                  />
              </Grid.Column>
        </Grid>
    )
  }
}

export default ChatSearchBar;
