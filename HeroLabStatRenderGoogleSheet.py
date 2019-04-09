# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from __future__ import print_function
from HeroLabStatBase import VERBOSITY
from HeroLabStatRender import Renderer
import sys,mimetypes,re,os,pickle,json
from PIL import Image
#from apiclient import discovery
#from oauth2client import client
#from oauth2client import tools
#from oauth2client.file import Storage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

DEFAULTMATCHER = 'GoogleSlide'
TEMPLATENAME = "StatList Template"
RANGENAME = "Sheet1!B:C"
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/spreadsheets.googleapis.com-python-HLRender.json
SCOPES = ('https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive')
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'HLRender'
ROWS = 'ROWS'
COLUMNS = 'COLUMNS'
#KEYS_WITH_TEXT = (u'pageElements',u'elementGroup',u'shape',u'table',u'children',
#                  u'text',u'textElements',u'textRun',u'content',u'tableRows',
#                  u'tableCells')



class GoogleSheetRenderer(Renderer):
    """
    GoogleSheet Renderer takes a Portfolio, a GoogleSheet Template and a Range
    creates a new GoogleSheet where the Range is duplicated for each character
    and calls the matcher to replace the text.  It is possible to list 
    multiple ranges, but to prevent misaddressing as columns or rows are inserted
    the ranges should be of different sheets within teh spreadsheet

    Methods:
      startPortfolio: issued after creating a Portfolio object to start rendering
      eachCharacter
      endPortfolio

    Attributes:

    """

    def __init__(self,portfolio,flags,matcherClass,*args,**kwargs):
        super(GoogleSheetRenderer, self).__init__(portfolio,flags,matcherClass,*args,**kwargs)
        self.templateName = len(self.options) > 0 and self.options[0] or TEMPLATENAME
        self.rangeNames = len(self.options) > 1 and self.options[1:] or [RANGENAME]
        self.credentials = self.get_credentials(flags=flags)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        
    def startPortfolio(self,*args,**kwargs):
        """ locate Google Drive Spreadsheet and Sheet within it and create matcher instances"""
        # find spreadsheet
        self.spreadsheetId,self.templateId = self.copy_template(
                self.drive_service,self.find_template(self.drive_service,self.templateName),self.portfolio.filecore)
        #self.spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        self.ranges = self.service.spreadsheets().values().batchGet(
                       spreadsheetId=self.spreadsheetId,ranges=self.rangeNames).execute().get('valueRanges')
        if self.verbosity >= 2: print('Created:"%s" "%s"' % (self.portfolio.filecore,self.spreadsheetId)):
            
    @staticmethod
    def getGridRange(service,ssId,rngName):
        sId=0
        # first get the sheetID is there is a sheet listed in the rngNAme
        
            
    def dumpTemplateValueRanges(self,*args,**kwargs):
        tId = hasattr(self,'templateId') and getattr(self,'templateId') or self.find_template(self.drive_service,self.templateName)
        rngs = self.service.spreadsheets().values().batchGet(
                     spreadsheetId=tId,ranges=self.rangeNames).execute()
        print(rngs.viewkeys())
        vRngs = rngs.get('valueRanges')
        for rngIndex,rng in enumerate(vRngs):
            print("Range Number %s",rngIndex)
            json.dump(rng,sys.stdout)
        
    def eachCharacter(self,character,*args,**kwargs):
        requests = []        
        # loop through ranges to replace
        for rngIndex,rng in enumerate(self.ranges):
            # determine if we are inserting rows or columns
            shiftDim = rng.get('majorDimension')
            if max([len(x) for x in rng]) > len(rng):
                shiftDim = shiftDim == ROWS and COLUMNS or ROWS
            # insert rows or columns
            requests.append({
              "insertRangeRequest": {
                "range": {
                },
                "shiftDimension":shiftDim 
              }
            }) 
            # replace all text in the values for the range
            
            # write range with new values to sheet in the shifted locshiftDimation
            
