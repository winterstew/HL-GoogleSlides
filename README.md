# HLRender
Parses Hero Lab Pathfinder portfolio files and renders custom stat blocks or character sheets

The impetous behind HLRender is that as a [Pathfinder](https://paizo.com/pathfinder) game master I love the ability to build custom characters and monsters in [Hero Lab](https://www.wolflair.com/hero-lab-classic/).  I can tweak and customize each characters abilities and gear during game preparation to build a unique encounter.  However, during actual game play I prefer to have physical copies of the stat blocks in front.  I also like to customize the stat block layout so I can find what I want at a glance.

## Install

### Python

### needed modules

### edit HLRender.bat to call the GUI

### create and install Google OAuth2 client ID
To use the GoogleSheet renderer, you will have to create an OAuth client ID for the application.  Then you will have to download the client_secrets.json file and authorize HLRender to access your Google Drive and Google Sheets.  

1. create a new project for HLRender at https://console.developers.google.com
2. under the "APIs & Services" -> Dashboard select "ENABLE APIS AND SERVICES" 
   - you need to enable "Google Drive API" 
   - and "Google Slides API"
3. under "API & Service" -> Credentials select the "OAuth consent screen" tab
   - Enter "HLRender" as the application name
   - Choose "Add scope" and select "../auth/drive" and "../auth/presentations" 
      - this is necessary as the GoogleSlide renderer copies your template to a new file and then duplicates the pages within it for each character in the portfolio
4. under "API & Service -> Credentials" select "Create credentials" -> "OAuth Client ID"
   - Select "Other" radio box for "Application Type" and enter "Python Desktop Application" as its name
5. back at "API & Service" -> Credentials" click the download JSON button and save the file as client_secret.json in the HLRender directory
6. authorize HLRender to access your google drive and slides
   - from the command line
   - from the GUI
  
