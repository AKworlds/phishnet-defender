import re
import urllib.parse

def extract_url_features(url):
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc or ""
    path = parsed.path or ""

    return {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "count_dots": url.count("."),
        "count_hyphens": url.count("-"),
        "count_at": url.count("@"),
        "count_question": url.count("?"),
        "count_equals": url.count("="),
        "count_https": int("https" in url),
        "has_ip": int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", hostname))),
        "is_shortened": int(any(x in url for x in ["bit.ly", "tinyurl", "goo.gl", "ow.ly"]))
    }
