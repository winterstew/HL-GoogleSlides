# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import *
from HeroLabStatRender import Renderer
import httplib2,mimetypes,re,os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

TEMPLATENAME = "StatBlock Template"
PAGENAME = "NPC-Combat-Image"
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-quickstart.json
SCOPES = ('https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive')
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'HL-GoogleSlides'
KEYS_WITH_TEXT = (u'pageElements',u'elementGroup',u'shape',u'table',u'children',
                  u'text',u'textElements',u'textRun',u'content',u'tableRows',
                  u'tableCells')


"""
def get_credentials(*args,**kwargs):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'slides.googleapis.com-python-HL-GoogleSlides.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        if self.verbosity >= 1: print('Storing credentials to ' + credential_path)
    return credentials

def copy_template(service,templateName,newName,*args,**kwargs):
    newId = None
    page_token=None
    #print(templateIds.keys())
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.presentation'",
                             spaces='drive',
                             fields='nextPageToken, files(id,name,mimeType)',
                             pageToken=page_token).execute()
        for presentation in response.get('files', []):
            if presentation.get('name') == templateName:
                newResponse = service.files().copy(fileId=presentation.get('id'),
                             body={ 'name': newName }).execute()
                newId = newResponse.get('id')
        page_token = response.get('nextPageToken',None)
        if page_token is None:
            break
        return newId

templateName =  TEMPLATENAME
slideName =  PAGENAME
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('slides', 'v1', http=http)
drive_service = discovery.build('drive', 'v3', http=http)
presentationId = copy_template(drive_service,templateName,'testtemplate')
presentation = service.presentations().get(presentationId=presentationId).execute()
slides = presentation.get('slides')
slideIds = map(lambda x:x.get('objectId'),slides)
"""

