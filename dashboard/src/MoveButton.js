import React from 'react';
import { styled } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';

const StyleButton = styled(Button)({
  boxShadow: '0 4px 6px 2px rgba(47,128,237, .3)', 
  backgroundColor:'#56CCF2',
  borderRadius: 3,
  color: 'white',
  width:100,
  height: 100,
  padding: '0 30px',
  display: 'inline-block'

});

export default function MoveButton(props) {
  return (
      <StyleButton variant="contained">
        {props.text}
      </StyleButton>

  );
}
