from django.db import models
from django.contrib.auth.models import User


class Sport(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_leagues')
    members = models.ManyToManyField(User, through='Membership')
    country = models.CharField(max_length=255, default='France')
    date_created = models.DateTimeField(auto_now_add=True)
    pending_requests = models.ManyToManyField(User, related_name='pending_league_requests')

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)


class Team(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='TeamMembership')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)


class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, related_name='matches_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='matches_as_team2', on_delete=models.CASCADE)
    match_date = models.DateField()
    result_team1 = models.PositiveIntegerField(null=True, blank=True)
    result_team2 = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.team1} vs. {self.team2}"


class UserPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    prediction_team1 = models.PositiveIntegerField()
    prediction_team2 = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}'s prediction for {self.match}"