class GoogleSlideRenderer(Renderer):
    """
    GoogleSlide Renderer takes a Portfolio and a GoogleSlide Template the Character and creates the output
    document from either a template and the Matcher or just based on the
    Matcher keywords alone.

    Methods:
      startPortfolio: issued after creating a Portfolio object to start rendering
      eachCharacter
      endPortfolio

    Attributes:

    """

    def __init__(self,portfolio,flags,matcherClass,*args,**kwargs):
        super(GoogleSlideRenderer, self).__init__(portfolio,flags,matcherClass,*args,**kwargs)
        self.templateName = len(self.options) > 0 and self.options[0] or TEMPLATENAME
        self.slideName = len(self.options) > 1 and self.options[1] or PAGENAME
        self.credentials = self.get_credentials(**kwargs)
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('slides', 'v1', http=self.http)
        self.drive_service = discovery.build('drive', 'v3', http=self.http)

    def render(self,*args,**kwargs):
        self.startPortfolio()
        for c in self.portfolio.characters:
            self.eachCharacter(c)
        self.endPortfolio()

    def startPortfolio(self,*args,**kwargs):
        """ locate Google Drive Presentation and Slides within it and create matcher instances"""
        # find presentation
        self.presentationId = self.copy_template(self.drive_service,self.templateName,self.portfolio.filecore)
        self.presentation = self.service.presentations().get(presentationId=self.presentationId).execute()
        if self.verbosity >= 2: print('Created:"%s" "%s"' % (self.portfolio.filecore,self.presentationId))
        # generate slide list and slideId list
        self.slides = self.presentation.get('slides')
        self.slideIds = map(lambda x:x.get('objectId'),self.slides)
        # find slide to use with characters that have an image and for those that do not
        self.imageSlideId = self.findSlideByText('{{' + re.sub(r'-(No)?[Ii]mage',r'-Image',self.slideName) + '}}')
        self.noImageSlideId = self.findSlideByText('{{' + re.sub(r'-(No)?[Ii]mage',r'-Noimage',self.slideName) + '}}')
        self.characterIndex = 0
        if self.verbosity >= 6: print(self.slideIds)
        if self.verbosity >= 2: print("Image Slide: %s" % self.imageSlideId)
        if self.verbosity >= 2: print("NoImage Slide: %s" % self.noImageSlideId)

    def findSlideByText(self,findText,*args,**kwargs):
        """ return the first slideId for slide containing the findText """
        for slideId in self.slideIds:
            # try to replace the findText with the same text
            body = { "requests":  [ {
              "replaceAllText": {
                "replaceText":  findText,
                "pageObjectIds": [slideId],
                "containsText": {
                  "text": findText,
                  "matchCase": True
                }
              }
            } ] }
            response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()
            # if the replacement succeded then the text is in the slide
            topReply = response.get('replies')[0]['replaceAllText']
            if "occurrencesChanged" in topReply.keys() and topReply["occurrencesChanged"] > 0:
                return slideId
        return None

    def eachCharacter(self,character,*args,**kwargs):
        # select slide to use
        slideId = self.noImageSlideId
        if hasattr(character,"images") and hasattr(character.images,"imageList") and len(character.images.imageList) > 0:
            slideId = self.imageSlideId
        # create image matcher instance
        imageMatcher = self.matcherClass(character,self.matcherClass.IMAGEMATCH,'image')
        # duplicate slide
        body = { "requests":  [ {
          "duplicateObject": {
            "objectId":  slideId
          }
        } ] }
        response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()
        newSlideId = response.get('replies')[0]['duplicateObject']['objectId']
        newSlide = self.service.presentations().pages().get(presentationId=self.presentationId,pageObjectId=newSlideId).execute()
        # create text matcher instance
        textMatcher = self.matcherClass(character,self.matcherClass.TEXTMATCH,'text')
        body = { "requests": [ {
                   "updateSlidesPosition": {
                     "slideObjectIds": [ newSlideId ],
                     "insertionIndex": self.characterIndex
                   }
                 } ] }
        # run through all the flag text from the template and replace from the matched
        for replaceKey in re.findall(r'(\{\{.*?\}\})',self.contentDig(newSlide,u'',textKeys=KEYS_WITH_TEXT)):
            body['requests'].append({
              "replaceAllText": {
                "replaceText":  textMatcher.getMatch(replaceKey),
                "pageObjectIds": [newSlideId],
                "containsText": {
                  "text": replaceKey,
                  "matchCase": True
                }
              }
            })
        # run through all the flags with an image matcher and
        # upload images keeping a keyed list on URLs
        # I am also going to have to figure out mimeTypes for the images
        #
        # then run through all the tags again this time
        # appending to the requests to replace with images
        #
        # finally execute the request
        # then clean up the images whish were uploaded
        #imageElem = character.find('images').find('image')
        #File_id=''
        #print(imageElem)
        #if ( imageElem != None ) :
        #    imageFile = imageElem.get('filename')
        #    #print(imageFile)
        #    upload = drive_service.files().create(
        #        body={'name': imageFile, 'mimeType': 'image/jpeg'},
        #        media_body=os.path.join(os.path.abspath(os.path.curdir),imageFile)).execute()
        #    file_id = upload.get('id')

        #    # Obtain a URL for the image.
        #    image_url = '%s&access_token=%s' % (drive_service.files().get_media(fileId=file_id).uri, credentials.access_token)

        #    body['requests'].append({
        #      'replaceAllShapesWithImage': {
        #        'imageUrl': image_url,
        #        'replaceMethod': 'CENTER_INSIDE',
        #        "pageObjectIds": [newSlideId],
        #        'containsText': {
        #          'text': '{{image}}',
        #          'matchCase': True
        #        }
        #      }
        #    })
        response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()
        self.characterIndex += 1
        # Remove the temporary image file from Drive.
        #if file_id != '': drive_service.files().delete(fileId=file_id).execute()


    def endPortfolio(self,*args,**kwargs):
        body = { "requests": [] }
        for slideId in self.slideIds:
            body["requests"].append({ "deleteObject": { "objectId":slideId }})
        response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()

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
                                       'slides.googleapis.com-python-HL-GoogleSlides.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if 'flags' in kwargs:
                credentials = tools.run_flow(flow, store, kwargs['flags'])
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            if 'verbosity' in kwargs and kwargs['verbosity'] >= 1: print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def copy_template(service,templateName,newName,*args,**kwargs):
        """Returns presentationId of newly copied template"""
        newId = None
        page_token=None
        #print(templateIds.keys())
        while True:
            response = service.files().list(q="mimeType='application/vnd.google-apps.presentation'",
                                 spaces='drive',
                                 fields='nextPageToken, files(id,name,mimeType)',
                                 pageToken=page_token).execute()
            for presentation in response.get('files', []):
                if presentation.get('name') == templateName:
                    newResponse = service.files().copy(fileId=presentation.get('id'),
                                 body={ 'name': newName }).execute()
                    newId = newResponse.get('id')
                    #if self.verbosity >= 2: print('"%s" copied to "%s"' % (presentation.get('name'),newresponse.get('name')))

            page_token = response.get('nextPageToken',None)
            if page_token is None:
                break
            return newId