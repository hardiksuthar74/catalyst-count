from django.urls import path
from .views import (
    FetchIndustryView,
    FetchCountryView,
    FetchStatesView,
    FetchCitiesView,
    FetchCompaniesView,
    SendAllUserHistoryView,
    upload_view,
    company_view,
)


urlpatterns = [
    path(
        "upload",
        upload_view,
    ),
    path(
        "company",
        company_view,
    ),
    path("fetch-industry/", FetchIndustryView.as_view()),
    path("fetch-country/", FetchCountryView.as_view()),
    path("fetch-state/<str:country_name>/", FetchStatesView.as_view()),
    path("fetch-cities/<str:state_name>/", FetchCitiesView.as_view()),
    path("fetch-total-companies/", FetchCompaniesView.as_view()),
    path("fetch-all-user-history/", SendAllUserHistoryView.as_view()),
]
