from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from . import custom_validators
from django.core.validators import MaxValueValidator, MinValueValidator


class Poll(models.Model):
	title = models.CharField('Заголовок', max_length=100, validators=[custom_validators.forbidden_words])
	description = models.CharField('Описание', max_length=100, blank=True, null=True, validators=[custom_validators.forbidden_words])
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	created = models.DateTimeField('Время создания', auto_now_add=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=('title', 'user'), name="unique_poll" )]

	def __str__(self):
		length = 50
		return self.title if len(self.title) < length else self.title[:length] + '…'

	def get_absolute_url(self):
		return reverse('poll_page', kwargs={"poll_pk": self.pk})

	@property
	def number_of_choices(self):
		return self.choice_set.count()

	@property
	def number_of_votes(self):
		return self.vote_set.count()

	@property
	def number_of_comments(self):
		return self.comment_set.count()

	@property
	def number_of_ratings(self):
		return self.rating_set.count()

	@property
	def average_rating(self):
		return self.rating_set.aggregate(Avg('value', default=0))['value__avg']

class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	text = models.CharField('', max_length=100, validators=[custom_validators.forbidden_words])

	class Meta:
		constraints = [models.UniqueConstraint(fields=('poll', 'text'), name="unique_choice" )]

	def __str__(self):
		length = 50
		return self.text if len(self.text) < length else self.text[:length] + '…'

	@property
	def number_of_votes(self):
		return self.vote_set.count()

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=('user', 'poll'), name="unique_vote" )]

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	created = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=('user', 'poll'), name="unique_rating" )]

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	text = models.CharField('Текст', max_length=100, validators=[custom_validators.forbidden_words])
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		length = 50
		return self.text if len(self.text) < length else self.text[:length] + '…'
