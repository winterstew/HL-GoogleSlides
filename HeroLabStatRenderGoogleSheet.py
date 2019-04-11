# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from __future__ import print_function
from pprint import pprint
from HeroLabStatBase import VERBOSITY
from HeroLabStatRender import Renderer
import re,os,pickle,copy
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pygsheets.utils import format_addr

DEFAULTMATCHER = 'GoogleSlide'
TEMPLATENAME = "StatList Template"
RANGENAME = "Sheet1!B:C"
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/spreadsheets.googleapis.com-python-HLRender.json
SCOPES = ('https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive')
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_DIR = os.path.join(os.path.expanduser('~'),'.credentials')
APPLICATION_NAME = 'HLRender'
RRR = ' rrr ' # flag used in values to flag that each item show get a new range



class GoogleSheetRenderer(Renderer):
    """
    GoogleSheet Renderer takes a Portfolio, a GoogleSheet Template and a Range
    creates a new GoogleSheet where the Range is duplicated for each character
    and calls the matcher to replace the text.  
    
    It is possible to list multiple ranges, but to prevent misaddressing as 
    columns or rows are inserted the ranges should be of different sheets 
    within the spreadsheet.  
    
    Ranges are specified in A1 notation with only contiguous ranges and on 
    only a single worksheet which can be named.  Thus valid ranges are:
      Sheet1!A1:B2
      Sheet1!A:A
      Sheet1!1:2
      Sheet1!A5:A
      A1:B2
    however, these are invalid:
      Sheet1!A1:Sheet1!B2
      Sheet1!A1:B2,Sheet1!D1:E2
      Sheet1!A1:B2,Sheet2!D1:E2
      A1:B2,D1:E2
      
    Note: These is a special render flag for lists, if you want a new range
     for every item in a matcher list (i.e. with the '..' flag) use the repeat
     flag ' rrr ' for render repeating row.  This will cause the matcher to 
     return a string where each item is seprated by ' rrr ' and 
     GoogleSheetRenderer will split the list and add a row (or column) for each
     item in the list

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
        #self.rangeNames = len(self.options) > 1 and self.options[1:] or ['Sheet1!A:B','Sheet1!B5:D6','Sheet2!A1:B2']
        self.credentials = self.get_credentials(flags=flags)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.templateId,self.templateName,self.templateFolder = self.find_template(self.drive_service,self.templateName)
        self.rangeSheetIds,self.rangeSheetNames,self.inSheetRangeNames,self.rangeRowMetadata,self.rangeColumnMetadata = \
            self.getRangeIds(self.service,self.templateId,self.rangeNames)
        #pprint(self.rangeRowMetadata)
        #pprint(self.rangeColumnMetadata)
        #pprint([self._getGridRange(ri) for ri,rng in enumerate(self.rangeNames)])
            
        
    def startPortfolio(self,*args,**kwargs):
        """ locate Google Drive Spreadsheet and Sheet within it and create matcher instances"""
        # copy the spreadsheet
        self.spreadsheetId = self.copy_template(self.drive_service,self.templateId,self.portfolio.filecore)
        if self.verbosity >= 2: print('Created:"%s" "%s"' % (self.portfolio.filecore,self.spreadsheetId))
        # get the ValueRange for all the ranges
        self.ranges = self.service.spreadsheets().values().batchGet(
                     spreadsheetId=self.templateId,
                     ranges=self.rangeNames,
                     majorDimension='ROWS',
                     valueRenderOption='FORMATTED_VALUE').execute().get('valueRanges')
            
    def dumpTemplate(self,*args,**kwargs):
        ss = self.service.spreadsheets().get(
                     spreadsheetId=self.templateId).execute()
        print(ss)
            
    def dumpTemplateValueRanges(self,*args,**kwargs):
        rngs = self.service.spreadsheets().values().batchGet(
                     spreadsheetId=self.templateId,
                     ranges=self.rangeNames,
                     majorDimension='ROWS',
                     valueRenderOption='FORMATTED_VALUE').execute().get('valueRanges')
        #print(rngs.viewkeys())
        for ri,rng in enumerate(rngs):
            print("Range Number %d from %s (id %d) cells %s" % (ri,self.rangeSheetNames[ri],self.rangeSheetIds[ri],self.inSheetRangeNames[ri]))
            pprint(rng.get('values'))
            print("Grid Range:")
            pprint(self._getGridRange(ri))

    def eachCharacter(self,character,*args,**kwargs):
        requests = []        
        valueData = []
        # create matcher instances
        textMatcher = self.matcherClass(character,self.matcherClass.TEXTMATCH,'text',verbosity=self.verbosity)
        booleanMatcher = self.matcherClass(character,self.matcherClass.BOOLEANMATCH,'boolean',verbosity=self.verbosity)
        # loop through ranges to replace
        for ri,rng in enumerate(self.ranges):
            # flag if repeated rows need to be rendered (i.e. the values have " rrr " in them())
            rrrFlag = True
            rrrMaxIndex = 0
            rrrIndex = 0
            while rrrFlag:
                rrrFlag = False
                # determine if we are inserting rows or columns
                rowNum = len(rng.get('values'))
                colNum = max([len(x) for x in rng.get('values')])
                gr = self._getGridRange(ri)
                newgr = self._getGridRange(ri)
                start,end = map(lambda x:self.format_addr(x,'tuple'),self.inSheetRangeNames[ri].split(':'))
                # insert columns if there are more rows than columns
                if rowNum > colNum:
                    requests.append({"insertRange":{"range":gr,"shiftDimension":'COLUMNS'}})
                    newgr['startColumnIndex'] += colNum
                    newgr['endColumnIndex'] += colNum
                    start = (start[0],start[1]+colNum)
                    end = (end[0],end[1]+colNum)
                # otherwise insert rows
                else:
                    requests.append({"insertRange":{"range":self._getGridRange(ri),"shiftDimension":'ROWS'}})  
                    newgr['startRowIndex'] += rowNum
                    newgr['endRowIndex'] += rowNum
                    start = (start[0]+rowNum,start[1])
                    end = (end[0]+rowNum,end[1])
                # copy the format over so the new values look the same
                requests.append({"copyPaste":{"source":newgr,"destination":gr,"pasteType":'PASTE_FORMAT'}})
                # NOTE The width update below coule be taken out ot the rowNum > colNum
                #  contitional is I want full control of the sizes, but I wanted
                #  to allow the cells to expand if text had to wrap or was too long.
                # if we are inserting columns lets copy the column widths
                if rowNum > colNum:
                    # update the column sizes to match
                    if 'startColumnIndex' in gr and 'endColumnIndex' in gr:
                        loopList = range(gr['startColumnIndex'],gr['endColumnIndex'])
                    else:
                        loopList = range(len(self.rangeColumnMetadata[ri]))
                    for colCnt,colInd in enumerate(loopList):
                        requests.append({"updateDimensionProperties":{
                                             "range":{"sheetId": self.rangeSheetIds[ri],
                                                      "dimension":'COLUMNS',
                                                      "startIndex":colInd,
                                                      "endIndex":colInd + 1},
                                             "properties":{"pixelSize":self.rangeColumnMetadata[ri][colCnt][u'pixelSize']},
                                             "fields":'pixelSize'}})
                # otherwise lest coppy the row widths
                else:
                    # update the row sizes to match
                    if 'startRowIndex' in gr and 'endRowIndex' in gr:
                        loopList = range(gr['startRowIndex'],gr['endRowIndex'])
                    else:
                        loopList = range(len(self.rangeRowMetadata[ri]))
                    for colCnt,colInd in enumerate(loopList):
                        requests.append({"updateDimensionProperties":{
                                             "range":{"sheetId": self.rangeSheetIds[ri],
                                                      "dimension":'ROWS',
                                                      "startIndex":colInd,
                                                      "endIndex":colInd + 1},
                                             "properties":{"pixelSize":self.rangeRowMetadata[ri][colCnt][u'pixelSize']},
                                             "fields":'pixelSize'}})
                # fill in the values
                myValues = copy.deepcopy(rng.get('values'))
                for oi,outer in enumerate(myValues):
                    for ci,cell in enumerate(outer):
                        myValues[oi][ci] = cell
                        for replaceKey in re.findall(r'(\{\{.*?\}\})',cell):
                            myValues[oi][ci] = myValues[oi][ci].replace(replaceKey,textMatcher.getMatch(replaceKey))
                            myValues[oi][ci] = myValues[oi][ci].replace(replaceKey,booleanMatcher.getMatch(replaceKey))
                            if RRR in myValues[oi][ci]:
                                rrrSplit = myValues[oi][ci].split(RRR)
                                rrrMaxIndex = max(rrrMaxIndex,len(rrrSplit)-1)
                                if rrrIndex < len(rrrSplit):
                                    myValues[oi][ci] = rrrSplit[rrrIndex]
                                else:
                                    myValues[oi][ci] = ''
                if rrrIndex < rrrMaxIndex:
                    rrrFlag = True
                    rrrIndex+=1
                valueData.append({"range":self.rangeNames[ri],
                                  "majorDimension": 'ROWS',
                                  "values": myValues })
                # create new rangeNames
                self.inSheetRangeNames[ri] = "%s:%s" % tuple(map(lambda x:self.format_addr(x,'label'),[start,end]))
                self.rangeNames[ri] = "%s!%s" % (self.rangeSheetNames[ri],self.inSheetRangeNames[ri])
        # actually carry out the batchUpdate request to insert rows or columns
        #pprint(requests)
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body={"requests":requests}).execute()
        # now carry out the value replacement
        response = self.service.spreadsheets().values().batchUpdate(
                              spreadsheetId=self.spreadsheetId,
                              body={
                                  "valueInputOption":'RAW',
                                  "data":valueData}).execute()       

    def endPortfolio(self,*args,**kwargs):
        requests = []
        # loop through ranges to delete
        for ri,rng in enumerate(self.ranges):
            # determine if we are deleting rows or columns
            rowNum = len(rng.get('values'))
            colNum = max([len(x) for x in rng.get('values')])
            gr = self._getGridRange(ri)
            # delete columns if there are more rows than columns
            if rowNum > colNum:
                requests.append({"deleteRange":{"range":gr,"shiftDimension":'COLUMNS'}})
            # otherwise delete rows
            else:
                requests.append({"deleteRange":{"range":self._getGridRange(ri),"shiftDimension":'ROWS'}})  
        # do the batch update
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body={"requests":requests}).execute()

    def _getGridRange(self,rangeIndex):
        gridRange = {}
        gridRange['sheetId'] = self.rangeSheetIds[rangeIndex]
        cells = self.inSheetRangeNames[rangeIndex].split(':')
        if len(cells) != 2: raise Exception,"bad A1 notation address %s in range %d" % (self.inSheetRangeNames[rangeIndex],rangeIndex)
        cellIndex = []
        # figure out the index number for the cell
        for c in cells:
            cellIndex.append(self.format_addr(c,'tuple'))
        if cellIndex[0][0]: gridRange['startRowIndex'] = cellIndex[0][0] - 1
        if cellIndex[1][0]: gridRange['endRowIndex'] = cellIndex[1][0] 
        if cellIndex[0][1]: gridRange['startColumnIndex'] = cellIndex[0][1] - 1
        if cellIndex[1][1]: gridRange['endColumnIndex'] = cellIndex[1][1] 
        return gridRange    
        
    @staticmethod
    def format_addr(addr,outType):
        """ pygsheets format_addr did not work for returning tuples for 
            A1 noted unbounded rows or columns, this wrapper fixes that """
        if outType == 'tuple':
            if type(addr) == type(()):
                return addr
            else:
                row,col = None,None
                if re.match(r'[A-Za-z]+[0-9]+$',addr):
                    row,col = format_addr(addr,'tuple')
                elif re.match(r'[A-Za-z]+$',addr):
                    col = format_addr('%s1' % addr,'tuple')[1]
                elif re.match(r'[0-9]+$',addr):
                    row = format_addr('A%s' % addr,'tuple')[0]
                else:
                    raise Exception,"bad A1 notation address %s" % addr
                return (row,col)
        elif outType == 'label':
            if type(addr) == type(''):
                return addr
            else:
                return format_addr(addr,'label')
        else:
            return format_addr(addr,outType)
        
    @staticmethod
    def getRangeIds(service,ssId,rngNames):
        """ return a tuple containing a list of Sheet ids, a list of Sheet 
            names, and a list of simplified rangeNames (whithout the sheet name) """
        rsid = []
        isrn = []
        rsname = []
        rcolmeta = []
        rrowmeta = []
        idDict = {}
        firstSheetName = ''
        # get the spreadsheet data, but only for the given ranges
        ss = service.spreadsheets().get(spreadsheetId=ssId,ranges=rngNames,includeGridData=True).execute()
        # loop through each sheet getting info
        for ws in ss.get('sheets'):
            #create a list of rowMetadata for each of the ranges
            map(lambda y:rrowmeta.append(y),map(lambda x:x.get('rowMetadata'),ws.get('data')))
            #create a list of columnMetadata for each of the ranges
            map(lambda y:rcolmeta.append(y),map(lambda x:x.get('columnMetadata'),ws.get('data')))
            # make a dictionary maping sheet titles to ids
            idDict[ws.get('properties').get('title')] = ws.get('properties').get('sheetId')            
            if ws.get('properties').get('sheetId') == 0: firstSheetName = ws.get('properties').get('title')
        # loop trough range names and extract the sheet name
        #  appending to and id list and a in-sheet range name list for each
        for rn in rngNames:
            rng = rn.split('!')
            # if no sheet name was included in the A1 notation
            # assume the sheet id is 0
            if len(rng) == 1:
                rsid.append(0)
                isrn.append(rng[0])
                rsname.append(firstSheetName)
            # if a sheet name was included in the A1 notation
            #  figure out its sheet id and extract its in sheet range name
            elif len(rng) == 2 and rng[0] in idDict:
                rsid.append(idDict[rng[0]])
                isrn.append(rng[1])
                rsname.append(rng[0])
            else:
                raise Exception,"%s is not a valid range" % rn  
        return (rsid,rsname,isrn,rrowmeta,rcolmeta)
            
            
    @staticmethod
    def get_credentials(*args,**kwargs):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        if not os.path.exists(CREDENTIAL_DIR):
            os.makedirs(CREDENTIAL_DIR)
        credential_path = os.path.join(CREDENTIAL_DIR,
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
    def find_template(service,tName,*args,**kwargs):
        """Returns spreadsheetId of the template"""
        tId = None
        page_token=None
        #print(templateIds.keys())
        while True:
            response = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'",
                                 spaces='drive',
                                 fields='nextPageToken, files(id,name,mimeType,parents)',
                                 pageToken=page_token).execute()
            for spreadsheet in response.get('files', []):
                if spreadsheet.get('name') == tName:
                    tId = spreadsheet.get('id')
                    tName = spreadsheet.get('name')
                    tFolder =  spreadsheet.get('parents')[0]                    
            page_token = response.get('nextPageToken',None)
            if page_token is None:
                break
        return (tId,tName,tFolder)
        
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
    #r.dumpTemplate()