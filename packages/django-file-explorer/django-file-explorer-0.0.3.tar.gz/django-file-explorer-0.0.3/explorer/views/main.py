from django.http import FileResponse
import os
import shutil
from django import http
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator

from .utils.operations import ExplorerOperations
from .utils.request_validator import RequestValidator
from .utils.volume_operations import get_volume_location

class Explorer(TemplateView):
    template_name = 'explorer/index.html'
    http_method_names = ['get']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.message = None
        self.isFile = False
        self.abs_location = None
        self.redirect_url = None

        # PAGINATOR STAUE
        self.max_row_on_page = 12
        self.max_page_link = 3

        # STATE VARIABLES
        self.selected_volume = None
        self.location = None
        self.action = None
        self.page_number = None
        return None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(f'/admin/login/?next={reverse("explorer-main")}')
        return super().dispatch(request, *args, **kwargs)

    def _updateState(self, request):
        """Update the status of state variables."""
        # MAKING CLASS VARIBALE
        validator = RequestValidator(request)

        # UPDATING
        self.selected_volume = validator.getSelectedVolume()
        self.action = validator.getAction()
        self.location = validator.getLocation()
        self.page_number = validator.getPageNumber()
        return None

    def _getVolumeContext(self, volume_list):
        """Generating context for the volumes."""
        # EXCEPTION FOR EMPTY VOLUME LIST
        if len(volume_list) == 0:
            self.message = 'No volume assigned. Please contact Admin.'
            return None

        # GETTING LIST OF VOLUME WHOSE PATH DOES NOT EXISTS
        valid_volumes, invalid_volumes = [], []
        for volume_name in volume_list:
            volume_root_path = get_volume_location(volume_name)
            if volume_root_path is None:
                invalid_volumes.append(volume_name)
            else:
                valid_volumes.append(volume_name)

        # EXCEPTION FOR NO SELECTION OF VOLUME
        if self.selected_volume is None:
            comb_vols = valid_volumes + invalid_volumes
            self.selected_volume = comb_vols[0]

        # EXCEPTION FOR NON EXISTANCE VOLUME
        if self.selected_volume not in volume_list:
            self.message = f'Volume {self.selected_volume} does not exists.'
            return None
        
        # LOOPING THROUGH EACH VOLUME
        volumes = []
        for volume in volume_list:
            if self.selected_volume == volume:
                volumes.append({'name': volume, 'selected': 'active', 'status': 'enable'})
            elif volume in invalid_volumes:
                volumes.append({'name': volume, 'selected': 'deactive', 'status': 'disabled'})
            else:
                volumes.append({'name': volume, 'selected': 'deactive', 'status': 'enable'})
        return volumes

    def _getPaginatorContext(self, page_data):
        """Generating context for the paginator."""
        # EMPTY PAGINATOR DATA
        paginator_data = {}

        # GETTING PREVIOUS PAGE LINK
        if page_data.has_previous():
            paginator_data['previous_page_number'] = page_data.previous_page_number()

        # GETTING NEXT PAGE LINK
        if page_data.has_next():
            paginator_data['next_page_number'] = page_data.next_page_number()

        # GETTING START PAGE LINK
        current_page_number = page_data.number
        mid_point = self.max_page_link // 2
        start_page_link = current_page_number - mid_point
        if start_page_link < 1:
            start_page_link = 1

        # GETTING LAST PAGE LINK
        last_page_link = current_page_number + mid_point
        if last_page_link > page_data.paginator.num_pages:
            last_page_link = page_data.paginator.num_pages
        
        # LOOPING TO GET MIDDLE PAGES
        middle_pages = []
        for page in range(start_page_link, last_page_link+1):
            # GETTING SELECTED STATUS
            if page == current_page_number:
                selected = 'active'
            else:
                selected = 'deactive'

            middle_pages.append({
                'number': page,
                'selected': selected
            })
        paginator_data['middle_pages'] = middle_pages
        return paginator_data

    def get(self, request, *args, **kwargs):
        # GETTING CONTEXT
        context = self.get_context_data()

        # UPDATING STATE
        self._updateState(request)

        # MAKING EXPLORER OPERATION CLASS
        xops = ExplorerOperations(request.user)

        # GETTING VOLUME INFORMATION
        volume_list = xops.getVolumesNameList()
        volumes = self._getVolumeContext(volume_list)
        if volumes is None: # Error in the case of unknown volume.
            return self.render_to_response(context)
        context['volumes'] = volumes
        volume_root_path = xops.getVolumeLocation(self.selected_volume)
        if volume_root_path is None: # Volume root path does not exists.
            self.message = xops.message
            return self.render_to_response(context)
        context['selected_vol'] = self.selected_volume

        # GETTING ABS PATH
        if (self.location is None) or (self.location == ''):
            self.abs_location = volume_root_path
            self.location = ''
        else:
            self.abs_location = os.path.join(volume_root_path, self.location)
        abs_location, rel_location = self.abs_location, self.location
        context['rel_location'] = rel_location

        # CHECKING IF ABS PATH EXISTS
        if not os.path.exists(self.abs_location):
            self.message = f'{rel_location} does not exists.'
            return self.render_to_response(context)

        # GETTING ACTION CONTEXT
        context['actions'] = xops.getActions(self.selected_volume)
        if (self.action not in context['actions']) and (self.action is not None):
            self.message = f'{self.action} action is not allowed.'
            return self.render_to_response(context)

        # DELETING FILE IF REQUIRED
        if self.action == 'delete':
            if os.path.exists(self.abs_location):
                try:
                    if os.path.isdir(self.abs_location):
                        shutil.rmtree(self.abs_location)
                    else:
                        os.remove(self.abs_location)
                except:
                    self.message = f'Unable to remove: {rel_location}'
                    return self.render_to_response(context)
                rel_location = os.path.split(rel_location)[0]
                self.redirect_url = f'/explorer/?volume={self.selected_volume}&location={rel_location}'
                return self.render_to_response(context)
            else:
                self.message = f'{rel_location} does not exists.'
                return self.render_to_response(context)

        # CHECKING DIR OR FILE
        if os.path.isfile(abs_location):
            self.isFile = True
            return self.render_to_response(context)
        
        # GETTING DIR LIST
        list_dir, file_count = xops.listDir(abs_location, rel_location)
        context['file_count'] = file_count

        # GETTING NEVIGATION BAR
        nev_bar = xops.getNevigationBar(rel_location)
        context['nev_location_list'] = nev_bar

        # GEFINING PAGINATOR
        p = Paginator(list_dir, self.max_row_on_page)
        page_data = p.get_page(self.page_number)
        context['page_data'] = page_data

        # CHECKING WEATHER THE PAGINATOR REQUIRED
        if len(list_dir) > self.max_row_on_page:
            paginator_required = True
            paginator_data = self._getPaginatorContext(page_data)
        else:
            paginator_required = False
            paginator_data = None
        context['paginator_required'] = paginator_required
        context['paginator_data'] = paginator_data

        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs) -> http.HttpResponse:
        # EXCEPTION FOR 404 PAGE NOT FOUND
        if self.message:
            return render(self.request, 'explorer/error.html', {'message': self.message})

        # PERFORMING REDIRECT
        if self.redirect_url:
            return http.HttpResponseRedirect(self.redirect_url)

        # PERFORMING OPERATION
        if self.action == 'download': # Download case
            if not self.isFile:
                zip_file_path = os.path.join(os.path.split(self.abs_location)[0], f'{os.path.split(self.abs_location)[-1]}')
                shutil.make_archive(zip_file_path, 'zip', self.abs_location)
                return FileResponse(open(zip_file_path+'.zip', 'rb'))
            else:
                return FileResponse(open(self.abs_location, 'rb'), as_attachment=True)
        else:
            # IF FILE THEN VIEW IT
            if self.isFile:
                return FileResponse(open(self.abs_location, 'rb'), as_attachment=False)
        
        return super().render_to_response(context, **response_kwargs)