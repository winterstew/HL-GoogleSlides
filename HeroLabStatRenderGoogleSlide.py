# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import VERBOSITY
from HeroLabStatRender import Renderer
import httplib2,mimetypes,re,os
from PIL import Image
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

DEFAULTMATCHER = 'GoogleSlide'
TEMPLATENAME = "StatBlockVertical Template"
PAGENAME = "BestiaryStyle-Image"
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-HLRender.json
SCOPES = ('https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive')
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'HLRender'
KEYS_WITH_TEXT = (u'pageElements',u'elementGroup',u'shape',u'table',u'children',
                  u'text',u'textElements',u'textRun',u'content',u'tableRows',
                  u'tableCells')



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
        self.slideName = len(self.options) > 1 and self.options[1:] or [PAGENAME]
        self.credentials = self.get_credentials(flags=flags)
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('slides', 'v1', http=self.http)
        self.drive_service = discovery.build('drive', 'v3', http=self.http)


    def startPortfolio(self,*args,**kwargs):
        """ locate Google Drive Presentation and Slides within it and create matcher instances"""
        # find presentation
        (self.presentationId,self.parents) = self.copy_template(self.drive_service,self.templateName,self.portfolio.filecore)
        self.presentation = self.service.presentations().get(presentationId=self.presentationId).execute()
        if self.verbosity >= 2: print('Created:"%s" "%s"' % (self.portfolio.filecore,self.presentationId))
        # generate slide list and slideId list
        self.slides = self.presentation.get('slides')
        self.slideIds = map(lambda x:x.get('objectId'),self.slides)
        # find slide to use with characters that have an image and for those that do not
        self.imageSlideId = [self.findSlideByText('{{' + re.sub(r'-(No)?[Ii]mage',r'-Image',sn) + '}}') for sn in self.slideName]
        self.noImageSlideId = [self.findSlideByText('{{' + re.sub(r'-(No)?[Ii]mage',r'-Noimage',sn) + '}}') or self.imageSlideId[sni] for sni,sn in enumerate(self.slideName)]
        self.characterIndex = 0
        if self.verbosity >= 6: print(self.slideIds)
        if self.verbosity >= 2: 
            for si in self.imageSlideId: print("Image Slide: %s" % si) 
        if self.verbosity >= 2: 
            for si in self.noImageSlideId: print("NoImage Slide: %s" % si)

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
        # loop through select slides to use
        for idIndex,slideId in enumerate(self.noImageSlideId):
            if hasattr(character,"images") and hasattr(character.images,"imageList") and len(character.images.imageList) > 0:
                slideId = self.imageSlideId[idIndex]
            # duplicate slide
            body = { "requests":  [ {
              "duplicateObject": {
                "objectId":  slideId
              }
            } ] }
            response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()
            newSlideId = response.get('replies')[0]['duplicateObject']['objectId']
            newSlide = self.service.presentations().pages().get(presentationId=self.presentationId,pageObjectId=newSlideId).execute()
            # create image matcher instance
            imageMatcher = self.matcherClass(character,self.matcherClass.IMAGEMATCH,'image',verbosity=self.verbosity)
            # create text matcher instance
            textMatcher = self.matcherClass(character,self.matcherClass.TEXTMATCH,'text',verbosity=self.verbosity)
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
            imageDict = {}
            for replaceKey in re.findall(r'(\{\{.*?\}\})',self.contentDig(newSlide,u'',textKeys=KEYS_WITH_TEXT)):
                images = imageMatcher.getMatch(replaceKey)
                # with GoogleSheets images need to have their keyword text within a shape,
                # and are replaced with a batchUpdate request of replaceAllShapesWithImage
                # this means that inserting a list of images will not work
                imageFile = type(images) == list and images[0] or images
                if imageFile and type(imageFile) == tuple:
                    # create an empth image if none exists
                    if not imageFile[1] or not os.path.exists(imageFile[1]):
                        imageFile = ('empty.png',os.path.join(character.tempDir,'empty.png'))
                        if not os.path.exists(imageFile[1]):
                            emptyImage = Image.new('RGBA',(50,50),color=(255,255,255,0))
                            emptyImage.save(imageFile[1])
                            emptyImage.close()
                    # upload the image
                    upload = self.drive_service.files().create(
                        body={'name': imageFile[0],
                              'parents': self.parents,
                              'mimeType': mimetypes.guess_type(imageFile[1])[0]},
                        fields='id, owners, permissions, webContentLink, mimeType, name',
                        media_body=imageFile[1]).execute()
                    # get its ID
                    file_id = upload.get('id')
                    
                    ## get its URL
                    ## access_token in query no longer supported
                    #image_url = '%s&access_token=%s' % (self.drive_service.files().get_media(fileId=file_id).uri, self.credentials.access_token)

                    # open up sharing for image
                    permission = self.drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
                    permission_id = permission.get('id')
                    # get URL
                    image_url = upload.get('webContentLink')
                    imageDict[replaceKey] = (file_id,image_url,permission_id)
            # run through all the tags again this time
            # appending to the requests to replace with images
            for replaceKey in imageDict.keys():
                image_url = imageDict[replaceKey][1]
                body['requests'].append({
                  'replaceAllShapesWithImage': {
                    'imageUrl': image_url,
                    'imageReplaceMethod': 'CENTER_INSIDE',
                    "pageObjectIds": [newSlideId],
                    'containsText': {
                      'text': replaceKey,
                      'matchCase': True
                    }
                  }
                })
            # Finally execute the big request
            response = self.service.presentations().batchUpdate(presentationId=self.presentationId,body=body).execute()
            self.characterIndex += 1
            # Remove the temporary image file from Drive.
            for file_id,permission_id in [(image[0],image[2]) for image in imageDict.values()]:
                if file_id != '': 
                    pass
                    self.drive_service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
                    self.drive_service.files().delete(fileId=file_id).execute()

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
                                       'slides.googleapis.com-python-HLRender.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            #setattr(kwargs['flags'],'logging_level','CRITICAL')
            #kwargs['flags'].logging_level=50
            #print(kwargs['flags'])
            #if 'flags' in kwargs:
            #    print('first one')
            #    credentials = tools.run_flow(flow, store, flags=kwargs['flags'])
            #else: 
            #    print('second one')
            #    from argparse import ArgumentParser
            #    credentials = tools.run_flow(flow, store, flags=ArgumentParser().parse_args())
            from argparse import Namespace
            n = Namespace()
            f = hasattr(kwargs,'flags') and kwargs['flags'] or None
            n.logging_level= (f and hasattr(f,'logging_level') and getattr(f,'logging_level')) or 'ERROR'
            n.auth_host_name= (f and hasattr(f,'auth_host_name') and getattr(f,'auth_host_name')) or 'localhost'
            n.auth_host_port= (f and hasattr(f,'auth_host_port') and getattr(f,'auth_host_port')) or [8080, 8090]
            n.noauth_local_webserver= (f and hasattr(f,'noauth_local_webserver') and getattr(f,'noauth_local_webserver')) or False
            credentials = tools.run_flow(flow, store, flags=n)
            if 'verbosity' in kwargs and kwargs['verbosity'] >= 1: print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def copy_template(service,templateName,newName,*args,**kwargs):
        """Returns presentationId and parents of newly copied template"""
        newId = None
        page_token=None
        parents = []
        #print(templateIds.keys())
        while True:
            response = service.files().list(q="mimeType='application/vnd.google-apps.presentation'",
                                 spaces='drive',
                                 fields='nextPageToken, files(id,name,mimeType,parents)',
                                 pageToken=page_token).execute()
            for presentation in response.get('files', []):
                if presentation.get('name') == templateName:
                    newResponse = service.files().copy(fileId=presentation.get('id'),
                                 body={ 'name': newName }).execute()
                    newId = newResponse.get('id')
                    parents = presentation.get('parents')
                    #if self.verbosity >= 2: print('"%s" copied to "%s"' % (presentation.get('name'),newresponse.get('name')))

            page_token = response.get('nextPageToken',None)
            if page_token is None:
                break
        return (newId,parents)
            
if __name__ == '__main__':
    GoogleSlideRenderer.get_credentials()