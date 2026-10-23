import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    venue = django_filters.CharFilter(
        field_name="venue",
        lookup_expr="icontains",
    )
    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact",
    )

    class Meta:
        model = Event
        fields = ["venue", "status"]
