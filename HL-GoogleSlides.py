from __future__ import print_function
import __builtin__
import httplib2
import os,re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import xml.etree.cElementTree as et

#
TEMPLATENAME = "StatBlock Template"
TEMPLATEPAGES = ["NPC-Combat-Image","NPC-Noncombat-Image",
                 "NPC-Combat-Noimage","NPC-Noncombat-Noimage"]
TEMPLATEKEYS = {'npc':'NPC-',
                'combat':'Combat-',
                'noncombat':'Noncombat-'
               }
REPLACEFLAGS = {
'trained skills...': "trained_skills(character)"
}

def trained_skills(character):
    text = ''
    for skill in character.iter('skill'): 
        if int(skill.attrib['ranks']) > 0 or int(skill.attrib['value']) > 4:
          skillName = re.sub(r'[aeiou ]',r'',skill.attrib['name'])
          skillName = re.search(r'\(.*\)',skillName) and skillName or skillName[0:4]
          skillName = skillName == "Hl" and "Heal" or skillName
          skillName = re.sub(r'Knwldg','Know',skillName)
          skillName = re.sub(r'Prfrm','Prfm',skillName)
          skillName = re.sub(r'Prfssn','Prof',skillName)
          skillName = re.sub(r'lchmy','alchmy',skillName)
          re.sub(r'Knwldg','Know',skillName)
          text += skillName
          text += int(skill.attrib['value'] >= 0) and " +" or " "
          text += '%d, ' % int(skill.attrib['value'])
    return(text[0:-2])      

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--page', choices=TEMPLATEKEYS.keys(), 
                        action='append', help="flages to identify pages to use")
    parser.add_argument('--template', default=TEMPLATENAME, help="template presentation name")
    parser.add_argument('XMLfiles', metavar='xml-file', type=argparse.FileType('r'), nargs='+', help='HeroLab Protfolio XML output file')
    flags = parser.parse_args()
except ImportError:
    flags = None
    
if not flags.page: flags.page = ['npc','noncombat']

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

def copy_template(service,newname):
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
            if presentation.get('name') == flags.template:
                newresponse = service.files().copy(fileId=presentation.get('id'),
                             body={ 'name': newname }).execute()                
                newId = newresponse.get('id')
                print('"%s" copied to "%s"' % (presentation.get('name'),newresponse.get('name')))
                
        page_token = response.get('nextPageToken',None)
        if page_token is None:
            break
    return newId
    
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
                    
    for xmlfile in flags.XMLfiles:
        portfolio = get_portfolio(xmlfile)
#        print(dir(portfolio))
#        break
        presentationName = os.path.splitext(os.path.basename(xmlfile.name))[0]
        # start presentation
        presentationId = copy_template(drive_service,presentationName)
        presentation = service.presentations().get(presentationId=presentationId).execute()
        print('Created:"%s" "%s"' % (presentationName,presentationId))
        slides = presentation.get('slides')
        slideIds = map(lambda x:x.get('objectId'),slides)
        slideNames = []
        #for s in slides:
        #    slideNames.append(s['pageElements'][0]['shape']['text'])
        for slideId in slideIds:
            for findText in TEMPLATEPAGES:
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
                response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
                topReply = response.get('replies')[0]['replaceAllText']
                if "occurrencesChanged" in topReply.keys() and topReply["occurrencesChanged"] > 0:
                    slideNames.append(findText)
        print(slideIds)
        print(slideNames)

        characterIndex = 0
        characterObjectId = []
        for character in portfolio.iter('character'):
            slideName = reduce(lambda x,y: '%s%s' % (TEMPLATEKEYS[x],TEMPLATEKEYS[y]),flags.page)
            characterImages = character.findall('images')[0].getchildren()
            slideName += (characterImages) and 'Image' or 'Noimage'
            slideId = slideIds[slideNames.index(slideName)]
            body = { "requests":  [ {
              "duplicateObject": {
                "objectId":  slideId
              }
            } ] }
            response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
            #print(response.get('replies'))            
            newSlideId = response.get('replies')[0]['duplicateObject']['objectId']
            body = { "requests":  [ {
              "updateSlidesPosition": {
                "slideObjectIds": [ newSlideId ],
                "insertionIndex": characterIndex
              }
            },{
              "replaceAllText": {
                "replaceText":  character.attrib['name'],
                "pageObjectIds": [newSlideId],
                "containsText": {
                  "text": '{{%s}}' % slideName,
                  "matchCase": True
                }
              }
            } ] }
            for replaceKey in REPLACEFLAGS.keys():
                body['requests'].append({
                  "replaceAllText": {
                    "replaceText":  eval(REPLACEFLAGS[replaceKey]),
                    "pageObjectIds": [newSlideId],
                    "containsText": {
                      "text": '{{%s}}' % replaceKey,
                      "matchCase": True
                    }
                  }
                })
            response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
            #print(response.get('replies'))       
            #print(slideName,slideId,newSlideId)
            characterIndex += 1
        # delete original template pages
        body = { "requests": [] }
        for slideId in slideIds:
            body["requests"].append({ "deleteObject": { "objectId":slideId }})
        response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
        xmlfile.close()
        
    #body = { 'title' : "TestTemplate" }
    #presentation = service.presentations().create(body=body).execute()
    #print('Created presentation with ID: {0}'.format(presentation.get('presentationId')))

if __name__ == '__main__':
    main()
