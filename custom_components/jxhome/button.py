"""Button entities for JXHome integration."""
from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities."""
    # 按钮已移除 - 参数配置通过设备的选项流访问（设备页面的设置菜单）
    # 用户可以在设备页面右上角的菜单中点击"设置"来打开参数配置

