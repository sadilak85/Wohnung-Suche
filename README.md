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

https://www.immosuchmaschine.de/

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

How to download a **Google Driver for Selenium**:

1) Go to the page:  https://chromedriver.chromium.org/downloads

2) Select the aprropriate executable file download link, as depicted below:

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/WebDriverChromeDownload.png" width="60%">

----------------------

After having your Selenium driver, you can download now the entire repo to your local machine. 


There are user specific files in **UserInputs** folder. One of them is **UserDataInput.txt**.

You will fill in this file ("UserDataInput.txt") with correct inputs on appropriate areas.

https://github.com/sadilak85/Wohnung-Suche/blob/main/UserInputs/UserDataInput.txt

Another important issue:
In "UserDataInput.txt" file, the last line is reserved for **Chrome user profile path** which is important to get rid of privacy settings pop ups in the absensce of any cookies, disabling selenium work properly.

How to set User Profile for Chrome: 

1) type in your browser this:   chrome://version/  

2) find in the page the necessary path: 

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/ChromeUserProfile.png" width="60%">

----------------------

Another file to modify by yourself in this "UserInputs" folder is **MessageTemplate.txt**:

https://github.com/sadilak85/Wohnung-Suche/blob/main/UserInputs/MessageTemplate.txt

This is your **message template** file to use as a text to fill in "Nachricht" message in online formular (form). There are parametric strings inside, like $myname , $mynumber, etc. Leave these words unchanged, your input values from "UserDataInput.txt" will replace on these parametric strings, but you can change anything in this file.

Similarly, **EmailTemplate.html** is for you to modify, a message text for emails in html format. You can find many email templates in html through a web search. What you must do is to change the message text part inside an appropriate html tag, again leaving parametric strings as described above.

If you are lazy enough, then simply copy paste your text from "MessageTemplate.txt" file into the <p> </p> tags inside the "EmailTemplate.html" file. But don't be too lazy not looking carefully in other parts, for example do not to forget to replace your Address with mine :)

----------------------

Output folder --> **log files**, with information on the objects focused (the ones that you will find and send messages) with web scraping packages of python. 

Output folder --> sub directory: **ExtractedEmails**  --> Possible email addresses on the object urls, program will ask you in the end to check the email addresses in the files in this sub-directory, to validate them in order to send extra emails automatically with a personalized, good looking way. You can validate those emails via the url provided in the files. If you think that some/all emails are not valid, only delete those emails from the files without deleting other things. 

----------------------

**Last Notes:**

It is free to download and use. In case of any bugs, errors, please contact to the author:

s_adilak@hotmail.com

Mostly Chrome driver is used to develop the tool. Recommended to use Chrome. Other browser options are only set up in the code sections for future implementations.

For **email_writer.py** (to write automatic email at the end) to function properly if you have email input as **gmail**, there is one more setup to overcome google security. You must only enable "less secure app" option in your google account. Here is how you find this out:

<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/LessSecureAppFind.png" width="60%">


<img src="https://github.com/sadilak85/Wohnung-Suche/blob/main/pics/LessSecureAppEnable.png" width="60%">

Don't forget to add your email password into the file **emailpassword.txt** Program will contact smtp server through your email and password similarly as you manually type in browser and login. That is why you must enter your password into this file in the working directory. 

Good luck with your "Wohnung" search!



author: Serhat Adilak
