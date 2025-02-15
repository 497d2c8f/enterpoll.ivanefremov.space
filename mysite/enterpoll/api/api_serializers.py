from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ..models import Poll, Choice, Vote, Rating, Comment
from .. import custom_validators
from rest_framework import exceptions as drf_exceptions
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'username', 'password']
#		read_only_fields = ['pk', 'number_of_votes']

	def create(self, validated_data):
		validate_password(validated_data['password'])
		user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
		return user


class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = ['pk', 'text', 'number_of_votes']
		read_only_fields = ['pk', 'number_of_votes']


class PollSerializer(serializers.ModelSerializer):
	choice_set = ChoiceSerializer(many=True, min_length=2, max_length=10)

	class Meta:
		model = Poll
		fields = [
			'pk',
			'title',
			'description',
			'number_of_choices',
			'choice_set',
			'number_of_votes',
			'number_of_ratings',
			'average_rating',
			'number_of_comments',
			'user',
			'created',
		]
		read_only_fields = [
			'pk',
			'number_of_choices',
			'number_of_votes',
			'number_of_ratings',
			'average_rating',
			'number_of_comments',
			'user',
			'created',
		]

	def create(self, validated_data):
		poll = Poll.objects.create(
			title=validated_data['title'],
			description=validated_data['description'],
			user=self.context['request'].user
		)
		choices = [Choice(poll=poll, text=choice['text']) for choice in validated_data['choice_set']]
		try:
			Choice.objects.bulk_create(choices)
		except Exception as e:
			poll.delete()
			raise drf_exceptions.APIException(detail=_(str(e)))
		return poll


class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ['pk', 'user', 'poll', 'choice', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		user = self.context['request'].user
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		vote, _ = Vote.objects.update_or_create(user=user, poll=poll, defaults={'choice': validated_data['choice']})
		return vote


class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = ['pk', 'user', 'poll', 'value', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		user = self.context['request'].user
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		rating, _ = Rating.objects.update_or_create(user=user, poll=poll, defaults={'value': validated_data['value']})
		return rating


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['pk', 'user', 'poll', 'text', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		comment = Comment.objects.create(user=self.context['request'].user, poll=poll, text=validated_data['text'])
		return comment
