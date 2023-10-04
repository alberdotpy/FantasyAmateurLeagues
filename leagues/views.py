# leagues/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import League
from core.models import UserPrediction, Match, Team, Membership, User, Sport
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, IntegerField, Q, F
from django.contrib import messages
from .forms import UserPredictionForm, TeamForm, MatchForm, MatchResultForm
from operator import itemgetter
from datetime import timedelta, datetime


def calculate_score(sport, prediction, match):
    if sport.name == "Football":
        if (
            match.result_team1 is not None
            and match.result_team2 is not None
            and prediction.prediction_team1 == match.result_team1
            and prediction.prediction_team2 == match.result_team2
        ):
            return 100
        elif (
            match.result_team1 is not None
            and match.result_team2 is not None
            and (
                (prediction.prediction_team1 > prediction.prediction_team2 and match.result_team1 > match.result_team2)
                or (prediction.prediction_team1 < prediction.prediction_team2 and match.result_team1 < match.result_team2)
            )
        ):
            return 50
        elif (
            match.result_team1 is not None
            and match.result_team2 is not None
            and (
                prediction.prediction_team1 == prediction.prediction_team2
                and match.result_team1 == match.result_team2
            )
        ):
            return 60
        else:
            return 0
    elif sport.name == "Basketball":
        if (
            match.result_team1 is not None
            and match.result_team2 is not None
            and prediction.prediction_team1 == match.result_team1
            and prediction.prediction_team2 == match.result_team2
        ):
            return 300
        elif (
            match.result_team1 is not None
            and match.result_team2 is not None
            and (
                (prediction.prediction_team1 > prediction.prediction_team2 and match.result_team1 > match.result_team2)
                or (prediction.prediction_team1 < prediction.prediction_team2 and match.result_team1 < match.result_team2)
            )
        ):
            return 50
        elif (
            match.result_team1 is not None
            and match.result_team2 is not None
            and (
                prediction.prediction_team1 == prediction.prediction_team2
                and match.result_team1 == match.result_team2
            )
        ):
            return 150
        else:
            return 10
    else:
        return 0


@login_required
def league_positions(request, league_id):
    league = get_object_or_404(League, id=league_id)
    teams = Team.objects.filter(league=league)
    is_creator = league.creator == request.user
    team_matches_data = []
    for team in teams:
        # Get all matches for the current team in the league
        team_matches = Match.objects.filter(league=league, team1=team) | Match.objects.filter(league=league, team2=team)

        # Initialize counters for wins, losses, draws, and other statistics
        wins = 0
        losses = 0
        draws = 0
        goals_scored = 0
        goals_conceded = 0
        matches_played = 0

        # Loop through the matches and calculate statistics
        for match in team_matches:
            if match.result_team1 is not None and match.result_team2 is not None:
                matches_played += 1
                if team == match.team1:
                    goals_scored += match.result_team1
                    goals_conceded += match.result_team2
                    if match.result_team1 > match.result_team2:
                        wins += 1
                    elif match.result_team1 < match.result_team2:
                        losses += 1
                    else:
                        draws += 1
                elif team == match.team2:
                    goals_scored += match.result_team2
                    goals_conceded += match.result_team1
                    if match.result_team2 > match.result_team1:
                        wins += 1
                    elif match.result_team2 < match.result_team1:
                        losses += 1
                    else:
                        draws += 1

        # Create a dictionary for the team's match data
        team_match_data = {
            'team': team,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'matches_played': matches_played,
            'points': wins * 3 + draws,
        }
        team_matches_data.append(team_match_data)

        team_matches_data.sort(key=itemgetter('points'), reverse=True)

    context = {
        'league': league,
        'team_matches_data': team_matches_data,
        'user': request.user,
        'is_creator': is_creator,
    }
    return render(request, 'leagues/league_positions.html', context)


