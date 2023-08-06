from typing import List, Optional

from django.http import QueryDict


def get_url(recipients: List[str], subject: str, body: str, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None) -> str:
    query = QueryDict(mutable=True)
    query["subject"] = subject
    query["body"] = body
    if cc is not None:
        query.setlist("cc", cc)
    if bcc is not None:
        query.setlist("bcc", bcc)
    return f"mailto:{','.join(recipients)}?{query.urlencode()}"
