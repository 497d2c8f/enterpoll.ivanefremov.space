from django.contrib.auth.models import User
from enterpoll.models import Poll, Choice, Vote, Rating, Comment
import wonderwords
import random

NUMBER_OF_POLLS = 100
NUMBER_OF_USERS = 98

User.objects.all().delete()
Poll.objects.all().delete()
Choice.objects.all().delete()
Vote.objects.all().delete()
Rating.objects.all().delete()
Comment.objects.all().delete()

random_word = wonderwords.RandomWord()
random_sentence = wonderwords.RandomSentence()

random_usernames = [rw + str(random.randint(1, 100)) for rw in random_word.random_words(NUMBER_OF_USERS, word_min_length=5)]
for i in range(NUMBER_OF_USERS - 1):
	random_username = random_usernames[i]
	User.objects.create_user(username=random_username, password='Helloworld1')
	print('user created')
User.objects.create_user(username='User1', password='Helloworld1')
User.objects.create_superuser(username='admin', password='admin')

users = User.objects.all()

random_words_and_sentences_methods = [
	random_word.word,
	random_sentence.sentence,
	random_sentence.bare_bone_with_adjective,
	random_sentence.simple_sentence,
	random_sentence.bare_bone_sentence,
]

for _ in range(NUMBER_OF_POLLS):

	random_title = random.choice(random_words_and_sentences_methods)()
	random_description = random.choice(random_words_and_sentences_methods)()
	random_user = random.choice(users)
	poll = Poll.objects.create(title=random_title, description=random_description, user=random_user)
	print('poll created')

	random_number_of_choices = random.randint(2, 10)
	for _ in range(random_number_of_choices):
		random_choice_text = random.choice(random_words_and_sentences_methods)()
		Choice.objects.create(poll=poll, text=random_choice_text)
		print('choice created')

	random_number_of_votes = random.randint(0, 100)
	for _ in range(random_number_of_votes):
		random_user = random.choice(users)
		random_choice = random.choice(Choice.objects.filter(poll=poll))
		try:
			vote = Vote.objects.get(user=random_user, poll=poll)
			vote.choice = random_choice
			vote.save()
		except:
			Vote.objects.create(user=random_user, poll=poll, choice=random_choice)
		print('vote created')

	random_number_of_ratings = random.randint(0, 100)
	for _ in range(random_number_of_ratings):
		random_user = random.choice(users)
		random_value = random.randint(random.randint(1, 4), 5)
		try:
			rating = Rating.objects.get(user=random_user, poll=poll)
			rating.value = random_value
			rating.save()
		except:
			Rating.objects.create(user=random_user, poll=poll, value=random_value)
		print('rating created')

	random_number_of_comments = random.randint(0, 10)
	for _ in range(random_number_of_comments):
		random_user = random.choice(users)
		random_comment_text = random.choice(random_words_and_sentences_methods)()
		Comment.objects.create(user=random_user, poll=poll, text=random_comment_text)
		print('comment created')
