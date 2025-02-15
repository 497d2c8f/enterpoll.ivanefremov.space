from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from ..models import Poll, Choice, Vote, Comment, Rating
import random
import redis
import pickle
from rest_framework import (
	views as drf_views,
	generics as drf_generics,
	response as drf_response,
	permissions as drf_permissions
)
from .api_permissions import (
	IsAuthorOrAdmin,
	IsUserOrAdmin,
	IsUserOnly
)
from .api_serializers import (
	UserSerializer,
	PollSerializer,
	CommentSerializer,
	VoteSerializer,
	RatingSerializer,
	ChoiceSerializer
)


class RegistrationAPIViewV1(drf_generics.CreateAPIView):

	serializer_class = UserSerializer


class ProfileAPIViewV1(drf_generics.RetrieveAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()


class UserPollListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = PollSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.poll_set.order_by('-created')
		return queryset


class UserVoteListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = VoteSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.vote_set.order_by('-created')
		return queryset


class UserRatingListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = RatingSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.rating_set.order_by('-created')
		return queryset


class UserCommentListAPIViewV1(drf_generics.ListAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = CommentSerializer

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user_pk'])
		queryset = user.comment_set.order_by('-created')
		return queryset


class DeleteAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [IsUserOrAdmin]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()


class LoginAPIViewV1(drf_views.APIView):

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
		response_dict = {'session_key': request.session.session_key, 'X-CSRFTOKEN': request.META['CSRF_COOKIE']}
		return drf_response.Response(response_dict)


class LogoutAPIViewV1(drf_views.APIView):

	def post(self, request, *args, **kwargs):
		logout(request)
		message = 'Failed logout.' if request.user.is_authenticated else 'Successful logout.'
		return drf_response.Response({'message': message})


class PasswordChangeAPIViewV1(drf_generics.UpdateAPIView):

	permission_classes = [IsUserOnly]
	serializer_class = UserSerializer
	lookup_url_kwarg = 'user_pk'
	queryset = User.objects.all()

	def partial_update(self, request, *args, **kwargs):
		validate_password(request.data['new_password'])
		requested_user = self.get_object()
		authenticated_user = authenticate(username=requested_user.username, password=request.data['current_password'])
		if authenticated_user:
			authenticated_user.set_password(request.data['new_password'])
			authenticated_user.save()
		serializer = self.get_serializer(authenticated_user)
		return drf_response.Response({'message': 'Password successfully changed.', **serializer.data})


class MainPageAPIViewV1(drf_views.APIView):

	def get(self, request, *args, **kwargs):
		try:
			r = redis.Redis()
			main_page_context_from_redis = r.get('main_page_context')
			if main_page_context_from_redis:
				main_page_context = pickle.loads(main_page_context_from_redis)
			else:
				polls = Poll.objects.all()
				main_page_context = {
					'most_popular_polls': sorted(polls, key=(lambda poll: poll.number_of_votes), reverse=True)[0:3],
					'highly_rated_polls': sorted(polls, key=(lambda poll: poll.average_rating), reverse=True)[0:3],
					'latest_polls': polls.order_by('-created')[0:3]
				}
				r.setex('main_page_context', 10, pickle.dumps(main_page_context))
		except redis.exceptions.ConnectionError:
			polls = Poll.objects.all()
			main_page_context = {
				'most_popular_polls': sorted(polls, key=(lambda poll: poll.number_of_votes), reverse=True)[0:3],
				'highly_rated_polls': sorted(polls, key=(lambda poll: poll.average_rating), reverse=True)[0:3],
				'latest_polls': polls.order_by('-created')[0:3]
			}
		response_dict = {
			'most_popular_polls_pk': [poll.pk for poll in main_page_context['most_popular_polls']],
			'highly_rated_polls_pk': [poll.pk for poll in main_page_context['highly_rated_polls']],
			'latest_polls_pk': [poll.pk for poll in main_page_context['latest_polls']]
		}
		return drf_response.Response(response_dict)


class PollListAPIViewV1(drf_generics.ListAPIView):

	queryset = Poll.objects.order_by('-created')
	serializer_class = PollSerializer


class CreatePollAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = PollSerializer


class GetPollAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	lookup_url_kwarg = 'poll_pk'


class GetRandomPollAPIViewV1(drf_views.APIView):

	def get(self, request, *args, **kwargs):
		poll_pk_list = Poll.objects.values_list('pk', flat=True)
		poll = get_object_or_404(Poll, pk=random.choice(poll_pk_list))
		serializer = PollSerializer(poll)
		return drf_response.Response(serializer.data)


class DeletePollAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]
	queryset = Poll.objects.all()
	lookup_url_kwarg = 'poll_pk'


class VoteListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = VoteSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.vote_set.order_by('-created')
		return queryset


class CreateVoteAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = VoteSerializer


class GetVoteAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'


class DeleteVoteAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	lookup_url_kwarg = 'vote_pk'


class RatingListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = RatingSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.rating_set.order_by('-created')
		return queryset


class CreateRatingAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = RatingSerializer


class GetRatingAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	lookup_url_kwarg = 'rating_pk'


class DeleteRatingAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]
	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	lookup_url_kwarg = 'rating_pk'


class CommentListAPIViewV1(drf_generics.ListAPIView):

	serializer_class = CommentSerializer

	def get_queryset(self):
		poll = Poll.objects.get(pk=self.kwargs['poll_pk'])
		queryset = poll.comment_set.order_by('-created')
		return queryset


class CreatePollCommentAPIViewV1(drf_generics.CreateAPIView):

	permission_classes = [drf_permissions.IsAuthenticated]
	serializer_class = CommentSerializer


class GetCommentAPIViewV1(drf_generics.RetrieveAPIView):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'


class DeleteCommentAPIViewV1(drf_generics.DestroyAPIView):

	permission_classes = [drf_permissions.IsAuthenticated, IsAuthorOrAdmin]
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_url_kwarg = 'comment_pk'
