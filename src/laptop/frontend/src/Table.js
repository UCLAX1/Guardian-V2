import React from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';


const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor:'#2F80ED',
    color: theme.palette.common.white,
    fontWeight: 'bold'
  },
  body: {
    size: 'small'
  },
}))(TableCell);


const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
}))  (TableRow);


function createRows(rows_data) {
  var rows = [];
  var size = rows_data.length;
  var i;

  for (i = 0; i < size; i++) {
    var row_obj = {};

    if (rows_data[i] == "NA")
    {
      row_obj = createData("N/A","N/A","N/A","N/A","N/A");
    }
    else
    {
      var row_entries = rows_data[i].split(",");
      var time = row_entries[row_entries.length-1];

      var time_trunc = [time.substring(0,time.length-4)]; //add -4 later to leave only 2 decimal seconds
      var link_coord = ["(" + row_entries[1] + "," + row_entries[2] + ")"];
      var laser_coord = ["("+ row_entries[3] + "," + row_entries[4] + ")"];
      var dist_offset = row_entries.slice(5,6);
      var ang_offset = row_entries.slice(6,7);

      row_obj = createData(time_trunc, link_coord, laser_coord, dist_offset, ang_offset);
    }
    rows.push(row_obj);
  }
  return rows;
}


function createData(time, link_coord, laser_coord, dist_offset, ang_offset) {
  return { time, link_coord, laser_coord, dist_offset, ang_offset };
}


export default function LinkTable(props) {

  var rows = createRows(props.rows_data);
  var table_height = Math.round( 400 * props.height / props.base_height );
  var table_width = Math.round( 700 * props.width / props.base_width );
  var header_font = Math.round( 18 * props.width / props.base_width );
  var body_font = Math.round( 16 * props.width / props.base_width );
  var time_width = Math.round( 40 * props.width / props.base_width ).toString() + "%";
  var coords_width = Math.round( 15 * props.width / props.base_width ).toString() + "%";
  var offset_width = Math.round( 15 * props.width / props.base_width ).toString() + "%";

  return (
    <TableContainer component={Paper}>
      <Table style = {{ width: table_width, height: table_height}} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell align="center" width={time_width} style = {{ fontSize: header_font}}>Time</StyledTableCell>
            <StyledTableCell align="center" width={coords_width} style = {{ fontSize: header_font}}>Link Coords</StyledTableCell>
            <StyledTableCell align="center" width={coords_width}style = {{ fontSize: header_font}}>Laser Coords</StyledTableCell>
            <StyledTableCell align="center" width={offset_width}style = {{ fontSize: header_font}}>Dist Offset</StyledTableCell>
            <StyledTableCell align="center" width={offset_width} style = {{ fontSize: header_font}}>Angle Offset</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <StyledTableRow key={row.name}>
              <StyledTableCell component="th" scope="row" align="center" width={time_width} style = {{ fontSize: body_font}}> {row.time}</StyledTableCell>
              <StyledTableCell align="center" width={coords_width} style = {{ fontSize: body_font}}>{row.link_coord}</StyledTableCell>
              <StyledTableCell align="center" width={coords_width} style = {{ fontSize: body_font}}>{row.laser_coord}</StyledTableCell>
              <StyledTableCell align="center" width={offset_width} style = {{ fontSize: body_font}}>{row.dist_offset}</StyledTableCell>
              <StyledTableCell align="center" width={offset_width} style = {{ fontSize: body_font}}>{row.ang_offset}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
