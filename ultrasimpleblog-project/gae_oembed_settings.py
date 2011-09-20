"""
Add in index for a text field.

Based on http://www.allbuttonspressed.com/blog/django/2010/07/Managing-per-field-indexes-on-App-Engine
"""

from oembed.models import StoredOEmbed

FIELD_INDEXES = {
    StoredOEmbed: {'indexed': ['match']},
}

