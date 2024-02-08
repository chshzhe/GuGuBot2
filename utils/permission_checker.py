import json
from typing import Any, Union
from nonebot import logger
from nonebot.adapters.onebot.v11 import Event, PrivateMessageEvent
from nonebot.permission import Permission
from nonebot.rule import Rule
from nonebot.plugin import get_loaded_plugins
from configs.path_config import PERMISSION_PATH

"""
{
    "group_id": 
    {
        "plugin_name": 
        {
            "cmd": True/"False
            "cmd": ["user_id"]
        },
        "plugin_name": True/False
        "plugin_name": ["user_id"]
    }
}

"""


class AuthManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.command_permissions = {}
        self.load_permissions()
        self.default_permissions = {}

    def load_permissions(self):
        """从 JSON 文件加载权限数据"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.command_permissions = json.load(f)
            logger.info(f"已加载权限数据：{self.command_permissions}")
        except FileNotFoundError:
            self.command_permissions = {}
        except json.JSONDecodeError:
            logger.error(f"权限文件 {self.filepath} 格式错误")
            self.command_permissions = {}

    def save_permissions(self):
        """将权限数据保存到 JSON 文件"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.command_permissions, f, ensure_ascii=False, indent=4)

    def check_permission(self, group_id: str, user_id: str, plugin_name: str, command: Union[str, None] = None) -> bool:
        """检查用户是否有执行命令的权限
        :param group_id: 群号
        :param user_id: 用户 QQ 号
        :param plugin_name: 插件名
        :param command: 命令(可选)
        """
        group_perms = self.command_permissions.get(group_id, {})
        if group_perms is None:
            logger.warning(f"未找到群 {group_id} 的权限设置，启用默认权限")
            self.update_permission(group_id, self.default_permissions)
            return self.check_permission(group_id, user_id, plugin_name, command)
        else:
            plugin_perms = group_perms.get(plugin_name, None)
            if plugin_perms is None:
                logger.warning(f"群{group_id}未找到插件{plugin_name}的权限设置，启用默认权限")
                group_perms[plugin_name] = self.default_permissions.get(plugin_name, {})
                self.update_permission(group_id, group_perms)
                return self.check_permission(group_id, user_id, plugin_name, command)
            else:
                if command is not None:
                    cmd_perms = plugin_perms.get(command, None)
                    if cmd_perms is None:
                        logger.warning(f"群{group_id}未找到插件{plugin_name}.{command} 的权限设置，启用默认权限")
                        group_perms[plugin_name][command] = self.default_permissions.get(plugin_name, {}).get(command,
                                                                                                              False)
                        self.update_permission(group_id, group_perms)
                        return self.check_permission(group_id, user_id, plugin_name, command)
                else:
                    cmd_perms = plugin_perms

        if isinstance(cmd_perms, list):
            return user_id in cmd_perms
        logger.debug(f"群{group_id}用户{user_id}插件{plugin_name}.{command}权限为{cmd_perms}")
        return cmd_perms  # If it's a boolean, return it directly

    def get_permission(self, plugin_name: str, command: Union[str, None] = None) -> Permission:
        """获取一个检查特定命令权限的 Permission 对象
        :param plugin_name: 插件名
        :param command: 命令(可选)
        :return: Permission 对象

        """

        async def _permission(event: Event) -> bool:
            if isinstance(event, PrivateMessageEvent):
                return True
            group_id = str(event.group_id)
            user_id = str(event.user_id)
            return self.check_permission(group_id, user_id, plugin_name, command)

        return Permission(_permission)

    def load_plugin_default_permissions(self):
        """加载所有插件的默认权限"""
        loaded_plugins = get_loaded_plugins()
        for plugin in loaded_plugins:
            # 从插件模块获取插件名和默认权限
            plugin_name = getattr(plugin.module, "__plugin_cmd_name__", None)
            if plugin_name is None and plugin.name not in ["on_bot_connect", "nonebot_plugin_apscheduler",
                                                           "message_storage"]:
                logger.warning(f"插件 {plugin.module} 未设置 __plugin_cmd_name__ 属性，无法加载默认权限")
                continue
            default_permission = getattr(plugin.module, "__default_permission__", None)
            logger.debug(f"插件 {plugin_name} 的默认权限：{default_permission}")
            if default_permission is not None:
                self.default_permissions[plugin_name] = default_permission
        logger.info(f"已加载所有插件的默认权限：{self.default_permissions}")

    def update_permission(self, group_id: str, value: Any):
        """更新权限"""
        self.command_permissions[group_id] = value
        self.save_permissions()
        self.load_permissions()
        logger.info(f"更新群 {group_id} 的权限设置：{value}")

    def get_rule(self, plugin_name: str, command: Union[str, None] = None) -> Rule:
        """获取一个检查特定命令权限的 Rule 对象
        :param plugin_name: 插件名
        :param command: 命令(可选)
        :return: Permission 对象

        """

        async def _role(event: Event) -> bool:
            if isinstance(event, PrivateMessageEvent):
                return True
            group_id = str(event.group_id)
            user_id = str(event.user_id)
            return self.check_permission(group_id, user_id, plugin_name, command)

        return Rule(_role)


auth_manager = AuthManager(PERMISSION_PATH)
