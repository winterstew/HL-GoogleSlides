from __future__ import print_function
import __builtin__
import httplib2
import os,re,urllib

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
#'race': "re.sub(r' ','',character.find('race').get('racetext'))",
'race': "character.find('race').get('racetext')",
'size': "character.find('size').get('name')[0]",
'space': "character.find('size').find('space').get('text')",
'reach': "character.find('size').find('reach').get('text')",
'deity': "character.find('deity').get('name')",
'CR': "character.find('challengerating').get('text')",
'XP': "'XP' + character.find('xpaward').get('value')",
'classes summary': "character.find('classes').get('summaryabbr')",
'types': "get_attrlist(character,'types','type','name')",
'subtypes': "get_attrlist(character,'subtypes','subtype','name')",
'hero': "(character.find('heropoints').get('enabled') == 'yes') and character.find('heropoints').get('total') or '-'",
'senses': "get_attrlist(character,'senses','special','shortname',fmt=JOINVOWELLESS)",
'auras': "get_attrlist(character,'auras','special','name')",
'auras head': "get_attrlisthead(character,'auras','special','\\nAuras: ')",
'favoredclasses': "get_attrlist(character,'favoredclasses','favoredclass','name',fmt=JOINVOWELLESS)",
'HP': "character.find('health').get('hitpoints')",
'HD': "character.find('health').get('hitdice')",
'xp': "character.find('xp').get('total')",
'money': "character.find('money').get('total')+'gp'",
'gender': "character.find('personal').get('gender').lower()",
'age': "character.find('personal').get('age')",
'hair': "character.find('personal').get('hair')",
'eyes': "character.find('personal').get('eyes')",
'skin': "character.find('personal').get('skin')",
'height': "re.sub(r' ','',character.find('personal').find('charheight').get('text'))",
'weight': "character.find('personal').find('charweight').get('text')",
'personal': "character.find('personal').find('description').text",
'personal description':"""re.sub(r'w/  skin  hair and  eyes.  ','',
  re.sub(r'^0[^1-9][^1-9]* yr old ','',
    get_nested(character,'{{height}} {{(weight)}} {{age}} yr old w/ {{skin}} skin {{hair}} hair and {{eyes}} eyes.  {{personal}}')
  ))""",
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
'Saves': "get_save_sit(character,'All Save')",
'defence special..': "get_attrlist(character,'defensive','special','shortname')",
'dr special..': "re.sub(r'^(...)','DR \1',get_attrlist(character,'damagereduction','special','shortname'))",
'immune special..': "get_attrlist(character,'immunities','special','shortname')",
'resist special..': "get_attrlist(character,'resistances','special','shortname')",
'weak special..': "get_attrlist(character,'weaknesses','special','shortname')",
'AC': "character.find('armorclass').get('ac')",
'tAC': "character.find('armorclass').get('touch')",
'ffAC': "character.find('armorclass').get('flatfooted')",
'ACs': "character.find('armorclass').find('situationalmodifiers').get('text')",
'ACP': "get_attrlist(character,'penalties','penalty','text',test=('name','%s == \"Armor Check Penalty\"'))",
'MaxDex': "get_attrlist(character,'penalties','penalty','text',test=('name','%s == \"Max Dex Bonus\"'))",
'CMB': "character.find('maneuvers').get('cmb')",
'CMBothers': "get_varied_maneuvers(character,'cmb')",
'CMD': "character.find('maneuvers').get('cmd')",
'CMDothers': "get_varied_maneuvers(character,'cmd')",
'ffCMD': "character.find('maneuvers').get('cmdflatfooted')",
'init': "character.find('initiative').get('total')",
'init situational': "character.find('initiative').find('situationalmodifiers').get('text')",
'basespeed': "character.find('movement').find('basespeed').get('value')",
'speed': "character.find('movement').find('speed').get('value')",
'encum': "character.find('encumbrance').get('light') + '/' + character.find('encumbrance').get('medium') + '/' + character.find('encumbrance').get('heavy') + ' (' + character.find('encumbrance').get('carried') + ')' + character.find('encumbrance').get('level')[0:1]",
'percep': "re.sub(r'\+-','-','+' + get_attr(character.find('skills').findall('skill'),('name','Perception'),(None,'value')))",
'percep situational': "get_attr(character.find('skills').findall('skill'),('name','Perception'),('situationalmodifiers','text'))",
'all skills..': "get_skills(character,minRank=0,minMod=-9999)",
'trained skills..': "get_skills(character,minRank=1,minMod=4)",
'feats..': "get_attrlist(character,'feats','feat','name',test=('profgroup','%s != \"yes\"'))",
'traits..': "get_attrlist(character,'traits','trait','name')",
'flaws..': "get_attrlist(character,'flaws','flaw','name')",
'skilltricks..': "get_attrlist(character,'skilltricks','skilltrick','name')",
'animaltricks..': "get_attrlist(character,'animaltricks','animaltrick','name')[0:-8]",
'BAB': "character.find('attack').get('baseattack')",
'meleeB': "character.find('attack').get('meleeattack')",
'rangeB': "character.find('attack').get('rangedattack')",
'attack special..': "get_attrlist(character,'attack','special','shortname')",
'melee weapons..': "get_weaponlist(character,'melee',onlyEquipped=False)",
'range weapons..': "get_weaponlist(character,'ranged',onlyEquipped=False)",
'melee equipped weapons..': "get_weaponlist(character,'melee',onlyEquipped=True)",
'range equipped weapons..': "get_weaponlist(character,'ranged',onlyEquipped=True)",
'defenses armor..': "get_attrlist(character,'defenses','armor','name',quant=True)",
'magic items..': "get_attrlist(character,'magicitems','item','name',quant=True)",
'gear items..': "get_attrlist(character,'gear','item','name',quant=True)",
'spelllike special..': "get_attrlist(character,'spelllike','special','name',quant=True)",
'tracked items..': "get_attrlist(character,'trackedresources','trackedresource','name',quant=True)",
'other special..': "get_attrlist(character,'otherspecials','special','name')",
'spells known..': "get_sortedspells(character,'spellsknown')",
'spells memorized..': "get_sortedspells(character,'spellsmemorized')",
'spells book..': "get_sortedspells(character,'spellbook')",
'spellclasses..': "get_spellclasses(character.find('spellclasses'))",
'npc description': "get_textformatch(character.find('npc'),('description',''),('',''))", 
'npc basics': "get_textformatch(character.find('npc'),('description',''),('',''))",
'npc basics-goals': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Motivations & Goals'))",
'npc basics-plots': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Schemes, Plots & Adventure Hooks'))",
'npc basics-hooks': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Schemes, Plots & Adventure Hooks'))",
'npc basics-boons': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Boon'))",
'npc tactics-before': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - Before Combat'))",
'npc tactics-during': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - During Combat'))",
'npc tactics-morale': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - Morale'))",
'npc ecology-stats': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Base Statistics'))",
'npc ecology-environment': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Environment'))",
'npc ecology-organization': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Organization'))",
'npc ecology-trerasure': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Treasure'))",
'npc history-goals': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','History / Goals'))",
'npc history-goals-boons': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','History / Goals'))",
'npc personality-mannerisms': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','Personality / Mannerisms'))",
'npc pc-interactions': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','PC Interactions'))",
'npc pc-interaction': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','PC Interactions'))",
'npc interaction': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','PC Interactions'))"
}

