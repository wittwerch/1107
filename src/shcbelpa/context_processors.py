from .models import Album

def gallery_processor(request):
    albums = Album.objects.all().order_by('-updated')[:5]
    return { 'albums': albums }