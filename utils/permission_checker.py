import json
from typing import Any, Union, Dict
from nonebot import logger, on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import Event, PrivateMessageEvent, GROUP, MessageEvent, Bot
from nonebot.params import CommandArg
from nonebot.permission import Permission
from nonebot.rule import Rule
from nonebot.plugin import get_loaded_plugins
from nonebot.typing import T_State

from configs.path_config import PERMISSION_PATH, TEMP_PATH
from utils.msg_util import template_to_image, upload_for_shamrock
from utils.send_queue import message_queue

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
        self.command_description = {}
        self.load_permissions()
        self.default_permissions = {}

    def load_permissions(self) -> None:
        """从 JSON 文件加载权限数据"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.command_permissions = json.load(f)
            self.save_permissions()
            logger.info(f"已加载权限数据：{self.command_permissions}")
        except FileNotFoundError:
            self.command_permissions = {}
        except json.JSONDecodeError:
            logger.error(f"权限文件 {self.filepath} 格式错误")
            self.command_permissions = {}

    def save_permissions(self) -> None:
        """将权限数据保存到 JSON 文件"""
        for k, v in self.command_permissions.items():
            self.command_permissions[k] = dict(sorted(v.items(), key=lambda x: x[0]))
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
            logger.debug(f"群{group_id}用户{user_id}插件{plugin_name}.{command}权限为{cmd_perms}")
            return int(user_id) in cmd_perms
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

    def load_plugin_default_perm_and_desc(self) -> None:
        """加载所有插件的默认权限和说明"""
        loaded_plugins = get_loaded_plugins()
        loaded_plugins_list = list(loaded_plugins)
        loaded_plugins_list.sort(key=lambda x: x.name)
        for plugin in loaded_plugins_list:
            # 从插件模块获取插件名和默认权限
            plugin_name = getattr(plugin.module, "__plugin_cmd_name__", None)
            if plugin_name is None and plugin.name not in ["on_bot_connect", "nonebot_plugin_apscheduler",
                                                           "message_storage"]:
                logger.warning(f"插件 {plugin.module} 未设置 __plugin_cmd_name__ 属性，无法加载默认权限")
                continue
            default_permission = getattr(plugin.module, "__default_permission__", None)
            command_description = getattr(plugin.module, "__command_description__", None)
            logger.debug(f"插件 {plugin_name} 的默认权限：{default_permission}")
            logger.debug(f"插件 {plugin_name} 的命令说明：{command_description}")
            if default_permission is not None:
                self.default_permissions[plugin_name] = default_permission
            if command_description is not None:
                self.command_description[plugin_name] = command_description
        logger.info(f"已加载所有插件的默认权限：{self.default_permissions}")
        logger.info(f"已加载所有插件的命令说明：{self.command_description}")

    def update_permission(self, group_id: str, value: Dict[str, Any]) -> None:
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
            if hasattr(event, 'user_id'):
                user_id = event.user_id
            elif hasattr(event, 'sender_id'):
                user_id = event.sender_id
            else:
                user_id = None
                logger.error(f"未找到用户ID, event: {event}")
            return self.check_permission(group_id, user_id, plugin_name, command)

        return Rule(_role)


auth_manager = AuthManager(PERMISSION_PATH)

PM_Command = on_command("-pm",
                        rule=auth_manager.get_rule("admin"),
                        permission=GROUP,
                        priority=6,
                        block=True,
                        )


@PM_Command.handle()
async def handle_pm_command(bot: Bot, event: MessageEvent, state: T_State, args=CommandArg()):
    args = str(args).strip().split()
    logger.debug(f"收到 -pm 命令：{args}")
    response_msg = ""
    if len(args) < 2:  # 检查参数数量
        response_msg = "命令格式错误，请按照'-pm <插件名称/命令> <动作> <参数>'的格式输入。"
    else:
        plugin_or_cmd, action = args[0:2]
        param = args[2] if len(args) > 2 else None  # 参数可选
        logger.debug(f"插件/命令：{plugin_or_cmd}，动作：{action}，参数：{param}")
        group_permissions = auth_manager.command_permissions.get(str(event.group_id), {})
        if group_permissions is None:
            logger.warning(f"未找到群 {event.group_id} 的权限设置")
            response_msg = "未找到群权限设置。"
        else:
            for k, v in group_permissions.items():
                if isinstance(v, dict) and plugin_or_cmd in v:
                    if isinstance(group_permissions[k][plugin_or_cmd], bool):
                        if action not in ['on', 'off']:
                            response_msg = "错误：动作必须是'on'或'off'。"
                            break
                        else:
                            group_permissions[k][plugin_or_cmd] = True if action == 'on' else False
                            auth_manager.update_permission(str(event.group_id), group_permissions)
                            response_msg = f"{plugin_or_cmd}→{action}。"
                            break
                    elif isinstance(group_permissions[k][plugin_or_cmd], list):
                        if action not in ['add', 'del']:
                            response_msg = "错误：动作必须是'add'或'del'。"
                            break
                        elif not param or not param.isdigit():
                            response_msg = "错误：需要一个数字参数。"
                            break
                        else:
                            if action == 'add':
                                if int(param) not in group_permissions[k][plugin_or_cmd]:
                                    group_permissions[k][plugin_or_cmd].append(int(param))
                                    auth_manager.update_permission(str(event.group_id), group_permissions)
                                else:
                                    response_msg = f"用户{param}已经在{plugin_or_cmd}了。"
                                    break
                            else:
                                if int(param) in group_permissions[k][plugin_or_cmd]:
                                    group_permissions[k][plugin_or_cmd].remove(int(param))
                                    auth_manager.update_permission(str(event.group_id), group_permissions)
                                else:
                                    response_msg = f"用户{param}不在{plugin_or_cmd}中。"
                                    break

                            response_msg = f"用户{param}已{'添加到' if action == 'add' else '从'}{plugin_or_cmd}中{'' if action == 'add' else '删除'}。"
                            break
                elif plugin_or_cmd == k:
                    if isinstance(v, bool):
                        if action not in ['on', 'off']:
                            response_msg = "错误：动作必须是'on'或'off'。"
                            break
                        else:
                            group_permissions[k] = True if action == 'on' else False
                            auth_manager.update_permission(str(event.group_id), group_permissions)
                            response_msg = f"{plugin_or_cmd}→{action}。"
                            break
                    elif isinstance(v, list):
                        if action not in ['add', 'del']:
                            response_msg = "错误：动作必须是'add'或'del'。"
                            break
                        elif not param or not param.isdigit():
                            response_msg = "错误：需要一个数字参数。"
                            break
                        else:
                            if action == 'add':
                                if int(param) not in group_permissions[k]:
                                    group_permissions[k].append(int(param))
                                    auth_manager.update_permission(str(event.group_id), group_permissions)
                                else:
                                    response_msg = f"用户{param}已经在{plugin_or_cmd}了。"
                                    break
                            else:
                                if int(param) in group_permissions[k]:
                                    group_permissions[k].remove(int(param))
                                    auth_manager.update_permission(str(event.group_id), group_permissions)
                                else:
                                    response_msg = f"用户{param}不在{plugin_or_cmd}中。"
                                    break

                            response_msg = f"用户{param}已{'添加到' if action == 'add' else '从'}{plugin_or_cmd}中{'' if action == 'add' else '删除'}。"
                            break
                    else:
                        response_msg = "未知的权限类型。"
                        break
                else:
                    response_msg = "未找到指定的插件或命令。"
    message_queue.put((response_msg, event, bot))
    await PM_Command.finish()


PM_Info = on_fullmatch(("-pm help", "-pm status"),
                       rule=auth_manager.get_rule("admin"),
                       permission=GROUP,
                       priority=5,
                       block=True,
                       )


@PM_Info.handle()
async def handle_pm_info(bot: Bot, event: MessageEvent, state: T_State):
    response_msg = ""
    if event.raw_message == "-pm help":
        response_msg = """管理插件功能：
