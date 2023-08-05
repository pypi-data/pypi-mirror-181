#!/usr/bin/env python3

#Imports
import argparse
import os, sys
import requests
import json
import flask
from flask import redirect, request, send_file
from configparser import ConfigParser
import re, shutil

#Argument Parsing

parser = argparse.ArgumentParser(prog = 'shpm', description='Scratch extension package manager', epilog='This version of shpm has Super Sus Powers.')
parser.add_argument("cmd", help="The command you use", nargs='?', default = '')
parser.add_argument("extra", help="Extra parameter", nargs="?",default='')
parser.add_argument("selection", help="Another extra parameter", nargs="?",default='')
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=True)
group.add_argument("-q", "--quiet", help="Do run quietly", action="store_true")
parser.add_argument("-d", "--dry", help="Do a dry run", action="store_true")
parser.add_argument("-A", "--amogus", help="Hmmmmmmm", action="store_true")
parser.add_argument("-l", "--local", help="Install package from local file", action="store_true")
parser.add_argument("-r", "--remote", help="Install package from remote file")


args = parser.parse_args()

#Metadata

version = '1.0.0'

#Flagset

verbose = args.verbose and not args.quiet
dry = args.dry

#INI

def write_config():
    with open("config.ini", "w") as f:
        f.write("""
[settings_start]
turbowarp_instance = https://turbowarp.org
sheeptester_instance = https://sheeptester.github.io/scratch-gui/
mode = turbowarp

[settings_workdir]
workdir = .scratch-modules
workfile = Project.sb3

[settings_install]
repository = https://familycomicsstudios.github.io/ShredRepository/packages.json
        """)

config = ConfigParser()
try:
    config.read('config.ini')
    config.get('settings_start', 'turbowarp_instance')
except:
    write_config()
    config.read('config.ini')

#PWD stuff

from os import listdir
from os.path import isfile, join
mypath = os.getcwd()+"/"+config.get('settings_workdir', 'workdir')
try:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
except:
    pass
workdir = os.getcwd()

#Flask

app = flask.Flask(__name__,
            static_url_path='', 
            static_folder=workdir+config.get('settings_workdir', 'workdir'))

@app.route('/')
def main():
    global onlyfiles, config
    if config.get('settings_start', 'mode') == "turbowarp":
        try:
            url = config.get('settings_start', 'turbowarp_instance')
            if len(onlyfiles) > 0:
                url += '?extension=https://'+request.host+'/modules/'+onlyfiles[0]
                fileno = 1
                for file in onlyfiles[1:]:
                    url += '&extension=https://'+request.host+'/modules/'+onlyfiles[fileno]
                    fileno += 1
                return redirect(url)
        except:
            pass
    elif config.get('settings_start','mode') == "sheeptester":
        url = config.get('settings_start','sheeptester_instance')
        if len(onlyfiles) > 0:
            url += '?load_plugin=https://'+request.host+'/modules/'+onlyfiles[0]
            fileno = 1
            for file in onlyfiles[1:]:
                url += '&load_plugin=https://'+request.host+'/modules/'+onlyfiles[fileno]
                fileno += 1
        return redirect(url)
    else:
        print("ERROR || Invalid mode")
            
    

@app.route('/build')
def build():
    build_json = """{"interpolation":false,"maxClones":300,"loadingScreen":{"text":"Loading...","progressBar":true,"imageMode":"normal","image":null},"controls":{"greenFlag":{"enabled":true},"stopAll":{"enabled":true},"fullscreen":{"enabled":true},"pause":{"enabled":false}},"app":{"windowTitle":"Test","icon":null,"packageName":"project","windowMode":"window","version":"1.0.0"},"cloudVariables":{"mode":"local","cloudHost":"wss://clouddata.turbowarp.org","custom":{},"specialCloudBehaviors":false,"unsafeCloudBehaviors":false},"turbo":false,"framerate":30,"highQualityPen":false,"fencing":true,"miscLimits":true,"stageWidth":480,"stageHeight":360,"resizeMode":"preserve-ratio","autoplay":false,"username":"player####","closeWhenStopped":false,"projectId":"p4-@Project.sb3","custom":{"css":"","js":""},"appearance":{"background":"#000000","foreground":"#ffffff","accent":"#ff4c4c"},"monitors":{"editableLists":false,"variableColor":"#ff8c1a","listColor":"#fc662c"},"compiler":{"enabled":true,"warpTimer":false},"packagedRuntime":true,"target":"html","chunks":{"gamepad":false,"pointerlock":false},"cursor":{"type":"auto","custom":null,"center":{"x":0,"y":0}},"extensions":["""
    extno = 1
    for extension in onlyfiles:
        if extno > 1:
            build_json += ',{"url":"'
        else:
            build_json += '{"url":"'
        build_json += 'https://'+request.host+'/modules/'+extension
        build_json += '"}'
        extno += 1
    build_json += '],"bakeExtensions":true}'
    return build_json

