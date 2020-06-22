import React from 'react';
import { styled } from '@material-ui/core/styles';
import { withStyles, makeStyles } from '@material-ui/core/styles';

import ToggleButton from '@material-ui/lab/ToggleButton';
import Button from '@material-ui/core/Button';


//Possible resource
//https://www.npmjs.com/package/react-csv

//learned something today: the text in a button is not encoded in a property value like background
//Two ways to do the same thing: styled and withStyles (in the comment below)


const buttonStyle = {
  background: 'linear-gradient(45deg, #56CCF2 30%, #2F80ED 90%)',
  //boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
  border: 0,
  borderRadius: 5,
  color: 'white',
  padding: '0 30px',
  height: 48,
  width: 160,
  display: 'flex',
  flexDirection:'column',
  textAlign: 'center', //horizontal center
  justifyContent: 'center', // vertical center
  textDecoration: 'none'
}

const fetch_all_data = () => {
  fetch("/allData")
    .then(response => {
      response.text().then(data => {
          let allData = 'ID,Link_X,Link_Y,Laser_X,Laser_Y,Distance_Offset,Angle_Offset,Time\n' + data;
          const csv_file = new Blob(
            [ allData ],
            { type: 'text/csv' }
          );
          const url = URL.createObjectURL(csv_file);
					let a = document.createElement('a');
					a.href = url;
					a.download = 'log.csv';
					a.click();
				});
    });
};

const DownloadButton = () =>{

  return (
    <div className="parent">
      <a style = {buttonStyle} onClick={() => fetch_all_data()} className="download">DOWNLOAD</a>
    </div>
  );
};

export default DownloadButton;
