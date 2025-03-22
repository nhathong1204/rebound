from django.shortcuts import render
from core.models import Blog, ContactUs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, "core/index.html")


def doctor_detail(request):
    return render(request, "core/dr-gary.html")

def list_blogs(request):
    list_blogs = Blog.objects.filter(is_active=True).order_by("-created_at")
    total_blogs  = list_blogs.count()
    page = request.GET.get("page", 1)
    paginator = Paginator(list_blogs, 3)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    context = {
        "blogs": blogs,
        "total_blogs": total_blogs,
    }
    return render(request, "core/list_blogs.html", context)

def blog_detail(request, slug):
    blog = Blog.objects.filter(slug=slug, is_active=True).first()
    return render(request, "core/blog-detail.html", {"blog": blog})

def contact_us(request):
    return render(request, "core/contact_us.html")

def ajax_contact_form(request):
    full_name = request.GET.get("full_name")
    email = request.GET.get("email")
    phone = request.GET.get("phone")
    subject = request.GET.get("subject") or "Make An Appointment"
    message = request.GET.get("message")
    
    from_email = settings.DEFAULT_FROM_EMAIL
    contact, _ = ContactUs.objects.get_or_create(full_name=full_name, email=email, phone=phone, subject=subject, message=message)
    context = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "subject": subject,
        "message": message
    }
    email_template = "emails/contact_email_template.html"
    message = render_to_string(email_template, context)
    to_email = settings.ADMIN_EMAIL
    mail = EmailMessage(subject, message, from_email, to=[to_email])
    mail.send()
    
    return JsonResponse({
        "success": True,
        "message": " Message sent successfully."
    })


def error(request, exception):
    return render(request, "error.html", {"message": exception})