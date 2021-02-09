🆆🅾🅷🅽🆄🅽🅶 🆂🆄🅲🅷🅴

Welcome to Wohnung Suche tool!


This python selenium based tool provides available rental apartments on the following websites:

https://www.immobilienscout24.de/

https://www.immowelt.de/

https://immobilienmarkt.sueddeutsche.de/

https://www.immonet.de/

https://www.ivd24immobilien.de/

https://www.null-provision.de/

https://www.wohnungsboerse.net/

... 

(below ones are not implemented yet:)

https://www.meinestadt.de/

...

User will specify choices in the input file , like number of rooms, his/her budget, personal information (Name, Address).


Tool is based on python language, essentially a python package "selenium" which automatically searches objects in websites given above with user defined properties (location, price, room numbers, etc.) and fills the forms then sends messages defined by the user as a template before.

Here is the selenium package:

https://selenium-python.readthedocs.io/

You will need a driver for your browser to execute this tool. Drivers are executable files. 

For example, for a Chrome browser, you will need a Chrome driver for selenium compatible with your browser's version.

Let's have a look... 

How to see the Chrome version:

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/ChromeVersion.png" width="60%">

How to download a Google Driver for Selenium:

1) Go to the page:  https://chromedriver.chromium.org/downloads

2) Select the aprropriate executable file download link, as depicted below:

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/WebDriverChromeDownload.png" width="60%">


You will fill in the file first to run the tool efficiently and without any possible errors. 

So first you will fill in the file called "UserDataInput.txt" in the working directory.

https://github.com/sadilak85/Wohnung-Suche/blob/main/UserDataInput.txt

Another important issue:
In "UserDataInput.txt" file, the last line is reserved for Chrome user profile path which is important to get rid of privacy settings pop ups in the absensce of any cookies, disabling selenium work properly.

How to set User Profile for Chrome: 

1) type in your browser this:   chrome://version/  

2) find in the page the necessary path: 

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/ChromeUserProfile.png" width="60%">

Output folder --> log files are filled with information on the objects focused (the ones that you will find and send messages) with web scraping packages of python. 

Last Notes:

It is still under construction and is buggy. Mostly Chrome driver is used to develop the tool. Recommended to use Chrome. Other browser options are only written in the code sections for future implementations.
