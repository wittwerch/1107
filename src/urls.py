from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import RedirectView

from shcbelpa.views import HomeView, PlayerView, RosterView, SeasonView, StatsView, GalleryView, AlbumView, \
    SponsorView, HallOfFameView, GameView, OrderListView
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

    # Cartridge URLs.
    ("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

    url("^$", HomeView.as_view(), name='home'),

    url(r'^(?P<team_pk>\d{1})/season/(?P<season>\d{4})', SeasonView.as_view(), name='season'),

    url(r"^game/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/", GameView.as_view(), name="game"),

    url(r'^player/(?P<pk>\d+)/$', PlayerView.as_view(), name='player'),

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

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.

    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
