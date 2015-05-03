from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings

from shcbelpa.views import *
from shcbelpa.forms import CustomOrderForm

admin.autodiscover()

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns('',

    url("^shop/checkout/$", "cartridge.shop.views.checkout_steps", name = "checkout_steps", kwargs=dict(form_class=CustomOrderForm)),

    url(r"^shop-backend/orders/$", OrderListView.as_view(), name="order_list"),
    url(r"^shop-backend/order/(?P<pk>\d+)$", OrderDetailView.as_view(), name="order_detail"),

    # Cartridge URLs.
    ("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

    url("^$", HomeView.as_view(), name='home'),

    url(r'^(?P<team_pk>\d{1})/season/(?P<season>\d{4})', SeasonView.as_view(), name='season'),

    url(r"^game/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/", GameView.as_view(), name="game"),

    # legacy url (redirect to slugified url)
    url(r'^player/(?P<pk>\d+)/$', PlayerRedirectView.as_view(), name='player-redirect'),

    url(r'^player/(?P<slug>[-\w]+)/$', PlayerView.as_view(), name='player'),

    url(r'^(?P<team_pk>\d+)/players$', RosterView.as_view(), name='roster'),

    url(r'^(?P<team_pk>\d{1})/stats/(?P<season>\d{4})/(?P<game_type>.*)$', StatsView.as_view(), name='stats'),

    url(r'^hall-of-fame$', HallOfFameView.as_view(), name='stats'),

    url(r'^gallery/$', GalleryView.as_view(), name='gallery'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),

    url(r'^sponsoring/$', SponsorView.as_view(), name='sponsor'),

    # Redirect from legacy url to mezzanine blog feed
    url(r'^feed/$', RedirectView.as_view(url='/blog/feeds/atom')),

    url(r'^news/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(url='/blog/%(slug)s/')
    ),

    ("^", include("mezzanine.urls")),
)

# block all bots on non-production environments
if settings.DEBUG is True:
    urlpatterns += patterns('',
        (r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
    )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
