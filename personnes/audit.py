from .models import JournalAudit

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def log_audit(request, action, personne=None, acte=None, details=""):
    user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
    ip = _get_client_ip(request) if request else None
    ua = request.META.get("HTTP_USER_AGENT", "") if request else ""

    JournalAudit.objects.create(
        user=user,
        action=action,
        personne=personne,
        acte=acte,
        ip_address=ip,
        user_agent=ua,
        details=details or "",
    )
