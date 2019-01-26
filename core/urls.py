from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('player/search/', views.player_search, name='player-search'),
    path('player/<str:username>/', views.player_detail, name='player-detail'),
    path(
        'player/<str:username>/season/<int:season_number>/',
        views.player_detail_by_season,
        name='player-detail-by-season',
    ),
    path('item/list/', views.item_list, name='item-list'),
    path('chart/list/', views.chart_list, name='chart-list'),
]
