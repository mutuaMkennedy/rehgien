import React from 'react';
import {
  Image
} from 'semantic-ui-react';
import styled from 'styled-components';
import shocked from '../static/shocked.svg';

const EmptyResults = styled.div`
  height: 100%;
  width: 100%;
  display:flex;
  justify-content:center;
  align-items:center;
`

function LeadNotFound() {
  return (
    <EmptyResults>
      <div style={{'display':'flex', 'justifyContent':'center', 'alignItems':'center', 'flexDirection':'column'}}>
        <Image size='small' src={shocked}/>
        <h4>No results found. Try again later</h4>
        <p>Leads requested does not exist. Make sure the address is correct.</p>
      </div>
    </EmptyResults>
  );
}

export default LeadNotFound;
