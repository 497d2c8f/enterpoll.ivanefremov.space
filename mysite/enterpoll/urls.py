from django.urls import path, include
from . import views


users_urls = [
	path("registration/", views.RegistrationView.as_view(), name="registration"),
	path("<int:user_pk>/profile/delete_user/", views.DeleteView.as_view(), name="delete_user"),
	path("login/", views.LoginView.as_view(), name="login"),
	path("logout/", views.logout, name="logout"),
	path("<int:user_pk>/profile/", views.ProfileView.as_view(), name="profile"),
	path("<int:user_pk>/profile/password_change", views.PasswordChangeView.as_view(), name="password_change"),
	path("<int:user_pk>/profile/password_change_done", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]


polls_urls = [
	path("list/", views.PollsListView.as_view(), name="poll_list"),
	path("create/", views.CreatePollView.as_view(), name="create_poll"),
	path("<int:poll_pk>/", views.PollPageView.as_view(), name="poll_page"),
	path("random/", views.RandomPollPageView.as_view(), name="random_poll_page"),
]


urlpatterns = [
	path("", views.MainPageView.as_view(), name="main_page"),
	path('users/', include(users_urls)),
	path('polls/', include(polls_urls)),
]
