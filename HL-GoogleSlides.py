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
JOIN = lambda x,y:'%s%s,' % (x,y)
JOINVOWELLESS = lambda x,y:'%s%s,' % (x,re.sub(r'[aeiou ]','',y))
REPLACEFLAGS = {
'align': "re.sub(r'[a-zT ]','',character.find('alignment').get('name'))",
'race': "re.sub(r' ','',character.find('race').get('racetext'))",
'size': "character.find('size').get('name')[0]",
'space': "character.find('size').find('space').get('text')",
'reach': "character.find('size').find('reach').get('text')",
'deity': "character.find('deity').get('name')",
'CR': "character.find('challengerating').get('text')",
'XP': "'XP' + character.find('xpaward').get('value')",
'classes summary': "character.find('classes').get('summaryabbr')",
'types': "get_attrlist(character,'types','type','name',test=('active','==\\\'yes\\\''))",
'subtypes': "get_attrlist(character,'subtypes','subtype','name')",
'hero': "(character.find('heropoints').get('enabled') == 'yes') and character.find('heropoints').get('total') or '-'",
'senses': "get_attrlist(character,'senses','special','shortname',fmt=JOINVOWELLESS)",
'auras': "get_attrlist(character,'auras','aura','name')",
'favoredclasses': "get_attrlist(character,'favoredclasses','favoredclass','name',fmt=JOINVOWELLESS)",
'HP': "character.find('health').get('hitpoints')",
'HD': "character.find('health').get('hitdice')",
'xp': "character.find('xp').get('total')",
'money': "character.find('money').get('total')",
'gender': "character.find('personal').get('gender').lower()",
'age': "character.find('personal').get('age')",
'hair': "character.find('personal').get('hair')",
'eyes': "character.find('personal').get('eyes')",
'skin': "character.find('personal').get('skin')",
'height': "re.sub(r' ','',character.find('personal').find('charheight').get('text'))",
'weight': "character.find('personal').find('charweight').get('text')",
'personal description':"get_nested(character,'{{height}} {{(weight)}} {{age}} yr old w/ {{skin}} skin {{hair}} hair and {{eyes}} eyes.  ')",
'languages': "get_attrlist(character,'languages','language','name')",
'strength': "get_ability(character,'Strength')",
'dexterity': "get_ability(character,'Dexterity')",
'constitution': "get_ability(character,'Constitution')",
'intelligence': "get_ability(character,'Intelligence')",
'wisdom': "get_ability(character,'Wisdom')",
'charisma': "get_ability(character,'Charisma')",
'str': "get_ability_value(character,'Strength')",
'dex': "get_ability_value(character,'Dexterity')",
'con': "get_ability_value(character,'Constitution')",
'int': "get_ability_value(character,'Intelligence')",
'wis': "get_ability_value(character,'Wisdom')",
'cha': "get_ability_value(character,'Charisma')",
'STR': "get_ability_mod(character,'Strength')",
'DEX': "get_ability_mod(character,'Dexterity')",
'CON': "get_ability_mod(character,'Constitution')",
'INT': "get_ability_mod(character,'Intelligence')",
'WIS': "get_ability_mod(character,'Wisdom')",
'CHA': "get_ability_mod(character,'Charisma')",
'STRs': "get_ability_sit(character,'Strength')",
'DEXs': "get_ability_sit(character,'Dexterity')",
'CONs': "get_ability_sit(character,'Constitution')",
'INTs': "get_ability_sit(character,'Intelligence')",
'WISs': "get_ability_sit(character,'Wisdom')",
'CHAs': "get_ability_sit(character,'Charisma')",
'Fortitude Save': "get_save(character,'Fortitude Save')",
'Fort': "get_save_mod(character,'Fortitude Save')",
'Forts': "get_save_sit(character,'Fortitude Save')",
'Reflex Save': "get_save(character,'Reflex Save')",
'Ref': "get_save_mod(character,'Reflex Save')",
'Refs': "get_save_sit(character,'Reflex Save')",
'Will Save': "get_save(character,'Will Save')",
'Will': "get_save_mod(character,'Will Save')",
'Wills': "get_save_sit(character,'Will Save')",
    
'trained skills...': "get_trained_skills(character)"
}

