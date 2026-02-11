"""Services for JXHome integration."""
from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol

from .const import DOMAIN

# 服务的 schema
SERVICE_PARAM_CONFIG = "param_config"

SERVICE_SCHEMA = vol.Schema({
    vol.Required("entry_id"): str,
    vol.Optional("action"): vol.In(["read", "save"]),
    vol.Optional("current_ratio"): float,
    vol.Optional("voltage_ratio"): float,
})

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up JXHome services."""
    
    async def handle_param_config(call: ServiceCall) -> None:
        """处理参数配置服务调用。"""
        entry_id = call.data.get("entry_id")
        action = call.data.get("action", "read")
        
        # 获取配置条目
        entry = None
        for config_entry in hass.config_entries.async_entries(DOMAIN):
            if config_entry.entry_id == entry_id:
                entry = config_entry
                break
        
        if not entry:
            return
        
        if action == "read":
            # 读取参数
            hass.bus.async_fire(
                f"{DOMAIN}_param_read",
                {"entry_id": entry_id}
            )
        elif action == "save":
            # 保存参数
            current_ratio = call.data.get("current_ratio", 1.0)
            voltage_ratio = call.data.get("voltage_ratio", 1.0)
            
            # 更新选项
            hass.config_entries.async_update_entry(
                entry,
                options={
                    **entry.options,
                    "current_ratio": current_ratio,
                    "voltage_ratio": voltage_ratio,
                }
            )
            
            # 触发事件
            hass.bus.async_fire(
                f"{DOMAIN}_param_saved",
                {
                    "entry_id": entry_id,
                    "current_ratio": current_ratio,
                    "voltage_ratio": voltage_ratio,
                }
            )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_PARAM_CONFIG,
        handle_param_config,
        schema=SERVICE_SCHEMA,
    )

async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services."""
    hass.services.async_remove(DOMAIN, SERVICE_PARAM_CONFIG)
