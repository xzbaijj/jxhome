from homeassistant import config_entries
from homeassistant.core import callback
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


class JXHomeOptionsFlowHandler(config_entries.OptionsFlow):
    """处理‘配置参数’弹出面板的逻辑"""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """选项流的起始步骤"""
        if user_input is not None:
            # 保存修改后的参数
            return self.async_create_entry(title="", data=user_input)

        # 获取当前的配置值，作为默认值
        current_temp_offset = self.config_entry.options.get("temp_offset", 0.0)
        current_scan_interval = self.config_entry.options.get("scan_interval", 30)

        # 定义弹窗中的表单
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("temp_offset", default=current_temp_offset): float,
                vol.Optional("scan_interval", default=current_scan_interval): int,
            })
        )