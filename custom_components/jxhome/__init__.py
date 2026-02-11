from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN, PLATFORMS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置集成条目"""
    # 注册配置更新监听器
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry
    
    # 获取设备信息
    device_name = entry.data.get("name", "杰效主控板")
    device_id = entry.entry_id[:8]  # 使用entry_id的前8位作为设备ID
    
    # 获取参数信息
    current_ratio = entry.options.get("current_ratio", 1.0)
    voltage_ratio = entry.options.get("voltage_ratio", 1.0)
    
    # 注册设备 - 在hw_version中显示所有信息
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=device_name,
        manufacturer="杰效科技",
        model="JXHome Control Board",
        hw_version=f"硬件: MAC: {device_id}",
        sw_version=f"固件: v1.0.0 | 电流变比: {current_ratio} | 电压变比: {voltage_ratio}",
    )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """当选项流更新时，重新加载集成以应用新参数"""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载集成条目"""
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        del hass.data[DOMAIN][entry.entry_id]
    
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载集成条目"""
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        del hass.data[DOMAIN][entry.entry_id]
    
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)