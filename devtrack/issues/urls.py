from django.urls import path
from .views import reporters_mgmt, IssueView


urlpatterns = [
    path("reporters/", reporters_mgmt, name="reporters-mgmt"),
    path("issues/",IssueView.as_view())
]