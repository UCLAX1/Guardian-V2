import React from 'react';
import { styled } from '@material-ui/core/styles';
import { withStyles, makeStyles } from '@material-ui/core/styles';

import ToggleButton from '@material-ui/lab/ToggleButton';
import Button from '@material-ui/core/Button';


const HelperButton = styled(Button)({
  background: 'linear-gradient(45deg, #56CCF2 30%, #2F80ED 90%)',
  border: 0,
  borderRadius: 5,
  color: 'white',
  display: 'flex',
  flexDirection:'column',
  textAlign: 'center', //horizontal center
  justifyContent: 'center', // vertical center
  textDecoration: 'none'
});

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

const DownloadButton = (props) => {

  var download_height = Math.round( 48 * props.height / props.base_height );
  var download_width = Math.round( 160 * props.width / props.base_width );
  var download_padding = Math.round( 30 * props.width / props.base_width ).toString();
  var font_size = Math.round( 15 * props.width * props.height / props.base_area ).toString();

  return (
    <div className="parent">
      <HelperButton onClick={() => fetch_all_data()} style = {{height: download_height, width: download_width, padding: '0 ' + download_padding + 'px', fontSize: font_size + 'px'}} className="download">
        DOWNLOAD
      </HelperButton>
    </div>
  );
};

export default DownloadButton;
