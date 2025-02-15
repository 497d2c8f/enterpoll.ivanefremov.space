from django.urls import path, include
from . import api_views


users_urls = [
	path("registration/", api_views.RegistrationAPIViewV1.as_view(), name="registration_api_v1"),
	path("login/", api_views.LoginAPIViewV1.as_view(), name="login_api_v1"),
	path("logout/", api_views.LogoutAPIViewV1.as_view(), name="logout_api_v1"),
	path("<int:user_pk>/profile/", api_views.ProfileAPIViewV1.as_view(), name="profile_api_v1"),
	path("<int:user_pk>/profile/poll_list/", api_views.UserPollListAPIViewV1.as_view(), name="user_poll_list_api_v1"),
	path("<int:user_pk>/profile/vote_list/", api_views.UserVoteListAPIViewV1.as_view(), name="user_vote_list_api_v1"),
	path("<int:user_pk>/profile/rating_list/", api_views.UserRatingListAPIViewV1.as_view(), name="user_rating_list_api_v1"),
	path("<int:user_pk>/profile/comment_list/", api_views.UserCommentListAPIViewV1.as_view(), name="user_comment_list_api_v1"),
	path("<int:user_pk>/profile/password_change/", api_views.PasswordChangeAPIViewV1.as_view(), name="password_change_api_v1"),
	path("<int:user_pk>/profile/delete/", api_views.DeleteAPIViewV1.as_view(), name="delete_user_api_v1"),
]


polls_urls = [
	path("list/", api_views.PollListAPIViewV1.as_view(), name="poll_list_api_v1"),
	path("create/", api_views.CreatePollAPIViewV1.as_view(), name="create_poll_api_v1"),
	path("<int:poll_pk>/", api_views.GetPollAPIViewV1.as_view(), name="get_poll_api_v1"),
	path("random/", api_views.GetRandomPollAPIViewV1.as_view(), name="get_random_poll_api_v1"),
	path("<int:poll_pk>/delete/", api_views.DeletePollAPIViewV1.as_view(), name="delete_poll_api_v1"),

	path("<int:poll_pk>/vote_list/", api_views.VoteListAPIViewV1.as_view(), name="vote_list_api_v1"),
	path("<int:poll_pk>/vote/", api_views.CreateVoteAPIViewV1.as_view(), name="create_vote_api_v1"),

	path("<int:poll_pk>/rating_list/", api_views.RatingListAPIViewV1.as_view(), name="rating_list_api_v1"),
	path("<int:poll_pk>/rate/", api_views.CreateRatingAPIViewV1.as_view(), name="create_rating_api_v1"),

	path("<int:poll_pk>/comment_list/", api_views.CommentListAPIViewV1.as_view(), name="comment_list_api_v1"),
	path("<int:poll_pk>/comment/", api_views.CreatePollCommentAPIViewV1.as_view(), name="create_comment_api_v1"),
]


votes_urls = [
	path("<int:vote_pk>/", api_views.GetVoteAPIViewV1.as_view(), name="get_vote_api_v1"),
	path("<int:vote_pk>/delete/", api_views.DeleteVoteAPIViewV1.as_view(), name="delete_vote_api_v1"),
]


ratings_urls = [
	path("<int:rating_pk>/", api_views.GetRatingAPIViewV1.as_view(), name="get_rating_api_v1"),
	path("<int:rating_pk>/delete/", api_views.DeleteRatingAPIViewV1.as_view(), name="delete_rating_api_v1"),
]


comments_urls = [
	path("<int:comment_pk>/", api_views.GetCommentAPIViewV1.as_view(), name="get_comment_api_v1"),
	path("<int:comment_pk>/delete/", api_views.DeleteCommentAPIViewV1.as_view(), name="delete_comment_api_v1"),
]


urlpatterns = [
	path("main_page/", api_views.MainPageAPIViewV1.as_view(), name="main_page_api_v1"),
	path('users/', include(users_urls)),
	path('polls/', include(polls_urls)),
	path('votes/', include(votes_urls)),
	path('ratings/', include(ratings_urls)),
	path('comments/', include(comments_urls)),
]
