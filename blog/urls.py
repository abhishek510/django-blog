from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('',HomeView.as_view(),name='home-page'),
    path('create_blog/',CreateBlogView.as_view(success_url='/'), name='create-blog'),
    path('blog/<int:pk>/',BlogView,name='blog-details'),
    # path('blog_up/<int:pk>/',BlogUpView,name='blog-details-up'),
    path('home/',dashboard,name='dashboard123'),
    path('top/',top_blogs,name='top-blogs'),
    path('dashboard/',ViewDashboard.as_view(),name='dashboard'),
    path('blog/<int:pk>/comment/',AddComment,name='add_comment_to_blog'),
    path('blog/<int:pk>/add_like/',add_like,name='add_like'),
    path('blog/<int:pk>/add_dislike/',add_dislike,name='add_dislike')
]