for k in REPLACEFLAGS.keys():
    REPLACEFLAGS['('+k+')'] = "(%s) and '(%%s)' %% (%s) or ''" % (REPLACEFLAGS[k],REPLACEFLAGS[k])

def get_attr(eList,test,ra):
    for e in eList:
        if (e.attrib[test[0]] == test[1]):
            if ( ra[0] == None ): 
                #print(ra[1],e.get(ra[1]))
                return e.get(ra[1])
            else:
                #print(ra[1],e.find(ra[0]),e.find(ra[0]).get(ra[1]))
                return e.find(ra[0]).get(ra[1])

def get_nested(character,myString):
    for rk in REPLACEFLAGS.keys():
        rkSearch = re.sub('\)','\\)',re.sub('\(','\\(',rk))
        if re.search("{{%s}}" % rkSearch,myString):
            rs = eval(REPLACEFLAGS[rk]) or ''
            #print(rk)
            #print(rs)
            #print(myString)
            myString = re.sub("{{%s}}" % rk, rs, myString)
    return myString
        
def get_attrlist(character,outer,inner,attr,fmt=JOIN,test=('',''),quant=False):
    l = ''
    for a in character.find(outer).findall(inner):
        if test[0] and test[0] in a.keys():
            testExpression = test[1] % "a.attrib[test[0]]"
        else:
            testExpression = "a.attrib[attr]" 
        if eval(testExpression): 
            # if the short name is generic use the long name
            if attr == 'shortname' and a.attrib[attr] == 'Generic Ability':
                attr = 'name'
            item = a.attrib[attr]
            # if quant is True add a quantity if it exists and is > 1
            if quant:
                if inner == "trackedresource":
                    #qattr = "[%s used]" % a.attrib["text"]
                    qattr = "[%d]" % int(a.attrib["left"])
                elif "quantity" in a.keys():
                    qattr = (int(a.attrib["quantity"]) > 1) and "[%d]" % int(a.attrib["quantity"]) or ""
                else:
                    qattr = ""
                item = "%s%s" % (item,qattr)
            l = fmt(l,item)                    
    return l[0:-1]

def get_attrlisthead(character,outer,inner,label):
    """ Print the label if there are elements in the inner """
    l = ''
    if character.find(outer).findall(inner):
        l = label     
    return l

def get_textformatch(npc,brchs,test):
    if npc:
        b1 = npc.find(brchs[0])
        if b1 and brchs[1]:
            for ni in b1.iter(brchs[1]):
                if ni.get(test[0]) == test[1]: return ni.text
        else: return b1.text
    return ''
            
