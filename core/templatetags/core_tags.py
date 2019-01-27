from django import template

from core.forms import SearchForm

register = template.Library()


@register.inclusion_tag('tags/search_form.html')
def search_form():
    form = SearchForm()
    return {
        'form': form,
    }


@register.simple_tag(name='stat_filter')
def stat_filter(request, stats, data):
    modes = ['solo', 'duo', 'squad']
    mode = request.GET.get('mode', 'squad').lower()
    if mode not in modes:
        mode = 'squad'
    all_stats_data = list()
    for stat in stats:
        all_stats_data.append(getattr(stat, f'stats_{mode}')[f'{data}_{mode}'])
    return all_stats_data
