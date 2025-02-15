from django import template

register = template.Library()

@register.inclusion_tag('pagination.html')
def pagination(page_kwarg, page_obj):
	return {'page_kwarg': page_kwarg, 'page_obj': page_obj}
