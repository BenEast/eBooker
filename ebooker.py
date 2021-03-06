#!/usr/bin/env python3
from tester import Tester, get_input, is_python_3
import sys
import os
import codecs
import webbrowser
import glob

# test if files exist
Tester().test()

# import urlopen
if is_python_3:
    from urllib.request import urlopen
    from urllib.error import URLError
else:
    from urllib2 import urlopen


##########################################################################
__version__ = "1.1.0"
__help_string__ = "eBooker v" + __version__ + " Help\n==============" + \
    ("=" * len(__version__)) + "\nhelp - show this help\nexit - quit the session\nabout - read about this tool\nedit - edit/create a file\nclear -\
      clear the screen\ndebug - give you a list of commonly occurring issues\nserve - open your book in a web browser for reviewing\n"
__about_string__ = "eBooker is a command-line tool which lets you create ebooks and other text files from command line with ease. \
You don't have to be a programming expert or a nerd to use this. Anyone with a basic knowledge in computers can use this tool very easily.\n"
##########################################################################


def install_markdown():
    ''' install markdown module if not found '''
    if is_python_3:
        os.system("pip3 install markdown")
    else:
        os.system("easy_install --home pip; pip install markdown")


is_unix = os.name == "posix"


def clear():
    ''' clears the terminal '''
    if is_unix:
        os.system("clear")
    else:
        os.system("cls")


def open_editor(fileString):
    if is_unix:
        os.system("nano " + fileString)
    else:
        os.system("notepad " + fileString)


def augment(filecontentsString):
    return "<!DOCTYPE html><html><head><title>" + "Your Book" + \
        "</title></head>" + filecontentsString + "</body></html>"


def debug():
    ''' print debug messages '''
    print(
        "|-----------------------|--------|\n"
        "|Message                |Code    |\n"
        "|-----------------------|--------|"
    )

    if is_unix:
        print(
            "|nano: command not found|42912246|\n"
            "|-----------------------|--------|\n"
            "|other message          |87376634|\n"
            "|-----------------------|--------|"
        )
    else:
        print(
            "|'notepad' is not       |64485253|\n"
            "|recognized as an       |        |\n"
            "|internal or external   |        |\n"
            "|command, operable      |        |\n"
            "|program or batch file. |        |\n"
            "|-----------------------|--------|\n"
            "|other message          |93856898|\n"
            "|-----------------------|--------|"
        )


def internet():
    try:
        urlopen("http://216.58.192.142", timeout=1)
        return True
    except URLError:
        return False


def markdown_installed():
    return 'markdown' in sys.modules


##########################################################################

clear()

if not markdown_installed():
    if internet():
        install_markdown()
    else:
        print("Your internet connection is either too slow or nonexistent! I cannot install the required packages for you.")
        sys.exit(1)

import markdown

clear()
print(
    "       ____              _ \n"
    "      |  _ \            | |\n"
    "   ___| |_) | ___   ___ | | _____ _ __\n"
    "  / _ \  _ < / _ \ / _ \| |/ / _ \  __|\n"
    " |  __/ |_) | (_) | (_) |   <  __/ |\n"
    "  \___|____/ \___/ \___/|_|\_\___|_| v" + __version__ + 
    "                       Running on Python " + 
    str(sys.version_info[0]) + "!\n"
    "\n"
    'Type in "help" at the prompt for, of course, help.'
)

##########################################################################

# Commands are mapped to this dict by decorators
_commands = dict()

# Define command decorator
def command(name):
    def call_command(func):
        _commands[name] = func  # Map name to func in _commands
        return func
    return call_command


@command("debug")
def cmd_debug():
    print("Debugging help for MacOS/*is_unix __version__:")
    print(
        "Email me at archmaster@yahoo.com with the error code for the error message you encountered.")
    debug()
    

@command("clear")
def cmd_clear():
    print("Clearing...")
    clear()
    print("******************** eBooker v" + 
          __version__ + " ********************")
    print("")
    

