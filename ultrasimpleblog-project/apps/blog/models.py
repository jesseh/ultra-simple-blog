from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel

class Article(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.BooleanField()
    published_date = models.DateTimeField(blank=True, null=True,
            help_text="The published date is set automatically when this is first published.")

    def clean(self, *args, **kwargs):
        """
        Set the publish date before saving and keep the slug unique.
        """
        if self.published and not self.published_date:
            self.published_date = datetime.now()

    @models.permalink
    def get_absolute_url(self):
        return('article_view', (self.slug,))


