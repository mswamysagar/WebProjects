from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from authentication.models import CustomUser
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
# import asyncio
# import aiohttp

def get_tokens_for_user(user: CustomUser):
    token = RefreshToken.for_user(user)
    token["full_name"] = user.full_name
    token["email"] = user.email
    token["mobile"] = user.mobile
    token['user_type'] = user.user_type
    # token['uuid'] = user.uuid
    # print('expiry time', token.access_token['exp'])
    return {
        'refresh': str(token),
        'access': str(token.access_token),
        'expiry_time': (token.access_token['exp'] * 1000)
    }

def datetime_fmt(datetime_obj=None) -> str:
    return datetime.strftime(datetime_obj, "%d %b %y %I:%M %p")
    
def handle_exception(exception: Exception):
    message = "Some Exception was thrown."
    if len(exception.args):
        message = exception.args[0]
    return message

def handle_pagination(paginator: PageNumberPagination):
    return_dict = {
        "page": 1,
        "next_page": 0,
        "prev_page": 0,
    }
    return_dict['page'] = paginator.page.number
    return_dict['next_page'] =  paginator.get_next_link() 
    return_dict['prev_page'] =  paginator.get_previous_link() 
    return return_dict

def copy_with_specific_properties(source_dict, properties):
    return {key: source_dict[key] for key in properties if key in source_dict}

def timefield_to_minutes(time_string: datetime.time):
    hours, minutes, seconds = time_string.hour, time_string.minute, time_string.second
    total_minutes = minutes
    return total_minutes

def get_filered_dates(period: str):
    context = {
        "from": None,
        "to": None,
    }
    today = timezone.datetime.today()
    match period:
        case 'this_week':
            context['from'] = start_of_week = today - timedelta(days=today.weekday())
            context['to'] = end_of_week = start_of_week + timedelta(days=6)
        case 'last_week':
            context['from'] = start_of_week = today - timedelta(days=today.weekday() + 7)
            context['to'] = end_of_week = start_of_week + timedelta(days=6)
        case 'this_month':
            context["from"] = start_of_month = today.replace(day=1)
            next_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1)
            context["to"] = end_of_month = next_month - timedelta(days=1)
        case 'last_month':
            start_of_month = today.replace(day=1)
            context['to'] = last_day_of_last_month = start_of_month - timedelta(days=1)
            context["from"] = first_day_of_last_month = last_day_of_last_month.replace(day=1)
        case 'last_30':
            thirty_days_ago = today - timedelta(days=30)
            context['from'] = beginning_date = thirty_days_ago.replace(day=1)
            context['to'] = ending_date = today
        case 'last_3_months':
            three_months_ago = today - timedelta(days=90)
            context['from'] = beginning_date = three_months_ago.replace(day=1)
            context['to'] = ending_date = today
    return context
