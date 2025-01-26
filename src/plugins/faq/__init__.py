#
# from argparse import Namespace
#
# from nonebot import on_shell_command
# from nonebot.typing import T_State
# from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, GroupMessageEvent, PrivateMessageEvent, Message
#
# from .parser import faq_parser
# from .handle import faqhelp
# from configs.config import SUPERUSERS
#
# __plugin_name__ = "自助问答"
# __plugin_usage__ = None
# __plugin_cmd_name__ = "faq"
#
# __default_permission__ = {
#     "faq": True,
#     "faqstatus": ["Normal"],
#     "faqadmin": [] + SUPERUSERS
# }
# __command_description__ = {
#     "faq": "自助问答：问 [...]\n不过还没写好",
#     "faqstatus": "自助问答权限管理状态",
#     "faqadmin": "自助问答管理"
# }
# __plugin_info__ = {
#     "name": "自助问答",
#     "description": "快来教我回答问题吧，别忘了空格哦",
#     "usage": {
#         "维护 add <问题> <答案>": {"description": "添加问题", "example": "维护 add 这个问题 这个答案"},
#         "维护 edit <问题> <新的答案>": {"description": "修改答案", "example": "维护 edit 这个问题 新的答案"},
#         "维护 amend <问题> <追加的答案>": {"description": "追加答案", "example": "维护 amend 这个问题 补充回答"},
#         "维护 del <问题>": {"description": "删除问题", "example": "维护 del 这个问题"},
#         "维护 alias <问题> <别名>": {"description": "添加别名", "example": "维护 jAccount 甲亢"},
#         "维护 show <cmd>(可选)": {"description": "显示当前所有问题",
#                                   "example": "维护 show ans：显示所有问题和答案；\n维护 show alias：显示所有别名", },
#         "维护 visible <问题>": {"description": "使问题可见", "example": "维护 visible 这个问题"},
#         "维护 invisible <问题>": {"description": "使问题不可见", "example": "维护 invisible 这个问题"},
#         "维护 auth @某人": "授权用户维护列表",
#         "维护 revoke @某人": "取消授权用户维护列表",
#         "维护 admin": "显示授权用户列表",
#         "维护 help": "显示帮助",  # deprecated
#     },
#     "author": "厨师长",
#     "version": "2.0",
#     "permission": 2,
# }
#
# # Couplet = on_startswith("维护 ", permission=GROUP, priority=2)
#
#
# faq_operate = on_shell_command("-维护", parser=faq_parser, permission=GROUP, priority=2)
#
#
# # ask_question = on_startswith("问 ", permission=GROUP)
# #
# # COMMAND_REGEX = re.compile(r'\s*(\S+)')
#
#
# @faq_operate.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#     # if SELF_DEBUG_MODE:
#     #     print(state)
#     args: Namespace = state['_args']
#     args.user = event.user_id
#     args.group = event.group_id if isinstance(event, GroupMessageEvent) else None
#     # if SELF_DEBUG_MODE:
#     #     print(args)
#     #     print(str(args))
#     #     # <ParserExit status=2 message=faq add: error: the following arguments are required: answer
#     #     # >
#     #     print(type(args))  # <class 'nonebot.exception.ParserExit'>
#     #     print("************************")
#     args.is_group = isinstance(event, GroupMessageEvent)
#     args.is_user = isinstance(event, PrivateMessageEvent)
#
#     if hasattr(args, "handle"):
#         message = await args.handle(args)
#         # img = await textToImage(message, cut=100)
#         # await bot.send(event, image(c=img))
#
#         await faq_operate.finish(Message(message))
#     else:
#         await faq_operate.finish(Message('咦？可能参数有问题？'))
#
# # TODO: 需要一个class来管理问答库，字段包括主问题，答案，别名，可见性，添加时间
# # 1. 优化回答的匹配算法
# # 2. 优化回答的匹配算法
#
# #
# # @ask_question.handle()
# # async def _(bot: Bot, event: MessageEvent, state: T_State):
# #     group = event.group_id
# #     QUESTIONS: dict = {}
# #     QUESTIONS_KEY: dict = {}
# #     ADMINS: list = []
# #     # TODO: 从数据库获取对应的问答库
# #
# #     question = event.raw_message.replace('问 ')
# #     question = COMMAND_REGEX.search(question).groups()[0]
# #
# #     (match_choice, score, choice_idx) = fuzz_match.extractOne(
# #         question, QUESTIONS_KEY.keys())
# #     match_choice = QUESTIONS_KEY[match_choice]
# #     # log.info(
# #     #     ','.join([str(x) for x in [question, match_choice, '{:.01f}'.format(score)]]))
# #     if score < 45:
# #         return f'我可能还不知道，教教我qwq'
# #     if score < 60:
# #         return f'不如试着问问[{match_choice}]？'
# #
# #     return QUESTIONS[match_choice]['answer'] + f'【{match_choice}】'
