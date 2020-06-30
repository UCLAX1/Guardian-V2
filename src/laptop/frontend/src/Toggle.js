import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { styled } from '@material-ui/core/styles';


class Toggle extends React.Component{

  render() {

    var font_size_1 = Math.round( 21 * this.props.width / this.props.base_width );
    var font_size_2 = Math.round( 16 * this.props.width / this.props.base_width );

    return (
      <FormGroup>
        <Typography component="div">
          <Grid component="label" container alignItems="center" spacing={2}>
            <Grid item style ={{color:'#B8E7F4', fontWeight: 'bold', fontSize: font_size_1 + 'px'}}>CONTROLS</Grid>
            <Grid item style ={{color:'#000000', fontWeight: 'bold', fontSize: font_size_2 + 'px'}}>toggle</Grid>
            <Grid item style ={{color:'#B8E7F4', fontWeight: 'bold', fontSize: font_size_1 + 'px'}}>HISTORY</Grid>
          </Grid>
        </Typography>
      </FormGroup>
    );
  }
}

export default Toggle;
