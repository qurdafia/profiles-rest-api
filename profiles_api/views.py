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


# Registering a guest
def register_guest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('nric_number'))
            messages.success(request, 'Guest is registered successfully!')
            return redirect('register_guest')
    else:
        form = GuestForm()

    return render(request, 'register_guest.html', {
        'form': form
    })
