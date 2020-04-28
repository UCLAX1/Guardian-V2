import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import MoveButton from './MoveButton.js';
import DownloadButton from './DownloadButton.js';
import GradientButton from './GradientButton.js'
import OnOffButton from './OnOffButton.js';
import DistanceAngle from './DistanceAngle.js'
import Header from './Header.js'
import CoordTable from'./Table.js'
import Spinner from './Spinner.js'
//comment out hamburger and project
//pulling from local csv and render the table data automatically
//pure: sliding window, one at a time
//shift everything to the left


//combine network's work


//4/20: merge column coordinates ()
//add Distance Offset and Angle Offset as 2 new columns
//Pixel dimensions: 960 x 720

//download log: route to Downloads. Have bar at the bottom showing progress. Have a dummy csv/
//download files generally: get general path


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
  state = {controls:false, video:false};

  render(){
    return(
      <div className = "dashboard">
        {this.renderContent()};
      </div>
    );

  }

  renderContent(){
    //{this.renderVideo()}
    //{this.renderImage()}

    return (
      <div>
        <Header/>
        {this.renderTable_Download()}
        {this.renderVideo()}
        {this.renderOnOffButton()}
        {this.renderControls()}
      </div>
    );

  }


  onToggleSwitch = (controls) =>{
    //console.log("onToggleSwitch is called");
    //console.log("value of controls is");
    //console.log(controls);

    this.setState({controls:controls});

  }
  renderOnOffButton = () =>{
      return(
        <div style = {{  position: 'absolute', top: '220px', left: '1300px'}} className = 'OnOffButton'>
         <OnOffButton onClick = {this.onToggleSwitch}  value = "hello"/>
        </div>

      );

  }
  renderTable_Download(){

    if (this.state.controls){
        return (
        <div className = 'History'>
          <div style= {{  position: 'absolute', top: '700px', left: '1350px'}} className = 'Download'>
            <DownloadButton
              filename = 'log.csv'
              text = 'DOWNLOAD'
            />
          </div>

          <div style ={{  position: 'absolute', top: '320px', left: '1060px'}}>
            <CoordTable/>
          </div>
        </div>
      );
    }
  }


  renderControls = ()=>{
    if (!this.state.controls){
      return(
        <div>
          <div className = "controls" style = {{  position: 'absolute', top: '330px', left: '1250px'}}>
            <DistanceAngle/>
          </div>

          <div style= {{  position: 'absolute', top: '540px', left: '1380px'}} className = 'execute_move'>
            <GradientButton  text = "EXECUTE"  />
          </div>
        </div>

      );
    }
    //console.log("I'm called! And bool value in function:")
    //console.log(this.state.controls);
    //return <div> no controls</div>;
  }





  renderVideo = () => {
    if (this.state.controls){
      return (
        <div>
          {this.renderImage()}
          <h2 style = {{position:'absolute', top:870, left:50, color:'#2F80ED'}}>Pixel Dimensions: 960 x 720 </h2>
        </div>
      );
      /*
      return(
        <video style = {{position:'absolute', top:150, left:50, maxWidth:960,height:720}} controls >
          Your brower does not support this video format.
        </video>
      );
      */
    }
    return (
        <div style = {{position:'absolute', top:150, left:50, width: 960, height:720 }}>
          <Spinner/>
          <h2 style = {{position:'absolute', top:900, left:50, color:'#2F80ED'}}>Pixel Dimensions: 960 x 720 </h2>
        </div>

    );
  }

  renderImage(){
    return (
      <div style = {{position:'absolute', top:150, left:50}}>
        <img style = {{borderRadius:5}} src={require('./data/test_pic.jpg')} />
      </div>
    );

  }



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
    if (this.state.controls){
        return (
        <div style= {{  position: 'absolute', top: '700px', left: '1360px'}} className = 'Download'>
          <GradeintButton  text = "DOWNLOAD LOG"  />
        </div>
      );
    }
  }
  */






ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
