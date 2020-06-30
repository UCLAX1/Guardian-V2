import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { styled } from '@material-ui/core/styles';


const AntSwitch = withStyles((theme) => ({
  root: {
    width: props => props.r_width,
    height: props => props.r_height,
    padding: props => props.r_padding,
    display: 'flex',
  },
  switchBase: {
    padding: 3,
    color: theme.palette.grey[500],
    '&$checked': {
      transform: `translateX(-10px)`,
      '& + $track': {
        opacity: 1,
        backgroundColor: '#228B22',
        borderColor: '#228B22'
      },
    },
  },
  thumb: {
    width: props => props.t_width,
    height: props => props.t_height,
    boxShadow: 'none',
  },
  track: {
    border: `1px solid ${theme.palette.grey[500]}`,
    borderRadius: 16/2,
    opacity: 1,
    backgroundColor: '#FF0000',
    borderColor: '#FF0000'
  },
  checked: {}
})) (Switch);


class OnOffButton extends React.Component{
  state = {controls:false};

  handleChange = (event) => {
    this.setState({controls: event.target.checked});
    this.props.onClick(!this.state.controls);
  };

  render() {

    var font_size = Math.round( 21 * this.props.width / this.props.base_width );
    var root_width = Math.round( 50 * this.props.width / this.props.base_width );
    var root_height = Math.round( 20 * this.props.height / this.props.base_height );
    var root_padding = 3 * this.props.width / this.props.base_width;
    var thumb_width = Math.round( 1 * this.props.width / this.props.base_width );
    var thumb_height = Math.round( 1 * this.props.height / this.props.base_height );
    var space = Math.round(2 * this.props.width / this.props.base_width);

    return (
      <FormGroup>
        <Typography component="div">
          <Grid component="label" container alignItems="center" spacing={2}>
            <Grid item style ={{color:'#FF0000', fontWeight: 'bold', fontSize: font_size + 'px'}}>CONTROLS</Grid>
            <Grid item>
              <AntSwitch
                checked={this.state.controls} onChange={this.handleChange} name="checkedC"
                r_width = {root_width}
                r_height = {root_height}
                r_padding = {root_padding}
                t_width = {thumb_width}
                t_height = {thumb_height}
              />
            </Grid>
            <Grid item style ={{color:'#228B22', fontWeight: 'bold', fontSize: font_size + 'px'}}>HISTORY</Grid>
          </Grid>
        </Typography>
      </FormGroup>
    );
  }
}

export default OnOffButton;
