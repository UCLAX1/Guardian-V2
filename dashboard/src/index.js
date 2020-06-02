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
//comment out hamburger and project
//pulling from local csv and render the table data automatically
//pure: sliding window, one at a time
//shift everything to the left
//combine network's work




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
  state = {controls:false, video:false, frame_counter:0, render:false};

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
    //setTimeout(() => { console.log("WAIT!"); }, 2000);
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
    //console.log("missing");
    //console.log(missing);
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
      //console.log("rows_data");
      //console.log(rows_data);

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
    //console.log("I'm called! And bool value in function:")
    //console.log(this.state.controls);
    //return <div> no controls</div>;
  }




  /*
  return(
    <video style = {{position:'absolute', top:150, left:50, maxWidth:960,height:720}} controls >
      Your brower does not support this video format.
    </video>
  );
  */
  renderVideo = () => {
    /*
    if (this.state.controls){
      return (
        <div>
          {this.renderImage()}
        </div>
      );

    }
    */

    //<Spinner/>
    //'./data/test_pic.jpg'
    //var file_path = "./data/rgb_frames/video_frame_" + (this.state.frame_counter+1).toString(10) + ".jpg";

    //var file_path = {'./data/video_frame_' + (this.state.frame_counter+1).toString(10) + '.jpg'};
    //console.log(file_path);
    //'./data/video_frame_1.jpg'

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
    //console.log("new_counter:");
    //console.log(new_counter);

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
    //this.fetch_new_frame();
    /*declaring intervalID but not using it

    when you called setInterval(
     () => this.fetch_new_frame(),
     1000
   );
   you are automaically calling this.fetch_new_frame every 1000 milisecond.
   */

    this.intervalID = setInterval(
     () => this.fetch_new_frame(),
     100
     );

   }

   componentWillUnmount() {
     clearInterval(this.intervalID);
   }


  componentDidUpdate(prevProps, prevState){
    //console.log("update")
    /*
    console.log("prevState.frame_counter")
    console.log(prevState.frame_counter)

    if (prevState.frame_counter == this.state.frame_counter) {
      this.fetch_new_frame();
    }
    */


  }



}

ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);

/*
function fetch_new_frame() {

     //display past image until you fetch new one
     pastImg = currentImg;
     document.querySelector('.display').innerHTML = '<img src=\''+pastImg+'\'>';

     //fetch image
     fetch('image.jpg')
       .then(response => response.blob())
       .then(images => {
           // once you fetch new one display that one
           currentImg = URL.createObjectURL(images)
           document.querySelector('.display').innerHTML = '<img src=\''+pastImg+'\'>'+'<img src=\''+currentImg+'\'>';
           document.querySelector('#update').innerHTML = 'update: ' + counter; counter += 1;
       });

     //fetch data
     fetch('data.txt').then(function(response){
       response.text().then(function(text){
         document.querySelector('#data').innerHTML = 'lazer: ' + text;
       })
     });
   }
*/




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




/*
   this.setState({ boardAddModalShow: true }, ()=> {
     // any code you want to execute only after the newState has taken effect.
            console.log(this.state.boardAddModalShow);
       });
*/


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
