from services.models.error_message import ErrorMessage


class Errors:
    NO_POLICY_OFFER_TEMPLATE = ErrorMessage('0001', 'No policy offer template with provided id')
    NO_OFFER_WITH_ID = ErrorMessage('0002', 'No policy offer with provided id')

