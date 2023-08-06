"""Hydroquebec contract module."""
from collections.abc import Callable
from datetime import date

from hydroqc.contract.common import check_period_data_present
from hydroqc.contract.contract_residential import ContractResidential
from hydroqc.hydro_api.client import HydroClient

from hydroqc.types import DPCDataTyping


def check_dpc_data_present(
    method: Callable[..., None | str | bool | float | date]
) -> Callable[..., None | str | bool | float | date]:
    """Check if contractDPC's data are present."""

    def wrapper(contract: "ContractDPC") -> None | str | bool | float | date:
        if hasattr(contract, "_dpc_data"):
            return method(contract)

        contract._logger.warning("You need to call get_dpc_data method first")
        return None

    return wrapper


class ContractDPC(ContractResidential):
    """Hydroquebec contract.

    Represents a FlexD contract (contrat)
    """

    _rate_code = "DPC"
    _rate_option_code = ""
    _dpc_data: DPCDataTyping

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

    async def get_dpc_data(self) -> DPCDataTyping:
        """Fetch FlexD data."""
        self._dpc_data = await self._hydro_client.get_dpc_data(
            self.applicant_id, self.customer_id, self.contract_id
        )
        return self._dpc_data

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

    @property
    @check_dpc_data_present
    def winter_start_date(self) -> str:
        """DPC start date."""
        return self._dpc_data["results"][0]["dateDebut"]

    @property
    @check_dpc_data_present
    def winter_end_date(self) -> str:
        """DPC end date."""
        return self._dpc_data["results"][0]["dateFin"]

    @property
    @check_dpc_data_present
    def last_update_date(self) -> str:
        """DPC data last update."""
        return self._dpc_data["results"][0]["dateDernMaj"]

    @property
    @check_dpc_data_present
    def critical_called_hours(self) -> int:
        """Get number of critical hours."""
        return int(self._dpc_data["results"][0]["hrsCritiquesAppelees"])

    @property
    @check_dpc_data_present
    def max_critical_called_hours(self) -> int:
        """Get max number of critical hours."""
        return int(self._dpc_data["results"][0]["hrsCritiquesAppeleesMax"])

    @property
    @check_dpc_data_present
    def amount_saved_vs_base_rate(self) -> float:
        """Amount saved or not versus the base rate."""
        return self._dpc_data["results"][0]["montantEconPerteVSTarifBase"]

    @property
    @check_dpc_data_present
    def winter_total_days(self) -> int:
        """Get number of winter days."""
        return self._dpc_data["results"][0]["nbJoursTotauxHiver"]

    @property
    @check_dpc_data_present
    def winter_total_days_last_update(self) -> int:
        """Get number of days since winter starts."""
        return self._dpc_data["results"][0]["nbJoursDernMaj"]

    @property
    @check_dpc_data_present
    def winter_state(self) -> str:
        """TODO: unknown."""
        return self._dpc_data["results"][0]["etatHiver"]
