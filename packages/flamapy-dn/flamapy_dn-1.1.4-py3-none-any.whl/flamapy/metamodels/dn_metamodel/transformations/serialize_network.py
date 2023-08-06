from typing import Any

from flamapy.core.transformations import Transformation

from flamapy.metamodels.dn_metamodel.models import DependencyNetwork


class SerializeNetwork(Transformation):

    '''
    SerializeNetwork(
        source_model: dict
    )
    '''

    source_model: dict[str, Any]
    destination_model: DependencyNetwork | None = None

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        valid_keys = [
            'source_model'
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

    def transform(self) -> None:
        self.destination_model = DependencyNetwork(**self.source_model)