from datetime import datetime
from decimal import Decimal

from .utils import (
    DistributionBranch,
    Fees,
    FeesResponse,
    ImpositionBranch,
    LoginResponse,
    Metadata,
    Order,
    Package,
    RenditionBranch,
    Shipment,
    SubmitShipmentResponse,
    SupplyBranch,
)


def serialize_fees_params(
    postalcode: str,
    contract: str,
    client: str,
    office: str,
    order: Order,
) -> dict:
    return {
        "cpDestino": postalcode,
        "contrato": contract,
        "cliente": client,
        "sucursalOrigen": office,
        "bultos[0][valorDeclarado]": order.price,
        "bultos[0][volumen]": order.volume,
        "bultos[0][kilos]": order.weight / 1000,
    }


def serialize_fees_response(
    http_response: dict,
) -> FeesResponse:
    return FeesResponse(
        messured_weight=Decimal(http_response["pesoAforado"]),
        gross_fees=Fees(
            distribution_insurance=Decimal(
                http_response["tarifaConIva"]["seguroDistribucion"]
            ),
            distribution=Decimal(http_response["tarifaConIva"]["distribucion"]),
            total=Decimal(http_response["tarifaConIva"]["total"]),
        ),
        net_fees=Fees(
            distribution_insurance=Decimal(
                http_response["tarifaSinIva"]["seguroDistribucion"]
            ),
            distribution=Decimal(http_response["tarifaSinIva"]["distribucion"]),
            total=Decimal(http_response["tarifaSinIva"]["total"]),
        ),
    )


def serialize_login_repsonse(http_response: dict) -> LoginResponse:
    return LoginResponse(
        token=http_response["token"],
        refresh=http_response["token"],
    )


def update_shipment_dictionary(shipment, shipment_dict, attrs_map):
    for field in attrs_map:
        temp_meta = []
        meta = getattr(shipment, field[1]).meta or []
        for data in meta:
            temp_meta.append({"meta": data.key, "contenido": data.value})

        shipment_dict[field[0]]["postal"].update({"componentesDeDireccion": temp_meta})


def serialize_submit_shipment_data(shipment: Shipment) -> dict:
    _attrs_map = [("origen", "sender_address"), ("destino", "receiver_address")]

    _serialized_shipment = {
        "contrato": shipment.contract,
        "origen": {
            "postal": {
                "codigoPostal": shipment.sender_address.postalcode,
                "calle": shipment.sender_address.street,
                "numero": shipment.sender_address.number,
                "localidad": shipment.sender_address.province,
                "componentesDeDireccion": [],
            },
        },
        "destino": {
            "postal": {
                "codigoPostal": shipment.receiver_address.postalcode,
                "calle": shipment.receiver_address.street,
                "numero": shipment.receiver_address.number,
                "localidad": shipment.receiver_address.province,
                "componentesDeDireccion": [],
            },
        },
        "remitente": {
            "nombreCompleto": f"{shipment.sender_info.first_name} {shipment.receiver_info.last_name}",
            "email": shipment.sender_info.email,
            "documentoTipo": shipment.sender_info.document_type,
            "documentoNumero": shipment.sender_info.document_number,
            "telefonos": [
                {
                    "tipo": 1,
                    "numero": shipment.sender_info.phone_number,
                }
            ],
        },
        "destinatario": [
            {
                "nombreCompleto": f"{shipment.receiver_info.first_name} {shipment.receiver_info.last_name}",
                "email": shipment.receiver_info.email,
                "documentoTipo": shipment.receiver_info.document_type,
                "documentoNumero": shipment.receiver_info.document_number,
                "telefonos": [
                    {
                        "tipo": 1,
                        "numero": shipment.receiver_info.phone_number,
                    }
                ],
            }
        ],
        "bultos": [
            {
                "kilos": shipment.order.weight,
                "volumenCm": shipment.order.volume,
                "valorDeclaradoConImpuestos": shipment.order.price,
            }
        ],
    }

    update_shipment_dictionary(shipment, _serialized_shipment, _attrs_map)

    return _serialized_shipment


def serialize_submit_shipment_response(http_response: dict) -> SubmitShipmentResponse:
    distribution_branch = http_response["sucursalDeDistribucion"]
    packages = []

    for p in http_response["bultos"]:
        metadata = [Metadata(link["meta"], link["contenido"]) for link in p["linking"]]
        package = Package(
            p["numeroDeBulto"], p["numeroDeEnvio"], p["totalizador"], metadata
        )
        packages.append(package)

    return SubmitShipmentResponse(
        http_response["estado"],
        http_response["tipo"],
        DistributionBranch(
            distribution_branch["nomenclatura"],
            distribution_branch["descripcion"],
            distribution_branch["id"],
        ),
        RenditionBranch(),
        ImpositionBranch(),
        SupplyBranch(),
        datetime.fromisoformat(http_response["fechaCreacion"]),
        http_response["numeroDePermisionaria"],
        http_response["descripcionServicio"],
        packages,
        http_response["agrupadorDeBultos"],
        http_response["etiquetasPorAgrupador"],
    )
