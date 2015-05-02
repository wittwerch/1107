# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Player.slug'
        db.add_column(u'shcbelpa_player', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='foo', max_length=50),
                      keep_default=False)

        if not db.dry_run:
            for player in orm['shcbelpa.Player'].objects.all():
                player.slug = slugify("%s-%s" % (player.first_name, player.last_name))
                player.save()

    def backwards(self, orm):
        # Deleting field 'Player.slug'
        db.delete_column(u'shcbelpa_player', 'slug')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blog.blogcategory': {
            'Meta': {'ordering': "(u'title',)", 'object_name': 'BlogCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'blog.blogpost': {
            'Meta': {'ordering': "(u'-publish_date',)", 'object_name': 'BlogPost'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'blogposts'", 'blank': 'True', 'to': u"orm['blog.BlogCategory']"}),
            u'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured_image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_posts_rel_+'", 'blank': 'True', 'to': u"orm['blog.BlogPost']"}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'blogposts'", 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'shcbelpa.album': {
            'Meta': {'ordering': "('-updated',)", 'object_name': 'Album'},
            'albumname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Game']", 'null': 'True', 'blank': 'True'}),
            'gphoto_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shcbelpa.Photo']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'shcbelpa.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '60', 'blank': 'True'})
        },
        u'shcbelpa.game': {
            'Meta': {'ordering': "['date_time']", 'object_name': 'Game'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': u"orm['shcbelpa.Team']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.GameType']"}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': u"orm['shcbelpa.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.League']"}),
            'lm_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Season']"})
        },
        u'shcbelpa.gameplayerstats': {
            'Meta': {'unique_together': "(('player', 'game'),)", 'object_name': 'GamePlayerStats'},
            'assist': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Game']"}),
            'goal': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Player']"}),
            'pm_10': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_2': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_20': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_25': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_5': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ppa': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ppg': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sha': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'shg': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'shcbelpa.gamerecap': {
            'Meta': {'ordering': "(u'-publish_date',)", 'object_name': 'GameRecap', '_ormbases': [u'blog.BlogPost']},
            u'blogpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['blog.BlogPost']", 'unique': 'True', 'primary_key': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Game']"})
        },
        u'shcbelpa.gametype': {
            'Meta': {'object_name': 'GameType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'shcbelpa.league': {
            'Meta': {'object_name': 'League'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_junior': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'shcbelpa.photo': {
            'Meta': {'ordering': "('-taken_date',)", 'object_name': 'Photo'},
            'content_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'geo_latitude': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'geo_longitude': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'gphoto_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photopage_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'small_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'taken_date': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'shcbelpa.player': {
            'Meta': {'ordering': "['first_name']", 'object_name': 'Player'},
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0', 'blank': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'shoots': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '0', 'blank': 'True'})
        },
        u'shcbelpa.roster': {
            'Meta': {'object_name': 'Roster'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Team']"})
        },
        u'shcbelpa.season': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Season'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lm_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'shcbelpa.seasonplayerstats': {
            'Meta': {'ordering': "['-points']", 'unique_together': "(('player', 'season', 'game_type', 'team', 'league'),)", 'object_name': 'SeasonPlayerStats'},
            'assist': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.GameType']"}),
            'goal': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gt': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.League']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Player']"}),
            'pm': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_10': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_2': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_20': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_25': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pm_5': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ppa': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ppg': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Season']"}),
            'sha': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'shg': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Team']"})
        },
        u'shcbelpa.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'shcbelpa.table': {
            'Meta': {'object_name': 'Table'},
            'diff': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.GameType']"}),
            'gp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.League']"}),
            'loss': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Season']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Team']"}),
            'tie': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'win': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'shcbelpa.team': {
            'Meta': {'object_name': 'Team'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.Club']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shcbelpa.League']", 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shcbelpa.Player']", 'null': 'True', 'through': u"orm['shcbelpa.Roster']", 'blank': 'True'})
        },
        u'shcbelpa.teaser': {
            'Meta': {'object_name': 'Teaser'},
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['shcbelpa']