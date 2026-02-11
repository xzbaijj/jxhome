from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfElectricPotential, UnitOfElectricCurrent
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, SENSOR_TYPE_VOLTAGE, SENSOR_TYPE_CURRENT

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: "AddEntitiesCallback") -> None:
    """设置传感器实体"""
    sensors = [
        JXHomeSensor(entry),
        JXHomeVoltageSensor(entry),
        JXHomeCurrentSensor(entry),
        JXHomeVoltageRatioSensor(entry, hass),
        JXHomeCurrentRatioSensor(entry, hass),
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
        }


class JXHomeVoltageRatioSensor(SensorEntity):
    """杰效电压互感器变比传感器"""
    
    _attr_icon = "mdi:resistor-nodes"
    
    def __init__(self, entry: ConfigEntry, hass: HomeAssistant):
        self._attr_name = f"{entry.data.get('name')} 电压互感器变比"
        self._attr_unique_id = f"{entry.entry_id}_voltage_ratio"
        self._entry_id = entry.entry_id
        self._config_entry = entry
        self.hass = hass
        self._attr_should_poll = False
        
        # 监听配置条目选项更新
        self._unsub_options = entry.add_update_listener(self._async_options_updated)

    async def _async_options_updated(self, hass: HomeAssistant, entry: ConfigEntry):
        """配置选项更新时的回调"""
        self.async_write_ha_state()

    @property
    def state(self):
        """返回当前电压互感器变比"""
        return self._config_entry.options.get("voltage_ratio", 1)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._config_entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
        }

    async def async_will_remove_from_hass(self) -> None:
        """移除实体时清理"""
        self._unsub_options()


class JXHomeCurrentRatioSensor(SensorEntity):
    """杰效电流互感器变比传感器"""
    
    _attr_icon = "mdi:resistor-nodes"
    
    def __init__(self, entry: ConfigEntry, hass: HomeAssistant):
        self._attr_name = f"{entry.data.get('name')} 电流互感器变比"
        self._attr_unique_id = f"{entry.entry_id}_current_ratio"
        self._entry_id = entry.entry_id
        self._config_entry = entry
        self.hass = hass
        self._attr_should_poll = False
        
        # 监听配置条目选项更新
        self._unsub_options = entry.add_update_listener(self._async_options_updated)

    async def _async_options_updated(self, hass: HomeAssistant, entry: ConfigEntry):
        """配置选项更新时的回调"""
        self.async_write_ha_state()

    @property
    def state(self):
        """返回当前电流互感器变比"""
        return self._config_entry.options.get("current_ratio", 1)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._config_entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
        }

    async def async_will_remove_from_hass(self) -> None:
        """移除实体时清理"""
        self._unsub_options()