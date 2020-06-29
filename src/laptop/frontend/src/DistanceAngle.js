import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';


const DistanceAngle = (props) => {

  var text_width = Math.round( 420 * props.width / props.base_width );
  var text_height = Math.round( 20 * props.height / props.base_height );

  return (
    <div>
      <div>
        <TextField
          id="distance_text_field"
          label="DISTANCE (cm)"
          style={{ margin: 8, width: text_width}}
          margin="normal"
          InputLabelProps={{
            shrink: true
          }}
          InputProps={{
            shrink: true,
            style: {fontSize: text_height}
          }}
          variant="filled"
        />

        <TextField
          id="angle_text_field"
          label="ANGLE (degrees)"
          style={{ margin: 8 , width: text_width}}
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
          InputProps={{
            shrink: true,
            style: {fontSize: text_height}
          }}
          variant="filled"
        />
      </div>
    </div>
  );
}

export default DistanceAngle;
