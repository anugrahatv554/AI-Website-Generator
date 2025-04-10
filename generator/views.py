import os
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.shortcuts import render
from .models import GeneratedWebsite
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")


def generate_gemini_content(business_type, industry):
    prompt = f"""
    Generate a complete HTML5 template for a {business_type} business in the {industry} industry.
    Include:
    - A <head> with <title>, basic CSS styles
    - A <body> with header, about us section, services, and contact details
    - Use modern HTML5 structure
    Return only HTML content, no explanation or extra text.
    """

    response = model.generate_content(prompt)
    content = response.text.strip()

    if content.startswith("```"):
        lines = content.splitlines()
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

        file_path = os.path.join(settings.BASE_DIR, 'generator', 'templates', 'preview.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        GeneratedWebsite.objects.create(
            business_type=business_type,
            industry=industry,
            html_content={"template": html_content}
        )

        return JsonResponse({
            "success": True,
            "redirect_url": "/api/generator/preview/"
        })


def preview_page(request):
    return render(request, 'preview.html')
