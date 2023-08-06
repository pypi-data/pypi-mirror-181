import logging

from django.conf import settings
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from huey.contrib.djhuey import task
from obapi.models import OBContentItem

from obpages.models import FeedbackNote

if settings.USE_RECAPTCHA:
    try:
        from google.cloud import recaptchaenterprise_v1
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "The google-cloud-recaptcha-enterprise package is required"
            " if using reCAPTCHA"
        )

SPAM_SCORE_THRESHOLD = getattr(settings, "SPAM_SCORE_THRESHOLD", 0.0)

logger = logging.getLogger(__name__)


@task()
def download_new_items():
    """Task which downloads new overcomingbias posts.

    Provide the user_pk argument if you want the additions to be logged in the admin
    site.
    """
    OBContentItem.objects.download_new_items()


@task()
def update_edited_items(user_pk=None):
    """Task which downloads new overcomingbias posts.

    Provide the user_pk argument if you want the additions to be logged in the admin
    site.
    """
    updated_items = OBContentItem.objects.update_edited_items()

    # Log item changes if user pk is provided
    if user_pk:
        content_type_pk = ContentType.objects.get_for_model(OBContentItem).pk
        for item in updated_items:
            LogEntry.objects.log_action(
                user_id=user_pk,
                content_type_id=content_type_pk,
                object_id=item.pk,
                object_repr=str(item),
                action_flag=CHANGE,
                change_message=f"Updated item {item}",
            )


@task()
def update_search_index():
    action = "update_index"
    args = ["--remove"]
    call_command(action, *args)


@task()
def rebuild_search_index():
    action = "rebuild_index"
    args = ["--noinput"]
    call_command(action, *args)


@task()
def drop_feedback_if_spam(feedback_pk: int, recaptcha_token: str):
    if settings.USE_RECAPTCHA:
        # Build client, event, assessment, request
        client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

        event = recaptchaenterprise_v1.Event()
        event.site_key = settings.RECAPTCHA_KEY
        event.token = recaptcha_token

        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = event

        request = recaptchaenterprise_v1.CreateAssessmentRequest()
        request.assessment = assessment
        request.parent = f"projects/{settings.GOOGLE_PROJECT_ID}"

        # collect report from recaptcha server
        response = client.create_assessment(request)

        feedback_note = FeedbackNote.objects.get(pk=feedback_pk)
        # is token valid? does it correspond to the right action? is its score
        # above the threshold?
        if not response.token_properties.valid:
            logger.warning("Deleting feedback item due to invalid reCAPTCHA token.")
            feedback_note.delete()
        elif response.token_properties.action != "submit":
            logger.warning(
                "Deleting feedback item with unknown action"
                f" {response.token_properties.action}."
            )
            feedback_note.delete()
        elif response.risk_analysis.score < SPAM_SCORE_THRESHOLD:
            logger.warning(
                "Deleting feedback item due to spam score less than threshold"
                f" ({response.risk_analysis.score}<{SPAM_SCORE_THRESHOLD})."
            )
            feedback_note.delete()
        else:
            # if yes, record its spam score
            feedback_note.spam_score = response.risk_analysis.score
            feedback_note.save()
