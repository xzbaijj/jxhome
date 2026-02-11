from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class JXHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理杰效的 UI 配置流程"""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", default="杰效智能设备"): str,
            })
        )