""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-02 10:43:49
Project:	 File explorer lib
Description: Provide class to perform explorer related operations.
"""

import os
import datetime

from explorer.models.user_role import UserRole
from explorer.models.volume import Volume
from .sorting import sort_files
from .volume_operations import get_volume_location


class ExplorerOperations():
    def __init__(self, user) -> None:
        self._user = user
        self.message = None
    
    def getVolumesNameList(self):
        """Listing the name of volumes availabe for the user."""
        # GETTING VOLUME LIST
        queryset = UserRole.userroles.filter(user=self._user)
        if queryset.exists():
            user_vol_list = [query.volume.name for query in queryset if query.volume.active]
        else:
            user_vol_list = []
        return user_vol_list

    def getVolumeLocation(self, volume_name):
        """Getting location of volume."""
        # GETTING LOCATION
        volume_root_path = get_volume_location(volume_name)
        if volume_root_path is None:
            self.message = f'Either volume {volume_name} or path does not exists.'
            return None
        return volume_root_path

    def listDir(self, abs_location, rel_location):
        """Getting list of files."""
        # GETTING LIST OF DIR
        list_dir = os.listdir(abs_location)

        # SEPRATING FILES AND DIRS
        file_list, deactive_file_list, file_ctime_list = [], [], []
        dir_list, deactive_dir_list, dir_ctime_list = [], [], []
        for dir in list_dir:
            path = os.path.join(abs_location, dir)
            if os.path.isfile(path):
                try:
                    # GETTING TIME
                    ctime = os.path.getctime(path)
                    file_ctime_list.append(ctime)
                    ftime = datetime.datetime.fromtimestamp(ctime)
                    creation_time = ftime.strftime("%d-%b-%Y %I:%M %p")

                    # GETTING SIZE
                    size = os.path.getsize(path)

                    # APPENDING INFORMATION
                    file_list.append({'name': dir, 'location': rel_location, 'type': 'File', 'valid': True, 'creation_time': creation_time, 'size': size})
                except:
                    deactive_file_list.append({'name': dir, 'location': rel_location, 'type': 'File', 'valid': False})
            else:
                try:
                    # GETTING TIME
                    ctime = os.path.getctime(path)
                    dir_ctime_list.append(ctime)
                    ftime = datetime.datetime.fromtimestamp(ctime)
                    creation_time = ftime.strftime("%d-%b-%Y %I:%M %p")

                    # GETTING SIZE
                    size = os.path.getsize(path)

                    # APPENDING INFORMATION
                    dir_list.append({'name': dir, 'location': rel_location, 'type': 'Directory', 'valid': True, 'creation_time': creation_time, 'size': size})
                except:
                    deactive_dir_list.append({'name': dir, 'location': rel_location, 'type': 'Directory', 'valid': False})

        # PERFORMING SORTING
        file_list = sort_files(file_ctime_list, file_list, mode='d')
        file_list += deactive_file_list
        dir_list = sort_files(dir_ctime_list, dir_list, mode='d')
        dir_list += deactive_dir_list

        # COUNTING FILE AND DIR
        file_count = len(file_list)
        dir_count = len(dir_list)

        # SORTING
        list_dir = dir_list + file_list

        # MAKING DICT
        file_count = {'file': file_count, 'dir': dir_count}
        return list_dir, file_count

    def getNevigationBar(self, location):
        """Making nevigation bar."""
        # MAKING NAVIGATION BAR
        sep_locations = location.split(os.path.sep)
        nev_location_list = []
        rel_loc = '/'
        for loc in sep_locations:
            if loc == '':
                continue
            rel_loc = os.path.join(rel_loc, loc)
            nev_location_list.append({'name': loc, 'location': rel_loc})
        return nev_location_list

    def getActions(self, selected_volume):
        """List the available actions."""
        # GETTING VOLUME
        volume = Volume.volumes.getIfExists(selected_volume)
        if volume is None:
            return []
        
        # GETTING ACTIONS
        queryset = UserRole.userroles.filter(user=self._user, volume=volume)
        actions = set()
        if queryset.exists():
            for query in queryset:
                action_list = query.opertations.all()
                for a in action_list:
                    actions.add(a.name)
        actions_list = list(actions)
        return actions_list