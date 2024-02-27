from nonebot import on_fullmatch, on_message, on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.path_config import TEMP_PATH
from utils.msg_util import template_to_image, upload_for_shamrock
from utils.permission_checker import auth_manager
from utils import message_queue
from configs.config import SUPERUSERS

__plugin_name__ = "群权限管理"
__plugin_usage__ = f"""大概是个占位符吧"""
__plugin_cmd_name__ = "admin"
__command_description__ = "群权限管理"
__default_permission__ = [] + SUPERUSERS

MessageStorage = on_message(permission=GROUP,
                            rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                            priority=3,
                            block=False

                            )



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
        if group_permissions == {}:
            logger.warning(f"未找到群 {group_id} 的权限设置")
            response_msg = "未找到群权限设置。"
        else:
            command_description = auth_manager.command_description
            plugins_data = []
            for plugin in group_permissions.keys():
                if command_description.get(plugin) is None:
                    continue
                temp = {'name': plugin, 'descriptions': {}}
                if isinstance(group_permissions[plugin], bool):
                    temp['descriptions'][command_description[plugin]] = group_permissions[plugin]
                if isinstance(group_permissions[plugin], dict):
                    for cmd, perm in group_permissions[plugin].items():
                        if command_description.get(plugin) is None:
                            continue
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
