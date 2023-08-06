from datetime import date
from typing import Any, Dict, List, Optional, cast, Union

import phonenumbers
import usaddress

# noinspection PyPackageRequirements
from fhir.resources.bundle import Bundle

# noinspection PyPackageRequirements
from fhir.resources.fhirtypes import (
    AddressType,
    ContactPointType,
    HumanNameType,
    IdentifierType,
)

# noinspection PyPackageRequirements
from fhir.resources.patient import Patient

# noinspection PyPackageRequirements
from fhir.resources.person import Person
from phonenumbers import PhoneNumber

from helix_personmatching.logics.scoring_input import ScoringInput

from scourgify import normalize_address_record


class FhirToAttributeDict:
    @staticmethod
    def get_scoring_input(resource: Union[Patient, Person]) -> ScoringInput:
        patient_name: Optional[HumanNameType] = (
            resource.name[0] if resource.name and len(resource.name) > 0 else None
        )
        address: Optional[AddressType] = FhirToAttributeDict.get_address(
            resource.address
        )
        # https://github.com/GreenBuildingRegistry/usaddress-scourgify
        # noinspection PyUnresolvedReferences
        address_formatted: Optional[Dict[str, str]] = (
            normalize_address_record(
                {
                    "address_line_1": address.line[0]
                    if len(address.line) > 0
                    else None,
                    "address_line_2": address.line[1]
                    if len(address.line) > 1
                    else None,
                    "city": address.city,
                    "state": address.state,
                    "postal_code": address.postalCode,
                }
            )
            if address and address.city and address.state and address.postalCode
            else None
        )
        # https://github.com/datamade/usaddress
        # noinspection PyUnresolvedReferences
        address_tagged, address_type = (
            (usaddress.tag(address.line[0]))
            if address and len(address.line) > 0
            else (None, None)
        )

        # noinspection PyUnresolvedReferences
        address_street_num: Optional[str] = (
            address_tagged.get("AddressNumber") if address_tagged else None
        )
        phone: Optional[str] = FhirToAttributeDict.get_phone_number(resource.telecom)
        # phone_formatted = re.sub("[+\s()-]+", "", phone)
        # https://github.com/daviddrysdale/python-phonenumbers
        phone_formatted: Optional[PhoneNumber] = (
            phonenumbers.parse(phone, "US") if phone else None
        )
        phone_clean = str(phone_formatted.national_number) if phone_formatted else None
        email: Optional[str] = FhirToAttributeDict.get_email(resource.telecom)
        email_user_name = email.split("@")[0] if email else None

        ssn = FhirToAttributeDict.get_ssn(resource.identifier)

        # noinspection PyUnresolvedReferences
        meta_security_code = (
            FhirToAttributeDict.get_access_tag(resource.meta.security)
            if resource.meta
            else None
        )

        age_in_years = FhirToAttributeDict.calculate_age_in_years(resource.birthDate)

        # noinspection PyUnresolvedReferences
        scoring_input: ScoringInput = ScoringInput(
            id_=resource.id,
            name_given=patient_name.given[0]
            if patient_name and len(patient_name.given) > 0
            else None,
            name_family=patient_name.family if patient_name else None,
            gender=resource.gender,
            birth_date=resource.birthDate.strftime("%Y-%m-%d")
            if resource.birthDate
            else None,
            address_postal_code=address.postalCode if address else None,
            address_line_1=address_formatted.get("address_line_1")
            if address_formatted
            else None,
            email=email,
            phone=phone_clean,
            birth_date_year=str(resource.birthDate.year)
            if resource.birthDate
            else None,
            birth_date_month=str(resource.birthDate.month)
            if resource.birthDate
            else None,
            birth_date_day=str(resource.birthDate.day) if resource.birthDate else None,
            phone_area=phone_clean[0:3] if phone_clean else None,
            phone_local=phone_clean[3:6] if phone_clean else None,
            phone_line=phone_clean[6:10] if phone_clean else None,
            address_line_1_st_num=address_street_num,
            email_username=email_user_name,
            is_adult_today=age_in_years >= 18 if age_in_years else None,
            ssn=ssn,
            meta_security_client_slug=meta_security_code,
        )
        return scoring_input

    @staticmethod
    def get_scoring_inputs_for_resource(
        resource: Union[Patient, Person, Bundle]
    ) -> List[ScoringInput]:
        if isinstance(resource, Bundle):
            # noinspection PyUnresolvedReferences
            resources = [e.resource for e in resource.entry]
        else:
            resources = [resource]
        return [
            FhirToAttributeDict.get_scoring_input(resource=resource)
            for resource in resources
        ]

    @staticmethod
    def get_access_tag(security_tags: Optional[List[Any]]) -> Optional[str]:
        if not security_tags or len(security_tags) == 0:
            return None
        access_tags = [
            tag
            for tag in security_tags
            if tag.system == "https://www.icanbwell.com/access"
        ]
        return access_tags[0].code if len(access_tags) > 0 else None

    @staticmethod
    def get_ssn(identifiers: Optional[List[IdentifierType]]) -> Optional[str]:
        if not identifiers or len(identifiers) == 0:
            return None
        ssn_identifiers = [
            identifier
            for identifier in identifiers
            if identifier.system == "http://hl7.org/fhir/sid/us-ssn"
        ]
        return ssn_identifiers[0].value if len(ssn_identifiers) > 0 else None

    @staticmethod
    def get_phone_number(telecom: Optional[List[ContactPointType]]) -> Optional[str]:
        if not telecom or len(telecom) == 0:
            return None
        phones = FhirToAttributeDict.get_telecom_with_system(telecom, "phone")
        if phones and len(phones) > 0:
            # prefer use=mobile
            mobile_phones = [phone for phone in phones if phone.use == "mobile"]
            if len(mobile_phones) > 0:
                return cast(Optional[str], mobile_phones[0].value)
            # noinspection PyUnresolvedReferences
            return cast(Optional[str], phones[0].value)
        else:
            return None

    @staticmethod
    def get_email(telecom: Optional[List[ContactPointType]]) -> Optional[str]:
        if not telecom or len(telecom) == 0:
            return None
        telecom_system = "email"
        emails = FhirToAttributeDict.get_telecom_with_system(telecom, telecom_system)
        if emails and len(emails) > 0:
            # noinspection PyUnresolvedReferences
            return cast(Optional[str], emails[0].value)
        else:
            return None

    @staticmethod
    def get_telecom_with_system(
        telecom: List[ContactPointType], telecom_system: str
    ) -> Optional[List[ContactPointType]]:
        if not telecom or len(telecom) == 0:
            return None

        # noinspection PyUnresolvedReferences
        matching_telecoms = [t for t in telecom if t.system == telecom_system]
        return matching_telecoms

    @staticmethod
    def get_address(addresses: Optional[List[AddressType]]) -> Optional[AddressType]:
        if not addresses or len(addresses) == 0:
            return None

        # 1. use == "official"
        official_addresses = [
            address for address in addresses if address.use == "official"
        ]
        official_address = (
            official_addresses[0] if len(official_addresses) > 0 else None
        )
        if official_address:
            return official_address

        # 2. use == "home"
        home_addresses = [address for address in addresses if address.use == "home"]
        home_address = home_addresses[0] if len(home_addresses) > 0 else None
        if home_address:
            return home_address

        # 3. IF there is no use property, use the first address element by default
        return addresses[0]

    @staticmethod
    def calculate_age_in_years(birthdate: Optional[date]) -> Optional[int]:
        if not birthdate:
            return None
        # Get today's date object
        today = date.today()

        # A bool that represents if today's day/month precedes the birth day/month
        one_or_zero = (today.month, today.day) < (birthdate.month, birthdate.day)

        # Calculate the difference in years from the date object's components
        year_difference = today.year - birthdate.year

        # The difference in years is not enough.
        # To get it right, subtract 1 or 0 based on if today precedes the
        # birthdate's month/day.

        # To do this, subtract the 'one_or_zero' boolean
        # from 'year_difference'. (This converts
        # True to 1 and False to 0 under the hood.)
        age = year_difference - one_or_zero

        return age
