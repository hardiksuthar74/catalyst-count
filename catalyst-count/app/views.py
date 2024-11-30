import os
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Company, UploadHistory
from app.tasks import add_csv_data_to_db
from .serializers import (
    IndustrySerializer,
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    CompanyFilterSerializer,
    UploadHistorySerializer,
)


@login_required
def company_view(request):

    return render(request, "app/company.html")


@login_required
def upload_view(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        file = request.FILES["csv_file"]
        file_path = os.path.join("uploads")
        fs = FileSystemStorage(location=file_path)
        filename = fs.save(file.name, file)
        upload_history = UploadHistory.objects.create(
            **{
                "user": request.user,
                "file_name": file.name,
                "progress": 0.0,
                "status": "Pending",
            },
        )

        add_csv_data_to_db.delay(filename, upload_history.id)

        return JsonResponse({"task_id": upload_history.id})

    return render(request, "app/upload.html")


class FetchIndustryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        industries = (
            Company.objects.values("industry").distinct().exclude(industry=None)
        )
        serializer = IndustrySerializer(industries, many=True)
        return Response({"industries": [item["industry"] for item in serializer.data]})


class FetchCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        countries = Company.objects.values("country").distinct().exclude(country=None)
        serializer = CountrySerializer(countries, many=True)
        return Response({"countries": [item["country"] for item in serializer.data]})


class FetchStatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, country_name):
        states = Company.objects.filter(country=country_name).values("state").distinct()
        serializer = StateSerializer(states, many=True)
        return Response({"states": [item["state"] for item in serializer.data]})


class FetchCitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, state_name):
        cities = Company.objects.filter(state=state_name).values("city").distinct()
        serializer = CitySerializer(cities, many=True)
        return Response({"cities": [item["city"] for item in serializer.data]})


class FetchCompaniesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CompanyFilterSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        filters = Q()

        if serializer.validated_data.get("keyword"):
            keyword = serializer.validated_data["keyword"]
            filters &= Q(name__icontains=keyword) | Q(domain__icontains=keyword)

        for field in ["industry", "year_founded", "country", "state", "city"]:
            if serializer.validated_data.get(field):
                filters &= Q(
                    **{field + "__icontains": serializer.validated_data[field]}
                )

        if serializer.validated_data.get("employees_from"):
            filters &= Q(
                current_employee_estimate__gte=serializer.validated_data[
                    "employees_from"
                ]
            )
        if serializer.validated_data.get("employees_to"):
            filters &= Q(
                current_employee_estimate__lte=serializer.validated_data["employees_to"]
            )

        companies = Company.objects.filter(filters)
        count = companies.count()
        return Response({"count": count})


class SendAllUserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_upload_history = UploadHistory.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        pending_count = UploadHistory.objects.exclude(progress=100).count()

        serializer = UploadHistorySerializer(user_upload_history, many=True)
        return Response({"data": serializer.data, "pending_count": pending_count})
