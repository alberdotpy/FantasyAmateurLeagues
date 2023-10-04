from django.contrib import admin
from .models import League, Membership, Sport, Team, TeamMembership, Match, UserPrediction


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'country', 'creator')
    list_filter = ('sport', 'country')
    search_fields = ('name', 'creator__username')


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'league', 'date_joined')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'sport')
    list_filter = ('league',)
    search_fields = ('name',)


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'date_joined')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('league', 'team1', 'team2', 'match_date', 'result_team1', 'result_team2')
    list_filter = ('league',)
    search_fields = ('team1__name', 'team2__name')


@admin.register(UserPrediction)
class UserPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'league', 'sport', 'match', 'prediction_team1', 'prediction_team2')
