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
  //backgroundColor: '#2F80ED', color:'white'
  return (
    <div className={classes.root}>

      <div>
        <TextField
          id="filled-full-width"
          label="DISTANCE"
          style={{ margin: 8 }}
          placeholder="(cm)"
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
          variant="filled"
        />

        <TextField
          id="filled-full-width"
          label="ANGLE"
          style={{ margin: 8 }}
          placeholder="(degree)"
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