for k in REPLACEFLAGS.keys():
    REPLACEFLAGS['('+k+')'] = "(%s) and '(%%s)' %% (%s) or ''" % (REPLACEFLAGS[k],REPLACEFLAGS[k])

def get_nested(character,myString):
    for rk in REPLACEFLAGS.keys():
        rkSearch = re.sub('\)','\\)',re.sub('\(','\\(',rk))
        if re.search("{{%s}}" % rkSearch,myString):
            rs = eval(REPLACEFLAGS[rk])
            #print(rk,rs,myString)
            myString = re.sub("{{%s}}" % rk, rs, myString)
    return myString
        
def get_attrlist(character,outer,inner,attr,fmt=JOIN,test=(None,'')):
    l = ''
    testExpression = test[0] and "a.attrib[test[0]] %s" % test[1] or "a.attrib[attr]" 
    for a in character.find(outer).findall(inner):
        if eval(testExpression): l = fmt(l,a.attrib[attr])
    return l[0:-1]

def get_save(character,svName):
    for sv in character.find('saves').iter('save'):
        if sv.get('name') == svName:
            rtn = sv.get('save')
            rtn = '%s = %sb %sa %sr %sm' % (rtn,(sv.get('base') or '+0'),(sv.get('fromattr') or '+0'),(sv.get('fromresist') or '+0'),(sv.get('frommisc') or '+0'))
            rtn = '%s <%s>' % (rtn,sv.find('situationalmodifiers').get('text'))
            return re.sub(' <>','',rtn)
            
def get_save_mod(character,svName):
    for sv in character.find('saves').iter('save'):
        if sv.get('name') == svName:
            return sv.get('save')

def get_save_sit(character,svName):
    for sv in character.find('saves').iter('save'):
        if sv.get('name') == svName:
            return sv.find('situationalmodifiers').get('text')            
        
def get_ability(character,abName):
    for ab in character.find('attributes').iter('attribute'):
        if ab.get('name') == abName:
            rtn = ab.find('attrvalue').get('text')
            rtn = '%s(%s) <%s>' % (rtn,ab.find('attrbonus').get('text'),ab.find('situationalmodifiers').get('text'))
            return re.sub(' <>','',rtn)
    
def get_ability_value(character,abName):
    for ab in character.find('attributes').iter('attribute'):
        if ab.get('name') == abName:
            return ab.find('attrvalue').get('text')
            
def get_ability_mod(character,abName):
    for ab in character.find('attributes').iter('attribute'):
        if ab.get('name') == abName:
            return ab.find('attrbonus').get('text')

def get_ability_sit(character,abName):
    for ab in character.find('attributes').iter('attribute'):
        if ab.get('name') == abName:
            return ab.find('situationalmodifiers').get('text')
        
def get_trained_skills(character):
    text = ''
    for skill in character.iter('skill'): 
        if int(skill.attrib['ranks']) > 0 or int(skill.attrib['value']) > 4:
          skillName = re.sub(r'[aeiou ]',r'',skill.attrib['name'])
          skillName = re.search(r'\(.*\)',skillName) and skillName or skillName[0:4]
          skillName = skillName == "Hl" and "Heal" or skillName
          skillName = skillName == "Rd" and "Ride" or skillName
          skillName = re.sub(r'Knwldg','Know',skillName)
          skillName = re.sub(r'Prfrm','Prfm',skillName)
          skillName = re.sub(r'Prfssn','Prof',skillName)
          skillName = re.sub(r'Crft(lchmy)','Crft(alchm)',skillName)
          skillName = re.sub(r'Know(ngnrng)','Prof(eng)',skillName)
          skillName = re.sub(r'Prof(nnkpr)','Prof(innkp)',skillName)
          skillName = re.sub(r'Prof(ck)','Prof(cook)',skillName)
          skillName = re.sub(r'nstrmnts','',skillName)
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
