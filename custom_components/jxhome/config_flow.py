from homeassistant import config_entries
from .const import DOMAIN

class JXHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理‘杰效’集成的配置流程"""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """用户点击‘添加集成’时调用的第一步"""
        if user_input is not None:
            # 创建集成条目
            return self.async_create_entry(title="杰效设备", data={})

        # 显示一个确认添加的表单
        return self.async_show_form(step_id="user")