@app.route('/modules/<path>')
def send_report(path):
    return open(config.get('settings_workdir', 'workdir')+'/'+path, 'r').read()

@app.route('/sb3')
def sb3():
    global workdir
    try:
        return send_file(workdir+'/'+config.get('settings_workdir', 'workfile'), attachment_filename='Project.sb3')
    except:
        return "ERROR || File not found"


@app.route('/rickroll')
def rickroll():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ", code=302)
    
#Functions

def init():
    global verbose, dry
    if not dry:
        os.mkdir(config.get('settings_workdir', 'workdir'))
    if verbose:
        print("INFO || Making modules directory.")

def update_repo():
    global verbose, dry
    url = config.get('settings_install','repository')
    if verbose:
        print("INFO || Getting repositories list.")
    r = requests.get(url, allow_redirects=True)
    if not dry:
        open('packages.json', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def get_package(package):
    global verbose, dry, args
    if args.local:
        r = open(package, 'r').read() # Local package
    elif args.remote != None: # Remote package
        r = requests.get(args.remote, allow_redirects=True)
        
        string = args.remote

        package = re.sub(r'.*\/', '', string)
    else: #From repository
        if verbose:
            print("INFO || Searching repositories list.")
        try:
            with open('packages.json', 'r') as fcc_file:
                url = json.load(fcc_file)[package]['repository_reqget']
        except:
            print("ERROR || Nonexistent package. Exiting.", file=sys.stderr)
            return
        if verbose:
            print("INFO || Getting package.")
        r = requests.get(url, allow_redirects=True)
    os.chdir(config.get('settings_workdir', 'workdir'))
    if verbose:
        print("INFO || Installing package.")
    
        
    if not dry:
        if args.remote:
            open(package, 'wb').write(r.content)
        else:
            open(package+'.js', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def package_list(search):
    global verbose
    if verbose:
        print("INFO || Searching repositories list.")
    with open('packages.json', 'r') as fcc_file:
        for key in json.load(fcc_file).keys():
            if search in key:
                print(key)
    

def start_server():
    if verbose:
        print("INFO || Starting server.")
    app.run(host="0.0.0.0", port=8000)

def get_package_info(package):
    global verbose, dry
    if verbose:
        print("INFO || Searching repositories list.")
    try:
        with open('packages.json', 'r') as fcc_file:
            jsont = json.load(fcc_file)[package]
    except:
        print("ERROR || Nonexistent package. Exiting.", file=sys.stderr)
        return
    print("Name:",jsont["name"])
    print("Description:",jsont["description"])
    print("Author:",jsont["author_name"])
    print("Contact:",jsont["author_contact"])
    print("Version:",jsont["version"])
    print("Sandboxed:",jsont["sandboxed"])
    if verbose:
        print("INFO || Done!")

def amogus():
    print("""                                                  
                                                  
                                                  
                                                  
                  (@@@@@@@@@@@@@@@(               
                *@@@%%%%%%%%%%%%%@@@@*            
               *@@&%%%%%%&@@@@@@@@@@@@@.          
               @@@%%%%&@@@/,,,,. ...,(@@&         
            ,%@@@&%%%%&@@#/,,,,..    .,/@@,       
        (@@@@&@@@&%%%%&@&####*,,,,,,/###@@#       
        &@@%%%&@@&&%%%%@@@############&@@@        
        &@@&&&@@@&&%%%%%%@@@@@@@@@@@@@@@%         
        @@@&&&@@@&&&%%%%%%%%%%%%%%%%%%@@@         
        @@&&&&@@@&&&%%%%%%%%%%%%%%%%%%@@@         
       .@@&&&&@@@&&&&%%%%%%%%%%%%%%%%&@@@.        
        @@&&&&@@@&&&&&&%%%%%%%%%%%%&&&@@&         
        #@@&&&&@@&&&&&&&&&&&&&&&&&&&&&@@(         
         #@@@@@@@&&&&&&&&@@@@@@@@@&&&@@@          
              *@@&&&&&&&@@@.*@@&&&&&&@@%          
               @@@&&&&&&@@@, @@&&&&&&@@*          
               @@@&&&&&@@@(  .@@@@@@@&            
                 &@@@@@@(                         
                                                  
                sus amognus                                  
                                                  
    """)

def remove_package(package):
    global verbose, dry
    if verbose:
        print("INFO || Changing directory to extensions folder.")
    os.chdir(config.get('settings_workdir', 'workdir'))
    if verbose:
        print("INFO || Uninstalling package.")
    if not dry:
        try:
            os.remove(package+'.js')
        except:
            print("ERROR || Package not existent.", file=sys.stderr)
    if verbose:
        print("INFO || Finished!")

def list():
    if verbose:
        print("INFO || Listing directory...")
    for item in onlyfiles:
        print(item)
    if verbose:
        print("INFO || Done!")

def configs(setting, value):
    if setting == "turbowarp_instance":
        config.set('settings_start', 'turbowarp_instance', value)
        if verbose:
            print("INFO || Setting value...")
    if setting == "workdir":
        config.set('settings_workdir', 'workdir', value)
        if verbose:
            print("INFO || Setting value...")
    if setting == "repository":
        config.set('settings_install','repository', value)
        if verbose:
            print("INFO || Setting value...")
    else:
        print("ERROR || No such setting", file=sys.stderr)

def clean():
    global verbose, dry
    if verbose:
        print("INFO || Cleaning directory...")
    if not dry:
        if os.path.isdir(config.get('settings_workdir', 'workdir')):
            shutil.rmtree(config.get('settings_workdir', 'workdir'))
        
def pack():
    global verbose, dry
    if verbose:
        print("INFO || Packaging...")
    if not dry:
        try:
            os.mkdir('build')
        except:
            try:
                os.system('rm -rf build')
                os.mkdir('build')
            except:
                print("ERROR || Failed to create build folder.", file=sys.stderr)
        os.chdir('build')
        # copy all .sb3 files
        for file in os.listdir(".."):
            if file.endswith(".sb3"):
                shutil.copy(os.path.join("..", file), ".")

        # copy settings_workdir
        shutil.copytree(os.path.join("..", config.get("settings_workdir","workdir")), "settings_workdir")
        os.chdir("..")
        os.system("tar -czf build")

def moo():
    print("I am sorry, but this program does not have Super Cow Powers. Please use the command line programs \"apt\" or \"aptitude\".")
    if input("Did you mean: apt-get moo? (yes/no) ") == "yes":
        os.system("apt-get moo")
    else:
        print("Okay. Bye.")
            
# Main

if args.cmd == "init":
    init()
elif args.cmd == "update":
    update_repo()
elif args.cmd == "install" or args.cmd == "i":
    get_package(args.extra)
elif args.cmd == "start":
    start_server()
elif args.cmd == "search":
    package_list(args.extra)
elif args.cmd == "version":
    print(version)
elif args.cmd == "info":
    get_package_info(args.extra)
elif args.cmd == "uninstall" or args.cmd == "remove" or args.cmd == "ui":
    remove_package(args.extra)
elif args.cmd == "list" or args.cmd == "l":
    list()
elif args.cmd == "config":
    configs(args.extra, args.selection)
elif args.cmd == "moo":
    moo()
elif args.amogus:
    amogus()
elif args.cmd == "clean":
    clean()
else:
    print("ERROR || No valid command selected. Exiting.", file=sys.stderr)
    parser.print_usage()
