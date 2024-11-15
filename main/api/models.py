from pydantic import BaseModel
from enum import Enum

class CountryEnum(str, Enum):
    usa = "United States"
    canada = "Canada"

# Expanded Enum to include all US states
class StateEnumUSA(str, Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"
    DC = "DC"
    all = "All"

# Expanded Enum to include all Canadian provinces and territories
class StateEnumCanada(str, Enum):
    AB = "AB"
    BC = "BC"
    MB = "MB"
    NB = "NB"
    NL = "NL"  # Newfoundland and Labrador
    NS = "NS"
    NT = "NT"
    NU = "NU"
    ON = "ON"
    PE = "PE"
    QC = "QC"
    SK = "SK"
    YT = "YT"
    all = "All"

class RoleEnum(str, Enum):
    software_engineer = "Software Engineer"
    data_scientist = "Data Scientist"
    data_analyst = "Data Analyst"

class CountryOnlyRequest(BaseModel):
    country: CountryEnum

class FullRequestData(BaseModel):
    country: CountryEnum
    state: str
    role: RoleEnum

class RolesRequestData(BaseModel):
    country: CountryEnum
    state: str
