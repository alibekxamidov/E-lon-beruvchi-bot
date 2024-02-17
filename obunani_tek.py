import logging
import main
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from typing import Union

kanalid = ["-1001575820271"]


class BigBrother(BaseMiddleware):
    async def tekshirish(self, update: types.Update):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', ]:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data in ['check_subs', ]:
                return
        else:
            return
        logging.info(user)
        result = str()
        final_status = True
        for channel in kanalid:
            status = await check(user_id=user,
                                 channel=channel)
            final_status *= status
            channel = await main.bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                result += f"❌ <a href='{invite_link}'><b>{channel.title}</b></a>\n"

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()


async def check(user_id, channel: Union[int, str]):
    bot = main.bot.get_current()
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.is_chat_member()