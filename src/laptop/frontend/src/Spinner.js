import React from 'react';
import styled from "styled-components";


const Spinner = (props) =>{
  return (
    <div className="ui segment">
      <div style = {{width:960, height:720}}class="ui active dimmer">
        <div className="ui indeterminate text loader">{props.message}</div>
      </div>
    </div>
  );
};

Spinner.defaultProps = {
  message :'Loading...'
};

export default Spinner;
