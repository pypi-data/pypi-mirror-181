from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Provider:
    name: str
    aliases: list[str]
    country: str
    region: str | None
    sms: str | None
    mms: str | None

    def has_location_support(self, country: str, region: str | None) -> bool:
        country_match = self.country.lower() == country.lower()
        region_match = (self.region is None) or (
            region is not None and self.region.lower() == region.lower()
        )
        return country_match and region_match

    def contains_term(self, term: str) -> bool:
        if self.name.find(term) != -1:
            return True
        for alias in self.aliases:
            if alias.find(term) != -1:
                return True
        if self.country.find(term) != -1:
            return True
        if self.region is not None and self.region.find(term) != -1:
            return True
        if self.sms is not None and self.sms.find(term) != -1:
            return True
        if self.mms is not None and self.mms.find(term) != -1:
            return True
        return False

    def to_string_list(self) -> list[str]:
        return [
            self.name,
            ', '.join(self.aliases),
            self.country,
            self.region if self.region is not None else 'N/A',
            self.sms if self.sms is not None else 'N/A',
            self.mms if self.mms is not None else 'N/A',
        ]


PROVIDERS: list[Provider] = [
    Provider(
        name='Virgin Mobile',
        aliases=['virgin', 'vmobile'],
        country='Canada',
        region=None,
        sms='[phone_number]@txt.virginplus.ca',
        mms=None,
    ),
]
