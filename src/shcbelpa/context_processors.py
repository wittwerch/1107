from django.conf import settings # import the settings file
from .models import Album

def gallery_processor(request):
    albums = Album.objects.all().order_by('-updated')[:5]
    return { 'albums': albums }

def ga_tracking(request):
    return {'GA_TRACKING_CODE': settings.GA_TRACKING_CODE}