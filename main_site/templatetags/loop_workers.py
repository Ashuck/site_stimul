from django import template

register = template.Library()


@register.filter(name="get_pack")
def get_pack(items, step):
    for i in range(0, len(items), step):

        yield items[i:i+step] 