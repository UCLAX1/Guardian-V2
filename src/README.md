# Guardian-V2/src
The project is run on one laptop and two Raspberry Pis, all connected to each other over LAN.

- - - -

To setup the project (for the first time):

* Assign static IPs to both Pis. [Instructions on setting static IPs can be found here.](https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-give-your-raspberry-pi-a-static-ip-address-update)
  * 192.168.0.124 for the Pi Zero
  * 192.168.0.125 for the Pi 3
* Configure the programs on the Pis so that they start running on Pi startup. [Instructions (five different ways) on how to do this can be found here.](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)
* Install and setup MySQL on your computer. Create a user with username 'x1' and password 'asme', and create a table called 'x1_guardian'.

- - - -

To run the project:

* Power up the router
* Connect your laptop to the router
* Navigate to the 'src/laptop/' directory and run './main.sh start'
* Power up both Raspberry Pis

- - - -

To stop running the project:

* Navigate to the 'src/laptop/' directory and run './main.sh stop'
* Power off both Raspberry Pis and the router
