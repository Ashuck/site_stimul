from django import template
from main_site.forms import FeedBackForm

register = template.Library()


@register.simple_tag
def test():
  return FeedBackForm().as_p()