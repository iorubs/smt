from rest_framework_nested import routers
from django.conf.urls import patterns, url, include
from smt.views import IndexView, bleuScoreView, meteorScoreView, nistScoreView, translateView

urlpatterns = patterns(
        '',
        url(r'^api/v1/bleu-score/$', bleuScoreView),
        url(r'^api/v1/meteor-score/$', meteorScoreView),
        url(r'^api/v1/nist-score/$', nistScoreView),
        url(r'^api/v1/translate/$', translateView),
        url('^.*$', IndexView.as_view(), name='index'),
)