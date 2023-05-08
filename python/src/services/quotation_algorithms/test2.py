from data_access.entities.policy_risk import PolicyRisk
from data_access.entities.vehicle import Vehicle

vehicle: Vehicle
policy_risks = list()

import datetime
from _decimal import Decimal

from data_access.entities.dict.currency import CurrencyEnum
from data_access.entities.dict.risk import RiskEnum


if vehicle.ProductionYear < 2010:
    risk = PolicyRisk()
    risk.CurrencyId = CurrencyEnum.EUR.value
    risk.RiskId = RiskEnum.TPL.value
    risk.CreationDate = datetime.date.today()
    risk.StartDate = datetime.date.today()
    risk.EndDate = datetime.date.today() + datetime.timedelta(days=2)
    risk.Premium = Decimal(100.0)
    policy_risks.append(risk)

    risk1 = PolicyRisk()
    risk1.CurrencyId = CurrencyEnum.EUR.value
    risk1.RiskId = RiskEnum.TPL.value
    risk1.CreationDate = datetime.date.today()
    risk1.StartDate = datetime.date.today()
    risk1.EndDate = datetime.date.today() + datetime.timedelta(days=2)
    risk1.Premium = Decimal(200.0)
    policy_risks.append(risk1)
