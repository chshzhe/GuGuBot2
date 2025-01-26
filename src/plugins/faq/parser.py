# from nonebot.rule import ArgumentParser
# from .handle import add, edit, amend, delete, alias, show, visible, invisible, auth, revoke, admin, faqhelp
#
# faq_parser = ArgumentParser("faq")
# faq_subparsers = faq_parser.add_subparsers()
#
# # 添加问题
# add_parser = faq_subparsers.add_parser("add", aliases=["添加", "ADD", "添加问题"])
# add_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# add_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# add_parser.add_argument("question", nargs="?", const="", type=str)
# add_parser.add_argument("answer", nargs="*", type=str)
# add_parser.set_defaults(handle=add)
#
# # 编辑问题
# edit_parser = faq_subparsers.add_parser("edit", aliases=["编辑", "EDIT", "编辑问题"])
# edit_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# edit_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# edit_parser.add_argument("question", nargs="?", const="", type=str)
# edit_parser.add_argument("new_answer", nargs="*", type=str, )
# edit_parser.set_defaults(handle=edit)
#
# # 追加回答
# amend_parser = faq_subparsers.add_parser("amend", aliases=["追加", "AMEND", "追加回答"])
# amend_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# amend_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# amend_parser.add_argument("question", nargs="?", const="", type=str)
# amend_parser.add_argument("amend_answer", nargs='*', type=str, )
# amend_parser.set_defaults(handle=amend)
#
# # 删除问题
# delete_parser = faq_subparsers.add_parser("del", aliases=["删除", "delete", "删除问题"])
# delete_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# delete_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# delete_parser.add_argument("question", nargs="?", const="", type=str)
# delete_parser.set_defaults(handle=delete)
#
# # 别名
# alias_parser = faq_subparsers.add_parser("alias", aliases=["别名", "ALIAS", "添加别名"])
# alias_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# alias_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# alias_parser.add_argument("question", nargs="?", const="", type=str)
# alias_parser.add_argument("alias", nargs="*", type=str)
# alias_parser.set_defaults(handle=alias)
#
# # 显示问题
# show_parser = faq_subparsers.add_parser("show", aliases=["显示", "SHOW", "显示问题"])
# show_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("cmd", nargs="?", const="", type=str)
# show_parser.set_defaults(handle=show)
#
# # 可见问题
# show_parser = faq_subparsers.add_parser("visible")
# show_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("questions", nargs="*", type=str)
# show_parser.set_defaults(handle=visible)
#
# # 隐藏问题
# show_parser = faq_subparsers.add_parser("invisible")
# show_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# show_parser.add_argument("questions", nargs="*", type=str)
# show_parser.set_defaults(handle=invisible)
#
# # 授权
# auth_parser = faq_subparsers.add_parser("auth", aliases=["授权", "AUTH", "授权用户"])
# auth_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# auth_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# auth_parser.add_argument("namelist", nargs="*", type=str)
# auth_parser.set_defaults(handle=auth)
#
# # 撤销授权
# revoke_parser = faq_subparsers.add_parser("revoke", aliases=["取消", "REVOKE", "取消授权"])
# revoke_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# revoke_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# revoke_parser.add_argument("namelist", nargs="*", type=str)
# revoke_parser.set_defaults(handle=revoke)
#
# # 查询管理员
# admin_parser = faq_subparsers.add_parser("admin", aliases=["管理员", "ADMIN", "查询管理员"])
# admin_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# admin_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# admin_parser.set_defaults(handle=admin)
#
# # 帮助
# help_parser = faq_subparsers.add_parser("help", aliases=["帮助", "HELP", "查看帮助"])
# help_parser.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
# help_parser.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
# help_parser.set_defaults(handle=faqhelp)
#
# # 其他情况
# # 有办法处理吗？
