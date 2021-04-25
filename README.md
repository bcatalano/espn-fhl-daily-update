# ESPN Fantasy Hockey Daily Update
![image](https://user-images.githubusercontent.com/72364619/114965115-f8d78680-9e3d-11eb-8ae9-a347147705e7.png)
A small utility that uses the relatively unknown and undocumented ESPN fantasy hockey API v3 to update you with the status of your roster every day by email. While this tool is unnecessary, it might save your butt once or twice when you accidentally forget to set your lineup! Some features include:
* Tells you who is injured, out, or players with postponed games
* Informs you of inactive players not on your bench 
* Notifies you of active players that are currently on your bench (if you don't already have the max of a certain position set) including the specific position - __this is the main reason I built this!__
* Tells you if your lineup is set properly

*Note that the ESPN API could change at any point (note the v3). It is likely this script will become non-functional if that is the case.*

## Usage
Simply download the files `main.py`, `config.py`, `lib.py`, and `gmail.py`. Put them all in the same directory. You can simply call the main function by typing `python3 main.py` from your command prompt or terminal, but it is more useful to automate this task through Windows or Mac/Linux. I will show the steps for doing this below. 

## How to use it
To get this to work, you will have to edit `config.py` and follow some steps to get the Gmail API working.

### Editing config.py
Open the config.py in an editor. Anything that is commented out needs to be replaced with the specifics of your league.
![Screenshot 2021-04-16 012641](https://user-images.githubusercontent.com/72364619/114976154-7d80cf80-9e53-11eb-9356-2b35f324ff0e.png)
* `league_id`: This is the number following "leagueId=" in the above url. Replace the comment with this number.
* `year`: This is just the current year of your league.
* `team_id`: This is the number following "teamId=" in the above url.
* `sender`: String containing the email address that the email will be sent from. For example, "brandoncatalano@gmail.com".
* `to`: String with the email address that the notification is sent to. You can set this to the same as sender to send it to yourself.

### Getting your private league's credentials (if needed)
You'll notice that I did not include what should be input for `swid` and `espn_s2`. You only need to provide parameters to these if your league is private. If you're in a public league, you can simply comment out both `swid` and `espn_s2`. You can tell if your league is private by whether or not you needed to be invited to join it, or if you attempt to use the script and you get an invalid credentials error when trying to access the API. I'll show the process of how to do this on Chrome. You will have to look up how to find cookies in your browser if you do not use Chrome.
* Click on the 3 dot symbol in the top right (next to your profile picture). Click on settings.
* Search for "cookies". Click on "Cookies and other site data".
* Click on "See all cookies and site data"
* In the "Search cookies" toolbar, seach for "espn"
* Click on the one that says "espn.com". Note that you will probably have another tab that says "www.espn.com", this is not the right one. 
* Copy the `SWID` and `espn_s2` values as strings (surround them in "") into the config.py file for their respective parameters. Copy them exactly as is, including the "{}" for the SWID.

### Using the Gmail API
I highly recommend following the top answer from [this tutorial](https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python/63847325#63847325) on a StackOverflow forum post that goes into detail on how to set up the Gmail API for usage with Python. __The most important thing is to ensure that the `client_secret.json` file is in the same directory as all the other files!__ I essentially adapted this answer's code to get the Gmail functionality working for this script. If you don't have a Gmail account or your Google account doesn't require OAUTH authentication, take a look at [this](https://realpython.com/python-send-email/) for an idea of how to incorporate generic SMTP communication to get your email to work.

## Automating the script using Task Scheduler
Windows has a really useful feature known as Task Scheduler that can be used to automate tasks, especially tasks such as running Python programs. If you want to automate on Linux or Mac, you will likely need to use something like [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) or modify main.py to use the Python sleep functionality and have it continuously running in the background. To set up Task Scheduler to automate this script, follow these steps:
* Search for "Task Scheduler" in the Windows taskbar
* In the top right, click "Create Basic Task..."
* Name your task something descriptive. Hit next.
* Select the task to trigger daily. Hit next. 
* Select the start date. I recommend selecting 11:00:00 as your start time so that even when matinee games happen you will be updated in time of any issues. Click next.
* Select "Start a program". Click next. 
* Hit "Browse..." and select `main.py` from the directory you saved this repo to. Click next.
* Check "Open the Properties dialog for this task when I click Finish". Click Finish.
* In the General tab, select "Run with highest privileges". You will need to have admin access to do this. Also, in the "Configure for:" drop down menu, select Windows 10.
* Click on the Power tab. If you are on a laptop, unselect the "Start the task only if the computer is on AC power" option. Check "Wake the computer to run this task". Hit OK.
* Navigate to the Task Scheduler Library and make sure that you can find the new task.
* If you want to stop this at any point, simply delete the task by right clicking on it and selecting "Delete"

## Contact me
Contact me at brandoncatalano@gmail.com if you have any questions, comments, concerns, or suggestions. 
