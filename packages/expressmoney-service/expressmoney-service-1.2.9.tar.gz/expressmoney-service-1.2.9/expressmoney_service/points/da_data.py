__all__ = ('ValidateAddressPoint',)

from ..api import *

_SERVICE = 'services'

EMPTY = 'EMPTY'
SUCCESS = 'SCS'
FAILURE = 'FAIL'

RESULT_CHOICES = (
    (EMPTY, EMPTY),
    (FAILURE, FAILURE),
    (SUCCESS, SUCCESS),
)


class ValidateAddressCreateContract(Contract):
    address = serializers.CharField(max_length=256)


class ValidateAddressResponseContract(Contract):
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    data = serializers.JSONField()


class _ValidateAddress(ID):
    _service = _SERVICE
    _app = 'da_data'
    _view_set = 'validate_address'


class ValidateAddressPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = _ValidateAddress()
    _create_contract = ValidateAddressCreateContract
    _response_contract = ValidateAddressResponseContract
