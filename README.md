# external-api-sdk

SDK to enable usage of the Autocode/Dadata/etc APIs inside Docr

## Installation

`pip install git+https://github.com/dbrainio/hitl-sdk/archive/v0.2.0.zip`

## Usage

### Errors handling

If any API wrapper fails to do the job in raises `APIConnectorException`.
It has `status` attribute, where http response code is stored and `payload` attribute where lies full api json response.

### Autocode

#### Example

```python
from externalapi import Autocode

api = Autocode("SECRET KEY")
res = await api.get_vehicle_info("VIN_NUMBER")
await api.close()
# or
async with Autocode("SECRET KEY") as api:
  res = await api.get_vehicle_info("VIN_NUMBER")

# if async/await is not an option use run_sync:
from externalapi.utils import run_sync

res = run_sync(api.get_vehicle_info("VIN_NUMBER"))
```

#### Output

```json
{
  "vin": "Z6F5XXEEC5FJ05240",
  "reg_num": "М646ТН48",
  "sts": "4833889866",
  "pts": "47НХ565289",
  "last_registered": {
    "region": "Липецкая Область",
    "city": "Завальное С.",
    "owner": "PERSON",
    "date_from": "2016-03-30 00:00:00"
  },
  "brand": "Ford",
  "model": "Focus",
  "year": 2015,
  "color": "Белый",
  "weight": {
    "netto": 1269,
    "max": 1825
  },
  "engine": {
    "fuel": "Бензиновый",
    "volume": 1598,
    "power": {
      "hp": 125.08,
      "kw": 92
    },
    "model": "PNDD"
  },
  "category": "B"
}
```

### Dadata

#### Suggest

-   ##### Address

    -   ###### Example

    ```python
    res = await api.suggest_address('нижегородская улица')
    ```

    -   ###### Output

    ```json
    [
      {
        "value": "г Москва, ул Нижегородская",
        "unrestricted_value": "г Москва, ул Нижегородская",
        "data": {
          "postal_code": null,
          "country": "Россия",
          "country_iso_code": "RU",
          "federal_district": null,
          "region_fias_id": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
          "region_kladr_id": "7700000000000",
          "region_iso_code": "RU-MOW",
          "region_with_type": "г Москва",
          "region_type": "г",
          "region_type_full": "город",
          "region": "Москва",
          "area_fias_id": null,
          "area_kladr_id": null,
          "area_with_type": null,
          "area_type": null,
          "area_type_full": null,
          "area": null,
          "city_fias_id": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
          "city_kladr_id": "7700000000000",
          "city_with_type": "г Москва",
          "city_type": "г",
          "city_type_full": "город",
          "city": "Москва",
          "city_area": null,
          "city_district_fias_id": null,
          "city_district_kladr_id": null,
          "city_district_with_type": null,
          "city_district_type": null,
          "city_district_type_full": null,
          "city_district": null,
          "settlement_fias_id": null,
          "settlement_kladr_id": null,
          "settlement_with_type": null,
          "settlement_type": null,
          "settlement_type_full": null,
          "settlement": null,
          "street_fias_id": "4de7e371-4cef-4945-ab3a-9d040e8b5101",
          "street_kladr_id": "77000000000007100",
          "street_with_type": "ул Нижегородская",
          "street_type": "ул",
          "street_type_full": "улица",
          "street": "Нижегородская",
          "house_fias_id": null,
          "house_kladr_id": null,
          "house_type": null,
          "house_type_full": null,
          "house": null,
          "block_type": null,
          "block_type_full": null,
          "block": null,
          "flat_type": null,
          "flat_type_full": null,
          "flat": null,
          "flat_area": null,
          "square_meter_price": null,
          "flat_price": null,
          "postal_box": null,
          "fias_id": "4de7e371-4cef-4945-ab3a-9d040e8b5101",
          "fias_code": null,
          "fias_level": "7",
          "fias_actuality_state": null,
          "kladr_id": "77000000000007100",
          "geoname_id": null,
          "capital_marker": "0",
          "okato": null,
          "oktmo": "45381000",
          "tax_office": null,
          "tax_office_legal": null,
          "timezone": null,
          "geo_lat": null,
          "geo_lon": null,
          "beltway_hit": null,
          "beltway_distance": null,
          "metro": null,
          "qc_geo": null,
          "qc_complete": null,
          "qc_house": null,
          "history_values": null,
          "unparsed_parts": null,
          "source": null,
          "qc": null
        }
      },
    ]
    ```

-   ##### FIO

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Email

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### FMS unit

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

#### Clean

-   ##### Phone

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Address

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### FIO

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Vehicle

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Passport

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Date

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```

-   ##### Email

    -   ###### Example

    ```python

    ```

    -   ###### Output

    ```json

    ```