@command("serve")
def cmd_serve():
    print("Serving book...")
    filenameArray = glob.glob(os.path.dirname(
        os.path.realpath(__file__)) + "/*.html")
    filebufferString = ""

    for filenameString in filenameArray:
        newfilenameString = os.path.basename(filenameString)
        chapternameString = os.path.splitext(newfilenameString)[0]
        chapternameString = chapternameString.replace("-", " ", 1)
        chapternameString = chapternameString.capitalize()
        filebufferString += "<h1>" + chapternameString + "</h1>"
        filecontentsString = codecs.open(
            newfilenameString, "r", "utf-8").read()
        filebufferString += markdown.markdown(filecontentsString)
        filebufferString += "<hr/>"
    filebufferString += "<center><h1>THE END!</h1></center>"
    filebufferString = augment(filebufferString)
    reviewfileFile = codecs.open("review-book.html", "w", "utf-8")
    reviewfileFile.write(filebufferString)
    reviewfileFile.close()
    webbrowser.open(
        "file://" + os.path.dirname(os.path.realpath(__file__)) + "/review-book.html")
    print(
        "Success! Your book is served. Press RETURN when you are done reviewing it."
    )

    get_input("")
    os.remove("review-book.html")
    

@command("edit")
def cmd_edit():
    editLoopBool = True

    while editLoopBool:
        editBool = get_input("Would you like to create a new chapter? (y/n) ").lower()

        if editBool == "y":
            editLoopBool = False
            print("You want to create a new chapter.")

            while True:
                newChapterNumber = get_input("What would you like the chapter number to be? ")
                try:
                    newChapterNumber = int(newChapterNumber)
                    break
                
                except (TypeError, ValueError):
                    print("You must enter a number.")

            print("Creating file...")

            newChapterFile = codecs.open(
                "chapter-" + str(newChapterNumber) + ".html", "a", "utf-8"
            )
            newChapterFile.write(
                "Press CTRL-O then hit return to save. Press CTRL-X to exit.\n"
            )
            newChapterFile.write(
                "Don't worry if you can't see part of your lines; they will\n"
            )

            newChapterFile.write("be saved anyway.")
            newChapterFile.close()

            print("Your file is created!")

            open_editor("chapter-" + str(newChapterNumber) + ".html")

            print('If you got an error, use the "debug" command.')

        elif editBool == "n":
            editLoopBool = False
            print("You want to edit an existing chapter!")

            while True:
                editChapterNumber = get_input("Please type in the chapter number. ")
                try:
                    editChapterNumber = int(editChapterNumber)
                    break
                 
                except (TypeError, ValueError):
                    print("You must enter a number.")

            print("Opening file for editing...")

            open_editor("chapter-" + str(editChapterNumber) + ".html")

            print('If you got an error, use the "debug" command.')

        else:
            print('Please type in "y" or  "n".')
            

@command("about")
def cmd_about():
    print(__about_string__)
    

@command("exit")
def cmd_exit():
    exitLoopBool = True
    while exitLoopBool:
        exitBool = get_input("Would you like to quit? (y/n) ")
        
        if exitBool.lower() == "y":
            clear()
            sys.exit()
            
        elif exitBool.lower() == "n":
            exitLoopBool = False
            print("OK, not exiting!")
            
        else:
            print('Please type in "y" or  "n".')
            

@command("help")
def cmd_help():
    print(__help_string__)


# Attempts to execute the specified command.
# Raises a KeyError if invalid command is given.
def run_command(name):
    try:
        _commands[name.lower()]()
    except KeyError:
        print('"' + name + '" is not a valid command. Type "help" for more options.\n')
    
##########################################################################

def main():
    while True:
        cmd = get_input("eBooker > ")
        run_command(cmd)
        
try:
    main()

except KeyboardInterrupt:
    print("")
    sys.exit()
