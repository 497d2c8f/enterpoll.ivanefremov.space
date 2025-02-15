from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Poll, Choice, Comment


class CustomUserAdmin(UserAdmin):

	has_add_permission = lambda *args: False
	readonly_fields = [
		'username',
		'password',
		'first_name',
		'last_name',
		'email',
		'is_active',
		'last_login',
		'date_joined'
	]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

	list_display = ['title', 'user', 'created']
	fields = [
		'title',
		'description',
		'choices',
		'user',
		(
			'created',
			'number_of_votes',
			'average_rating'
		)
	]
	readonly_fields = [
		'title',
		'description',
		'choices',
		'user',
		'created',
		'number_of_votes',
		'average_rating',
	]
	search_fields = ['title', 'description', 'user__username']
	search_help_text = 'Поиск по заголовку, описанию или автору.'
	list_filter = ['created']
	list_per_page = 10
	list_max_show_all = 100
	ordering = ['-created']
	show_facets = admin.ShowFacets.ALWAYS
	has_add_permission = lambda *args: False
	has_change_permission = lambda *args: False

	@admin.display(description='Варианты ответа (количество голосов)')
	def choices(self, instance):
		choices_and_votes = sorted(
			(
				(c.text, c.number_of_votes) for c in instance.choice_set.all()
			),
			key=lambda item: item[1],
			reverse=True
		)
		text = '\n'.join(f'{c} ({v})' for c, v in choices_and_votes)
		return text
