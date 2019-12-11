# external-api-sdk

SDK to enable usage of the Autocode/Dadata/etc APIs inside Docr

## Installation

`pip install git+https://github.com/dbrainio/external-api-sdk`

## Usage

### Autocode

```python
from externalapi import Autocode

api = Autocode('SECRET KEY')
res = await api.get_vehicle_info('VIN_NUMBER')
await api.close()
# or
async with Autocode('SECRET KEY') as api:
  res = await api.get_vehicle_info('VIN_NUMBER')

# if async/await is not an option use run_sync:
from externalapi.utils import run_sync

res = run_sync(api.get_vehicle_info('VIN_NUMBER'))
```

Output: `None` or

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
