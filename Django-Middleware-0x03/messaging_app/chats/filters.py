from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='sender__username')
    date_range = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Message
        fields = ['user', 'date_range']
