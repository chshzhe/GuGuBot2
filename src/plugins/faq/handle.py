# from nonebot.log import logger
#
# import re
# from argparse import Namespace
# from typing import Tuple
# from configs.config import SELF_DEBUG_MODE
# from msg_db.faq_operation import *
# from msg_db.groupconfig_operation import *
# from msg_db.model import Database
#
#
# class GroupFAQ:
#     """
#     问答库
#     """
#
#     def __init__(self, group_id: int):
#
#         self.group_id = group_id
#         self.db_model = Database("gugubot_faq")
#         self.db_model.create_database()
#         self.FAQ = {}
#         self.faq_admin = []
#         self.faq_db_name = f"faq_{group_id}"
#         self.admin_db_name = f"admin_{group_id}"
#         self.auth_type = "Normal"
#
#         """
#         从数据库 `gugubot_faq.redirect_<qq_id>` 中获取重定向的问答库名 db_name 和 auth_type
#         从 `gugubot_faq.faq_<db_name>` 中获取问答库
#         从 `gugubot_faq.admin_<db_name>` 中获取问答库维护列表
#         从 `gugubot_faq.faq_<db_name>_history` 中获取问答库历史记录
#
#
#         """
#
#     async def get_group_config(self) -> Tuple[str, List[int], List[int], Dict[str, str], str]:
#         """
#         根据groupId获取config和db name
#         :param groupId: 群ID
#         :return: 鉴权类型，问答库维护列表，问答库
#         """
#         group_config = await get_group_config(self.group_id)
#         if group_config is None:
#             return "all", [], [], {}, "faq"
#         else:
#             return group_config[0], group_config[1], group_config[2], group_config[3], group_config[4]
# #
# from configs.path_config import DATABASE_PATH
# from utils import SQLiteDB
#
#
# class FAQ_db(SQLiteDB):
#     def __init__(self):
#         super().__init__(DATABASE_PATH + "faq.msg_db")
#         super().delete()






