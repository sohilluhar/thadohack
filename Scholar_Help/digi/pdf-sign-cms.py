#!/usr/bin/env vpython3
# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

# from endesive.pdf import cmsn as cms

# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "sigflags": 3,
        "sigbutton": True,
        "signaturebox": (470, 0, 570, 100),
        "signature": "Approved",
#        "signature_img": "signature_test.png",
        "contact": "sohil.l@somaiya.edu",
        "location": "India",
        "signingdate": date,
        "reason": "Approved",
        'signature_img': 'sign.png',
        "password": "1234",

        # b'sigpage': 0,
    
    }
    with open("Key.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"Sky@76445", backends.default_backend()
        )
    fname = "resume.pdf"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    datau = open(fname, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-signed-cms.pdf")
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)


main()
