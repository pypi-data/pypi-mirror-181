"""Hydroqc custom types."""
from hydroqc.types.common import IDTokenTyping, Rates
from hydroqc.types.conso import (
    ConsoAnnualTyping,
    ConsoDailyTyping,
    ConsoHourlyTyping,
    ConsoMonthlyTyping,
    DPCDataTyping,
    DTDataTyping,
)
from hydroqc.types.info_compte import (
    ComptesTyping,
    ContractSummaryTyping,
    InfoCompteTyping,
    ListContractsTyping,
    listeComptesContratsTyping,
    listeContratModelTyping,
)
from hydroqc.types.winter_credit import (
    CriticalPeakDataTyping,
    PeriodDataTyping,
    WinterCreditDataTyping,
)

__all__ = [
    "InfoCompteTyping",
    "ConsoHourlyTyping",
    "ConsoDailyTyping",
    "ConsoMonthlyTyping",
    "ConsoAnnualTyping",
    "CriticalPeakDataTyping",
    "PeriodDataTyping",
    "WinterCreditDataTyping",
    "listeComptesContratsTyping",
    "listeContratModelTyping",
    "ComptesTyping",
    "IDTokenTyping",
    "ContractSummaryTyping",
    "ListContractsTyping",
    "DPCDataTyping",
    "DTDataTyping",
    "Rates",
]
