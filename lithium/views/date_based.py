import datetime, time

from django.db.models.fields import DateTimeField
from django.http import Http404
from django.views.generic import list_detail

def archive_index(request, queryset, date_field, allow_future=False, **kwargs):
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: datetime.datetime.now()})
    queryset = queryset.order_by('-' + date_field)
    
    return list_detail.object_list(request, queryset=queryset, **kwargs)

def archive_year(request, year, queryset, date_field, allow_future=False, **kwargs):
    now = datetime.datetime.now()
    lookup_kwargs = {'%s__year' % date_field: year}
    if int(year) >= now.year and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs).order_by('-' + date_field)
    
    return list_detail.object_list(request, queryset=queryset, **kwargs)

def archive_month(request, year, month, queryset, date_field, allow_future=False, month_format='%b', **kwargs):
    try:
        date = datetime.date(*time.strptime(year+month, '%Y'+month_format)[:3])
    except ValueError:
        raise Http404
    now = datetime.datetime.now()
    
    # Calculate first and last day of month, for use in a date-range lookup.
    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {
        '%s__gte' % date_field: first_day,
        '%s__lt' % date_field: last_day,
    }
    
    # Only bother to check current date if the month isn't in the past and future objects are requested.
    if last_day >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs).order_by('-' + date_field)
    
    return list_detail.object_list(request, queryset=queryset, **kwargs)
    

def archive_week(request, year, week, queryset, date_field, allow_future=False, **kwargs):
    try:
        date = datetime.date(*time.strptime(year+'-0-'+week, '%Y-%w-%U')[:3])
    except ValueError:
        raise Http404
    
    now = datetime.datetime.now()
    
    # Calculate first and last day of week, for use in a date-range lookup.
    first_day = date
    last_day = date + datetime.timedelta(days=7)
    lookup_kwargs = {
        '%s__gte' % date_field: first_day,
        '%s__lt' % date_field: last_day,
    }
    
    # Only bother to check current date if the week isn't in the past and future objects aren't requested.
    if last_day >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs).order_by('-' + date_field)
    
    return list_detail.object_list(request, queryset=queryset, **kwargs)

def archive_day(request, year, month, day, queryset, date_field, allow_future=False, month_format='%b', day_format='%d', **kwargs):
    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y'+month_format+day_format)[:3])
    except ValueError:
        raise Http404
    
    model = queryset.model
    now = datetime.datetime.now()
    
    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))}
    else:
        lookup_kwargs = {date_field: date}
    
    # Only bother to check current date if the date isn't in the past and future objects aren't requested.
    if date >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs).order_by('-' + date_field)
    
    return list_detail.object_list(request, queryset=queryset, **kwargs)

def archive_today(request, **kwargs):
    today = datetime.date.today()
    kwargs.update({
        'year': str(today.year),
        'month': today.strftime('%b').lower(),
        'day': str(today.day),
    })
    return archive_day(request, **kwargs)

def object_detail(request, year, month, day, queryset, date_field, allow_future=False, month_format='%b', day_format='%d', **kwargs):
    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y'+month_format+day_format)[:3])
    except ValueError:
        raise Http404
    
    model = queryset.model
    now = datetime.datetime.now()
    
    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))}
    else:
        lookup_kwargs = {date_field: date}
    
    # Only bother to check current date if the date isn't in the past and future objects aren't requested.
    if date >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    
    queryset = queryset.filter(**lookup_kwargs).order_by('-' + date_field)
    
    return list_detail.object_detail(request, queryset=queryset, **kwargs)
