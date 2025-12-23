"""leetcode_visualizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from . import compare

urlpatterns = [
    # Profile resources
    path('', views.profile_form, name='index'),  # Landing page with profile form
    path('profiles/', views.profile_form, name='profile_form'),  # Profile search form
    path('profiles/<str:username>/', views.profile_detail, name='profile_detail'),  # Individual profile details
    
    # Comparison resources
    path('compare/', compare.comparison_form, name='comparison_form'),  # Comparison form
    path('compare/<str:username1>/<str:username2>/', compare.comparison_detail, name='comparison_detail'),  # Specific comparison
]