def get_spellclasses(spellClasses):
    rtn = ''
    for sc in spellClasses.iter('spellclass'):
        hasLevels = False
        rt = '%s:' % (sc.get('name'))
        for s in sc.iter('spelllevel'):
            hasLevels = True
            rt = '%s%s/%s,' % (rt,s.get('level'),s.get('maxcasts'))
        if hasLevels:
            rtn = '%s%s;' % (rtn,rt[0:-1])
    return rtn
    
def get_sortedspells(character,spName):
    spells = []
    for sp in character.find(spName).iter('spell'): 
        spells.append((sp.get('name'),sp.get('level')))
    (lv,l) = (-1,'')
    for spTup in sorted(spells,key=lambda x: x[1]):
        if lv != int(spTup[1]): 
            l = '%s (%d):' % (l,int(spTup[1]))
            lv = int(spTup[1])
        l = '%s%s,' % (l,spTup[0])
    if l: return spName + l[0:-1]
        
def get_weaponlist(character,wpType,onlyEquipped=True):
    l = ''
    for wp in character.find(wpType).iter('weapon'):
        if wp.get('equipped') != None:
            l = "%s(%s) %s %s (%s  %s), \n%s" % (re.sub(r' \(..*\)$','',wp.get('name')),wp.get('typetext'),wp.get('attack'),wp.get('equipped'),wp.get('damage'),wp.get('crit'),l)
        elif not onlyEquipped:
            l = "%s%s(%s) %s (%s  %s), \n" % (l,re.sub(r' \(..*\)$','',wp.get('name')),wp.get('typetext'),wp.get('attack'),wp.get('damage'),wp.get('crit'))
    if len(l) > 3:
        l = re.sub('Masterwork','mwk',l)
        return l[0:-3]
    else:
        return l
    
def get_varied_maneuvers(character,mType):
    mVal = character.find('maneuvers').get(mType)
    l = ''
    for m in character.find('maneuvers').iter('maneuvertype'):
        #print(m)
        if m.get(mType) != mVal: l = '%s %s:%s,' % (l,m.get('name'),m.get(mType))
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
    svElement = (svName == "All Save") and 'allsaves' or 'save'
    for sv in character.find('saves').iter(svElement):
        if svElement == 'allsaves' or sv.get('name') == svName:
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
        
def get_skills(character,minRank=0,minMod=-9999):
    l = ''
    for skill in character.find('skills').iter('skill'): 
        if int(skill.attrib['ranks']) >= minRank or int(skill.attrib['value']) > minMod:
          skillName = re.sub(r'[aeiou ]',r'',skill.attrib['name'])
          skillName = re.search(r'\(.*\)',skillName) and skillName or skillName[0:4]
          skillName = skillName == "Hl" and "Heal" or skillName
          skillName = skillName == "Rd" and "Ride" or skillName
          skillName = skillName == "Dsgs" and "Disg" or skillName
          skillName = skillName == "Lngs" and "Ling" or skillName
          skillName = skillName == "Spll" and "Spel" or skillName
          skillName = skillName == "Stlt" and "Slth" or skillName
          skillName = re.sub(r'Knwldg','Know',skillName)
          skillName = re.sub(r'Prfrm','Prfm',skillName)
          skillName = re.sub(r'Prfssn','Prof',skillName)
          skillName = re.sub(r'Crft\(lchmy\)','Crft(alchm)',skillName)
          skillName = re.sub(r'Know\(ngnrng\)','Prof(eng)',skillName)
          skillName = re.sub(r'Prof\(nnkpr\)','Prof(innkp)',skillName)
          skillName = re.sub(r'Prof\(ck\)','Prof(cook)',skillName)
          skillName = re.sub(r'nstrmnts','',skillName)
          l += skillName
          l += int(skill.attrib['value']) >= 0 and " +" or " "
          l += '%d, ' % int(skill.attrib['value'])
    return(l[0:-2])      

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
print(flags.page)

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
            # upload image
            imageElem = character.find('images').find('image')
            file_id=''
            #print(imageElem)
            if ( imageElem != None ) :
                imageFile = imageElem.get('filename')
                #print(imageFile)
                upload = drive_service.files().create(
                    body={'name': imageFile, 'mimeType': 'image/jpeg'},
                    media_body=os.path.join(os.path.abspath(os.path.curdir),imageFile)).execute()
                file_id = upload.get('id')

                # Obtain a URL for the image.
                image_url = '%s&access_token=%s' % (drive_service.files().get_media(fileId=file_id).uri, credentials.access_token)

                body['requests'].append({
                  'replaceAllShapesWithImage': {
                    'imageUrl': image_url,
                    'replaceMethod': 'CENTER_INSIDE',
                    "pageObjectIds": [newSlideId],
                    'containsText': {
                      'text': '{{image}}',
                      'matchCase': True
                    }
                  }
                })
            response = service.presentations().batchUpdate(presentationId=presentationId,body=body).execute()
            characterIndex += 1
            # Remove the temporary image file from Drive.
            if file_id != '': drive_service.files().delete(fileId=file_id).execute()            
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
