import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import MoveButton from './MoveButton.js';
import GradeintButton from './GradeintButton.js';
import OnOffButton from './OnOffButton.js';
import DistanceAngle from './DistanceAngle.js'
import Header from './Header.js'


//remove link x link y
//Switch controls and history
//put actual image on
//Add Loadng icon of same size

//Show last 5 data points in a table when you press history
//some ui on the table, dividling line
//bold the header : time, linkx, etc
//04/06/20 12:43:29.79
//5 columns: first is time,
//3 decimal points for link x y
//go above the download button


/*flow chart of eventhandlers:
1.dashboard has a state of controls= true
2. have a OnOffButton.js, and we use it in this main
3. declare a onToggleSwitch function that setState when the onOffButton is pressed (and hence calls the render function)
4. pass the onToggleSwitch as a prop to the onOffButton
5. In onOffButton, create an event handler function for when the button is pressed. Inside that func, call the func that was
passed from the parent with the param of the latest controls state
6.the onToggleSwitch finally setStates and renders
7.Also need to make sure the func render calls has conditionals in it

*/

class Dashboard extends React.Component {
  state = {controls:'true'};

  render(){
    return(
      <div className = "dashboard">
        {this.renderContent()};
      </div>
    );

  }

  renderContent(){
    //{this.renderVideo()}

    return (
      <div >
        <Header/>
        {this.renderVideo()}
        {this.renderOnOffButton()}
        {this.renderControls()}
        {this.renderCoord()}
        {this.renderDownload()}
      </div>
    );

  }
  renderControls = ()=>{
    if (this.state.controls){
      return(
        <div>
          <div className = "controls" style = {{  position: 'absolute', top: '350px', left: '900px'}}>
            <DistanceAngle/>
          </div>

          <div style= {{  position: 'absolute', top: '520px', left: '1040px'}} className = 'execute_move'>
            <GradeintButton  text = "EXECUTE"  />
          </div>
        </div>

      );
    }
    //console.log("I'm called! And bool value in function:")
    //console.log(this.state.controls);
    //return <div> no controls</div>;
  }
  /*
  renderControls = ()=>{
    if (this.state.controls){
      //console.log("renderControls called! And bool value in function:")
      //console.log(this.state.controls);
      return(
        <div className = "controls">
          <div style = {{  position: 'absolute', top: '580px', left: '1000px'}} className = 'ThreeMoveButtons'>
            <MoveButton text = "Left"  />
            <MoveButton  text = "Down"/>
            <MoveButton  text = "Right"  />
          </div>

          <div style= {{  position: 'absolute', top: '480px', left: '1100px'}} className = 'Top'>
            <MoveButton  text = "Top"  />
          </div>
        </div>

      );
    }
    //console.log("I'm called! And bool value in function:")
    //console.log(this.state.controls);
    //return <div> no controls</div>;
  }
  */


  renderCoord(){
    return(
      <div className="coordinates">
        <p style = {{position:'absolute',top:700, left:120, color:'#2F80ED', fontWeight: 'bold'}}> LINK X: 452 </p>
        <p style = {{position:'absolute',top:700, left:240, color:'#2F80ED', fontWeight: 'bold'}}> LINK Y: 568 </p>
        <p style = {{position:'absolute',top:730, left:120, color:'#2F80ED', fontWeight: 'bold'}}> LASER X: 128 </p>
        <p style = {{position:'absolute',top:730, left:240, color:'#2F80ED', fontWeight: 'bold'}}> LASER Y: 345 </p>
      </div>
    );
  }
  renderDownload(){
    if (!this.state.controls){
        return (
        <div style= {{  position: 'absolute', top: '400px', left: '1020px'}} className = 'Download'>
          <GradeintButton  text = "DOWNLOAD LOG"  />
        </div>
      );
    }
  }

  renderOnOffButton = () =>{
      return(
        <div style = {{  position: 'absolute', top: '145px', left: '1000px'}} className = 'OnOffButton'>
         <OnOffButton onClick = {this.onToggleSwitch}  value = "hello"/>
        </div>

      );

  }
  renderVideo(){
    return(
      <video style = {{position:'relative', top:110, left:120, maxWidth:600,height:570}} controls >
        Your brower does not support this video format.
      </video>
    );
  }

  onToggleSwitch = (controls) =>{
    //console.log("onToggleSwitch is called");
    //console.log("value of controls is");
    //console.log(controls);

    this.setState({controls:controls});

  }



  }





ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
