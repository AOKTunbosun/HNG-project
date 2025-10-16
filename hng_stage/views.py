from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


MY_DETAILS = {
    "full_name": "Keruwole AbdAllah Olatunbosun",
    "email": "aokolatunbosun@gmail.com",
    "tech_stack": ["Django"],
    "stage": 0,
}

@require_http_methods(["GET"])
def me_endpoint(request):
    try:
        cat_fact_url = "https://catfact.ninja/fact"

        response = requests.get(cat_fact_url, timeout=5)
        response.raise_for_status()

        cat_data = response.json()

        final_response = MY_DETAILS.copy()
        final_response["cat_fact"] = cat_data.get("fact", "No fact available")

        return JsonResponse(final_response)


    except requests.exceptions.RequestException as e:
        error_response = {
            "error": f"Service Unavailable: Could not fetch cat fact. Error Details: {e}"
        }
        return JsonResponse(error_response, status=503)
    
    except Exception as e:
        error_response = {
            "error": f"An unexpected error occured. Error Details: {e}"
        }
        return JsonResponse(error_response, status=500)