from data_access.entities.policy_offer_template import PolicyOfferTemplate
from data_access.entities.vehicle import Vehicle

# DO NOT REMOVE FOLLOWING IMPORTS
from data_access.entities.policy_risk import PolicyRisk


class CalculationService:
    def calculate(self, vehicle: Vehicle, policy_offer_template: PolicyOfferTemplate):
        policy_risks = list()
        exec(policy_offer_template.QuotationAlgorithm)
        return policy_risks
