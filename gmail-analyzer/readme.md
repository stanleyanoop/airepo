# Gmail Analyzer App

## Introduction

This application is to automatically delete the gmail. When the number of emails in the gmail server are multiple thousands, it does not make sense to delete manually. Hence, this small script will be utilized to bulk delete the gmails from the given account.

There will be an anlyzer logic implemented to check the content of the email before we delete using the script. This will be checking for the configurable keyword's for its presence and skip without deleting, so that we might be able to check back in case needed. Also, there will be blind skipping of emails from configured emails (or domains such as @accenture.com, @cognizant.com etc)

This will be integrated with the Gemini flash AI model, to enhance the skipping logic as a second step.

## Dependencies

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Environment Setup for Gmail Cleanup Tool
To keep your Gmail API credentials secure, this project uses a credentials file that is never committed to GitHub.
Instead, you’ll have to create your own local credentials.json file with your personal credentials and add to the local repository.

1. Create and Add Your Gmail API Credentials

You can get these values from:
Google Cloud Console → APIs & Services → Credentials → Create OAuth Client ID
Download the credentials file, and rename it to "credentials.json" and copy it to the root folder of this project (./gmail-analyzer)

3. Keep credentials.json Private
	•	The credentials file must not be pushed to GitHub.
	•	This repo already includes credentials.json in .gitignore to prevent accidental commits.

4. First Run

On the first run, the script will:
	1.	Read your GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET from credentials.json
	2.	Launch the browser for you to sign in to Gmail and authorize
	3.	Save your session token in token.json (also in .gitignore)

## How to run

### One touch run

For executing the script, check out the code, make sure the .env file is properly updated with the client id and secret and execute the run.sh script from the root directory of this project (./gmail-analyzer)
```
./run.sh
```

### Step by Step execution

For running the script, we need to have python installed, and all the dependencies in the requirements.txt file installed on the virutal environment/environment.

The virtual environment should be activated for running the application so that all the dependencies installed in the virtual environment will be accessible to the scripts.

```
cd <REPO HOME DIR>
python3 -m venv lc-agent-env
source lc-agent-env/bin/activate

python app.py
```
Please note that when you run it for the first time, it will prompt you with the OAUTH screen of gmail. You need to select the target gmail account for the clean up, and authenticate. This is one time activity for a particular gmail ID. However if you want to switch between gmail IDs, please follow the below steps.

Please note that, all these steps are scripted within the run.sh, and if you run the one touch option, you dont have to worry about any of the venv stuff.

### Switching Gmail accounts
When you authenticate the selected gmail account, it will create a token.pickle (token.json in our case) file in your local. This file will be used everytime you try to access the GMAIL API service, and you dont have to provide the authentication each and everytime, as long as this file exists in the root folder in the code base. Delete this token.json before running the script to trigger OAuth to select a different Gmail account. Example:
```
rm token.json
python app.py
```