# result_filters.py

from django import template
from authenticator.models import Results  # Import your Results model

register = template.Library()


@register.filter
def get_result(results, student_id):
    return results.filter(student__id=student_id)


@register.filter
def get_result_subject(result, subject_id):
    if result:
        try:
            return result.filter(subject__id=subject_id).first()
        except Results.DoesNotExist:
            return None
    return None
