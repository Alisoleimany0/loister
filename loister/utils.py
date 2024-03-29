from django.http import HttpResponse


def truncate_text(text, max_length):
    """
    Truncate a text to a maximum number of characters, adding an ellipsis if the text is too long.

    Args:
    text (str): The text to be truncated.
    max_length (int): The maximum length of the text including the ellipsis.

    Returns:
    str: The truncated text.
    """
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    else:
        return text


def get_toast_response(request, message, message_type):
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return HttpResponse(
            f"<script>localStorage.setItem('reload', 'true');localStorage.setItem('message', 'true'); localStorage.setItem('message_text', '{message}'); localStorage.setItem('message_type', '{message_type}'); setTimeout(() => {{history.back();}}, 700);</script>"
        )
    else:
        return HttpResponse(
            f"<script>localStorage.setItem('reload', 'true');localStorage.setItem('message', 'true'); localStorage.setItem('message_text', '{message}'); localStorage.setItem('message_type', '{message_type}'); history.back();</script>"
        )


def get_back_reload_response(request):
    """
    This is a test documentation
    """
    if request.user_agent.is_mobile or request.user_agent.is_tablet:
        return HttpResponse(
            "<script>localStorage.setItem('reload', 'true'); setTimeout(() => {{history.back();}}, 500); </script>"
        )
    else:
        return HttpResponse("<script>localStorage.setItem('reload', 'true');history.back();</script>")


def expire_session(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session.set_expiry(86400)
        return func(request, *args, **kwargs)

    return wrapper
