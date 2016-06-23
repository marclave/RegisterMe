RegisterMe
==========

Automates course registration at UVic, ideal for first years competitively registering for courses

##Requirements

1. Python is installed (Tested with version 2.6.8)
2. mechanize library is installed [Mechanize download!](http://wwwsearch.sourceforge.net/mechanize/download.html) V0.2.5
3. PyYAML libray is installed [PyYAML download!](pyyaml.org/wiki/PyYAML) V3.11

##Setup
Clone this repository:
```
git clone https://github.com/marclave/RegisterMe.git
```
Modify the profile to include your information, example:
```
UVIC_LOGIN:
  USERNAME: astudent
  PASSWORD: cleverPassword
SEMESTER:
  FIRST: "First Term: Sep - Dec 2014"
  SUMMER: "Summer Session: May - Aug 2015"
  SECOND: "Second Term: Jan - Apr 2015"
DESIRED_SEMESTER:
  SECOND
GMAIL:
  ADDRESS: A.STUDENT@gmail.com
  PASSWORD: lessCleverPassword
CRN:
  - 101010
```

You need to allow less secure app access for your gmail account. [Less secure app access](https://support.google.com/accounts/answer/6010255) 

Then test run:
```
python RegisterMe.py --test
```
Review the ouput to ensure everything is fine.

Now you can setup a cron to run this script, example to run everyday at midnight:
```
0 23 * * * python /path/to/script/RegisterMe/RegisterMe.py
```
If you run windows, set up a Windows Task Scheduler
 
##Description

When run, RegisterMe logs into UVic's website, and attempts to register for desired courses. If successful, you will recieve an email with this notification.

Developed for simple use, RegisterMe uses a profile where all the required information is stored and used.
