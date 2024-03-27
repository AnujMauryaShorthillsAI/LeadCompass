import math
from pydantic import BaseModel, EmailStr, constr, Field, validator, confloat, field_validator, conlist
from datetime import datetime
from typing import Optional, Union, Any
from Enum import StatusEnum

#
# class PropertyData(BaseModel):
#     FIPSCode: Any
#     PropertyZipCode: Any
#     PropertyZip4: Any
#     PropertyUnitNumber: Any
#     PropertyHouseNumber: Any
#     RecordingDate: Any
#     RecorderBookNumber: Any
#     RecorderPageNumber: Any
#     RecorderDocumentNumber: Any
#     APN: Any
#     MultiAPNFlag: Any
#     LegalBlock: Any
#     LegalSection: Any
#     LegalDistrict: Any
#     LegalLandLot: Any
#     LegalUnit: Any
#     LegalPhaseNumber: Any
#     LegalTractNumber: Any
#     LenderNameID: Any
#     DueDate: Any
#     AdjustableRateRider: Any
#     FirstChangeDateYearConversionRider: Any
#     FirstChangeDateMonthDayConversionRider: Any
#     PrepaymentRider: Any
#     PrepaymentTermPenaltyRider: Any
#     BorrowerMailUnitNumber: Any
#     BorrowerMailZipCode: Any
#     BorrowerMailZip4: Any
#     OriginalDateOfContract: Any
#     LenderMailFullStreetAddress: Any
#     LenderMailZipCode: Any
#     LenderMailZip4: Any
#     LoanTermMonths: Any
#     LoanTermYears: Any
#     AssessorLandUse: Any
#     LoanTransactionType: Any
#     LoanOrganizationNMLS_ID: Any
#     MortgageBrokerNMLS_ID: Any
#     LoanOfficerNMLS_ID: Any
#     DPID: Any
#     UpdateTimeStamp: Any


# class PropertyData(BaseModel):
#     FIPSCode: Union[str, int]
#     PropertyZipCode: Union[str, int]
#     PropertyZip4: Union[str, int]
#     PropertyUnitNumber: Union[str, int]
#     PropertyHouseNumber: Union[str, int]
#     RecordingDate: Union[str, int]
#     RecorderBookNumber: Union[str, int]
#     RecorderPageNumber: Union[str, int]
#     RecorderDocumentNumber: Union[str, int]
#     APN: Union[str, int]
#     MultiAPNFlag: Union[float, str, int, None]
#     LegalBlock: Union[str, int]
#     LegalSection: Union[str, int]
#     LegalDistrict: Union[str, int]
#     LegalLandLot: Union[str, int]
#     LegalUnit: Union[str, int]
#     LegalPhaseNumber: Union[str, int]
#     LegalTractNumber: Union[str, int]
#     LenderNameID: Union[str, int]
#     DueDate: Union[str, int]
#     AdjustableRateRider: Union[str, None]
#     FirstChangeDateYearConversionRider: Union[str, int]
#     FirstChangeDateMonthDayConversionRider: Union[str, int]
#     PrepaymentRider: Union[str, None]
#     PrepaymentTermPenaltyRider: Union[str, int]
#     BorrowerMailUnitNumber: Union[str, int]
#     BorrowerMailZipCode: Union[str, int]
#     BorrowerMailZip4: Union[str, int]
#     OriginalDateOfContract: Union[str, int]
#     LenderMailFullStreetAddress: Union[str, None]
#     LenderMailZipCode: Union[str, int]
#     LenderMailZip4: Union[str, int]
#     LoanTermMonths: Union[str, int]
#     LoanTermYears: Union[str, int, float]
#     AssessorLandUse: Union[str, int]
#     LoanTransactionType: Union[str, int]
#     LoanOrganizationNMLS_ID: Union[str, int]
#     MortgageBrokerNMLS_ID: Union[str, int]
#     LoanOfficerNMLS_ID: Union[str, int]
#     DPID: Union[str, int]
#     UpdateTimeStamp: Union[str, int]

