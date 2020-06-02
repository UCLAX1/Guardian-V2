import React from 'react';
import ToggleButton from '@material-ui/lab/ToggleButton';
import styled from "styled-components";


const ToggleButtonWrapper = styled.div`
  position: absolute;
  top: 100px;
  left: 100px;

`;

export default function StandaloneToggleButton(props) {
  const [selected, setSelected] = React.useState(false);

  return (
    <ToggleButtonWrapper>
      <ToggleButton
        value="check"
        selected={selected}
        onChange={() => {
          setSelected(!selected);
        }}
      >
      {props.text1}

      </ToggleButton>
    </ToggleButtonWrapper>

  );
}
