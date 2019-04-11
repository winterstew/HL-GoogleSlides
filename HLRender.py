# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 07:13:15 2019

@author: steve
"""

from __future__ import print_function
import sys,re,os,json
import PySimpleGUI27 as sg      
import subprocess,threading,Queue 

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(re.sub(r'\n','',line))
    out.close()

def ExecuteCommandSubprocess(w,command, *args):
    try:
        cmd = [command] + list(args)
        portDir = len(args) > 1 and os.path.dirname(args[-1]) or os.path.abspath('.')
        sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, cwd=portDir, close_fds=ON_POSIX)
        q = Queue.Queue()
        t = threading.Thread(target=enqueue_output, args=(sp.stdout, q))
        t.daemon = True # thread dies with the program
        t.start()
        # read line without blocking
        while t.isAlive():
            try:  
                line = q.get_nowait()
            except Queue.Empty:
                pass
                #print('empty')
            else: 
                print(line.decode("utf-8"))
            w.Refresh()
    except:
        pass
    
def getRenderers():
    Renderers = []
    for f in os.listdir('.'):
        renderMatch = re.search(r'HeroLabStatRender(.*)\.py$',f)
        if renderMatch: 
            Renderers.append(renderMatch.group(1))
    return Renderers

def getMatchers():
    Matchers = []
    for f in os.listdir('.'):
        matchMatch = re.search(r'HeroLabStatMatch(.*)\.py$',f)
        if matchMatch: 
            Matchers.append(matchMatch.group(1))
    return Matchers

def getIconFile():
    if os.path.isfile('iconsPaizo.zip'): return os.path.abspath('iconsPaizo.zip')
    if os.path.isfile('icons.zip'): return os.path.abspath('icons.zip')
    return ''
    
def loadDefaults(dp):
    defaults = {}
    if os.path.isfile(dp):
        f = open(dp,'r')
        defaults = json.load(f)
        f.close()
    return defaults

def saveDefaults(dp,v):
    f = open(dp,'w')
    json.dump(v,f)
    f.close()
    return

home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
defaults_path = os.path.join(credential_dir,'HLRender_defaults.json')
defaults = loadDefaults(defaults_path)

toprow = [sg.Text('Output Window', key='head', size=(40, 1))]
if 'GoogleSlide' in getRenderers():
    toprow.append(sg.Button('get Google credentials',key='credentials'))
    sg.Button()
layout = [      
    toprow,
    [sg.Output(size=(88, 20))],
    [sg.Text('Icon file'),sg.InputText(default_text='iconFile' in defaults and defaults['iconFile'] or getIconFile(),
                                       key='iconFile'), sg.FileBrowse()],
    [sg.Text('Renderer'),sg.InputCombo(getRenderers(),
                                       default_value='renderer' in defaults and defaults['renderer'] or '',
                                       key='renderer'),
     sg.Text('renderer options'),sg.InputText(default_text='renderer_options' in defaults and defaults['renderer_options'] or '',
                                              key='renderer_options')],
    [sg.Text('Matcher'),sg.InputCombo(getMatchers(),
                                      default_value='matcher' in defaults and defaults['matcher'] or '',
                                      key='matcher'),
     sg.Text('matcher options'),sg.InputText(default_text='matcher_options' in defaults and defaults['matcher_options'] or '',
                                             key='matcher_options')],
    [sg.Text('Portfolio file'),sg.InputText(default_text='portFile' in defaults and defaults['portFile'] or '',
                                            key='portFile'), sg.FileBrowse()], 
    [sg.Button('Render',key='render'),sg.Button('Exit',key='exit')]
        ]
        
window = sg.Window('Script launcher').Layout(layout)      
# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:
    (event, value) = window.Read()
    if event == 'exit' or event is None:      
        break # exit button clicked      
    if event == 'render':
        window.Element('render').Update('Working',disabled=True)
        window.Element('exit').Update('Exit',disabled=True)
        window.Element('head').Update('Render output...')
        window.Refresh()
        cmd = ['python',os.path.abspath('HeroLabStatExport.py')]
        if value['iconFile']: cmd += ['-i',value['iconFile']]
        if value['renderer']: cmd += ['-R',value['renderer']]
        if value['renderer_options']: cmd += ['-r',value['renderer_options']]
        if value['matcher']: cmd += ['-M',value['matcher']]
        if value['matcher_options']: cmd += ['-m',value['matcher_options']]
        if value['portFile']: 
            cmd += [value['portFile']]
            ExecuteCommandSubprocess(window,*cmd)
        else:
            print('Need a Portfolio File')
        window.Element('head').Update('Output Window')     
        window.Element('exit').Update('Exit',disabled=False)
        window.Element('render').Update('Render',disabled=False)        
        value['authorized'] = 'authorized' in defaults and defaults['authorized'] or False
        saveDefaults(defaults_path,value)
    elif event == 'credentials':
        window.Element('render').Update('Working',disabled=True)
        window.Element('exit').Update('Exit',disabled=True)
        window.Element('credentials').Update('authorizing...',disabled=True)
        cmd = ['python',os.path.abspath('HeroLabStatRenderGoogleSlide.py')]
        print('running:')
        print(" ".join(cmd))
        ExecuteCommandSubprocess(window,*cmd)
        cmd = ['python',os.path.abspath('HeroLabStatRenderGoogleSheet.py')]
        print('running:')
        print(" ".join(cmd))
        ExecuteCommandSubprocess(window,*cmd)
        window.Element('exit').Update('Exit',disabled=False)
        window.Element('render').Update('Render',disabled=False)
        window.Element('credentials').Update('authorized',disabled=True)
        value['authorized'] = True
        saveDefaults(defaults_path,value)

    
