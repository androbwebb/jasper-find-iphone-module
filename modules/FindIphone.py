# -*- coding: utf-8-*-

import re
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException

WORDS = ["FIND", "IPHONE", "PHONE", "RING"]

# SHOULD PROBABLY BE GLOBAL IN JASPER
AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

# iCloud Settings
ICLOUD_USERNAME = "EMAIL@GMAIL.com"
ICLOUD_PASSWORD = "PASSWORD

def handle(text, mic, profile):
    """
        Makes your iPhone ring

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    try:
        api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
    except PyiCloudFailedLoginException:
        mic.say("Invalid Username & Password")
        return

    # All Devices
    devices = api.devices

    # Just the iPhones
    iphones = []

    # The one to ring
    phone_to_ring = None

    for device in devices:
        current = device.status()
        if "iPhone" in current['deviceDisplayName']:
            iphones.append(device)

    # No iphones
    if len(iphones) == 0:
        mic.say("No IPhones Found on your account")
        return

    # Many iphones
    elif len(iphones) > 1:
        mic.say("There are multiple iphones on your account.")
        for phone in iphones:
            mic.say("Did you mean the {type} named {name}?".format(type=phone.status()['deviceDisplayName'], name=phone.status()['name']))
            command = mic.activeListen()
            if any(aff in command for aff in AFFIRMATIVE):
                phone_to_ring = phone
                break

    # Just one
    elif len(iphones) == 1:
        phone_to_ring = iphones[0]

    if not phone_to_ring:
        mic.say("You didn't select an iPhone")
        return

    mic.say("Sending ring command to the phone now")
    phone_to_ring.play_sound()


def isValid(text):
    """
        Returns True if input is related to the item.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return re.search(r'\bfind.*phone\b', text, re.IGNORECASE) or \
        re.search(r'\b(ring)?.*phone.*(ring)?\b', text, re.IGNORECASE)