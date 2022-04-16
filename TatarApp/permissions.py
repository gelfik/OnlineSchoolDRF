from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode

from rest_framework.permissions import BasePermission


def is_valid(*, query: dict, secret: object) -> bool:
    """Check VK Apps signature"""
    vk_app_id = query.get('vk_app_id', None)
    if vk_app_id is None:
        return False
    secret = getattr(secret, vk_app_id, None)
    if secret is None:
        return False
    vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
    hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
    return query["sign"] == decoded_hash_code


class IsVK(BasePermission):
    def has_permission(self, request, view):
        return is_valid(query=request.GET, secret={8138635: 'SK4gYHpAfQmNzP1f12No',
                                                   8138857: 'bY1A871PEjR7khy0bY9E'})
