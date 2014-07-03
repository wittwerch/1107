from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from shcbelpa.picasaweb import PicasawebSyncr

class Command(BaseCommand):

    def handle(self, *args, **options):
        picasa = PicasawebSyncr(settings.PICASA_USER , settings.PICASA_PASSWORD, cli_verbose=0)
        picasa.syncAllAlbums(settings.PICASA_USER)