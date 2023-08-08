## Overview:
This scanner is a script I wrote with the original purpose to search github for OpenAI API Tokens and validate them if I would find something which matches the regex.

This script is customizable to search github for any regex. Additionally it checks for disk space, so no worry about that.

OS: Linux only


## How it works
- The Script creates a temporary directory, clones the directory, scans it for the regex. If something is found it is written to a log file.
- Logging: 
  + The logfile is named */tmp/gitquery/log* by default
  + The file wich stores valid keys is named */tmp/gitquery/store* by default
  + Log messages are: A git repo is cloned, A git repo is scanned, A git repo is removed, Storage information
- When done I recommend to save all findings in a different file because it will be deleted during a rerun of the script


## Customization:
- In the Head of the script you can freely customize the config
- The wordlist and regex-pattern is probably the most interesting, letting you change it to whatever you want to search for in github
- The script accesses github via API calls, so a github access token is neccessary, even it does not need any priviledges

