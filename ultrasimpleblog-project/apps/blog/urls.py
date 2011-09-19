from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from apps.blog.models import Article
from apps.blog.views import ArticleListView, ArticleUnpublishedListView, ArticleDetailView



urlpatterns = patterns('',
    url('^$', ArticleListView.as_view(), name="article_index"),

    # 'unpublished' and 'new' are prefixed with '.' to prevent clash with a slug like 'new'.
    url('^.unpublished/$',
        login_required(ArticleUnpublishedListView.as_view()),
        name="article_unpublished_index"),

    url(r'^(?P<slug>[\w\d-]+)/$', ArticleDetailView.as_view(), name="article_view"),

    url('^.new/$', # see above comment about '.' prefix.
        login_required(CreateView.as_view(model=Article)),
        name="article_new"),

    url('^(?P<slug>[\w\d-]+)/edit/$',
        login_required(UpdateView.as_view(model=Article, context_object_name="article")),
        name="article_edit"),

    url('^(?P<slug>[\w\d-]+)/delete/$',
        login_required(DeleteView.as_view(model=Article,
                           context_object_name="article",
                           success_url="/blog/")), # @@@ Should be more DRY
        name="article_delete"),
)
