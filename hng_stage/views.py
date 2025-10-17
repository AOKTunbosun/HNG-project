from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.conf import settings


MY_DETAILS = {
    "status": "success",
    "user":{
        "name": settings.NAME,
        "email": settings.EMAIL,
        "stack": settings.STACK},
    
}

@require_http_methods(["GET"])
def me_endpoint(request):
    try:
        cat_fact_url = settings.CAT_FACT_URL

        response = requests.get(cat_fact_url, timeout=5)
        response.raise_for_status()

        cat_data = response.json()

        now_utc_time = datetime.utcnow()

        final_response = MY_DETAILS.copy()
        final_response["timestamp"] = now_utc_time.isoformat()
        final_response["cat_fact"] = cat_data.get("fact", "No fact available")

        return JsonResponse(final_response)


    except requests.exceptions.RequestException as e:
        error_response = {
            "error": f"Service Unavailable: Could not fetch cat fact. Error Details: {e}"
        }
        error_response["timestamp"] = datetime.utcnow().isoformat()
        return JsonResponse(error_response, status=503)
    
    except Exception as e:
        error_response = {
            "error": f"An unexpected error occured. Error Details: {e}"
        }
        error_response["timestamp"] = datetime.utcnow().isoformat()
        return JsonResponse(error_response, status=500)