from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

from .forms import GuestForm
from django.shortcuts import redirect
from django.contrib import messages

import requests
import json
import base64
import os
import os.path

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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


def history(request):
    url = "https://10.12.201.64:9812/visitors/history"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXJ0bmVyIiwiY3JlYXRlZCI6MTU4MzI4Njg2MzIzOSwibmFtZSI6InBhcnRuZXIiLCJleHAiOjE1ODMzNzMyNjMsImlhdCI6MTU4MzI4Njg2M30.O6B9QUW5Sm9g_cps0JryU7Oqn5rveyRykuUtQebZ7Gs"
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    history = json.loads(response.text)
    info = history.get("result", {})
    print(json.dumps(info, indent=2))
    # for item in info:
    #     person = item["person_information"]
    #     print(type(person))
    #     # person_name = person["name"]
    #     # person_company = person["company"]
    #     # person_visit = person["visit_start_timestamp"]

    context = {'info': info }

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
            form_company = form.cleaned_data['company']

            form_img_url = "/vagrant/media/photos/" + str(form_img)

            with open(form_img_url, "rb") as file:
                enc_img = base64.b64encode(file.read())
                dec_img = enc_img.decode("utf-8")
                print(dec_img)

            url = "https://10.12.201.64:9812/visitors"

            headers = {
                "Content-Type": "application/json",
                "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXJ0bmVyIiwiY3JlYXRlZCI6MTU4MzI4Njg2MzIzOSwibmFtZSI6InBhcnRuZXIiLCJleHAiOjE1ODMzNzMyNjMsImlhdCI6MTU4MzI4Njg2M30.O6B9QUW5Sm9g_cps0JryU7Oqn5rveyRykuUtQebZ7Gs"
            }

            payload = {
              "visitor_list" : [ {
                "card_numbers" : [ form_nric ],
                "face_image_content" : dec_img,
                "meta" : {},
                "person_information" : {
                  "company" : form_company,
                  "identity_number" : form_nric,
                  "name" : form_name,
                  "phone" : "",
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

            response = requests.request("POST", url, headers=headers, data=jsonpayload, verify=False)

            print(response.text)

            messages.success(request, 'Guest is registered successfully!')
            return redirect('register_guest')
    else:
        form = GuestForm()

    return render(request, 'register_guest.html', {
        'form': form
    })
