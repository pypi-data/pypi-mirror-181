class Attribute:
    # Rule
    RULE_ID: str = "rule_id"
    RULE_NAME: str = "rule_name"
    RULE_DESC: str = "rule_desc"
    RULE_SCORE: str = "rule_score"

    # FHIR Person or Patient attributes
    ID: str = "id_"
    META_SECURITY_CLIENT_SLUG: str = "meta_security_client_slug"
    NAME_USE: str = "name_use"  # required, "usual | official | temp | nickname | anonymous | old | maiden"
    NAME_TEXT: str = "name_text"
    NAME_GIVEN: str = "name_given"
    NAME_FAMILY: str = "name_family"
    TELECOM_SYSTEM: str = (
        "telecom_system"  # required, "phone | fax | email | pager | url | sms | other"
    )
    TELECOM_USE: str = "telecom_use"  # required, "home | work | temp | old | mobile"
    TELECOM_VALUE: str = "telecom_value"
    GENDER: str = "gender"
    BIRTH_DATE: str = "birth_date"
    ADDRESS_USE: str = "address_use"  # required, "home | work | temp | old | billing"
    ADDRESS_TYPE: str = "address_type"  # required, "postal | physical | both"
    ADDRESS_LINE_1: str = "address_line_1"
    ADDRESS_LINE_2: str = "address_line_2"
    ADDRESS_CITY: str = "address_city"
    ADDRESS_STATE: str = "address_state"
    ADDRESS_POSTAL_CODE: str = "address_postal_code"
    ADDRESS_COUNTRY: str = "address_country"
    ACTIVE: str = "active"
    LINK_TARGET: str = "link_target"
    LINK_ASSURANCE: str = (
        "link_assurance"  # required, "level1 | level2 | level3 | level4"
    )

    # other attributes specifics, needs to be parsed
    EMAIL: str = "email"  # WHEN telecom.system = "email"
    EMAIL_USERNAME: str = "email_username"  # email username, string before the "@"

    PHONE: str = "phone"  # WHEN telecom.system = "phone"
    PHONE_AREA: str = "phone_area"  # phone area number (first 3 digit)
    PHONE_LOCAL: str = "phone_local"  # phone local number (middle 3 digit)
    PHONE_LINE: str = "phone_line"  # phone line number (last 4 digit)

    BIRTH_DATE_YEAR: str = "birth_date_year"  # YYYY from birthDate
    BIRTH_DATE_MONTH: str = "birth_date_month"  # MM from birthDate
    BIRTH_DATE_DAY: str = "birth_date_day"  # DD from birthDate

    ADDRESS_LINE_1_ST_NUM: str = "address_line_1_st_num"

    # this is a "calculate-on-the-fly" attribute,
    #   IS_ADULT_TODAY = (today's Date - birthDate) >= 18 years old
    IS_ADULT_TODAY: str = "is_adult_today"

    # ssn can be under the identifier array, identifier.value
    #   WHEN identifier.system = "http://hl7.org/fhir/sid/us-ssn"
    SSN: str = "ssn"

    # Scores
    SCORE: str = "score"
    TOTAL_SCORE: str = "total_score"
    MAX_POSSIBLE_SCORE: str = "max_possible_score"
