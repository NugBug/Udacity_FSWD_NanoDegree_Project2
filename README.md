# Udacity-FSWD-NanoDegree-Project-1

## Project 2 - Tournament Results (with extra credit additions to support multiple tournaments)

To run the Tournament Results database program and test script, place all downloaded files in the same 
folder within the appropriate vagrant directory (such as '/Users/user/fullstack/vagrant/tournament').
**This help documentation assumes the user has installed their VM correctly using Vagrant and VirtualBox.**

1. Run the VM
From the terminal window, cd into your vagrant directory and type 'vagrant up' to launch the VM.
Type 'vagrant ssh' to log in to the VM.

2. Create the database
Once logged in to the VM, run psql to interact with the PostgreSQL database.
Create the tournament database ('CREATE DATABASE tournament;').
Connect to the tournament database ('\c tournament') and enter the following statement to create the appropriate tables.
'\i tournament.sql'
Exit the database ('\q').

3. Run the test script
cd into the appropriate directory containing Tournament Results files.
From this directory, run the following python script.
'python tournament_test.py'
This will test the Tournament Results database and program functionality.

**Please Note** This database schema and program have been modified to attempt to support more than one tournament in the
database as well as allow players to enter multiple tournaments on the same database.  As such, the tournament_test.py
script has been modified to address new and refactored functions in the tournament.py file to make such a database and 
program work correctly.  Should the test script fail, the database will have to be dropped and steps 2 and 3 will have 
to be repeated to test the database again.  Multiple fails indicate programming error that have been overlooked.