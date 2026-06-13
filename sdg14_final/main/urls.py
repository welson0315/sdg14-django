from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('articles/<int:article_id>/comment/', views.add_comment, name='add_comment'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    path('profile/', views.profile, name='profile'),

    path('report/', views.report_pollution, name='report_pollution'),
    path('reports/', views.report_list, name='report_list'),
]