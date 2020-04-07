import React from 'react';
import { styled } from '@material-ui/core/styles';
import ToggleButton from '@material-ui/lab/ToggleButton';
//import StyleToggleButton from './StyleToggleButton.js'


const StyleToggleButton = styled(ToggleButton)({
  background: 'linear-gradient(45deg, #56CCF2 30%, #2F80ED 90%)',
  //boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
  border: 0,
  borderRadius: 5,
  color: 'white',
  height: 48,
  padding: '0 30px',
  display: 'inline-block'
});

export default function MyToggleButton(props) {
  const [selected, setSelected] = React.useState(false);
  return (
      <StyleToggleButton
        value="check"
        selected={selected}
        onChange={() => {
          setSelected(!selected);
        }}
      >
      {props.text}

      </StyleToggleButton>




  );
}
/*
<div style = {{  position: 'absolute', top: '30px', left: '40px'}} className = 'wrapper'>

  </div>
*/
