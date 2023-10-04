# leagues/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('<int:league_id>/', views.league_ranking, name='league'),
    path('<int:league_id>/positions/', views.league_positions, name='league_positions'),
    path('<int:league_id>/predictions/', views.league_predictions, name='league_predictions'),
    path('<int:league_id>/add_team/', views.add_team, name='add_team'),
    path('<int:league_id>/add_match/', views.add_match, name='add_match'),
    path('<int:league_id>/create_prediction/<int:match_id>/', views.create_prediction, name='create_prediction'),
    path('<int:league_id>/edit_prediction/<int:match_id>/', views.edit_prediction, name='edit_prediction'),
    path('<int:league_id>/delete_prediction/<int:match_id>/', views.delete_prediction, name='delete_prediction'),
    path('<int:league_id>/edit_match_result/<int:match_id>/', views.edit_match_result, name='edit_match_result'),
    path('participate/requests/<int:league_id>/', views.participation_requests, name='participate_requests'),
    path('participate/accept/<int:league_id>/<int:user_id>/', views.accept_participation, name='accept_participation'),
    path('participate/reject/<int:league_id>/<int:user_id>/', views.reject_participation, name='reject_participation'),
    path('request_participation/<int:league_id>/', views.request_participation, name='request_participation'),
]
