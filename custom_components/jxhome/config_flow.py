from homeassistant import config_entries
from homeassistant.core import callback, HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from .const import DOMAIN

class JXHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理初次添加集成时的逻辑"""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", default="杰效设备"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """关联选项流（点击配置按钮时调用）"""
        return JXHomeOptionsFlowHandler(config_entry)

    @staticmethod
    @callback
    def async_supports_device_config_entry_flow(config_entry):
        """支持设备级别配置"""
        return True

    async def async_step_options(self, user_input=None):
        """打开选项流 - 用于从按钮打开参数配置"""
        # 获取对应的配置条目
        entry_id = self.context.get("entry_id")
        if not entry_id:
            # 如果没有entry_id，从第一个config entry获取
            entries = self.hass.config_entries.async_entries(DOMAIN)
            if entries:
                entry = entries[0]
            else:
                return self.async_abort(reason="not_found")
        else:
            entry = self.hass.config_entries.async_get_entry(entry_id)
            if not entry:
                return self.async_abort(reason="not_found")
        
        # 显示options流
        options_handler = JXHomeOptionsFlowHandler(entry)
        return await options_handler.async_step_init(user_input)



class JXHomeOptionsFlowHandler(config_entries.OptionsFlow):
    """处理集成选项流的逻辑 - 在集成配置中显示参数配置选项"""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """选项流的起始步骤 - 直接显示参数编辑表单"""
        if user_input is not None:
            # 保存参数到配置条目选项
            config_data = {
                "current_ratio": user_input.get("current_ratio", 1.0),
                "voltage_ratio": user_input.get("voltage_ratio", 1.0),
            }
            
            # 发送参数到设备（通过 MQTT）
            await self._save_to_device(config_data)
            
            # 更新选项时使用 async_abort_entry_setup_complete()
            return self.async_abort_entry_setup_complete()
        
        # 获取当前的配置值，作为默认值
        current_current_ratio = self.config_entry.options.get("current_ratio", 1.0)
        current_voltage_ratio = self.config_entry.options.get("voltage_ratio", 1.0)
        
        # 定义参数编辑表单 - 直接显示修改表单
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("voltage_ratio", default=current_voltage_ratio): float,
                vol.Required("current_ratio", default=current_current_ratio): float,
            }),
            description_placeholders={
                "voltage_help": "电压互感器变比（用于校准电压测量值），默认为 1.0",
                "current_help": "电流互感器变比（用于校准电流测量值），默认为 1.0",
            }
        )

    async def _save_to_device(self, config_data):
        """通过 MQTT 保存参数到设备"""
        # TODO: 实现 MQTT 保存逻辑
        # 这里应该发送 MQTT 消息到设备，包含新的参数值
        pass
