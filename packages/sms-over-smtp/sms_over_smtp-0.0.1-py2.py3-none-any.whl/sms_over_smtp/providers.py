from dataclasses import dataclass

import smtplib
from typing import Optional

@dataclass
class Provider:
    name: str
    aliases: list[str]
    country: str
    region: Optional[str]
    sms: Optional[str]
    mms: Optional[str]

    def has_sms_support(self):
        return self.sms is not None

    def has_mms_support(self):
        return self.mms is not None

    def has_country_support(self, country: str):
        return self.country.lower() == country.lower()

    def has_region_support(self, region: str):
        return (self.region is None) or (self.region.lower() == region.lower())


providers: list[Provider] = [
    Provider(
        name="virgin mobile",
        aliases=["virgin", "vmobile"],
        country="canada",
        region=None,
        # or [phone_number]@vmobile.ca
        sms="[phone_number]@txt.virginplus.ca",
        mms=None,
    )
]

def get_provider_by_name(name: str):
    pass

def search_providers(term: str):
    pass


def get_providers_by_country_region(country: str, region: Optional[str]):
    pass


class SMSoverSMTP:
    def __init__(self, provider: Provider, smtp: smtplib.SMTP):
        pass

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def sms(self, message: str):
        pass

    def mms(self, message: str):
        pass