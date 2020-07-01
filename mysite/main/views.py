from django.shortcuts import render
from django.views import View
# Create your views here.

class IndexClass(View):
    def get(self, request):
        return render(request, 'main/homepage.html')
