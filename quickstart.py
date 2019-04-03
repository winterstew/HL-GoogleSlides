# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 07:51:54 2018

@author: steve
"""

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.file import Storage
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/presentations.readonly'

# The ID of a sample presentation.
PRESENTATION_ID = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'

DEFAULTMATCHER = 'GoogleSlide'
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


def main():
        
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
        credentials = tools.run_flow(flow, store)        
        
        
#    service = build('slides', 'v1', http=creds.authorize(Http()))
#
#    # Call the Slides API
#    presentation = service.presentations().get(
#        presentationId=PRESENTATION_ID).execute()
#    slides = presentation.get('slides')
#
#    print('The presentation contains {} slides:'.format(len(slides)))
#    for i, slide in enumerate(slides):
#        print('- Slide #{} contains {} elements.'.format(
#            i + 1, len(slide.get('pageElements'))))


if __name__ == '__main__':
    main()