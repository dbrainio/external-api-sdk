# external-api-sdk

SDK to enable usage of the Autocode/Dadata/etc APIs inside Docr

## Installation

`pip install git+https://github.com/dbrainio/external-api-sdk/archive/v0.3.1.zip`

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
  "brand_model_rus": "ФОРД ФОКУС",
  "type": "Комби (хэтчбек)",
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
      }
    ]
    ```

-   ##### FIO

    -   ###### Example

        ```python
        res = await api.suggest_fio('иванов ив')
        ```

    -   ###### Output

        ```json
        [
          {
            "value": "Иванов Иван",
            "unrestricted_value": "Иванов Иван",
            "data": {
                "surname": "Иванов",
                "name": "Иван",
                "patronymic": null,
                "gender": "MALE",
                "source": null,
                "qc": "0"
            }
          }
        ]
        ```

-   ##### Email

    -   ###### Example

        ```python
        res = await api.suggest_email('foo@ya')
        ```

    -   ###### Output

        ```json
        [
          {
            "value": "foo@yandex.ru",
            "unrestricted_value": "foo@yandex.ru",
            "data": {
               "local": "foo",
               "domain": "yandex.ru",
               "source": null,
               "qc": null
            }
          }
        ]
        ```

-   ##### FMS unit

    -   ###### Example

    ```python
    res = await api.suggest_fms_unit('Щукино')
    # or
    res = await api.find_fms_unit_by_code('770-098')
    ```

    -   ###### Output

    ```json
    [
        {
            "value": "ГУ МВД РОССИИ ПО Г. МОСКВЕ",
            "unrestricted_value": "ГУ МВД РОССИИ ПО Г. МОСКВЕ",
            "data": {
                "code": "770-098",
                "name": "ГУ МВД РОССИИ ПО Г. МОСКВЕ",
                "region_code": "77",
                "type": "0"
            }
        },
        {
            "value": "ОТДЕЛЕНИЕМ ПО РАЙОНУ ЩУКИНО ОУФМС РОССИИ ПО Г. МОСКВЕ В СЗАО",
            "unrestricted_value": "ОТДЕЛЕНИЕМ ПО РАЙОНУ ЩУКИНО ОУФМС РОССИИ ПО Г. МОСКВЕ В СЗАО",
            "data": {
                "code": "770-098",
                "name": "ОТДЕЛЕНИЕМ ПО РАЙОНУ ЩУКИНО ОУФМС РОССИИ ПО Г. МОСКВЕ В СЗАО",
                "region_code": "77",
                "type": "0"
            }
        },
        {
            "value": "ОТДЕЛЕНИЕМ УФМС РОССИИ ПО Г. МОСКВЕ ПО РАЙОНУ ЩУКИНО",
            "unrestricted_value": "ОТДЕЛЕНИЕМ УФМС РОССИИ ПО Г. МОСКВЕ ПО РАЙОНУ ЩУКИНО",
            "data": {
                "code": "770-098",
                "name": "ОТДЕЛЕНИЕМ УФМС РОССИИ ПО Г. МОСКВЕ ПО РАЙОНУ ЩУКИНО",
                "region_code": "77",
                "type": "0"
            }
        }
    ]
    ```

#### Clean

-   ##### Phone
-   ###### Example

    ```python
    res = await api.clean_phone(['9160212104', '8905 569 44 18'])
    ```

    -   ###### Output

    ```json
    [
      {
        "source": "9160212104",
        "type": "Мобильный",
        "phone": "+7 916 021-21-04",
        "country_code": "7",
        "city_code": "916",
        "number": "0212104",
        "extension": null,
        "provider": "ПАО \"Мобильные ТелеСистемы\"",
        "country": "Россия",
        "region": "Москва и Московская область",
        "city": null,
        "timezone": "UTC+3",
        "qc_conflict": 0,
        "qc": 0
      },
      {
        "source": "8905 569 44 18",
        "type": "Мобильный",
        "phone": "+7 905 569-44-18",
        "country_code": "7",
        "city_code": "905",
        "number": "5694418",
        "extension": null,
        "provider": "ПАО \"Вымпел-Коммуникации\"",
        "country": "Россия",
        "region": "Москва и Московская область",
        "city": null,
        "timezone": "UTC+3",
        "qc_conflict": 0,
        "qc": 0
      }
    ]
    ```

-   ##### Address
-   ###### Example

    ```python
    res = await.api.clean_address(["б0льщая татрская 35/3"])
    ```

    -   ###### Output

    ```json
    [
      {
        "source": "б0льщая татрская 35/3",
        "result": "г Москва, ул Татарская Б., д 35/3",
        "postal_code": "115184",
        "country": "Россия",
        "country_iso_code": "RU",
        "federal_district": "Центральный",
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
        "city_fias_id": null,
        "city_kladr_id": null,
        "city_with_type": null,
        "city_type": null,
        "city_type_full": null,
        "city": null,
        "city_area": "Центральный",
        "city_district_fias_id": null,
        "city_district_kladr_id": null,
        "city_district_with_type": "р-н Замоскворечье",
        "city_district_type": "р-н",
        "city_district_type_full": "район",
        "city_district": "Замоскворечье",
        "settlement_fias_id": null,
        "settlement_kladr_id": null,
        "settlement_with_type": null,
        "settlement_type": null,
        "settlement_type_full": null,
        "settlement": null,
        "street_fias_id": "343c2d32-444d-4a00-8a71-8765b4f5a26e",
        "street_kladr_id": "77000000000718700",
        "street_with_type": "ул Татарская Б.",
        "street_type": "ул",
        "street_type_full": "улица",
        "street": "Татарская Б.",
        "house_fias_id": null,
        "house_kladr_id": null,
        "house_type": "д",
        "house_type_full": "дом",
        "house": "35/3",
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
        "fias_id": "343c2d32-444d-4a00-8a71-8765b4f5a26e",
        "fias_code": "77000000000000071870000",
        "fias_level": "7",
        "fias_actuality_state": "0",
        "kladr_id": "77000000000718700",
        "capital_marker": "0",
        "okato": "45286560000",
        "oktmo": "45376000",
        "tax_office": "7705",
        "tax_office_legal": "7705",
        "timezone": "UTC+3",
        "geo_lat": "55.7384469",
        "geo_lon": "37.6362042",
        "beltway_hit": "IN_MKAD",
        "beltway_distance": null,
        "qc_geo": 1,
        "qc_complete": 9,
        "qc_house": 10,
        "qc": 3,
        "unparsed_parts": "ЛЬЩАЯ",
        "metro": [
          {
              "distance": 0.6,
              "line": "Замоскворецкая",
              "name": "Новокузнецкая"
          },
          {
              "distance": 0.7,
              "line": "Калининско-Солнцевская",
              "name": "Третьяковская"
          },
          {
              "distance": 0.7,
              "line": "Калужско-Рижская",
              "name": "Третьяковская"
          }
        ]
      }
    ]
    ```

-   ##### FIO
-   ###### Example

    ```python
    res = await api.clean_fio(["iван0в иван иван0ви4"])
    ```

-   ###### Output

    ```json
    [
      {
        "source": "iван0в и ван иван0ви4",
        "result": "Иванов И Ван Иван",
        "result_genitive": "Иванова И Вана Ивана",
        "result_dative": "Иванову И Вану Ивану",
        "result_ablative": "Ивановым И Ваном Иваном",
        "surname": "Иванов И Ван",
        "name": "Иван",
        "patronymic": null,
        "gender": "М",
        "qc": 1
      }
    ]
    ```

-   ##### Vehicle
-   ###### Example

    ```python
    res = await api.clean_vehicle(["land r0ver range r0ver"])
    ```

-   ###### Output

    ```json
    [
      {
        "source": "land r0ver range r0ver",
        "result": "LAND ROVER RANGE ROVER",
        "brand": "LAND ROVER",
        "model": "RANGE ROVER",
        "qc": 0
      }
    ]
    ```

-   ##### Passport
-   ###### Example

    ```python
    res = await api.clean_passport(["4 5 0 9 6 3 3 3 8 1 "])
    ```

-   ###### Output

    ```json
    [
      {
        "source": "4 5 0 9 6 3 3 3 8 1 ",
        "series": "45 09",
        "number": "633381",
        "qc": 0
      }
    ]
    ```

-   ##### Date

-   ###### Example

    ```python
    res = await api.clean_date(["1/6/16"])
    ```

-   ###### Output

    ```json
    [
      {
        "source": "1/6/16",
        "birthdate": "01.06.2016",
        "qc": 0
      }
    ]
    ```

-   ##### Email

-   ###### Example

    ```python
    res = await api.clean_email(["foo..@bar...com"])
    ```

-   ###### Output

    ```json
    [
      {
        "source": "foo..@bar...com",
        "email": "foo.@bar.com",
        "qc": 1
      }
    ]
    ```
