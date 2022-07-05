from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('register', views.register_render),
    path('register/user', views.register_user),
    path('users/new', views.users_new),
    path('users/show/<user_id>', views.users_show),
    path('users/edit', views.users_edit),
    path('new/user', views.new_user),
    path('message/user', views.message_user),
    path('message/reply', views.message_reply),
    path('edit/user/information/<user_id>', views.edit_user_info),
    path('dashboard', views.dashboard),
    path('remove/user/<user_id>', views.remove_user),
    path('logout', views.logout),
]
