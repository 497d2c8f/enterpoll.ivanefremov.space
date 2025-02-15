from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


class IsUserOrAdmin(permissions.BasePermission):

	code = 'forbidden'

	def has_object_permission(self, request, view, obj):
		requested_user = User.objects.get(pk=view.kwargs[view.lookup_url_kwarg])
		self.message = _(f'The action is available to the user ({requested_user.username}) or the admin.')
		return requested_user == request.user or request.user.is_staff

	def has_permission(self, request, view):
		requested_user = get_object_or_404(User, pk=view.kwargs['user_pk'])
		self.message = _(f'The action is available to the user ({requested_user.username}) or the admin.')
		return request.user == requested_user or request.user.is_staff

class IsUserOnly(permissions.BasePermission):

	code = 'forbidden'

	def has_object_permission(self, request, view, obj):
		requested_user = User.objects.get(pk=view.kwargs[view.lookup_url_kwarg])
		self.message = _(f'The action is available only to the user ({requested_user.username}).')
		return requested_user == request.user


class IsAuthorOrAdmin(permissions.BasePermission):

	code = 'forbidden'

	def has_object_permission(self, request, view, obj):
		self.message = _(f'The action is available only to the user ({obj.user.username}) or the admin.')
		return obj.user == request.user or request.user.is_staff
