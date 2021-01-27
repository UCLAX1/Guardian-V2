## Intro to Darknet:
    
The directory darknet-master contains all the files needed to do basic testing and training with the link detection system.
It's pretty overwhelming, but to start off with only worry about the files contained in 'darknet-master\test' . This is where
almost all the code actually written by this team and all the files used by the Guardian are located. The rest is mainly
existing infrastructure to make darknet detection work.

- - - -

## Testing:

All the files you need for local testing are in 'darknet-master\test'
This directory contains scripts for testing detection on multiple images and collecting analytics.


However, the default behavior of darknet is to test a single file. 
To do so, navigate to 'darknet-master/test' and invoke a console command with the following form:

`darknet.exe detector test data\link.data cfg\yolo-link.cfg weights\yolo-link_final.weights -ext_output -out result.json`

This will load the specified weights file, which is based on the specified config (cfg) file, then prompt you for an image path. 
Enter any image path, relative to 'darknet-master\test', and darknet will attempt to draw bounding boxes around recognized objects, 
which are specified in 'data\link.data', displaying the result.


To make the script more useful, it allows us to pass in a text file containing a list of images to process. This file should
be specified in link.data, and should list all the relative paths of the images we want to perform detection on. The invocation 
should now look like:

`darknet.exe detector test data\link.data cfg\yolo-link.cfg weights\yolo-link_final.weights -ext_output -out result.json < data\test.txt`

Where data\test.txt is the list we are processing and is specified in data\link.data. The python scripts contained in 
'darknet-master\test' use these files to pass to the darknet program, so be careful making changes to them. If you change the files
in the 'data/test' directory, these changes must be reflected in test.txt . 

By invoking the command above, darknet will pause after every image, showing you the detection result. However, this behavior can 
be changed, and needs to be for our implementation. The python scripts in 'darknet-master\test' handle this.

- - - -

## Training:
Training is much more computationally intensive, and as a result we use virtual hardware to perform this task. 

Additionally, training requires a set of images along with a set of pre-made labels for these images. To create these labels is no
trivial task, and we use a tool called 'labelImg' to help speed up this process.

Once you have a set of images and labels you want to train with, upload the file 'colab\Tutorial_DarknetToColab.ipynb' to Google drive,
and open it using Google Colab. We do this because of the powerful, free processing available. The ipynb file itself contains detailed
instructions on how to make use of it, but for additional info check the colab\README.md .

From our experience, training takes about 1 hour/1000 iterations, and you would want to do a good 12000 - 20000 iterations of training
before stopping.
