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

Create ```.env``` file to save sensitive variables

```
ACCOUNT_ID = 'YourZoomAccountId'
CLIENT_ID = 'YourZoomClientId'
CLIENT_SECRET = 'YourZoomClientSecret'
DB_LOCATION = 'PathToYourDataBase'
TARGET_EMAIL = 'EmailOfZoomUserWithVoicemailBoxAccess'
VOICEMAIL_DOWNLOAD_LOCATION = 'LocationOfVoicemailStorageDirectory'
```

I just used a sqlite database to store the access token as to not have to continuely request a token every time this script runs, but you can choose to handle that however you'd like. 

