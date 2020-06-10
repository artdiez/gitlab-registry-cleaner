import sys
import re
import logging

# Enter URL GitLab server, example https://git.yourcompany.org
gitServer = ''
# Enter Access Token for GitLab API
token = ''


class Configs:

    # Initial configs
    def __init__(self):
        self.server = gitServer
        self.token = token
        self.checkInput()

    # Check input arguments: sys.argv[1] -name_regex_delete, sys.argv[2] - keep_tags, sys.argv[3] - older_tags

    def checkInput(self):
        if (len(sys.argv) != 4 or len(sys.argv) == 0):
            print('ERROR! Wrong input data ')
            sys.exit(1)
        elif len(sys.argv[1]) < 2:
            print('ERROR! First argument must be regexp')
            sys.exit(1)
        elif sys.argv[2].isdecimal() is not True:
            print('ERROR! Second argument must be integer')
            sys.exit(1)
        elif len(re.findall(r'^[1-9]{1,2}([h|d]|month){1}', sys.argv[3])) == 0:
            print(
                'ERROR! Second argument must be written in human readable form. Example: 1h, 1d, 1month')
            sys.exit(1)
        else:
            self.name_regex_delete = sys.argv[1]
            self.keep_tags = sys.argv[2]
            self.older_tags = sys.argv[3]
