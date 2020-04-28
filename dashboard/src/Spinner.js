import React from 'react';
import styled from "styled-components";


const Spinner = (props) =>{
  return (
    <div class="ui segment">
      <div style = {{width:960, height:720}}class="ui active dimmer">
        <div class="ui indeterminate text loader">{props.message}</div>
      </div>
    </div>
  );
};

Spinner.defaultProps = {
  message :'Loading...'
};

export default Spinner;




/*
const Spinner2 = (props) =>{
  return (
      <div className="ui active dimmer">
        <div className="ui text loader">{props.message} </div>
      </div>

  );
};

Spinner2.defaultProps = {
  message :'Loading...'
};

export const Spinner = styled(Spinner2)({
    backgroundColorcolor: 'red!important',
    width:'960px', //700
    borderRadius:5
});
*/