命令：-pm <插件名称/命令> <动作> <参数(可选)>
==============
如果插件名称是couplet，也就是对联功能，那-pm couplet on可以打开对联功能，-pm couplet off即为关闭对联功能。
===============
任命/取消任命群管：
-pm admin add/del <qq号>
===============
查看当前群权限设置：
-pm status
查看帮助：
-pm help
        """
    if event.raw_message == "-pm status":
        logger.debug(f"收到 -pm status 命令")
        # message_queue.put((f"正在生成图片，请稍后...", event, bot))
        group_id = event.group_id
        group_permissions = auth_manager.command_permissions.get(str(group_id), {})
        command_description = auth_manager.command_description
        plugins_data = []
        for plugin in group_permissions.keys():
            temp = {'name': plugin, 'descriptions': {}}
            if isinstance(group_permissions[plugin], bool):
                temp['descriptions'][command_description[plugin]] = group_permissions[plugin]
            if isinstance(group_permissions[plugin], dict):
                for cmd, perm in group_permissions[plugin].items():
                    temp['descriptions'][command_description[plugin][cmd]] = perm
            if isinstance(group_permissions[plugin], list):
                temp['descriptions'][command_description[plugin]] = group_permissions[plugin]
            plugins_data.append(temp)
        logger.debug(f"群{group_id}权限设置：{plugins_data}")
        extra_info = {
            'group_id': group_id,
            'powered_by': 'GuGuBot2.0'
        }
        path = TEMP_PATH
        file = f"permission_manager_{group_id}"
        logger.debug(f"开始渲染{plugins_data}")
        await template_to_image(template_name="permission_manager",
                                img_name=file,
                                plugins=plugins_data,
                                **extra_info)
        response_msg = await upload_for_shamrock(path, f"{file}.png")
    # else:
    #     response_msg = f"当前群权限设置：{auth_manager.command_permissions.get(str(event.group_id), '未设置')}"
    if response_msg:
        message_queue.put((response_msg, event, bot))
    await PM_Info.finish()
