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
/*
function TextMaskCustom(props) {
  const { inputRef, ...other } = props;

  return (
    <MaskedInput
      {...other}
      ref={(ref) => {
        inputRef(ref ? ref.inputElement : null);
      }}
      mask={['(', /[1-9]/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]}
      placeholderChar={'\u2000'}
      showMask
    />
  );
}

TextMaskCustom.propTypes = {
  inputRef: PropTypes.func.isRequired,
};


function NumberFormatCustom(props) {
  const { inputRef, onChange, ...other } = props;

  return (
    <NumberFormat
      {...other}
      getInputRef={inputRef}
      onValueChange={(values) => {
        onChange({
          target: {
            name: props.name,
            value: values.value,
          },
        });
      }}
      thousandSeparator
      isNumericString
      prefix="$"
    />
  );
}

NumberFormatCustom.propTypes = {
  inputRef: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
};
*/
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
