# external-api-sdk
SDK to enable usage of the Autocode/Dadata/etc APIs inside Docr

## Installation
`pip install git+https://github.com/dbrainio/external-api-sdk`

## Usage
### Autocode
```python
from externalapi import autocode
res = autocode.get_vehicle_info_sync('VIN_NUMBER')
res = await autocode.get_vehicle_info_async('VIN_NUMBER')
```
### Dadata
