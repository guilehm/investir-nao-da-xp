from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('players/search/', views.player_search, name='player-search'),
    path('players/<str:username>/', views.player_detail, name='player-detail'),
    path(
        'players/<str:username>/season/<str:season_name>/',
        views.player_detail_by_season,
        name='player-detail-by-season'
    ),
]
