from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.shortcuts import get_object_or_404

from .models import UserProfile

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

from .forms import GuestForm
from django.shortcuts import redirect
from django.contrib import messages

import requests
import json
import pandas as pd
from functools import reduce

import base64
import os
import os.path

from datetime import datetime
import time
from django.db.models import Q

from profiles_project.secrets import YITU_AUTH

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


url_visitors = "https://10.12.201.64:9812/visitors"
url_history = "https://10.12.201.64:9812/visitors/history"

headers = {
    "Content-Type": "application/json",
    "Authorization": YITU_AUTH
}

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and update profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'nric_number',)


class UserLoginApiView(ObtainAuthToken):
    """Handle user authentication token"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class VisitorList(ListView):

    template_name = 'userprofile_list.html'
    model = UserProfile
    context_object_name = 'visitors'
    ordering = ['reg_date']
    paginate_by = 3

    def get_queryset(self): # new
        query = self.request.GET.get('q', '')
        object_list = UserProfile.objects.filter(
            Q(name__icontains=query) | Q(nric_number__icontains=query)
        )
        return object_list


# Granting access to a registered guest
class VisitorDetail(DetailView):

    model = UserProfile
    template_name = 'userprofile.html'
    context_object_name = 'visitor'

    def post(self, request, pk=None):

        if request.method == 'POST':
            form = UserProfile.objects.get(pk=pk)

            form_img = form.photo
            form_nric = form.nric_number
            form_name = form.name
            form_mobile_number = form.mobile_number
            form_company = form.company

            form_img_url = "/vagrant/media/" + str(form_img)

            last_access = form.last_access_date.strftime("%Y-%m-%d")
            now_access = datetime.today().strftime("%Y-%m-%d")

            if last_access == now_access:
                messages.success(request, 'Visitor access in on going')
                return redirect('userprofile', pk=pk)
            else:
                form.last_access_date = datetime.today()

                form.save(update_fields=['last_access_date'])

                print(form_name)
                print(last_access)

                with open(form_img_url, "rb") as file:
                    enc_img = base64.b64encode(file.read())
                    dec_img = enc_img.decode("utf-8")
                    print(dec_img)

                payload = {
                  "visitor_list" : [ {
                    "card_numbers" : [ form_nric ],
                    "face_image_content" : dec_img,
                    "meta" : {},
                    "person_information" : {
                      "company" : form_company,
                      "identity_number" : form_nric,
                      "name" : form_name,
                      "phone" : form_mobile_number,
                      "remark" : "",
                      "visit_end_timestamp" : 0,
                      "visit_start_timestamp" : 0,
                      "visit_time_type" : 1,
                      "visitee_name" : ""
                    },
                    "tag_id_list" : [ "5e58b6d9e2e6a700014a2b19" ]
                  } ]
                }

                jsonpayload = json.dumps(payload)

                response = requests.request("POST", url_visitors, headers=headers, data=jsonpayload, verify=False)

                print(response.text)

                messages.success(request, 'Visitor is allowed to access')
                return redirect('userprofile', pk=pk)

        else:
            form = GuestForm()

        return render(request, 'userprofile.html', {
            'form': form
        })


def search(request):
    return render(request, 'search.html', {})


def history(request):

    # response = requests.request("GET", url_history, headers=headers, verify=False)
    #
    # history = json.loads(response.text)
    # info = history.get("result", {})
    # info_for_csv = history.get("result", {})
    #
    # infoarr = json.dumps(info, indent=2)
    #
    # # pagination
    #
    # page = request.GET.get('page', 1)
    #
    # paginator = Paginator(info, 3)
    #
    # try:
    #     info = paginator.page(page)
    # except PageNotAnInteger:
    #     info = paginator.page(1)
    # except EmptyPage:
    #     info = paginator.page(paginator.num_pages)
    #
    # context = {'info': info }
    #
    # file = []
    #
    # for item in info_for_csv:
    #     name = item['person_information']['name']
    #     inf = item['person_information']
    #     file.append(inf)
    #
    # for f in file:
    #     t_start = datetime.fromtimestamp(f['visit_start_timestamp'])
    #     t_end = datetime.fromtimestamp(f['visit_end_timestamp'])
    #     t_check = datetime.fromtimestamp(f['check_out_timestamp'])
    #     f['visit_start_timestamp'] = t_start.strftime("%d-%m-%Y %H:%M:%S")
    #     f['visit_end_timestamp'] = t_end.strftime("%d-%m-%Y %H:%M:%S")
    #     f['check_out_timestamp'] = t_check.strftime("%d-%m-%Y %H:%M:%S")
    #
    #
    # outname = 'history.csv'
    # outdir = './media/logs'
    #
    # fullname = os.path.join(outdir, outname)
    #
    # result = pd.DataFrame(file)
    #
    # result.to_csv(fullname, index=False)

    context = {}

    df1 = pd.read_table('./media/logs/history.csv', sep=',')
    df2 = pd.read_table('./media/logs/log_hw.csv', sep=',')

    time_yitu = df1['visit_start_timestamp']
    time_hw = df2['visit_start_timestamp_hw']

    delta = []

    for t1, t2 in zip(time_yitu, time_hw):
        fmt = '%d-%m-%Y %H:%M:%S'
        ts1 = datetime.strptime(t1, fmt)
        ts2 = datetime.strptime(t2, fmt)
        dt = ts2 - ts1
        dt_secs = int(dt.total_seconds())
        delta.append(dt_secs)

    # print(delta)
    # delta_time = time_hw == time_yitu

    new_delta = []

    for time in delta:
        if time >= 5:
            new_delta.append('FAILED')
        elif time < 5:
            new_delta.append('PASSED')

    df1['success_test'] = new_delta

    print(df1)

    outname = 'history_log.csv'
    outdir = './media/logs'
    fullname = os.path.join(outdir, outname)

    result = pd.DataFrame(df1)
    result.to_csv(fullname, index=False)

    return render(request, 'history.html', context)


# Registering a guest
def register_guest(request):

    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            form_img = form.cleaned_data['photo']
            form_nric = form.cleaned_data['nric_number']
            form_name = form.cleaned_data['name']
            form_mobile_number = form.cleaned_data['mobile_number']
            form_company = form.cleaned_data['company']

            form_img_url = "/vagrant/media/photos/" + str(form_img)

            with open(form_img_url, "rb") as file:
                enc_img = base64.b64encode(file.read())
                dec_img = enc_img.decode("utf-8")
                print(dec_img)

            payload = {
              "visitor_list" : [ {
                "card_numbers" : [ form_nric ],
                "face_image_content" : dec_img,
                "meta" : {},
                "person_information" : {
                  "company" : form_company,
                  "identity_number" : form_nric,
                  "name" : form_name,
                  "phone" : form_mobile_number,
                  "remark" : "",
                  "visit_end_timestamp" : 0,
                  "visit_start_timestamp" : 0,
                  "visit_time_type" : 1,
                  "visitee_name" : ""
                },
                "tag_id_list" : [ "5e58b6d9e2e6a700014a2b19" ]
              } ]
            }

            jsonpayload = json.dumps(payload)

            response = requests.request("POST", url_visitors, headers=headers, data=jsonpayload, verify=False)

            print(response.text)

            messages.success(request, 'Guest is registered successfully!')
            return redirect('register_guest')
    else:
        form = GuestForm()

    return render(request, 'register_guest.html', {
        'form': form
    })
