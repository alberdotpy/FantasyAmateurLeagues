# leagues/templatetags/custom_filters.py

from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='user_predictions')
def user_predictions(predictions, user):
    return predictions.filter(user=user)


@register.filter(name='sum_values')
def sum_values(value):
    return sum(value)


@register.filter
def get_prediction_by_match(predictions, match_id):
    try:
        return next(prediction for prediction in predictions if prediction.match.id == match_id)
    except StopIteration:
        return None


@register.filter
def can_edit_match(match_date):
    today = match_date.today()
    one_day_before = today - timedelta(days=1)
    return match_date > one_day_before