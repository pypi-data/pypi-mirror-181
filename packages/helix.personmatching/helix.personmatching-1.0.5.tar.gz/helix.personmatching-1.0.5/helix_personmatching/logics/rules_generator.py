from typing import List

from helix_personmatching.models.constants import Attribute
from helix_personmatching.models.rule import Rule


class RulesGenerator:
    @staticmethod
    def generate_rules() -> List[Rule]:
        """
        generate default match rules
        :return: generated rules for matching
        """

        rules: List[Rule] = [
            Rule(
                name="Rule-001",
                description="given name, family name, gender, dob, zip",
                number=1,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.GENDER,
                    Attribute.BIRTH_DATE,
                    Attribute.ADDRESS_POSTAL_CODE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-002",
                description="given name, dob, address 1, zip",
                number=2,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.ADDRESS_LINE_1,
                    Attribute.ADDRESS_POSTAL_CODE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-003",
                description="given name, date of birth, email",
                number=3,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.EMAIL,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-004",
                description="given name, date of birth, phone",
                number=4,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.PHONE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-005",
                description="given name, family name, year of date of birth, gender, address 1, zip",
                number=5,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE_YEAR,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1,
                    Attribute.ADDRESS_POSTAL_CODE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-006",
                description="given name, family name, dob month, dob date, gender, address 1, zip",
                number=6,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE_MONTH,
                    Attribute.BIRTH_DATE_DAY,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1,
                    Attribute.ADDRESS_POSTAL_CODE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-007",
                description="given name, family name, date of birth, gender, phone",
                number=7,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.PHONE_AREA,
                    Attribute.PHONE_LOCAL,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-008",
                description="first name, last name, date of birth, gender, phone local exchange, phone line",
                number=8,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.PHONE_LOCAL,
                    Attribute.PHONE_LINE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-009",
                description="first name, last name, date of birth, gender, phone area code, phone line",
                number=9,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.PHONE_AREA,
                    Attribute.PHONE_LINE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-010",
                description="given name, dob, gender, address 1 street number, zip, email username, phone line",
                number=10,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1_ST_NUM,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.EMAIL_USERNAME,
                    Attribute.PHONE_LINE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-011",
                description="given name, dob, gender, address 1 street number, zip, "
                + "phone area code, phone local exchange code",
                number=11,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1_ST_NUM,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.PHONE_AREA,
                    Attribute.PHONE_LOCAL,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-012",
                description="given name, dob, gender, address 1 street number, zip, phone area code, phone line number",
                number=12,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1_ST_NUM,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.PHONE_AREA,
                    Attribute.PHONE_LINE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-013",
                description="given name, dob, gender, address 1 street number, zip, "
                + "phone local exchange code, phone line number",
                number=13,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1_ST_NUM,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.PHONE_LOCAL,
                    Attribute.PHONE_LINE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-014",
                description="family name, date of birth, is adult today flag, gender, address 1, zip, phone",
                number=14,
                attributes=[
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE,
                    Attribute.IS_ADULT_TODAY,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.PHONE,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-015",
                description="family name, date of birth, is adult today flag, gender, address 1, zip, email",
                number=15,
                attributes=[
                    Attribute.NAME_FAMILY,
                    Attribute.BIRTH_DATE,
                    Attribute.IS_ADULT_TODAY,
                    Attribute.GENDER,
                    Attribute.ADDRESS_LINE_1,
                    Attribute.ADDRESS_POSTAL_CODE,
                    Attribute.EMAIL,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-016",
                description="given name, email, phone, dob_year",
                number=16,
                attributes=[
                    Attribute.NAME_GIVEN,
                    Attribute.EMAIL,
                    Attribute.PHONE,
                    Attribute.BIRTH_DATE_YEAR,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-017",
                description="SSN",
                number=17,
                attributes=[
                    Attribute.SSN,
                ],
                score=0.0,
            ),
            Rule(
                name="Rule-018",
                description="client slug, given_name, dob_year",
                number=18,
                attributes=[
                    Attribute.META_SECURITY_CLIENT_SLUG,
                    Attribute.NAME_GIVEN,
                    Attribute.BIRTH_DATE_YEAR,
                ],
                score=0.0,
            ),
        ]

        return rules
