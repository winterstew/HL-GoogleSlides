from __future__ import print_function
import __builtin__
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import xml.etree.cElementTree as et

#
TEMPLATEKEYS = {'combat':'NPCStatBlock-Combat-',
                'noncombat':'NPCStatBlock-NonCombat-'
               }
TEMPLATEIDS = {'NPCStatBlock-Combat-Image Template':'',
               'NPCStatBlock-Combat-NoImage Template':'',
               'NPCStatBlock-NonCombat-Image Template':'',
               'NPCStatBlock-NonCombat-NoImage Template':''
              }

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--template', choices=TEMPLATEKEYS.keys(), default='noncombat')
    parser.add_argument('XMLfiles', metavar='xml-file', type=argparse.FileType('r'), nargs='+', help='HeroLab Protfolio XML output file')
    flags = parser.parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-quickstart.json
SCOPES = ('https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive')
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'HL-GoogleSlides'



def get_portfolio(xmlfile=None):
    """Returns an etree Element portfolio a HeroLab XML file"""
    if (isinstance(xmlfile,__builtin__.file)):
        return et.fromstring(xmlfile.read())
        
def get_credentials():
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
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_templates(service):
    """Returns Dictionary of template presentation IDs"""
    page_token=None
    templateIds = TEMPLATEIDS.copy()
    #print(templateIds.keys())
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.presentation'",
                             spaces='drive',
                             fields='nextPageToken, files(id,name,mimeType)',
                             pageToken=page_token).execute()
        for presentation in response.get('files', []):
            if presentation.get('name') in templateIds.keys():
                templateIds[presentation.get('name')] = presentation.get('id')
                print('%s: %s' % (presentation.get('name'),presentation.get('id')))
                
        page_token = response.get('nextPageToken',None)
        if page_token is None:
            break
    return templateIds
    
def main():
    """Shows basic usage of the Slides API.

    Creates a Slides API service object and prints the number of slides and
    elements in a sample presentation:
    https://docs.google.com/presentation/d/1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('slides', 'v1', http=http)
    drive_service = discovery.build('drive', 'v3', http=http)
    
    templateIds = get_templates(drive_service)
    
    #presentationId = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'
    presentationId = '1p1HprHcAxek4oSIamLlhioB1BAs7-qkjxuyEjm5Y6u8'
    #presentationId = '1unFqqmtBtljhg1_qJ0cr1o5ENZr_r1m6HK_yj1_x_0A'
    presentation = service.presentations().get(
        presentationId=presentationId).execute()
    slides = presentation.get('slides')

    print ('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        print(slide.get('objectId'))
        print(dir(slide))
        #print(slide.items())
        print('- Slide #{} contains {} elements.'.format(i + 1,
            len(slide.get('pageElements'))))
            
    for xmlfile in flags.XMLfiles:
        portfolio = get_portfolio(xmlfile)
        presentationName = os.path.splitext(os.path.basename(xmlfile.name))[0]
        # start presentation
        body = { 'title' : presentationName }
        presentation = service.presentations().create(body=body).execute()
        presentationId = presentation.get('presentationId')
        print('Created:"%s" "%s"' % (presentationName,presentationId))
        characterIndex = 0
        characterObjectId = []
        for character in portfolio.iter('character'):
            characterImages = character.findall('images')[0].getchildren()
            templateName = TEMPLATEKEYS[flags.template]
            templateName += (characterImages) and 'Image' or 'NoImage'
            templateName += ' Template'
            templateId = templateIds[templateName]
            #print(templateId)
            print(templateId,character.attrib['name'])            
            # locate the template slide
            templatePresentation = service.presentations().get(presentationId=templateId).execute()
            templateSlide = templatePresentation.get('slides')[0]
            # clear its objectId
            newSlide = templateSlide.copy()
            del(newSlide['objectId'])
            # slide creation request
            #### ERROR This does not work the copied object is not in the correct 
            #### format to create a new one
            requests = [ { 'createSlide' : newSlide }]
            body = { 'requests': requests }
            # execute request
            response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
            create_slide_response = response.get('replies')[0].get('createSlide')    
            characterObjectId[characterIndex] = create_slide_response.get('objectId')
            characterIndex += 1
        characterIndex = 0
        for character in portfolio.iter('character'):
            print(characterObjectId[characterIndex],character.attrib)
            # replace content
            characterIndex += 1
        xmlfile.close()
        
    #body = { 'title' : "TestTemplate" }
    #presentation = service.presentations().create(body=body).execute()
    #print('Created presentation with ID: {0}'.format(presentation.get('presentationId')))

if __name__ == '__main__':
    main()
