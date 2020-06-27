import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import ClearButton from './ClearButton.js';
import DistanceAngle from './DistanceAngle.js';
import DownloadButton from './DownloadButton.js';
import ExecuteButton from './ExecuteButton.js';
import Header from './Header.js';
import LinkTable from'./Table.js';
import OnOffButton from './OnOffButton.js';
import Spinner from './Spinner.js';


class Dashboard extends React.Component {
  state = {controls:false, video:false, frame_counter:0, render:false, currentImg:require('./data/intro.jpg'), tableData:[], specificData:[]};

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
        {this.renderDisplay()}
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

  //given this.state.frame_counter, process tableData so that rows_data contains exactly 5 rows
  update_table(){

    const tableData = this.state.specificData;
    var missing = 5 - tableData.length;

    var k;
    for (k=0; k<missing; k++){
      tableData.push("NA");
    }

    if (tableData[0] == "") {
      tableData[0] = "NA"
    }

    return tableData;

  }

  renderTable_Download(){
    if (this.state.controls){
      const tableData = this.update_table();
        return (
          <div className = 'History'>
            <div style= {{  position: 'absolute', top: '790px', left: '1350px'}} className = 'Clear'>
              <ClearButton/>
            </div>
            <div style= {{  position: 'absolute', top: '850px', left: '1350px'}} className = 'Download'>
              <DownloadButton/>
            </div>
            <div style ={{  position: 'absolute', top: '320px', left: '1060px'}}>
              <LinkTable rows_data = {tableData}/>
            </div>
          </div>
      );
    }
  }


  renderControls = () => {
    if (!this.state.controls){
      return(
        <div>
          <div className = "controls" style = {{  position: 'absolute', top: '330px', left: '1220px'}}>
            <DistanceAngle/>
          </div>

          <div style= {{  position: 'absolute', top: '540px', left: '1368px'}} className = 'execute_move'>
            <ExecuteButton  text = "EXECUTE"  />
          </div>
        </div>
      );
    }
  }


  renderDisplay = () => {
    const imageName = this.state.currentImg;
    return (
        <div className = "display">
          <img style = {{borderRadius:5}}  src={imageName} style = {{position:'absolute', top:150, left:50, width: 960, height:720 }}/>
        </div>
    );
  }

  fetch_new_frame = () => {
    fetch("/image")
      .then(response => response.blob())
      .then(image => {
        this.setState({currentImg: URL.createObjectURL(image)})
      });
  };

  fetch_specific_data = () => {
    fetch("/specificData")
      .then(response => response.text())
      .then(data => {
        this.setState({specificData: data.split("\n")})
      });
  };

  componentDidMount() {
    this.interval_frame = setInterval(() => this.fetch_new_frame(), 300);
    this.interval_data = setInterval(() => this.fetch_specific_data(), 1000);
   }

  componentWillUnmount() {
     clearInterval(this.interval_frame);
     clearInterval(this.interval_data);
  }

  componentDidUpdate(prevProps, prevState){

  }
}

ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);
