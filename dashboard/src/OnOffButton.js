import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { styled } from '@material-ui/core/styles';



//withStyles((theme)
const AntSwitch = withStyles((theme) => ({
  root: {
    width: 70, //28 //16 //50
    height: 30, //16 //12 //24
    padding: 3.8, //3, size of ball relative to button
    display: 'flex',
  },
  switchBase: {
    padding: 3, //2 really means top
    color: theme.palette.grey[500],
    '&$checked': {
      transform: 'translateX(42px)', //how much it moves
      color: theme.palette.common.white,
      '& + $track': {
        opacity: 1,
        backgroundColor: '#2F80ED', //theme.palette.primary.main,
        borderColor: '#2F80ED'//theme.palette.primary.main,
      },
    },
  },
  thumb: {
    width: 26, //12
    height: 26, //12
    boxShadow: 'none',
  },
  track: {
    border: `1px solid ${theme.palette.grey[500]}`,
    borderRadius: 16/2, //16/2
    opacity: 1,
    backgroundColor: theme.palette.common.white,
  },
  checked: {},
})) (Switch);


const InlineFormControlLabel = styled(FormControlLabel)({
  display: 'inline-block'
});



class OnOffButton extends React.Component{
  state ={controls:false};

  handleChange = (event) => {
    //console.log(this.state.controls);
    //console.log(this.props.textstring);

    //console.log("controls value in handleChange before");
    //console.log(this.state.controls);

    //console.log(this);
    this.setState({controls: event.target.checked}); //needs to set state for this OnOffButton for it to rerender

    //console.log("controls value in handleChange after");
    //console.log(this.state.controls);

    //added a ! because it seems that this.state.controls does not change immediately after the setState call.
    this.props.onClick(!this.state.controls); //send the controls state back to the parent, who can then make controls disappear or not,


  };

  render(){
    return (
      <FormGroup>
        <Typography component="div">
          <Grid component="label" container alignItems="center" spacing={2}>
            <Grid item style ={{color:'#2F80ED', fontWeight: 'bold', fontSize:'20px' }}>CONTROLS</Grid>
            <Grid item>
              <AntSwitch checked={this.state.controls} onChange={this.handleChange} name="checkedC" />
            </Grid>
            <Grid item style ={{color:'#2F80ED', fontWeight: 'bold', fontSize:'20px' }}>HISTORY</Grid>
          </Grid>
        </Typography>
      </FormGroup>
    );
  }
}
export default OnOffButton;

/*
export default function OnoffButton(props) {
  const [state, setState] = React.useState({
    checkedA: true,
    checkedB: true,
    checkedC: true,
  });

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    props.renderControls(this.state.checkedC);

  };


  console.log(props.textstring); //the props passing worked here

  return (
    <FormGroup>
      <Typography component="div">
        <Grid component="label" container alignItems="center" spacing={2}>
          <Grid item style ={{color:'#2F80ED', fontWeight: 'bold' }}>HISTORY</Grid>
          <Grid item>
            <AntSwitch checked={state.checkedC} onChange={handleChange} name="checkedC" />
          </Grid>
          <Grid item style ={{color:'#2F80ED', fontWeight: 'bold' }}>CONTROLS</Grid>
        </Grid>
      </Typography>
    </FormGroup>
  );
}
*/

/*

class SearchBar extends React.Component{
  state ={term:''};

  onFormSubmit = (event)=>{

    event.preventDefault();

    props.onSearchEntered(this.state.term);
  }

  render(){
    return(
      <div className = "ui segment">
        <form onSubmit={this.onFormSubmit}className = "ui form">
          <div  className = "field">
            <label> Image Search </label>
            <input type ="text"
            value = {this.state.term}
            onChange ={(e)=>this.setState({term:e.target.value})} //update the state term as the most up to date user input
            />
          </div>
        </form>
      </div>
    );
  }
}

//export default SearchBar;
*/
