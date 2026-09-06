# -*- coding: utf-8 -*-
"""GSC без сторонних библиотек: JWT подписывается через openssl, запросы — urllib.
Причина: google-auth стоит только в venv, а скрипты запускаются системным python3.
   from seo.gsc_lite import query
   rows = query(["query"], start="2026-06-05", end="2026-09-02")
"""
import json, subprocess, time, base64, urllib.request, urllib.parse, tempfile, os, ssl

# Системный python3 на этой машине идёт без набора корневых сертификатов, и любой вызов падает с
# CERTIFICATE_VERIFY_FAILED. Дважды (2026-09-06) это тормозило проверяющих, которым приходилось
# самим подставлять SSL_CERT_FILE. Берём набор из certifi, если он есть, иначе — стандартный.
def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()

_SSL = _ctx()
SA   = os.path.expanduser("~/.gsc_service_account.json")
SITE = "sc-domain:splitcam.com"
_tok = {"v": None, "exp": 0}

def _token():
    if _tok["v"] and time.time() < _tok["exp"] - 60:
        return _tok["v"]
    sa = json.load(open(SA))
    b64 = lambda d: base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).rstrip(b'=')
    now = int(time.time())
    si = b64({"alg": "RS256", "typ": "JWT"}) + b"." + b64({
        "iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/webmasters.readonly",
        "aud": "https://oauth2.googleapis.com/token", "exp": now + 3600, "iat": now})
    kf = tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False); kf.write(sa["private_key"]); kf.close()
    df = tempfile.NamedTemporaryFile(delete=False); df.write(si); df.close()
    sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", kf.name, df.name],
                         capture_output=True, check=True).stdout
    os.unlink(kf.name); os.unlink(df.name)
    jwt = si + b"." + base64.urlsafe_b64encode(sig).rstrip(b'=')
    r = urllib.request.urlopen(context=_SSL, url=urllib.request.Request("https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                     "assertion": jwt.decode()}).encode()))
    d = json.load(r)
    _tok["v"], _tok["exp"] = d["access_token"], now + d.get("expires_in", 3600)
    return _tok["v"]

def query(dimensions, start, end, filters=None, limit=25000, start_row=0):
    body = {"startDate": start, "endDate": end, "dimensions": dimensions, "rowLimit": limit, "startRow": start_row}
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    r = urllib.request.Request(
        "https://searchconsole.googleapis.com/webmasters/v3/sites/"
        + urllib.parse.quote(SITE, safe="") + "/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + _token(), "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, context=_SSL)).get("rows", [])

def query_all(dimensions, start, end, filters=None):
    """Все строки, постранично по 25 000 — API больше за раз не отдаёт."""
    out, row = [], 0
    while True:
        part = query(dimensions, start, end, filters, 25000, row)
        out += part
        if len(part) < 25000:
            return out
        row += 25000