#            body = { "requests":  [ {
#              "duplicateObject": {
#                "objectId":  slideId
#              }
#            } ] }
#            response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
#            newSlideId = response.get('replies')[0]['duplicateObject']['objectId']
#            newSlide = self.service.spreadsheets().pages().get(spreadsheetId=self.spreadsheetId,pageObjectId=newSlideId).execute()
#            # create image matcher instance
#            imageMatcher = self.matcherClass(character,self.matcherClass.IMAGEMATCH,'image',verbosity=self.verbosity)
#            # create text matcher instance
#            textMatcher = self.matcherClass(character,self.matcherClass.TEXTMATCH,'text',verbosity=self.verbosity)
#            body = { "requests": [ {
#                       "updateSlidesPosition": {
#                         "slideObjectIds": [ newSlideId ],
#                         "insertionIndex": self.characterIndex
#                       }
#                     } ] }
#            # run through all the flag text from the template and replace from the matched
#            for replaceKey in re.findall(r'(\{\{.*?\}\})',self.contentDig(newSlide,u'',textKeys=KEYS_WITH_TEXT)):
#                body['requests'].append({
#                  "replaceAllText": {
#                    "replaceText":  textMatcher.getMatch(replaceKey),
#                    "pageObjectIds": [newSlideId],
#                    "containsText": {
#                      "text": replaceKey,
#                      "matchCase": True
#                    }
#                  }
#                })
#            # run through all the flags with an image matcher and
#            # upload images keeping a keyed list on URLs
#            imageDict = {}
#            for replaceKey in re.findall(r'(\{\{.*?\}\})',self.contentDig(newSlide,u'',textKeys=KEYS_WITH_TEXT)):
#                images = imageMatcher.getMatch(replaceKey)
#                # with GoogleSheets images need to have their keyword text within a shape,
#                # and are replaced with a batchUpdate request of replaceAllShapesWithImage
#                # this means that inserting a list of images will not work
#                imageFile = type(images) == list and images[0] or images
#                if imageFile and type(imageFile) == tuple:
#                    # create an empth image if none exists
#                    if not imageFile[1] or not os.path.exists(imageFile[1]):
#                        imageFile = ('empty.png',os.path.join(character.tempDir,'empty.png'))
#                        if not os.path.exists(imageFile[1]):
#                            emptyImage = Image.new('RGBA',(50,50),color=(255,255,255,0))
#                            emptyImage.save(imageFile[1])
#                            emptyImage.close()
#                    # upload the image
#                    upload = self.drive_service.files().create(
#                        body={'name': imageFile[0],
#                              'mimeType': mimetypes.guess_type(imageFile[1])[0]},
#                        media_body=imageFile[1]).execute()
#                    # get its ID
#                    file_id = upload.get('id')
#                    # get its URL
#                    image_url = '%s&access_token=%s' % (self.drive_service.files().get_media(fileId=file_id).uri, self.credentials.access_token)
#                    imageDict[replaceKey] = (file_id,image_url)
#            # run through all the tags again this time
#            # appending to the requests to replace with images
#            for replaceKey in imageDict.keys():
#                image_url = imageDict[replaceKey][1]
#                body['requests'].append({
#                  'replaceAllShapesWithImage': {
#                    'imageUrl': image_url,
#                    'replaceMethod': 'CENTER_INSIDE',
#                    "pageObjectIds": [newSlideId],
#                    'containsText': {
#                      'text': replaceKey,
#                      'matchCase': True
#                    }
#                  }
#                })
#            # Finally execute the big request
#            response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
#            self.characterIndex += 1
#            # Remove the temporary image file from Drive.
#            for file_id in [image[0] for image in imageDict.values()]:
#                if file_id != '': self.drive_service.files().delete(fileId=file_id).execute()

    def endPortfolio(self,*args,**kwargs):
        body = { "requests": [] }
        for slideId in self.slideIds:
            body["requests"].append({ "deleteObject": { "objectId":slideId }})
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def contentDig(self,element,value=u'',**kwargs):
        if type(element) == list:
            for e in element:
                value = self.contentDig(e,value,**kwargs)
        if type(element) == dict:
            for k in element.keys():
                if kwargs.has_key('textKeys') and k in kwargs['textKeys']:
                    value = self.contentDig(element.get(k),value,**kwargs)
        if type(element) == unicode or type(element) == str:
            value += element
        return value

    @staticmethod
    def get_credentials(*args,**kwargs):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'spreadsheets.googleapis.com-python-HLRender.pickle')
        credentials = None
        if os.path.isfile(credential_path):
            with open(credential_path, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(credential_path, 'wb') as token:
                pickle.dump(credentials,token)
                if 'verbosity' in kwargs and kwargs['verbosity'] >= 1: print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def find_template(service,templateName,*args,**kwargs):
        """Returns spreadsheetId of the template"""
        templateId = None
        page_token=None
        #print(templateIds.keys())
        while True:
            response = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'",
                                 spaces='drive',
                                 fields='nextPageToken, files(id,name,mimeType)',
                                 pageToken=page_token).execute()
            for spreadsheet in response.get('files', []):
                if spreadsheet.get('name') == templateName:
                    templateId = spreadsheet.get('id')
                    
            page_token = response.get('nextPageToken',None)
            if page_token is None:
                break
        return templateId
        
    @staticmethod
    def copy_template(service,templateId,newName,*args,**kwargs):
        """Returns spreadsheetId of newly copied template"""
        newResponse = service.files().copy(fileId=templateId,
                                           body={ 'name': newName }).execute()
        return newResponse.get('id')

if __name__ == '__main__':
    #GoogleSheetRenderer.get_credentials()
    r = GoogleSheetRenderer('',{},DEFAULTMATCHER,TEMPLATENAME,RANGENAME)
    r.dumpTemplateValueRanges()