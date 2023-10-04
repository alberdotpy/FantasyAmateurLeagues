# leagues/forms.py
from django import forms
from core.models import UserPrediction, Team, Match


class UserPredictionForm(forms.ModelForm):
    class Meta:
        model = UserPrediction
        fields = ['prediction_team1', 'prediction_team2']

    def __init__(self, *args, team1_name=None, team2_name=None, **kwargs):
        super(UserPredictionForm, self).__init__(*args, **kwargs)
        if team1_name:
            self.fields['prediction_team1'].label = team1_name
        if team2_name:
            self.fields['prediction_team2'].label = team2_name


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        team_choices = kwargs.pop('team_choices', None)
        super(MatchForm, self).__init__(*args, **kwargs)
        if team_choices is not None:
            self.fields['team1'].queryset = team_choices
            self.fields['team2'].queryset = team_choices

    class Meta:
        model = Match
        fields = ['team1', 'team2', 'match_date']
        widgets = {
            'match_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MatchResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['result_team1', 'result_team2']

    def __init__(self, *args, team1_name=None, team2_name=None, **kwargs):
        super(MatchResultForm, self).__init__(*args, **kwargs)
        if team1_name:
            self.fields['result_team1'].label = team1_name
        if team2_name:
            self.fields['result_team2'].label = team2_name
