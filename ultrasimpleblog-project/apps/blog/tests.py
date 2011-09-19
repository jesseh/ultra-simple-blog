"""
The purpose of these test is both to provide good test coverage and to define
and report expected behavior to project stakeholders. The names of the tests
are composed to generate readable sentences declaring each element of
functionality.  These sentences form a set of acceptance test declarations for a loose form of
Behavior Driven Development.

The sentence are generated concating the class name + (test name - 'test' prefix). Then the camel casing is replaced inserted spaces.

Tests that should not be included in the generated ouput should use the prefix
'testunit' rather than 'test'.

Use the management command 'expectations' to generate the sentences.

For more information see:
http://blog.i-iterate.com/2011/05/13/the-business-value-of-an-automated-test-suite/
"""

from django.test import TestCase
from django.test.client import RequestFactory

def _get_article(slug="testslug"):
    from apps.blog.models import Article
    return Article(title="test title", slug=slug, content="test content")

def _create_user_and_login(client):
    from django.contrib.auth.models import User
    u = User.objects.create(username="a")
    u.set_password("a")
    u.save()
    client.login(username="a", password="a")
    
class ArticleShould(TestCase):
    def setUp(self):
        """
        Clean out the database in case the previous test failed.
        """
        pass

    def tearDown(self):
        from apps.blog.models import Article
        Article.objects.all().delete()

    def testLeaveThePublishedDateUnsetBeforeBeingPublished(self):
        article = _get_article()
        article.full_clean()
        self.assertFalse(article.published_date)

    def testSetThePublishedDateWhenFirstPublished(self):
        article = _get_article()
        article.published = True
        article.full_clean()
        self.assertTrue(article.published_date)

    def testSetThePublishedDateRemainsStableWhenRePublished(self):
        article = _get_article()
        article.published = True
        article.full_clean()
        first_date = article.published_date
        article.published = False
        article.full_clean()
        article.published = True
        article.full_clean()
        self.assertTrue(article.published_date)

    def testShouldHaveAnAdminView(self):
        response = self.client.get("/admin/blog/article/")
        self.assertEqual(response.status_code, 200)


class ArticleViewsShould(TestCase):
    slug = "testslug"

    def _create_article(self):
        article = _get_article(slug=self.slug)
        article.save()

    def testRequireLoginForCreate(self):
        response = self.client.get("/blog/.new/")
        self.assertRedirects(response, "/accounts/login/?next=/blog/.new/")

    def testCreate(self):
        _create_user_and_login(self.client)
        response = self.client.get("/blog/.new/")
        self.assertEqual(response.status_code, 200)

    def testRequireLoginForEdit(self):
        self._create_article()
        url = "/blog/%s/edit/" % self.slug
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=%s" % url)

    def testEdit(self):
        self._create_article()
        _create_user_and_login(self.client)
        url = "/blog/%s/edit/" % self.slug
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRequireLoginForDelete(self):
        self._create_article()
        url = "/blog/%s/delete/" % self.slug
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=%s" % url)

    def testDelete(self):
        self._create_article()
        _create_user_and_login(self.client)
        url = "/blog/%s/delete/" % self.slug
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArticleIndexViewShould(TestCase):
    def _generate_articles(self, count=1):
        from apps.blog.models import Article
        articles = []
        for i in range(count):
            title = "Test article %s" % i
            slug  = "testarticle%s" % i
            content = "Test content for article %s" % i
            published = True
            articles.append(Article.objects.create(title=title, slug=slug,
                                                   content=content, published=published))
        return articles

    def testBePaginated(self):
        self._generate_articles(6)
        response = self.client.get("/blog/")
        self.assertEqual(len(response.context_data['article_list']), 4)

    def testOnlyShowPublishedPages(self):
        articles = self._generate_articles(3)
        articles[0].published = False
        articles[0].save()
        response = self.client.get("/blog/")
        self.assertEqual(len(response.context_data['article_list']), 2)

class ArticleUnpublishedIndexViewShould(TestCase):
    def _generate_articles(self, count=1):
        from apps.blog.models import Article
        articles = []
        for i in range(count):
            title = "Test article %s" % i
            slug  = "testarticle%s" % i
            content = "Test content for article %s" % i
            published = False
            articles.append(Article.objects.create(title=title, slug=slug,
                                                   content=content, published=published))
        return articles

    def testRequireLogin(self):
        url = "/blog/.unpublished/"
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=%s" % url)

    def testBePaginated(self):
        _create_user_and_login(self.client)
        self._generate_articles(6)
        response = self.client.get("/blog/.unpublished/")
        self.assertEqual(len(response.context_data['article_list']), 4)

    def testOnlyShowUnpublishedPages(self):
        _create_user_and_login(self.client)
        articles = self._generate_articles(3)
        articles[0].published = True
        articles[0].save()
        response = self.client.get("/blog/.unpublished/")
        self.assertEqual(len(response.context_data['article_list']), 2)

class ArticleDetailViewShould(TestCase):
    slug = "testslug"

    def testBeViewableWithoutLoginIfArticleIsPublished(self):
        article = _get_article(slug=self.slug)
        article.published = True
        article.save()
        url = "/blog/%s/" % self.slug
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRequireLoginIfArticleIsNotPublished(self):
        article = _get_article(slug=self.slug)
        article.published = False
        article.save()
        url = "/blog/%s/" % self.slug
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next=%s" % url)

