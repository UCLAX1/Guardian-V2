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
    backgroundColor:'#2F80ED', // '#2F80ED' theme.palette.common.black
    color: theme.palette.common.white,
    fontWeight: 'bold',
    fontSize: 16,

  },
  body: {
    size: 'small',
    fontSize: 14,
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

    if (rows_data[i] == "NA"){
      row_obj = createData("N/A","N/A","N/A","N/A","N/A");
    }
    else{
      var row_entries = rows_data[i].split(",");
      var time = row_entries[row_entries.length-1];

      var time_trunc = [time.substring(0,time.length-4)]; //add -4 later to leave only 2 decimal seconds
      var link_coord = ["(" + row_entries[1] + "," + row_entries[2] + ")"];
      var laser_coord = ["("+ row_entries[3] + "," + row_entries[4] + ")"];
      var dist_offset = row_entries.slice(5,6);
      var ang_offset = row_entries.slice(6,7);

      row_obj = createData(time_trunc, link_coord, laser_coord, dist_offset, ang_offset);

    }


    //var row_result = time_trunc + link_coord + laser_coord + dist_offset + ang_offset;
    //[time_trunc].concat(row_entries.slice(1,6));

    //console.log(row_result);
    //var row_obj = createData(row_result[0], row_result[1], row_result[2], row_result[3], row_result[4]);

    rows.push(row_obj);
    //console.log("rows.length");
    //console.log(rows.length);


  }
  return rows;
}

function createData(time, link_coord, laser_coord, dist_offset, ang_offset) {
  return { time, link_coord, laser_coord, dist_offset, ang_offset };
}

var rows = [

  createData('04/06/20 12:43:29.78 ', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),

];





const useStyles = makeStyles({
  table: {
    width: 700,
    height: 400,
    //minWidth: 700, //700
  },
});

export default function LinkTable(props) {
  const classes = useStyles();
  //console.log(props.rows);
  var rows = createRows(props.rows_data);
  console.log(rows);




  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell align="center">Time</StyledTableCell>
            <StyledTableCell align="center">Link Coords</StyledTableCell>
            <StyledTableCell align="center">Laser Coords</StyledTableCell>
            <StyledTableCell align="center">Dist Offset</StyledTableCell>
            <StyledTableCell align="center">Angle Offset</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <StyledTableRow key={row.name}>
              <StyledTableCell component="th" scope="row" align="center" width="30%"> {row.time}</StyledTableCell>
              <StyledTableCell align="center" width="20%">{row.link_coord}</StyledTableCell>
              <StyledTableCell align="center" width="20%">{row.laser_coord}</StyledTableCell>
              <StyledTableCell align="center" width="15%">{row.dist_offset}</StyledTableCell>
              <StyledTableCell align="center" width="15%">{row.ang_offset}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
