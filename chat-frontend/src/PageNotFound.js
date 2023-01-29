import React from 'react';
import pageNotFound from './static/404 Error.svg';

function NoMatch() {
  return (
    <div style={{
      'width':'100%', 'height':'100vh', 'display':'flex', 'flexDirection':'column',
      'justifyContent':'center','alignItems':'center', 'position':'absolute', 'top':'0',
      'background':'#fff','zIndex':'999'
  }}>
        <div style={{'width':'500px', 'height':'500px'}}>
          <img src={pageNotFound} style={{'width':'100%', 'height':'100%', 'objectFit':'cover'}}/>
        </div>
        <h2>Page Not found</h2>
    </div>
  );
}

export default NoMatch;