class PropertyData(BaseModel):
    FIPSCode: Union[str, int]
    PropertyFullStreetAddress: Union[str, int, None]
    PropertyCityName: Union[str, int, None]
    PropertyState: Union[str, int, None]
    PropertyZipCode: Union[str, int, None]
    PropertyZip4: Union[str, int, None]
    PropertyUnitType: Union[str, int, None]
    PropertyUnitNumber: Union[str, int, None]
    PropertyHouseNumber: Union[str, int, None]
    PropertyStreetDirectionLeft: Union[str, int, None]
    PropertyStreetName: Union[str, int, None]
    PropertyStreetSuffix: Union[str, int, None]
    PropertyStreetDirectionRight: Union[str, int, None]
    PropertyAddressCarrierRoute: Union[str, int, None]
    RecordType: Union[str, int, None]
    RecordingDate: Union[str, int, None]
    RecorderBookNumber: Union[str, int, None]
    RecorderPageNumber: Union[str, int, None]
    RecorderDocumentNumber: Union[str, int, None]
    APN: Union[str, int, None]
    MultiAPNFlag: Union[ str, int, None]
    Borrower1FirstNameMiddleName: Union[str, int, None]
    Borrower1LastNameOeCorporationName: Union[str, int, None]
    Borrower1IDCode: Union[str, int, None]
    Borrower2FirstNameMiddleName: Union[str, int, None]
    Borrower2LastNameOrCorporationName: Union[str, int, None]
    Borrower2IDCode: Union[str, int, None]
    BorrowerVestingCode: Union[str, int, None]
    LegalLotNumbers: Union[str, int, None]
    LegalBlock: Union[str, int, None]
    LegalSection: Union[str, int, None]
    LegalDistrict: Union[str, int, None]
    LegalLandLot: Union[str, int, None]
    LegalUnit: Union[str, int, None]
    LegalCityTownshipMunicipality: Union[str, int, None]
    LegalSubdivisionName: Union[str, int, None]
    LegalPhaseNumber: Union[str, int, None]
    LegalTractNumber: Union[str, int, None]
    LegalBriefDescription: Union[str, int, None]
    LegalSectionTownshipRangeMeridian: Union[str, int, None]
    LenderNameBeneficiary: Union[str, int, None]
    LenderNameID: Union[str, int, None]
    LenderType: Union[str, int, None]
    LoanAmount: Union[str, int, None]
    LoanType: Union[str, int, None]
    TypeFinancing: Union[str, int,None]
    InterestRate: Union[str,int, None]
    DueDate: Union[str, int, None]
    AdjustableRateRider: Union[str, int, None]
    AdjustableRateIndex: Union[str, int, None]
    ChangeIndex: Union[str, int, None]
    RateChangeFrequency: Union[str, int, None]
    InterestRateNotGreaterThan: Union[str, int, None]
    InterestRateNotLessThan: Union[str, int, None]
    MaximumInterestRate: Union[str, int, None]
    InterestOnlyPeriod: Union[str, int, None]
    FixedStepConversionRateRider: Union[str, int, None]
    FirstChangeDateYearConversionRider: Union[str, int, None]
    FirstChangeDateMonthDayConversionRider: Union[str, int, None]
    PrepaymentRider: Union[str, int, None]
    PrepaymentTermPenaltyRider: Union[str, int, None]
    BuyerMailFullStreetAddress: Union[str, int, None]
    BorrowerMailUnitType: Union[str, int, None]
    BorrowerMailUnitNumber: Union[str, int, None]
    BorrowerMailCity: Union[str, int, None]
    BorrowerMailState: Union[str, int, None]
    BorrowerMailZipCode: Union[str, int, None]
    BorrowerMailZip4: Union[str, int, None]
    OriginalDateOfContract: Union[str, int, None]
    TitleCompanyName: Union[str, int, None]
    LenderDBAName: Union[str, int, None]
    LenderMailFullStreetAddress: Union[str, int, None]
    LenderMailUnitType: Union[str, int, None]
    LenderMailUnit: Union[str, int, None]
    LenderMailState: Union[str, int, None]
    LenderMailZipCode: Union[str, int, None]
    LenderMailZip4: Union[str, int, None]
    LoanTermMonths: Union[str, int, None]
    LoanTermYears: Union[str, int, float, None]
    LoanNumber: Union[str, int, None]
    PID: Union[str, int, None]
    AssessorLandUse: Union[str, int, None]
    ResidentialIndicator: Union[str, int, None]
    ConstructionLoan: Union[str, int,None]
    CashPurchase: Union[str, int, None]
    StandAloneRefi: Union[str, int, None]
    EquityCreditLine: Union[str, int, None]
    PropertyUseCode: Union[str, int, None]
    LoanTransactionType: Union[str, int, None]
    MainRecordIDCode: Union[str, int, None]
    LoanOrganizationNMLS_ID: Union[str, int, None]
    LoanOrganizationName: Union[str, int, None]
    MortgageBrokerNMLS_ID: Union[str, int, None]
    MortgageBroker: Union[str, int, None]
    LoanOfficerNMLS_ID: Union[str, int, None]
    LoanOfficerName: Union[str, int, None]
    DPID: Union[str, int, None]
    UpdateTimeStamp: Union[str, int, None]




# @field_validator('MultiAPNFlag')
# def check_nan(cls, value):
#     if isinstance(value, (float, int)):
#         return float(value)
#     elif isinstance(value, str) and value.lower() == 'nan':
#         return 0
#     raise ValueError('Invalid value for MultiAPNFlag')
