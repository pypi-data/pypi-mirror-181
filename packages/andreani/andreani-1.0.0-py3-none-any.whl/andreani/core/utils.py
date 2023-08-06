from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class Order:
    price: Decimal
    weight: Decimal
    width: Decimal
    height: Decimal
    length: Decimal

    @property
    def volume(self):
        return self.width * self.height * self.length


@dataclass
class Metadata:
    key: str
    value: str


@dataclass
class Address:
    postalcode: str
    street: str
    number: str
    apartment: str
    floor: str
    region: str
    province: str
    country: str
    meta: Optional[List[Metadata]] = None


@dataclass
class Person:
    first_name: str
    last_name: str
    email: str
    document_number: str
    phone_number: str
    document_type: str = "DNI"


@dataclass
class Shipment:
    contract: str
    sender_info: Person
    sender_address: Address
    receiver_info: Person
    receiver_address: Address
    order: Order


@dataclass
class Package:
    package_number: str
    shipment_number: str
    totalizer: str
    linking: Optional[List[Metadata]] = None


@dataclass
class BaseBranch:
    nomenclature: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None


@dataclass
class DistributionBranch(BaseBranch):
    pass


@dataclass
class RenditionBranch(BaseBranch):
    pass


@dataclass
class ImpositionBranch(BaseBranch):
    pass


@dataclass
class SupplyBranch:
    pass


@dataclass
class SubmitShipmentResponse:
    status: str
    shipment_type: str
    distribution_branch: DistributionBranch
    rendition_branch: RenditionBranch
    imposition_branch: ImpositionBranch
    supply_branch: SupplyBranch
    creation_date: datetime
    permisionary_number: str
    service_description: str
    packages: List[Package]
    package_group: str
    group_labels: str


@dataclass
class LoginResponse:
    token: str
    refresh: str


@dataclass
class Fees:
    distribution_insurance: Decimal
    distribution: Decimal
    total: Decimal


@dataclass
class FeesResponse:
    messured_weight: Decimal
    gross_fees: Fees
    net_fees: Fees
