"""Hydroquebec contract module."""
from hydroqc.contract.common import check_period_data_present
from hydroqc.contract.contract_residential import ContractResidential
from hydroqc.hydro_api.client import HydroClient

from hydroqc.types import DPCDataTyping


class ContractDPC(ContractResidential):
    """Hydroquebec contract.

    Represents a FlexD contract (contrat)
    """

    _rate_code = "DPC"
    _rate_option_code = ""

    def __init__(
        self,
        applicant_id: str,
        customer_id: str,
        account_id: str,
        contract_id: str,
        hydro_client: HydroClient,
        log_level: str | None = None,
    ):
        """Create a new Hydroquebec contract."""
        ContractResidential.__init__(
            self,
            applicant_id,
            customer_id,
            account_id,
            contract_id,
            hydro_client,
            log_level,
        )

    async def get_flexd_data(self) -> DPCDataTyping:
        """Fetch FlexD data."""
        return await self._hydro_client.get_flexd_data(
            self.applicant_id, self.customer_id, self.contract_id
        )

    @property
    @check_period_data_present
    def cp_lower_price_consumption(self) -> float:
        """Total lower priced consumption since the current period started."""
        return self._all_period_data[0]["consoRegPeriode"]

    @property
    @check_period_data_present
    def cp_higher_price_consumption(self) -> float:
        """Total higher priced consumption since the current period started."""
        return self._all_period_data[0]["consoHautPeriode"]
