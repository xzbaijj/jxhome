"""Button entities for JXHome integration."""
from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry, SOURCE_OPTIONS
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities."""
    async_add_entities([
        JXHomeParamConfigButton(hass, entry),
    ])


class JXHomeParamConfigButton(ButtonEntity):
    """设置按钮 - 点击打开参数配置对话框"""

    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_icon = "mdi:cog"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_param_config_button"
        self._attr_name = "设置"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.data.get("name", "杰效主控板"),
            "manufacturer": "杰效科技",
        }

    async def async_press(self) -> None:
        """点击按钮时打开参数配置对话框"""
        try:
            # 打开选项流，显示参数配置对话框
            await self.hass.config_entries.flow.async_init(
                DOMAIN,
                context={
                    "source": SOURCE_OPTIONS,
                    "entry_id": self._entry.entry_id,
                },
                data=None,
            )
        except Exception as err:
            raise HomeAssistantError(f"无法打开参数配置: {err}") from err
