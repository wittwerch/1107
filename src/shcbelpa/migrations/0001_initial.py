# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table(u'shcbelpa_league', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('is_junior', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shcbelpa', ['League'])

        # Adding model 'Club'
        db.create_table(u'shcbelpa_club', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=60, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Club'])

        # Adding model 'Player'
        db.create_table(u'shcbelpa_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('number', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=0, blank=True)),
            ('born', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=0, blank=True)),
            ('shoots', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('photo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Player'])

        # Adding model 'Team'
        db.create_table(u'shcbelpa_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Club'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.League'], null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'shcbelpa', ['Team'])

        # Adding model 'Roster'
        db.create_table(u'shcbelpa_roster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Team'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Player'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'shcbelpa', ['Roster'])

        # Adding model 'Season'
        db.create_table(u'shcbelpa_season', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('lm_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Season'])

        # Adding model 'GameType'
        db.create_table(u'shcbelpa_gametype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'shcbelpa', ['GameType'])

        # Adding model 'Table'
        db.create_table(u'shcbelpa_table', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Season'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.League'])),
            ('game_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.GameType'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Team'])),
            ('gp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('win', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('loss', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('tie', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('diff', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'shcbelpa', ['Table'])

        # Adding model 'Game'
        db.create_table(u'shcbelpa_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Season'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.League'])),
            ('game_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.GameType'])),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', to=orm['shcbelpa.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', to=orm['shcbelpa.Team'])),
            ('lm_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Game'])

        # Adding model 'GameRecap'
        db.create_table(u'shcbelpa_gamerecap', (
            (u'blogpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blog.BlogPost'], unique=True, primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Game'])),
        ))
        db.send_create_signal(u'shcbelpa', ['GameRecap'])

        # Adding model 'SeasonPlayerStats'
        db.create_table(u'shcbelpa_seasonplayerstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Player'])),
            ('goal', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('assist', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_5', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_10', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_20', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_25', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ppg', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ppa', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('shg', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sha', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gw', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gt', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Team'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Season'])),
            ('game_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.GameType'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.League'])),
        ))
        db.send_create_signal(u'shcbelpa', ['SeasonPlayerStats'])

        # Adding unique constraint on 'SeasonPlayerStats', fields ['player', 'season', 'game_type', 'team', 'league']
        db.create_unique(u'shcbelpa_seasonplayerstats', ['player_id', 'season_id', 'game_type_id', 'team_id', 'league_id'])

        # Adding model 'GamePlayerStats'
        db.create_table(u'shcbelpa_gameplayerstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Player'])),
            ('goal', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('assist', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_5', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_10', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_20', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pm_25', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ppg', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ppa', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('shg', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sha', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gw', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gt', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Game'])),
        ))
        db.send_create_signal(u'shcbelpa', ['GamePlayerStats'])

        # Adding unique constraint on 'GamePlayerStats', fields ['player', 'game']
        db.create_unique(u'shcbelpa_gameplayerstats', ['player_id', 'game_id'])

        # Adding model 'Photo'
        db.create_table(u'shcbelpa_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gphoto_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('taken_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('photopage_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('small_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('medium_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('geo_latitude', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('geo_longitude', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'shcbelpa', ['Photo'])

        # Adding model 'Album'
        db.create_table(u'shcbelpa_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gphoto_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('albumname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shcbelpa.Game'], null=True, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Album'])

        # Adding M2M table for field photos on 'Album'
        m2m_table_name = db.shorten_name(u'shcbelpa_album_photos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'shcbelpa.album'], null=False)),
            ('photo', models.ForeignKey(orm[u'shcbelpa.photo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'photo_id'])

        # Adding model 'Sponsor'
        db.create_table(u'shcbelpa_sponsor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('logo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Sponsor'])

        # Adding model 'Teaser'
        db.create_table(u'shcbelpa_teaser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shcbelpa', ['Teaser'])


    def backwards(self, orm):
        # Removing unique constraint on 'GamePlayerStats', fields ['player', 'game']
        db.delete_unique(u'shcbelpa_gameplayerstats', ['player_id', 'game_id'])

        # Removing unique constraint on 'SeasonPlayerStats', fields ['player', 'season', 'game_type', 'team', 'league']
        db.delete_unique(u'shcbelpa_seasonplayerstats', ['player_id', 'season_id', 'game_type_id', 'team_id', 'league_id'])

        # Deleting model 'League'
        db.delete_table(u'shcbelpa_league')

        # Deleting model 'Club'
        db.delete_table(u'shcbelpa_club')

        # Deleting model 'Player'
        db.delete_table(u'shcbelpa_player')

        # Deleting model 'Team'
        db.delete_table(u'shcbelpa_team')

        # Deleting model 'Roster'
        db.delete_table(u'shcbelpa_roster')

        # Deleting model 'Season'
        db.delete_table(u'shcbelpa_season')

        # Deleting model 'GameType'
        db.delete_table(u'shcbelpa_gametype')

        # Deleting model 'Table'
        db.delete_table(u'shcbelpa_table')

        # Deleting model 'Game'
        db.delete_table(u'shcbelpa_game')

        # Deleting model 'GameRecap'
        db.delete_table(u'shcbelpa_gamerecap')

        # Deleting model 'SeasonPlayerStats'
        db.delete_table(u'shcbelpa_seasonplayerstats')

        # Deleting model 'GamePlayerStats'
        db.delete_table(u'shcbelpa_gameplayerstats')

        # Deleting model 'Photo'
        db.delete_table(u'shcbelpa_photo')

        # Deleting model 'Album'
        db.delete_table(u'shcbelpa_album')

        # Removing M2M table for field photos on 'Album'
        db.delete_table(db.shorten_name(u'shcbelpa_album_photos'))

        # Deleting model 'Sponsor'
        db.delete_table(u'shcbelpa_sponsor')

        # Deleting model 'Teaser'
        db.delete_table(u'shcbelpa_teaser')


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