#
# async def get_group_config(groupId: int) -> Tuple[str, List[int], List[int], Dict[str, str], str]:
#     """
#     根据groupId获取config和db name
#     :param groupId: 群ID
#     :return: 鉴权类型，问答库维护列表，问答库
#     """
#     # TODO: 根据groupId获取config和db name
#
#     groupconfig = await GetGroupConfig(groupId)
#     auth_mode = groupconfig['faq_mode']
#     faq_db_name = groupconfig['faq_db_name']
#     faq_admins = await GetFAQAdmin(groupId)
#     group_admins = await GetGroupAdmin(groupId)
#     QUESTIONS = await GetFaqItems(faq_db_name)
#
#     if SELF_DEBUG_MODE:
#         print(f"*******************************\n"
#               f"Group: {groupId}\n"
#               f"Auth Mode: {auth_mode}\n"
#               f"FAQ Admins: {faq_admins}\n"
#               f"Group Admins: {group_admins}\n"
#               f"FAQ DB Name: {faq_db_name}\n"
#               f"*******************************\n"
#               )
#
#     return auth_mode, faq_admins, group_admins, QUESTIONS, faq_db_name
#
#
# async def add(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is ADD")
#         if not hasattr(args, "question") or not hasattr(args, "answer"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     question = args.question
#     answer = ' '.join(args.answer)
#
#     if SELF_DEBUG_MODE:
#         print(f"ADD\nGroup: {group}\nUser: {user}\nQuestion: {question}\nAnswer: {answer}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#     if 'CQ:image' in question:
#         return '问题标题内带有图片，请修改后再添加'
#     if not answer:
#         return f'请填写回答'
#     if question not in QUESTIONS:
#         flag = await AddFaqItem(table_name=db_table, question=question, answer=answer)
#         if flag:
#             return f'问题添加成功，问题：《{question}》，回答：《{answer}》'
#         else:
#             return f'问题添加失败，请查看日志'
#     else:
#         return f'问题已存在，请进行更新qwq'
#
#
# async def edit(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is EDIT")
#         if not hasattr(args, "question") or not hasattr(args, "new_answer"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     question = args.question
#     new_answer = ' '.join(args.new_answer)
#     if SELF_DEBUG_MODE:
#         print(f"EDIT\nGroup: {group}\nUser: {user}\nQuestion: {question}\nAnswer: {new_answer}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#     if not new_answer:
#         return f'请填写回答'
#     if question in QUESTIONS:
#         # if type(QUESTIONS[question]) == str:
#         #     QUESTIONS[question] = {}
#         #     QUESTIONS[question]['alias'] = [question]
#
#         flag = await EditFaqAnswer(db_table, question, new_answer)
#
#         # old_ans = QUESTIONS[question]['answer']
#         # QUESTIONS[question]['answer'] = new_answer
#         # save_questions(db_name)
#         # log.warning(
#         #     f'question 【{cmd_q}】 answer updated【{old_ans}】->【{cmd_a}】')
#         if flag:
#             return f'回答更新成功，问题：《{question}》，新回答：《{new_answer}》'
#         else:
#             return f'回答编辑失败，请查看日志'
#     else:
#         return f'问题【{question}】尚不存在，请先添加'
#
#
# async def amend(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is AMEND")
#         if not hasattr(args, "question") or not hasattr(args, "amend_answer"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     question = args.question
#     amend_answer = ' '.join(args.amend_answer)
#
#     if SELF_DEBUG_MODE:
#         print(f"AMEND\nGroup: {group}\nUser: {user}\nQuestion: {question}\nAnswer: {amend_answer}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#
#     if question in QUESTIONS:
#         # if type(QUESTIONS[question]) == str:
#         #     QUESTIONS[question] = {}
#         #     QUESTIONS[question]['alias'] = [question]
#         # QUESTIONS[question]['answer'] += amend_answer
#         # answer = QUESTIONS[question]['answer']
#         newAnswer = await AmendFaqAnswer(db_table, question, amend_answer)
#         # save_questions(db_name)
#         # log.warning(
#         #     f'question 【{cmd_q}】 answer amended 【{old_ans}】 -> 【{cmd_a}】')
#         if newAnswer:
#             return f'回答补充成功，问题：《{question}》，新回答：《{newAnswer}》'
#         else:
#             return f'回答补充失败，请查看日志'
#     else:
#         return f'问题【{question}】尚不存在，请先添加'
#
#     # return "Here is AMEND function return"
#
#
# async def delete(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is DEL")
#         if not hasattr(args, "question"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     question = args.question
#
#     if SELF_DEBUG_MODE:
#         print(f"DELETE\nGroup: {group}\nUser: {user}\nQuestion: {question}\n")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#
#     if question in QUESTIONS:
#         flag = await DeleteFaqItem(db_table, question)
#         if flag:
#             return f'问题《{question}》删除成功'
#         else:
#             return f'问题删除失败，请查看日志'
#     else:
#         return f'问题不存在，无法删除'
#
#     # return "Here is DELETE function return"
#
#
# async def alias(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is ALIAS")
#         if not hasattr(args, "question") or not hasattr(args, "alias"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     question = args.question
#     aliasList = args.alias
#     if SELF_DEBUG_MODE:
#         print(f"ALIAS\nGroup: {group}\nUser: {user}\nQuestion: {question}\nAlias: {aliasList}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#     if not aliasList:
#         return "请输入别名"
#     if question in QUESTIONS:
#         # for alias in aliasList:
#         #     if alias not in QUESTIONS[question]['alias']:
#         #         QUESTIONS[question]['alias'].append(alias)
#         #         # save_questions(db_name)
#         #         # log.warning(
#         #         #     f'question alias【{cmd_q}】 = 【{cmd_a}】added!')
#         newAlias = await AliasFaqItem(db_table, question, aliasList)
#         if newAlias:
#             return f"问题别名添加成功，问题：《{question}》，别名：《{'、'.join(newAlias)}》"
#         else:
#             return f"问题别名添加失败，请查看日志"
#     else:
#         return f'问题尚不存在，请先添加'
#     # return "Here is ALIAS function return"
#
#
# async def show(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is SHOW")
#         # if not hasattr(args, "question") or not hasattr(args, "alias"):
#         #     return "Parameter error"
#     group = args.group
#     user = args.user
#     cmd = args.cmd
#     if SELF_DEBUG_MODE:
#         print(f"SHOW\nGroup: {group}\nUser: {user}\nCommand: {cmd}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if cmd == 'ans':
#         if auth_mode and (user not in faq_admins and user not in group_admins):
#             return unauthorized_text
#         ans = '\n'.join(
#             [
#                 f"问：【{k}？】\n答：【{v['answer']}】\n"
#                 for k, v in QUESTIONS.items()
#                 if type(v) == dict
#             ]
#         )
#     elif cmd == 'alias':
#         print(type(QUESTIONS['Question1']['alias']))
#         ans = '问题及其别名列表：'
#         ans += '、'.join(
#             [
#                 f"{k}:[{','.join(v['alias'])}]"
#                 for k, v in QUESTIONS.items()
#
#             ]
#         )
#     else:
#         # TODO ignore优化
#         IGNORE_QUESTIONS = []
#         if group != 863047977:
#             ans = '【问题列表】\n'
#             if not QUESTIONS:
#                 ans += '暂无问题'
#             else:
#                 ans += '、'.join(
#                     [
#                         f"{k}"
#                         for k, v in QUESTIONS.items()
#                     ]
#                 )
#         else:
#             ans = '【部分问题列表】\n'
#             ans += '、'.join(
#                 [
#                     f"{k}" for k, v in QUESTIONS.items()
#                     if str(k) not in IGNORE_QUESTIONS
#                 ]
#             )
#     return ans
#     # return "Here is SHOW function return"
#
#
# async def visible(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is VISIBLE")
#         if not hasattr(args, "questions"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     questionList = args.questions
#     if SELF_DEBUG_MODE:
#         print(f"SHOW\nGroup: {group}\nUser: {user}\nQuestion: {questionList}")
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#     if not questionList:
#         return f'请填写需要修改的问题'
#     msg_list = []
#     for question in questionList:
#         if question in QUESTIONS:
#             flag = await ChangeQuestionVisible(db_table, question, True)
#             if flag:
#                 msg_list.append(f'问题《{question}》可见性修改成功')
#             else:
#                 msg_list.append(f'问题《{question}》可见性修改失败，请查看日志')
#         else:
#             msg_list.append(f'问题《{question}》不存在，请检查')
#     return '\n'.join(msg_list)
#
#
# async def invisible(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is INVISIBLE")
#         if not hasattr(args, "questions"):
#             return "Parameter error"
#     group = args.group
#     user = args.user
#     questionList = args.questions
#     if SELF_DEBUG_MODE:
#         print(f"SHOW\nGroup: {group}\nUser: {user}\nQuestion: {questionList}")
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'Strict' and (user not in faq_admins and user not in group_admins):
#         return unauthorized_text
#     if not questionList:
#         return f'请填写需要修改的问题'
#     msg_list = []
#     for question in questionList:
#         if question in QUESTIONS:
#             flag = await ChangeQuestionVisible(db_table, question, False)
#             if flag:
#                 msg_list.append(f'问题《{question}》可见性修改成功')
#             else:
#                 msg_list.append(f'问题《{question}》可见性修改失败，请查看日志')
#         else:
#             msg_list.append(f'问题《{question}》不存在，请检查')
#     return '\n'.join(msg_list)
#
#
# async def auth(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is AUTH")
#         # if not hasattr(args, "question") or not hasattr(args, "alias"):
#         #     return "Parameter error"
#     group = args.group
#     user = args.user
#     namelist = []
#     for person in args.namelist:
#         if person.startswith('[CQ:at'):
#             namelist.append(int(re.findall(r"\[CQ:at,qq=(.+?)\]", str(person))[0]))
#         elif person.isdigit():
#             namelist.append(int(person))
#         else:
#             return "好像没at上哦"
#     if SELF_DEBUG_MODE:
#         print(f"AUTH\nGroup: {group}\nUser: {user}\nNamelist: {namelist}")
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'None':
#         return '问答库维护已经向所有人开放啦qwq'
#     if user not in faq_admins and user not in group_admins:
#         return unauthorized_text + '\n当前模式：' + auth_mode
#
#     msg = ''
#     if namelist:
#         for person in namelist:
#             if person not in faq_admins and person not in group_admins:
#                 if await AddFaqAdmin(group, person):
#                     msg += f'用户授权成功，[CQ:at,qq={person}]（QQ号{person}）现在已经能够维护智能解答列表。\n'
#                 else:
#                     msg += f'用户{person}添加失败，请查看日志。\n'
#             else:
#                 msg += f'用户{person}已经是群/问答库管理员了，无需再次授权。\n'
#         faq_admins_length, group_admins_length = await GetLength(group)
#         return msg + f"当前问答库管理员共{faq_admins_length}人\n" + f"当前群管理员共{group_admins_length}人\n" + '当前模式：' + auth_mode
#     else:
#         return '请艾特一个或多个待授权用户'
#     # return "Here is AUTH function return"
#
#
# async def revoke(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is REVOKE")
#         # if not hasattr(args, "question") or not hasattr(args, "alias"):
#         #     return "Parameter error"
#     group = args.group
#     user = args.user
#     namelist = []
#     for person in args.namelist:
#         if person.startswith('[CQ:at'):
#             namelist.append(int(re.findall(r"\[CQ:at,qq=(.+?)\]", str(person))[0]))
#         elif person.isdigit():
#             namelist.append(int(person))
#         else:
#             return "好像没at上哦"
#
#     if SELF_DEBUG_MODE:
#         print(f"REVOKE\nGroup: {group}\nUser: {user}\nNamelist: {namelist}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'None':
#         return '问答库维护已经向所有人开放啦qwq'
#     if user not in group_admins:
#         return unauthorized_text + '\n当前模式：' + auth_mode
#     msg = ''
#     if namelist:
#         for person in namelist:
#             if person in faq_admins:
#                 if await DelFaqAdmin(group, person):
#                     msg += f'用户{person}已经被撤销问答库管理员权限。\n'
#                 else:
#                     msg += f'用户{person}撤销失败，请查看日志。\n'
#             else:
#                 msg += f'用户{person}不是问答库管理员，无需撤销。\n'
#         faq_admins_length, group_admins_length = await GetLength(group)
#         return msg + f"当前管理员共{faq_admins_length}人" + '\n当前模式：' + auth_mode
#     else:
#         return '请艾特一个或多个待撤销用户'
#
#     # return "Here is REVOKE function return"
#
#
# async def admin(args: Namespace) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is ADMIN")
#         # if not hasattr(args, "question") or not hasattr(args, "alias"):
#         #     return "Parameter error"
#     group = args.group
#     user = args.user
#     print(f"ADMIN\nGroup: {group}\nUser: {user}")
#
#     auth_mode, faq_admins, group_admins, QUESTIONS, db_table = await get_group_config(group)
#     msg_admin_list = f"问答库管理员列表：{'、'.join([str(x) for x in faq_admins])}。\n" \
#                      f"群管理员列表：{'、'.join([str(x) for x in group_admins])}。"
#     unauthorized_text = f'用户【{user}】无权操作，请联系管理员索要管理员权限。\n{msg_admin_list}\n当前模式：{auth_mode}'
#
#     if auth_mode == 'None':
#         '问答库维护已经向所有人开放啦qwq'
#     return msg_admin_list + '\n当前模式：' + auth_mode
#     # return "Here is ADMIN function return"
#
#
# async def faqhelp(args: Namespace, ) -> str:
#     if SELF_DEBUG_MODE:
#         print(args)
#         print("Here is HELP")
#         # if not hasattr(args, "question") or not hasattr(args, "alias"):
#         #     return "Parameter error"
#     group = args.group
#     user = args.user
#     print(f"HELP\nGroup: {group}\nUser: {user}")
#     # print(f"{__plugin_info__} ")
#     return """请输入"#help 问答库"参考说明哦\nWarning: This command will be deprecated in the future"""