@login_required
def league_predictions(request, league_id):
    league = get_object_or_404(League, id=league_id)
    is_creator = league.creator == request.user
    user_predictions = UserPrediction.objects.filter(user=request.user, match__league=league)
    predictions_data = []
    matches_with_predictions = []
    matches_without_predictions = []
    current_date = datetime.now().date()

    all_matches = Match.objects.filter(league=league).order_by('-match_date')

    for match in all_matches:
        user_prediction = user_predictions.filter(match=match).first()
        total_points = 0

        if user_prediction:
            score = calculate_score(league.sport, user_prediction, match)
            total_points += score

            if score > 10:
                status = 'Win'
            else:
                if match.result_team1 is None and match.result_team2 is None:
                    status = 'Not Played'
                else:
                    status = 'Lose'

            predictions_data.append({
                'match': match,
                'result_team1': match.result_team1,
                'result_team2': match.result_team2,
                'prediction_team1': user_prediction.prediction_team1,
                'prediction_team2': user_prediction.prediction_team2,
                'status': status,
                'points': score,
            })
            matches_with_predictions.append(match)
        else:
            matches_without_predictions.append(match)

    one_day_before_match_dates = {}
    for match in all_matches:
        one_day_before_match_dates[match.id] = match.match_date - timedelta(days=1)

    context = {
        'league': league,
        'predictions_data': predictions_data,
        'matches_with_predictions': matches_with_predictions,
        'matches_without_predictions': matches_without_predictions,
        'user': request.user,
        'is_creator': is_creator,
        'one_day_before_match_dates': one_day_before_match_dates,
        'current_date': current_date,
    }

    return render(request, 'leagues/league_predictions.html', context)


@login_required
def league_ranking(request, league_id):
    league = get_object_or_404(League, id=league_id)
    is_creator = league.creator == request.user
    league_members = league.members.all()
    members_data = []

    for member in league_members:
        member_predictions = UserPrediction.objects.filter(user=member, match__league=league)
        total_points = 0
        correct_predictions = 0
        wrong_predictions = 0

        for prediction in member_predictions:
            if prediction.match.result_team1 is not None and prediction.match.result_team2 is not None:
                # Calculate the score based on sport type and prediction details
                score = calculate_score(league.sport, prediction, prediction.match)
                total_points += score

                if score > 10:
                    correct_predictions += 1
                else:
                    wrong_predictions += 1

        members_data.append({
            'user': member,
            'total_points': total_points,
            'correct_predictions': correct_predictions,
            'wrong_predictions': wrong_predictions,
        })

    # Sort the ranking data in descending order of total points
    members_data.sort(key=lambda x: x['total_points'], reverse=True)

    context = {
        'league': league,
        'members_data': members_data,
        'user': request.user,
        'is_creator': is_creator,
    }

    return render(request, 'leagues/league_ranking.html', context)


