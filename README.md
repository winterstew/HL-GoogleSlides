# HLRender
Parses Hero Lab Pathfinder portfolio files and renders custom stat blocks or character sheets

The impetous behind HLRender is that as a [Pathfinder](https://paizo.com/pathfinder) game master I love the ability to build custom characters and monsters in [Hero Lab](https://www.wolflair.com/hero-lab-classic/).  I can tweak and customize each characters abilities and gear during game preparation to build a unique encounter.  However, during actual game play I prefer to have physical copies of the stat blocks in front.  I also like to customize the stat block layout so I can find what I want at a glance.

## Install
This was written for Python 2.7

### needed modules
#### for anything
- string
- re
- os
- tempfile
- zipfile
- shutil
- sys
- types
- collections
- xml.etree.cElementTree
- argparse
#### for GUI
- PySimpleGUI27,
- subprocess,
- threading,
- Queue
- json
#### for CSpdf render
- pypdftk
#### for GoogleSlide render
- httplib2
- mimetypes
- PIL
- apiclient
- oauth2client
#### for GoogleSheet render
- pickle
- copy
- google-api-python-client 
- google-auth-httplib2 
- google-auth-oauthlib
- pygsheets


### edit HLRender.bat to call the GUI
Currently it is set up to call the Anaconda activate script from the user's Anaconda2 directory and then start the GUI.  

### create and install Google OAuth2 client ID
To use the GoogleSlide renderer, you will have to create an OAuth client ID for the application.  Then you will have to download the client_secrets.json file and authorize HLRender to access your Google Drive and Google Slide.  

1. create a new project for HLRender at [GoogleAPI](https://console.developers.google.com/apis/dashboard)
2. under the "APIs & Services" -> "Dashboard" select "ENABLE APIS AND SERVICES" 
   - you need to enable "Google Drive API" 
   - and "Google Slides API"
3. under "API & Service" -> "Credentials" select the "OAuth consent screen" tab
   - Enter "HLRender" as the application name
   - Choose "Add scope" and select "../auth/drive" and "../auth/presentations" 
      - this is necessary as the GoogleSlide renderer copies your template to a new file and then duplicates the pages within it for each character in the portfolio
4. under "API & Service" -> "Credentials" select "Create credentials" -> "OAuth Client ID"
   - Select "Other" radio box for "Application Type" and enter "Python Desktop Application" as its name
5. back at "API & Service" -> "Credentials" click the download JSON button and save the file as client_secret.json in the HLRender directory
6. authorize HLRender to access your google drive and slides
   - from the command line
     ```
     python HeroLabStatRenderGoogleSlide.py
     ```
   - from the GUI
     click "get Google credentials"
  
## Usage
### GoogleSlide
  The GoogleSlide renderer can take two or more (comma separated) options.  The first is the name of the Google Slide presentation you want to use as the starting template.  The rest of the options are names of pages to duplicate and match-replace for each character.  This page name should be some text on the page, and must be unique whithin the presentation.  Typically I use a page name which is also a key in the matcher that maps to the name of the character.  That way it is replaced during the rendering.  A few examples which I have used or am using include [StatBlock Template](https://drive.google.com/open?id=1C5u4HXB_9jbBXUD6y8l37bxckqei6ipy5TCIRDgsZFw), [StatBlockVertical Template](https://drive.google.com/open?id=1TPJzOrotRVVM5X-tgJI6BCEtY23I_K6DweiOwooaSAE), and [StatBlockVerticalTwoPage Template](https://drive.google.com/open?id=19EYt8vSpSl6kR8-ImSKmekF4uTGCvL7_NrazZV34IWk).  For an explanation of how the keywords work, look in the docs string for [HeroLabStatMatch](HeroLabStatMatch.py), for keyworks which are already defined by default look in the [HeroLabStatMatchGoogleSlide](HeroLabStatMatchGoogleSlide.py) code

### GoogleSheet
  The GoogleSheet renderer cat take two or more (comma separated) options.  The first is the name of the Google Sheet spreadsheet you
  want to use as the starting template.  The rest of the options are names of ranges (in a1 notation) which will be duplicated within
  the sheet and match-replace for each character.  Be aware if the range has more columns than rows, it will insert columns.  Otherwise
  it will insert rows.  The GoogleSheetRenderer(HeroLabStatRenderGoogleSheet.py) uses the same [matcher](HeroLabStatMatchGoogleSlide.py) as GoogleSlideRenderer(HeroLabStatRenderGoogleSlide.py).  An example template can be found at [StatList Template](https://docs.google.com/spreadsheets/d/17gyE-L8508glDQtJGSYijMniYxOTFh3K-UmPNtXg0do/edit?usp=sharing).  Also if the string '``` rrr ```' is used as a separater in list keyword, the renderer will recongnize it and add extra ranges for each item in the list.  This is useful if you want to render an equipment list for the whole portfolio.  This use can be seen in the [GearList Template](https://docs.google.com/spreadsheets/d/1Zw0BHrzt_u9emLCK9Gpwn9y89T-lE9FJ3rsVX8v1gWM/edit?usp=sharing)

### CSpdf
  The CSpdf renderer works with ``Character Sheet fillable.pdf`` which comes from [Paizo](https://www.paizo.com).  Unfortunately, while I have a list of all the fields, I have not yet matched them all up to HLRender values.  It is a very long list, and requires choosing what to include since there are not enough blanks.  This defeats the purpose of quick, easy, and complete transfer in information from Hero Lab, so I am less interested in finishing this.
