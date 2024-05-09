# anonymous-recording-download

> ### **Note:**

> The following sample application is a personal, open-source project shared by the app creator and not an officially supported Zoom Video Communications, Inc. sample application. Zoom Video Communications, Inc., its employees and affiliates are not responsible for the use and maintenance of this application. Please use this sample application for inspiration, exploration and experimentation at your own risk and enjoyment. You may reach out to the app creator and broader Zoom Developer community on https://devforum.zoom.us/ for technical discussion and assistance, but understand there is no service level agreement support for this application. Thank you and happy coding!

This is a sample application for a specific purpose. The need was to anonymously capture voicemails left on a specific voicemail box so that they could be downloaded without knowledge of the caller or phone number. 

# Installation

Clone this project

```
git clone https://github.com/PandaBacon21/anonymous-recording-download.git
```

Change to project directory

```
cd anonymous-recording-download
```

It is recommended to use a virtual environment using which ever method you prefer.

Once your virtual environment is created and activated, install project dependencies

```
pip install -r requirements.txt
```

You will need to create a Zoom Server-to-Server OAuth app in order to gain credentials required and define scopes needed. Please see instructions [here](https://developers.zoom.us/docs/internal-apps/s2s-oauth/).

You will also need to create (if not done already) an [Auto Receptionist](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061421) in your Zoom Phone Admin Portal that sends all calls directly to voicemail on the current extention 24/7. 

You will then need to give a specific user access to [voicemails](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0069406#h_f2297d99-00de-4a28-92cd-c0831066c555) for that specific auto receptionist. Currently, Zoom does not allow for pulling voicemails for auto receptionists or call queues directly via API, so you will do so by retrieving voicemails for a specific users, and then parsing out only the voicemails for that particular auto receptionist. 

The ```TARGET_EMAIL``` below will be the email address of the user with access to that particular auto receptionist.
The ```TARGET_AUTO_RECEPTIONIST``` below will be the name of the particular auto receptionist you need to retrieve the voicemails for. 


Create ```.env``` file to save sensitive variables

```
ACCOUNT_ID = 'YourZoomAccountId'
CLIENT_ID = 'YourZoomClientId'
CLIENT_SECRET = 'YourZoomClientSecret'
DB_LOCATION = 'PathToYourDataBase'
TARGET_EMAIL = 'EmailOfZoomUserWithVoicemailBoxAccess'
TARGET_AUTO_RECEPTIONIST = 'NameofAutoReceptionistToReceiveVoicemails'
VOICEMAIL_DOWNLOAD_LOCATION = 'LocationOfVoicemailStorageDirectory'
```

I just used a sqlite database to store the access token as to not have to continuely request a token every time this script runs, but you can choose to handle that however you'd like.

Lastly, you could go another step further and set up a specific Site for this Auto Receptionist and under the Site Policy Settings, you can chose to auto delete the call logs and voicemails after a set retention period. This can be set to delete after a single day for example, allowing you to schedule the retreival via the API prior to deletion to ensure no call history or voicemail remains within Zoom. By default, these retention periods are set to an unlimited time frame. 
