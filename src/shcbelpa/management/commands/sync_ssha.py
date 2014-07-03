from django.core.management.base import BaseCommand, CommandError

from shcbelpa.synchronizer import LigaManager

class Command(BaseCommand):

    def handle(self, *args, **options):
        lm = LigaManager()
        lm.sync_games()