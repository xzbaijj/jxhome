from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([JXHomeSensor(entry)], True)

class JXHomeSensor(SensorEntity):
    def __init__(self, entry):
        self._attr_name = f"{entry.data.get('name')} 状态"
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def state(self):
        return "在线"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "jxhome_fixed_id")},
            "name": "杰效主控板",
            "manufacturer": "杰效科技",
        }