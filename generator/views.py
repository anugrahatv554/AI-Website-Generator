import os
import google.generativeai as genai
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.shortcuts import redirect,render
from pymongo import MongoClient
from .models import GeneratedWebsite



from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # 🔁 Updated here
# def generate_gemini_content(business_type, industry):
#     prompt = f"""
#     Generate a complete HTML5 template for a {business_type} business in the {industry} industry.
#     Include:
#     - A <head> with <title>, basic CSS styles
#     - A <body> with header, about us section, services, and contact details
#     - Use modern HTML5 structure
#     Return only HTML content, no explanation or extra text.
#     """
#     response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(prompt)
#     return response.text.strip()

def generate_gemini_content(business_type, industry):
    prompt = f"""
    Generate a complete HTML5 template for a {business_type} business in the {industry} industry.
    Include:
    - A <head> with <title>, basic CSS styles
    - A <body> with header, about us section, services, and contact details
    - Use modern HTML5 structure
    Return only HTML content, no explanation or extra text.
    """
    response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(prompt)
    content = response.text.strip()

    # Remove starting and ending triple backticks (``` or ```html)
    if content.startswith("```"):
        lines = content.splitlines()
        # Remove first and last lines if they are backticks
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)

    return content



def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_website(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        business_type = data.get('business_type')
        industry = data.get('industry')

        html_content = generate_gemini_content(business_type, industry)

        # Save to file
        file_path = os.path.join(settings.BASE_DIR, 'generator', 'templates', 'preview.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("here-")
         # Save to MongoDB (without any migration)
        GeneratedWebsite.objects.create(
            business_type=business_type,
            industry=industry,
            html_content={"template": html_content}
        )
        print("here-------")

        # return JsonResponse({
        #     "success": True,
        #     "content": html_content,
        #     # "mongo_id": str(result.inserted_id)
        # })
        return redirect('/api/generator/preview/')


def preview_page(request):
    # Load the previously generated HTML file and return as raw HTML response
    # file_path = os.path.join(settings.BASE_DIR, 'generator', 'templates', 'preview.html')
    print("hello")
    return render(request, 'preview.html')
    # if os.path.exists(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as f:
    #         html = f.read()
    #     return HttpResponse(html)
    # else:
    #     return HttpResponse("No preview available. Please generate a site first.", status=404)