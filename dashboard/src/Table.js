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

function createData(time, link_coord, laser_coord, dist_offset, ang_offset) {
  return { time, link_coord, laser_coord, dist_offset, ang_offset };
}

const rows = [
  createData('04/06/20 12:43:29.78 ', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
  createData('04/06/20 12:43:29.78', '(159, 423)', '(159, 423)', 30, 46),
];


const useStyles = makeStyles({
  table: {
    minWidth: 700,
  },
});

export default function CoordTable() {
  const classes = useStyles();

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
