from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfElectricPotential, UnitOfElectricCurrent
from .const import DOMAIN, SENSOR_TYPE_VOLTAGE, SENSOR_TYPE_CURRENT

async def async_setup_entry(hass, entry, async_add_entities):
    """设置传感器实体"""
    sensors = [
        JXHomeSensor(entry),
        JXHomeVoltageSensor(entry),
        JXHomeCurrentSensor(entry),
    ]
    async_add_entities(sensors, True)

class JXHomeSensor(SensorEntity):
    """杰效状态传感器"""
    
    def __init__(self, entry):
        self._attr_name = f"{entry.data.get('name')} 状态"
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._entry_id = entry.entry_id
        self._config_entry = entry

    @property
    def state(self):
        return "在线"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._config_entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
            "configuration_url": f"/config/devices/device/{self._entry_id}",
        }

class JXHomeVoltageSensor(SensorEntity):
    """杰效电压传感器"""
    
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    
    def __init__(self, entry):
        self._attr_name = f"{entry.data.get('name')} 电压"
        self._attr_unique_id = f"{entry.entry_id}_voltage"
        self._entry_id = entry.entry_id
        self._config_entry = entry
        self._state = 220  # 默认电压值，可根据实际情况修改

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._config_entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
            "configuration_url": f"/config/devices/device/{self._entry_id}",
        }

class JXHomeCurrentSensor(SensorEntity):
    """杰效电流传感器"""
    
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    
    def __init__(self, entry):
        self._attr_name = f"{entry.data.get('name')} 电流"
        self._attr_unique_id = f"{entry.entry_id}_current"
        self._entry_id = entry.entry_id
        self._config_entry = entry
        self._state = 0  # 默认电流值，可根据实际情况修改

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._config_entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
            "configuration_url": f"/config/devices/device/{self._entry_id}",
        }