import base64
import json
import time
import urllib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage


class Client(object):
    def __init__(self, project_id, client_email, private_key):
        self.project_id = project_id
        self.client_email = client_email
        self.private_key = private_key

    @inlineCallbacks
    def get_token(self, scope=None):
        r = yield getPage(
            "https://www.googleapis.com/oauth2/v4/token",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                },
            postdata=urllib.urlencode({
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": get_assertion(self.client_email, scope, self.private_key),
                }))

        returnValue(json.loads(r)["access_token"])

    @inlineCallbacks
    def zones(self):
        token = yield self.get_token(
            scope="https://www.googleapis.com/auth/compute.readonly")

        url = 'https://www.googleapis.com/compute/v1/projects/{}/zones'.format(
            self.project_id)

        r = yield getPage(
            url,
            method="GET",
            headers={"Authorization": "Bearer {}".format(token)})

        returnValue(json.loads(r))


def b64encode(msg):
    return base64.urlsafe_b64encode(msg.rstrip('='))


def json_encode(data):
    return json.dumps(data, separators=(',', ':')).encode("utf-8")


def get_jwt_header(alg="RS256", typ="JWT"):
    return {"alg": alg, "typ": typ}


def get_jwt_claim_set(iss, scope, aud=None, exp=None, iat=None):
    if aud is None:
        aud = "https://www.googleapis.com/oauth2/v4/token"

    if exp is None or iat is None:
        now = int(time.time())

        if iat is None:
            iat = now

        if exp is None:
            exp = iat + 1800

    return {
        "iss": iss,
        "scope": scope,
        "aud": aud,
        "exp": exp,
        "iat": iat,
        }


def prepare_key(key):
    return load_pem_private_key(key.encode("utf-8"), password=None, backend=default_backend())


def sign(msg, key):
    signer = key.signer(padding.PKCS1v15(), hashes.SHA256())
    signer.update(msg)
    return signer.finalize()


def get_assertion(iss, scope, key):
    header = get_jwt_header()
    payload = get_jwt_claim_set(iss, scope)

    segments = [
        b64encode(json_encode(header)),
        b64encode(json_encode(payload)),
        ]

    signing_input = b'.'.join(segments)
    key = prepare_key(key)
    signature = sign(signing_input, key)
    segments.append(b64encode(signature))

    return b'.'.join(segments)


if __name__ == '__main__':
    from twisted.internet import reactor

    client = Client(
        "zenossmonitor-1308",
        "zenoss@zenossmonitor-1308.iam.gserviceaccount.com",
        "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCshRe8+PRn+4QL\nh1/6OQORMA1NdOmYFXFYexmVVbMIRCmHImibES29vbraFYUAeMNZ/Ibrg6rX3aMr\nAL+7xp1hTiGzSztsoz7s+m6Cav20UhPXv8kiiyI/8nM2kfGw1pbdpgaOhlIAnW4+\n/oDHqe26f5xVqhde+GGPNnYwPmjj5L0WLF8kNuusvSBAzfS7enRDJGL1cUdswzci\ndDIA6YgwFBCZYVXIUy1txRr7j6oLIdfUxjAMi46PjCEkjt/ikKz7kdRcfpchddBM\ndBXguJRtXkqb8d5zzz8EdYHRVxJ5VfgYSmQKdI8X0+KUTvRMRg759j54CssqnCsJ\nL6Xaf5jfAgMBAAECggEBAJdfsJR/XPRgHFyBTBWiMR8TqphsHQr0xZ99Y9VEfPKj\n3ExWRLLLP/dcorb4atsfG0m56ih8P0tpjeINpi5891qJ08geGuYX1v7YPl7wweuW\nmRKVlUZaDpNNiQo4xHkF0RpqsxYbhZhEipd7eEO5Nn6Nuf7wX9FU30Vp5AowuJg8\niFcUen28KB6h5H7Aij7cp4LUQUTVx61GDcpwK6PZFigZ/CQ+nHf+M9OG4LeuR9/S\nVOzREPENVWqaLYrl8DoZ1rcMHeiLbxKyhfYyJeYx7/RA+l5cSfuCtzaJcrtPJgJH\nlaI2TTbvHdCpTCZ8tjIsaXJb09aTAv+IvZ+VMUIbTgECgYEA7us+Kjtz7eiIzzR/\n9+bVcD3gFuVPfrBZUquPirCaI1ESDgnopr2F3hpIXEbnC0dcuUDcu+BKL9sn2Jkj\nmg+5J7DQ/hMitfSkWin3QRVLJC1sL+04BtOMfAuqEdViGGWWoZYD4QXpCXfjrQDu\nsje+jDE4uowIckXJiIqVY9K+PmcCgYEAuNqY8AUnHUXwxtv9B819qyDHxOZJ5uyA\n/i0br+olQK5bdK2yO/oD9jW8noQn1rBHYK7PZMcd3mJocx4Q1SNJad1U5tzDV7W2\n/yRf7ebQ606vpyaTe8arGeb7+ZQ86cJXqc3eThs2YZVdWPpVuxrJNEtaMX+RHtSH\ntq/PUgZGVskCgYBEs1ZL1I6wYYY9ds45XaIQRWqTitrCBjmZIQYEjmW0NBKqAMVq\ndOLyi8I07ppvTtTl3DXcvFD4097wVJC9Mzo9pIVkGeKISdGcr6aOi23w+DK80Uyk\nAd7KqJv9xssPUt7ulfGFmip5c4T/cV4x1v+u1lSGp8+h9FlQLvFoI+hajwKBgHLs\n7RKkkXngpt5rnPfB6TSAj9K5vg6E0Xm1P7Zx4zFAdXmoF9y0BsyHAjqnPUF7nRTd\n+fDU3pwJIJkZgyuP4a+gvI0/iW85eYlM6xs0WoVBCXHpSN42WOAkvFmhsPFAM1JN\nvL1gq8GlpECSesR11cveYTfO8MFzLuEEkueTIR4JAoGAObBQqh3h1/TM4E4v/s24\n+Y6tY1aehOdSUzP6M4Cg1Ug60EUy5IiouOOUjV/2ikihb/SrlvrsfM0OtJE5N19P\nJz9ZsHDw+nHj1Y/xlx6nVXt2IWsRcj6Mycg6HYuBr9OeYdhF8tAzPdR335ALCCRj\nYLcEthlajYRvlEfkLTd52wg=\n-----END PRIVATE KEY-----\n")

    d = client.zones()

    def done(r):
        print r
        reactor.stop()

    d.addBoth(done)
    reactor.run()
