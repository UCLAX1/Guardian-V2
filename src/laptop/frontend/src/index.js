import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import MoveButton from './MoveButton.js';
import DownloadButton from './DownloadButton.js';
import GradientButton from './GradientButton.js'
import OnOffButton from './OnOffButton.js';
import DistanceAngle from './DistanceAngle.js'
import Header from './Header.js'
import LinkTable from'./Table.js'
import Spinner from './Spinner.js'




class Dashboard extends React.Component {
  state = {controls:false, video:false, frame_counter:0, render:false};

  render(){
    return(
      <div className = "dashboard">
        {this.renderContent()};
      </div>
    );

  }

  renderContent(){

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


    this.setState({controls:controls});

  }


  renderOnOffButton = () =>{
      return(
        <div style = {{  position: 'absolute', top: '220px', left: '1270px'}} className = 'OnOffButton'>
         <OnOffButton onClick = {this.onToggleSwitch}  value = "hello"/>
        </div>

      );

  }

  //given this.state.frame_counter, process test_data so that rows_data contains exactly 5 rows
  read_5_rows (){
    var rows_data = [];

    if (this.state.frame_counter > 4){
      rows_data = this.test_data.slice(this.state.frame_counter-5,this.state.frame_counter);
    }

    else{ //if current l
      rows_data = this.test_data.slice(0,this.state.frame_counter);
    }
    var missing = 5 - rows_data.length;

    var k;
    for (k=0; k<missing; k++){
      rows_data.push("NA"); //NA________________       rows_data.push("NA,NA,NA,NA,NA,NA,NA");
    }

    return rows_data;

  }

  renderTable_Download(){
    //if controll button is currently toggled:
    if (this.state.controls){
      var rows_data = this.read_5_rows();

        return (
        <div className = 'History'>
          <div style= {{  position: 'absolute', top: '790px', left: '1350px'}} className = 'Download'>
            <DownloadButton
              filename = 'log.csv'
              text = 'DOWNLOAD'
            />
          </div>

          <div style ={{  position: 'absolute', top: '320px', left: '1060px'}}>
            <LinkTable rows_data = {rows_data}/>
          </div>
        </div>
      );
    }
  }


  renderControls = ()=>{
    if (!this.state.controls){
      return(
        <div>
          <div className = "controls" style = {{  position: 'absolute', top: '330px', left: '1220px'}}>
            <DistanceAngle/>
          </div>

          <div style= {{  position: 'absolute', top: '540px', left: '1350px'}} className = 'execute_move'>
            <GradientButton  text = "EXECUTE"  />
          </div>
        </div>

      );
    }

  }





  renderVideo = () => {

    return (
        <div style = {{position:'absolute', top:150, left:50, width: 960, height:720 }}>
          <img style = {{borderRadius:5}} src={require('./data/video_frame_' + (this.state.frame_counter+1).toString(10) + '.jpg')} />
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

  test_data=
  [
    '1662,60,53,57,51,7,46,2020-04-27 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',
    '1661,41,62,98,35,81,24,2020-04-27 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-27 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-04-27 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-04-27 15:36:14.519775',
    '1662,60,53,57,51,7,46,2020-04-28 15:36:14.529748',
    '1661,41,62,98,35,81,24,2020-04-29 15:36:14.526756',
    '1660,99,72,50,40,58,76,2020-04-30 15:36:14.524763',
    '1659,70,30,74,20,49,34,2020-05-01 15:36:14.521769',
    '1658,5,94,6,21,19,73,2020-05-02 15:36:14.519775',

  ];

  //fetch function: right now it's just setting state and causing the screen to rerender
  //the acutal data we use right now is a local var called test_data in this class
  fetch_new_frame =  () => {
    console.log("frame_counter:");
    //console.log(this.state.frame_counter);
    var new_counter = this.state.frame_counter + 1;

    if (this.state.frame_counter < 200){// CHANGE later, hard coded now
      //this.update_frame_counter();
      this.setState({frame_counter: new_counter});
      return true;
    }
    else{
      return false;
    }
  };

  componentDidMount(){

    this.intervalID = setInterval(
     () => this.fetch_new_frame(),
     100
     );

   }

   componentWillUnmount() {
     clearInterval(this.intervalID);
   }


  componentDidUpdate(prevProps, prevState){


  }



}

ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);
