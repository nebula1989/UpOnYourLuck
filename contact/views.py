from django.conf import settings

from uponyourluck.settings import DOMAIN
from .forms import ContactForm

# Andrew's imports
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email_subject = f'New contact {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
            return render(request, 'success.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)


# DEBUG STUFF
import logging
logging.basicConfig(level=logging.INFO)

def password_reset_request(request):
    logging.info("PASSWORD RESET VIEW")
    domain = DOMAIN
    logging.info("DOMAIN: %s" % domain)
    if request.method == "POST":
        logging.info("Line 43")
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            logging.info("Line 46")
            data = password_reset_form.cleaned_data['email']
            logging.info('data: %s' % data)
            associated_users = User.objects.filter(Q(email=data))
            logging.info(f'associated_users: {associated_users}')
            if associated_users.exists():
                logging.info("Line 50")
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    context = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    logging.info("Line 63")

                    try:
                        logging.info("TRY SEND MAIL")
                        send_mail(subject, email, user.email, fail_silently=False)

                    except BadHeaderError:
                        logging.info("BAD HEADER")
                        return HttpResponse('Invalid header found.')

                    logging.info("MESSAGE SUCCESS")
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/")
            else:
                messages.error(request, "Password Reset Fail!")
                return redirect('/')

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"password_reset_form": password_reset_form}
    )
