import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';

import MyToggleButton from './ToggleButton.js';
import MoveButton from './MoveButton.js';
import CustomButton from './StyleToggleButton.js'


//control and history is just one button: one and off light switch
//click on history: show downlaod log button, make controls disappear
//click on controls (by default)
//header: darker shade, same color. x1 robotics: Guardian
//distance(cm): forward and top, angle(degrees): right and left
//
const App = () => {
  return  (
  <div className = "parent" >
    <video style = {{position:'relative', top:110, left:120, maxWidth:600,height:570}} controls >
      Your brower does not support this video format.
    </video>


    <p style = {{position:'absolute',top:700, left:120, color:'#0bace0'}}> LINK X: 452 </p>
    <p style = {{position:'absolute',top:700, left:240, color:'#0bace0'}}> LINK Y: 568 </p>
    <p style = {{position:'absolute',top:730, left:120, color:'#0bace0'}}> LASER X: 128 </p>
    <p style = {{position:'absolute',top:730, left:240, color:'#0bace0'}}> LASER Y: 345 </p>

    <div style = {{  position: 'absolute', top: '110px', left: '1010px'}} className = 'TwoButtons'>
      <MyToggleButton text = "Controls" />
      <MyToggleButton  text = "History"/>
    </div>

    <div style = {{  position: 'absolute', top: '580px', left: '1000px'}} className = 'ThreeMoveButtons'>
      <MoveButton text = "Left"  />
      <MoveButton  text = "Down"/>
      <MoveButton  text = "Right"  />
    </div>

    <div style= {{  position: 'absolute', top: '480px', left: '1100px'}} className = 'Top'>
      <MoveButton  text = "Top"  />
    </div>

    <div style= {{  position: 'absolute', top: '715px', left: '370px'}} className = 'Download'>
      <CustomButton  text = "DOWNLOAD LOG"  />
    </div>





  </div>

  );
};


ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
