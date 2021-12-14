from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView

# Create your views here.


class UserRedirectView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return redirect('/user/profile')
        pass