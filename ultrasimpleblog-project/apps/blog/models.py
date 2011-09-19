from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel

class Article(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # Unique is ignored in non-rel. Enforced at save.
    content = models.TextField()
    published = models.BooleanField()
    published_date = models.DateTimeField(blank=True, null=True,
            help_text="Is set automatically when first published.")

    def validate_unique(self, *args, **kwargs):
        """
        Directly validate that the slug is unique.
        @@@ Is this the right way to do a uniqueness check in nonrel?
        """
        if self.id is None:
            try:
                article = Article.objects.get(slug=self.slug)
                raise ValidationError("The slug '%s' is already in use. Please make it unique." % self.slug)
            except Article.DoesNotExist:
                pass

    def clean(self, *args, **kwargs):
        """
        Set the publish date before saving.
        """
        if self.published and not self.published_date:
            self.published_date = datetime.now()
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return('article_view', (self.slug,))


