from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect

from apps.blog.models import Article

class ArticleListView(ListView):
    queryset = Article.objects.filter(published=True).order_by("-published_date")
    context_object = "article_list"
    paginate_by = 4

class ArticleUnpublishedListView(ListView):
    queryset = Article.objects.filter(published=False).order_by("-created")
    context_object = "article_list"
    paginate_by = 4

class ArticleDetailView(DetailView):
    model = Article
    context_object = "article"

    def render_to_response(self, context):
        """
        Ensure that only authenticated users can access unpublished articles.
        """
        if not self.request.user.is_authenticated() and not context['article'].published:
            redirect_url = "%s?next=%s" % (reverse("login"), self.request.path_info)
            return redirect(redirect_url)
        return super(ArticleDetailView, self).render_to_response(context)

