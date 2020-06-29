import React from 'react';
import { styled } from '@material-ui/core/styles';
import { withStyles, makeStyles } from '@material-ui/core/styles';

import ToggleButton from '@material-ui/lab/ToggleButton';
import Button from '@material-ui/core/Button';


const HelperButton = styled(Button)({
  background: 'linear-gradient(45deg, #56CCF2 30%, #2F80ED 90%)',
  border: 0,
  borderRadius: 5,
  color: 'white',
  display: 'flex',
  flexDirection:'column',
  textAlign: 'center', //horizontal center
  justifyContent: 'center', // vertical center
  textDecoration: 'none'
});

const clear_data = () => {
  fetch('/clearData', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({'clear':'data'})
  });
};

const ClearButton = (props) => {

  var clear_height = Math.round( 48 * props.height / props.base_height );
  var clear_width = Math.round( 160 * props.width / props.base_width );
  var clear_padding = Math.round( 30 * props.width / props.base_width ).toString();
  var font_size = Math.round( 15 * props.width * props.height / props.base_area ).toString();

  return (
    <div className="parent">
      <HelperButton onClick={() => clear_data()} style = {{height: clear_height, width: clear_width, padding: '0 ' + clear_padding + 'px', fontSize: font_size + 'px'}} className="clear">
        CLEAR
      </HelperButton>
    </div>
  );
};

export default ClearButton;
