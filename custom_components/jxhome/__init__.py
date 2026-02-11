from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, PLATFORMS
from .services import async_setup_services, async_unload_services

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 注册配置更新监听器
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry
    
    # 注册服务（仅在首次设置时）
    if not hass.data[DOMAIN].get("services_registered"):
        await async_setup_services(hass)
        hass.data[DOMAIN]["services_registered"] = True
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """当选项流更新时，重新加载集成以应用新参数"""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        del hass.data[DOMAIN][entry.entry_id]
    
    # 清理服务
    if hass.data[DOMAIN].get("services_registered"):
        await async_unload_services(hass)
        hass.data[DOMAIN]["services_registered"] = False
    
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)