""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-02 11:15:21
Project:	 File explorer lib
Description: Provide class to perform request validation.
"""

import os

class RequestValidator():
    def __init__(self, request) -> None:
        self._request = request

    def getSelectedVolume(self):
        return self._request.GET.get('volume')

    def getAction(self):
        return self._request.GET.get('action')

    def getLocation(self):
        # GETTING LOCATION VALUE
        location = self._request.GET.get('location')

        # RETURNING BACK IF NONE
        if (location is None) or (location == ''):
            return location
        
        # IF PATH CONATIN SEPRATOR
        if location[0] == os.path.sep:
            location = location[1:]
        return location

    def getPageNumber(self):
        return self._request.GET.get('page')