# stdlib Imports
import json
import urllib

# Twisted Imports
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin


class Projects(PythonPlugin):

    '''Google instances'''
    relname = 'projects'
    modname = 'ZenPacks.galaxz.GoogleCloud.Project'

    @inlinecallbacks
    def collect(self, device, log):
        apikey = '''{
  "type": "service_account",
  "project_id": "zenossmonitor-1308",
  "private_key_id": "9eb430704d5d4dfb5adb96c09f60494de16347b9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCshRe8+PRn+4QL\nh1/6OQORMA1NdOmYFXFYexmVVbMIRCmHImibES29vbraFYUAeMNZ/Ibrg6rX3aMr\nAL+7xp1hTiGzSztsoz7s+m6Cav20UhPXv8kiiyI/8nM2kfGw1pbdpgaOhlIAnW4+\n/oDHqe26f5xVqhde+GGPNnYwPmjj5L0WLF8kNuusvSBAzfS7enRDJGL1cUdswzci\ndDIA6YgwFBCZYVXIUy1txRr7j6oLIdfUxjAMi46PjCEkjt/ikKz7kdRcfpchddBM\ndBXguJRtXkqb8d5zzz8EdYHRVxJ5VfgYSmQKdI8X0+KUTvRMRg759j54CssqnCsJ\nL6Xaf5jfAgMBAAECggEBAJdfsJR/XPRgHFyBTBWiMR8TqphsHQr0xZ99Y9VEfPKj\n3ExWRLLLP/dcorb4atsfG0m56ih8P0tpjeINpi5891qJ08geGuYX1v7YPl7wweuW\nmRKVlUZaDpNNiQo4xHkF0RpqsxYbhZhEipd7eEO5Nn6Nuf7wX9FU30Vp5AowuJg8\niFcUen28KB6h5H7Aij7cp4LUQUTVx61GDcpwK6PZFigZ/CQ+nHf+M9OG4LeuR9/S\nVOzREPENVWqaLYrl8DoZ1rcMHeiLbxKyhfYyJeYx7/RA+l5cSfuCtzaJcrtPJgJH\nlaI2TTbvHdCpTCZ8tjIsaXJb09aTAv+IvZ+VMUIbTgECgYEA7us+Kjtz7eiIzzR/\n9+bVcD3gFuVPfrBZUquPirCaI1ESDgnopr2F3hpIXEbnC0dcuUDcu+BKL9sn2Jkj\nmg+5J7DQ/hMitfSkWin3QRVLJC1sL+04BtOMfAuqEdViGGWWoZYD4QXpCXfjrQDu\nsje+jDE4uowIckXJiIqVY9K+PmcCgYEAuNqY8AUnHUXwxtv9B819qyDHxOZJ5uyA\n/i0br+olQK5bdK2yO/oD9jW8noQn1rBHYK7PZMcd3mJocx4Q1SNJad1U5tzDV7W2\n/yRf7ebQ606vpyaTe8arGeb7+ZQ86cJXqc3eThs2YZVdWPpVuxrJNEtaMX+RHtSH\ntq/PUgZGVskCgYBEs1ZL1I6wYYY9ds45XaIQRWqTitrCBjmZIQYEjmW0NBKqAMVq\ndOLyi8I07ppvTtTl3DXcvFD4097wVJC9Mzo9pIVkGeKISdGcr6aOi23w+DK80Uyk\nAd7KqJv9xssPUt7ulfGFmip5c4T/cV4x1v+u1lSGp8+h9FlQLvFoI+hajwKBgHLs\n7RKkkXngpt5rnPfB6TSAj9K5vg6E0Xm1P7Zx4zFAdXmoF9y0BsyHAjqnPUF7nRTd\n+fDU3pwJIJkZgyuP4a+gvI0/iW85eYlM6xs0WoVBCXHpSN42WOAkvFmhsPFAM1JN\nvL1gq8GlpECSesR11cveYTfO8MFzLuEEkueTIR4JAoGAObBQqh3h1/TM4E4v/s24\n+Y6tY1aehOdSUzP6M4Cg1Ug60EUy5IiouOOUjV/2ikihb/SrlvrsfM0OtJE5N19P\nJz9ZsHDw+nHj1Y/xlx6nVXt2IWsRcj6Mycg6HYuBr9OeYdhF8tAzPdR335ALCCRj\nYLcEthlajYRvlEfkLTd52wg=\n-----END PRIVATE KEY-----\n",
  "client_email": "zenoss@zenossmonitor-1308.iam.gserviceaccount.com",
  "client_id": "107587010351632718649",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/zenoss%40zenossmonitor-1308.iam.gserviceaccount.com"
}'''
        password = 'nosecret'
