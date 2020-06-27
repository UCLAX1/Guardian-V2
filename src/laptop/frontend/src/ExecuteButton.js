import React from 'react';
import { styled } from '@material-ui/core/styles';
import { withStyles, makeStyles } from '@material-ui/core/styles';

import ToggleButton from '@material-ui/lab/ToggleButton';
import Button from '@material-ui/core/Button';


const HelperButton = styled(Button)({
  background: 'linear-gradient(45deg, #56CCF2 30%, #2F80ED 90%)',
  //boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
  border: 0,
  borderRadius: 5,
  color: 'white',
  height: 48,
  padding: '0 30px',
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

export default function ExecuteButton() {

  return (
      <HelperButton onClick={() => send_controls_data()}>
      EXECUTE
      </HelperButton>
  );
}