@login_required
def request_participation(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    if request.user == league.creator or request.user in league.members.all() or request.user in league.pending_requests.all():
        # You can add a message here if needed
        return redirect('leagues')
    league.pending_requests.add(request.user)

    # You can add a success message here if needed
    return redirect('leagues')


@login_required
def accept_participation(request, league_id, user_id):
    league = get_object_or_404(League, pk=league_id)
    user = get_object_or_404(User, pk=user_id)
    if request.user != league.creator:
        # You can add an error message here if needed
        return redirect('leagues')
    league.pending_requests.remove(user)
    league.members.add(user)
    # Notify the user about their acceptance
    # You can add a success message here if needed
    return redirect('participate_requests', league_id=league_id)


@login_required
def reject_participation(request, league_id, user_id):
    league = get_object_or_404(League, pk=league_id)
    user = get_object_or_404(User, pk=user_id)
    if request.user != league.creator:
        # You can add an error message here if needed
        return redirect('leagues')
    league.pending_requests.remove(user)
    # Notify the user about their rejection
    # You can add a success message here if needed
    return redirect('participate_requests', league_id=league_id)


@login_required
def participation_requests(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    if request.user != league.creator:
        return redirect('leagues')
    pending_requests = league.pending_requests.all()
    return render(request, 'leagues/participation_requests.html', {'league': league, 'pending_requests': pending_requests})


@login_required
def create_prediction(request, league_id, match_id):
    league = get_object_or_404(League, id=league_id)
    match = get_object_or_404(Match, id=match_id)
    sport = get_object_or_404(Sport, name=league.sport)
    team1_name = match.team1.name
    team2_name = match.team2.name

    # Define the form variable with an initial value of None
    form = None

    if request.method == 'POST':
        form = UserPredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            prediction.match = match
            prediction.sport = sport
            prediction.league = league
            prediction.save()
            messages.success(request, 'Prediction saved successfully.')
            return redirect('league_predictions', league_id=league_id)
    else:
        # Check if the user has already made a prediction for this match
        existing_prediction = UserPrediction.objects.filter(user=request.user, match=match).first()
        if existing_prediction:
            # If a prediction exists, populate the form with the existing prediction data
            form = UserPredictionForm(instance=existing_prediction, team1_name=team1_name, team2_name=team2_name)
        else:
            # If no prediction exists, create an empty form with team names
            form = UserPredictionForm(team1_name=team1_name, team2_name=team2_name)

    context = {
        'match': match,
        'form': form,
        'league_id': league_id,
        'team1_name': team1_name,
        'team2_name': team2_name
    }

    return render(request, 'leagues/create_prediction.html', context)


@login_required
def delete_prediction(request, league_id, match_id):
    match = get_object_or_404(Match, id=match_id)
    prediction = UserPrediction.objects.filter(user=request.user, match=match).first()
    if prediction:
        if prediction.league.id == league_id:
            prediction.delete()
            messages.success(request, 'Prediction deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this prediction for this league.')
    else:
        messages.error(request, 'Prediction not found.')
    return redirect('league_predictions', league_id=league_id)


@login_required
def edit_prediction(request, league_id, match_id):
    league = get_object_or_404(League, id=league_id)
    match = get_object_or_404(Match, id=match_id)
    sport = get_object_or_404(Sport, name=league.sport)
    team1_name = match.team1.name
    team2_name = match.team2.name

    # Check if the user has already made a prediction for this match
    existing_prediction = UserPrediction.objects.filter(user=request.user, match=match).first()
    if not existing_prediction:
        messages.error(request, 'You cannot edit a prediction that does not exist.')
        return redirect('league_predictions', league_id=league_id)
    if request.method == 'POST':
        form = UserPredictionForm(request.POST, instance=existing_prediction)
        if form.is_valid():
            prediction = form.save()
            messages.success(request, 'Prediction edited successfully.')
            return redirect('league_predictions', league_id=league_id)
    else:
        form = UserPredictionForm(instance=existing_prediction, team1_name=team1_name, team2_name=team2_name)
    context = {
        'match': match,
        'form': form,
        'league_id': league_id,
        'team1_name': team1_name,
        'team2_name': team2_name,
        'edit_mode': True,
    }
    return render(request, 'leagues/create_prediction.html', context)


@login_required
def add_team(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.league_id = league_id
            team.sport = league.sport
            team.save()
            return redirect('league', league_id=league_id)
    else:
        form = TeamForm()

    context = {'form': form,
               'league_id': league_id
               }
    return render(request, 'leagues/add_team.html', context)


@login_required
def add_match(request, league_id):
    league = get_object_or_404(League, id=league_id)

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.league = league
            match.save()
            return redirect('league', league_id=league_id)
    else:
        # Create the MatchForm instance with filtered team choices
        team_choices = Team.objects.filter(league=league)
        form = MatchForm(team_choices=team_choices)

    context = {'form': form, 'league_id': league_id}
    return render(request, 'leagues/add_match.html', context)


@login_required
def edit_match_result(request, league_id, match_id):
    match = get_object_or_404(Match, id=match_id)
    team1_name = match.team1.name
    team2_name = match.team2.name
    if request.method == 'POST':
        form = MatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('league_predictions', league_id=league_id)
    else:
        form = MatchResultForm(instance=match, team1_name=team1_name, team2_name=team2_name)
    context = {
        'form': form,
        'league_id': league_id,
        'match_id': match_id,
        'match': match,
        'team1_name': team1_name,
        'team2_name': team2_name
    }
    return render(request, 'leagues/edit_match_result.html', context)