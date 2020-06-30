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
import Toggle from './Toggle.js';
import Spinner from './Spinner.js';


class Dashboard extends React.Component {


  state = {controls:false, video:false, frame_counter:0, render:false, currentImg:require('./data/intro.jpg'), tableData:[], specificData:[], width: 0, height: 0, base_width: 1920, base_height: 947, base_area: 1818240};
  updateWindowDimensions = this.updateWindowDimensions.bind(this);

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
    var toggle_top = Math.round( 220 * this.state.height / this.state.base_height ).toString();
    var toggle_left = Math.round( 1370 * this.state.width / this.state.base_width ).toString();
    var text_top = Math.round( 200 * this.state.height / this.state.base_height ).toString();
    var text_left = Math.round( 1371 * this.state.width / this.state.base_width ).toString();

      return(
        <div>
        <div style = {{  position: 'absolute', top: toggle_top + 'px', left: toggle_left + 'px'}} className = 'OnOffButton'>
          <OnOffButton
            onClick = {this.onToggleSwitch}
            width = {this.state.width}
            height = {this.state.height}
            base_width = {this.state.base_width}
            base_height = {this.state.base_height}
            base_area = {this.state.base_area}
          />
        </div>
        <div style = {{  position: 'absolute', top: text_top + 'px', left: text_left + 'px'}} className = 'Toggle'>
          <Toggle
            width = {this.state.width}
            height = {this.state.height}
            base_width = {this.state.base_width}
            base_height = {this.state.base_height}
            base_area = {this.state.base_area}
          />
        </div>
        </div>
      );
  }

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
    var clear_top = Math.round( 780 * this.state.height / this.state.base_height ).toString();
    var clear_left = Math.round( 1440 * this.state.width / this.state.base_width ).toString();
    var download_top = Math.round( 840 * this.state.height / this.state.base_height ).toString();
    var download_left = Math.round( 1440 * this.state.width / this.state.base_width ).toString();
    var table_top = Math.round( 300 * this.state.height / this.state.base_height ).toString();
    var table_left = Math.round( 1170 * this.state.width / this.state.base_width ).toString();

    if (this.state.controls){
      const tableData = this.update_table();
        return (
          <div className = 'History'>
            <div style= {{  position: 'absolute', top: clear_top + 'px', left: clear_left + 'px'}} className = 'Clear'>
              <ClearButton
                width = {this.state.width}
                height = {this.state.height}
                base_width = {this.state.base_width}
                base_height = {this.state.base_height}
                base_area = {this.state.base_area}
              />
            </div>
            <div style= {{  position: 'absolute', top: download_top + 'px', left: download_left + 'px'}} className = 'Download'>
              <DownloadButton
                width = {this.state.width}
                height = {this.state.height}
                base_width = {this.state.base_width}
                base_height = {this.state.base_height}
                base_area = {this.state.base_area}
              />
            </div>
            <div style ={{  position: 'absolute', top: table_top + 'px', left: table_left + 'px'}}>
              <LinkTable
                rows_data = {tableData}
                width = {this.state.width}
                height = {this.state.height}
                base_width = {this.state.base_width}
                base_height = {this.state.base_height}
                base_area = {this.state.base_area}
              />
            </div>
          </div>
      );
    }
  }

  renderControls = () => {
    var controls_top = Math.round( 300 * this.state.height / this.state.base_height ).toString();
    var controls_left = Math.round( 1305 * this.state.width / this.state.base_width ).toString();
    var execute_top = Math.round( 550 * this.state.height / this.state.base_height ).toString();
    var execute_left = Math.round( 1440 * this.state.width / this.state.base_width ).toString();

    if (!this.state.controls){
      return(
        <div id="container">
          <div className = "controls" style = {{  position: 'absolute', top: controls_top + 'px', left: controls_left + 'px'}}>
            <DistanceAngle
              width = {this.state.width}
              height = {this.state.height}
              base_width = {this.state.base_width}
              base_height = {this.state.base_height}
              base_area = {this.state.base_area}
            />
          </div>

          <div style= {{  position: 'absolute', top: execute_top + 'px', left: execute_left + 'px'}} className = 'execute_move'>
            <ExecuteButton
              width = {this.state.width}
              height = {this.state.height}
              base_width = {this.state.base_width}
              base_height = {this.state.base_height}
              base_area = {this.state.base_area}
            />
          </div>
        </div>
      );
    }
  }

  renderDisplay = () => {
    const imageName = this.state.currentImg;
    var image_top = Math.round( 27 + 120 * this.state.height / this.state.base_height ).toString();
    var image_left = Math.round( 50 * this.state.width / this.state.base_width ).toString();
    var image_width = Math.round( 960 * this.state.width / this.state.base_width ).toString();
    var image_height = Math.round( 720 * this.state.height / this.state.base_height ).toString();
    var text_top = Math.round( 870 * this.state.height / this.state.base_height ).toString();
    var text_left = Math.round( 50 * this.state.width / this.state.base_width ).toString();
    var text_font = Math.round( 20 * this.state.width / this.state.base_width ).toString();

    return (
        <div className = "display">
          <img style = {{borderRadius:5}}  src={imageName} style = {{position:'absolute', top: image_top + 'px', left: image_left + 'px', width: image_width + 'px', height: image_height + 'px'}}/>
          <p style = {{position:'absolute', fontSize: text_font + 'px', top: text_top + 'px', left: text_left + 'px', color:'#2F80ED'}}>Pixel Dimensions: 960 x 720 </p>
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
    this.updateWindowDimensions();
    window.addEventListener(('resize'), this.updateWindowDimensions);
   }

  componentWillUnmount() {
     clearInterval(this.interval_frame);
     clearInterval(this.interval_data);
     window.removeEventListener(('resize'), this.updateWindowDimensions);
  }

  updateWindowDimensions() {
    this.setState({width: window.innerWidth, height: window.innerHeight});
  }

  componentDidUpdate(prevProps, prevState){

  }
}

ReactDOM.render(
    <Dashboard />,
  document.getElementById('root')
);
