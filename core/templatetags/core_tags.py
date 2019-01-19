from django import template

from core.forms import SearchForm

register = template.Library()


@register.inclusion_tag('tags/search_form.html')
def search_form():
    form = SearchForm()
    return {
        'form': form,
    }
