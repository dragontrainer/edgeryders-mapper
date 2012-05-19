Dragon Trainer - Edgeryders network extraction scripts
======================================================

In this repository you'll find the code used to extract a network from the raw data from the Edgeryders site. 


The experiment code is driven by the ```edgeryders_export.rb``` file and uses the classes defined in the ```edgeryders_dataset.rb``` and ```dataset/*.rb``` files. Running the edgeryders_export.rb file you'll obtain the network exported PAJEK format (.net files) whcih is usable also in other network analysis tools (e.g. Tulip or Gephi).

Running the script
------------------

#### Prerequisites

To run the script you need to prepare your computer installing the Ruby interpreter, see here for details on how to do it for your OS: http://www.ruby-lang.org/

#### Downloading the code

Download the code from github and save it in a directory on your computer

#### Preparing the data

You need to obtain the data from the Edgeryders site and you need to put the json files obtained from the Edgeryders site in the ```json``` directory. 

The files should be named as follows:

* _nodes.js_ for the file containing the dump of the Drupal nodes objects
* _comments.js_ for the file containing the comment objects
* _users.js_ for the file containing the user objects

#### Extracting the network

From the command line:

* cd into the edgeryders-mapper directory
* run the command ```ruby -rubygems edgeryders_export.rb```

While running the script will log to the screen traces and eventually errors or warnings it finds.

After the script has run you'll find in the ```export``` directory a new sub-directory named YYYYMMDD-HHmm after the current date and time which will contain the two .net files extracted:

* _edgeryders-ANON.net_ contains the network without any direct user identifying information
* _edgeryders-NAMES.net_ contains the network whcih uses the user's name to identify the nodes


