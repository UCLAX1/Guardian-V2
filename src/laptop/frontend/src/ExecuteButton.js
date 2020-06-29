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
  display: 'inline-block'
});

const send_controls_data = () => {
  fetch('/controls', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(
      {
        'distance': document.getElementById('distance_text_field').value,
        'angle': document.getElementById('angle_text_field').value
      })
  });
};

const ExecuteButton = (props) => {

  var execute_height = Math.round( 48 * props.height / props.base_height );
  var execute_width = Math.round( 160 * props.width / props.base_width );
  var execute_padding = Math.round( 30 * props.width / props.base_width ).toString();
  var font_size = Math.round( 15 * props.width * props.height / props.base_area ).toString();

  return (
      <HelperButton onClick={() => send_controls_data()} style = {{height: execute_height, width: execute_width, padding: '0 ' + execute_padding + 'px', fontSize: font_size + 'px'}}>
        EXECUTE
      </HelperButton>
  );
}

export default ExecuteButton;
