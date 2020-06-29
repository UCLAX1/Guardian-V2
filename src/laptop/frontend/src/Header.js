import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(4),
  },
  title: {
    flexGrow: 1,
  },
}));

//want to add: left:'50%', top:'50%' in typography style
export default function Header() {
  const classes = useStyles();

  return (
    <div className={classes.root} style = {{position:'absolute', width:'100%'}}>
      <AppBar position="static" style={{backgroundColor:'#2F80ED'}}>
        <Toolbar>
          {/*<IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>*/}
          <Typography variant="h5" className={classes.title} style = {{textAlign: 'center'}}>
            X1 Robotics: The Guardian
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
  );
}
