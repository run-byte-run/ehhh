from urllib.parse import urlparse


def get_domain_from_url(url: str):
    return urlparse(url).hostname
