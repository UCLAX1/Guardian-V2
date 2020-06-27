import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: '25ch',
  },
}));

export default function DistanceAngle() {
  const classes = useStyles();
  return (
    <div className={classes.root}>

      <div>
        <TextField
          id="distance_text_field"
          label="DISTANCE (cm)"
          style={{ margin: 8 }}
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
          variant="filled"
        />

        <TextField
          id="angle_text_field"
          label="ANGLE (degrees)"
          style={{ margin: 8 }}
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
          variant="filled"
        />

      </div>

    </div>
  );
}
