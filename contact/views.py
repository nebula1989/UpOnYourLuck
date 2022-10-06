import os

from django.conf import settings
from google.oauth2 import service_account

from uponyourluck.settings import DOMAIN
from .forms import ContactForm

# Google
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

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
    project_id = 'recaptcha-354614'
    recaptcha_action = 'SUBMIT'
    recaptcha_site_key = '6Lfyj1QiAAAAAGJ8-iFk22fmSJu8p4gmAdhKBE5E'

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            token = request.POST['g-recaptcha-response']
            create_assessment(project_id, recaptcha_action, recaptcha_site_key, token)
            form.save()
            email_subject = f'New contact {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
            return render(request, 'success.html')
        else:
            messages.error(request, "Your message did not get sent.")
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)


# DEBUG STUFF
import logging
logging.basicConfig(level=logging.INFO)

# from Jaysha's tutorial at https://ordinarycoders.com/blog/article/django-password-reset
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
                        'token': default_token_generator.make_token(user)
                    }
                    email = render_to_string(email_template_name, context)
                    logging.info("Line 63")

                    try:
                        logging.info("TRY SEND MAIL")
                        send_mail(subject, email, settings.CONTACT_EMAIL, [user.email], fail_silently=False)

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


def create_assessment(
    project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str
) -> Assessment:
    """Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """
    filename = "google_cred.json"
    credentials = service_account.Credentials.from_service_account_file(filename)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (id). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response

