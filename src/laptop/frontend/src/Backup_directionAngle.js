import React from 'react';
import PropTypes from 'prop-types';
//import MaskedInput from 'react-text-mask';
//import NumberFormat from 'react-number-format';
import { makeStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function DirectionAngle() {
  const classes = useStyles();
  const [values, setValues] = React.useState({
    textmask: '(cm)',
    numberformat: '(degree)',
  });

  const handleChange = (event) => {
    setValues({
      ...values,
      [event.target.name]: event.target.value,
    });
  };

  return (
    <div className={classes.root}>
      <FormControl>
        <InputLabel htmlFor="formatted-text-mask-input"  style = {{fontSize:"24px"}}> Distance (cm)</InputLabel>
        <Input
          value={values.textmask}
          onChange={handleChange}
          name="textmask"
          id="formatted-text-mask-input"
          style = {{fontSize:"18px"}}

        />


      </FormControl>

      <FormControl>
        <InputLabel htmlFor="formatted-text-mask-input"  style = {{fontSize:"24px"}}> Angle (degree)</InputLabel>
        <Input
          value={values.numberformat}
          onChange={handleChange}
          name="numberformat"
          id="formatted-numberformat-input"
          style = {{fontSize:"18px"}}

        />


      </FormControl>

    </div>
  );
}
*/
