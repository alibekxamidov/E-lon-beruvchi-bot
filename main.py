import logging
import obunani_tek
import buttons
from config import Token, kanal_id
from buttons import kirish, kanal, majburiyobuna
from states import holat
from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    ism = message.from_user.first_name
    familiya = message.from_user.last_name
    await holat.el.set()
    await message.answer(f"<b><i>👋🏻 Assolomu alaykum <u>{ism} {familiya}</u> quyidagi kanalga obuna bo'ling:</i></b>",
                         parse_mode="html",
                         reply_markup=majburiyobuna)


@dp.callback_query_handler(state=holat.kir)
async def elon_send(call: types.CallbackQuery):
    await call.message.answer(f"<b><i>🚘Rusumi:\nAvtomobilingiz nomini yozing!</i></b>", parse_mode="html")
    await holat.rusumi.set()


@dp.message_handler(state=holat.rusumi)
async def rusumi_send(message: types.Message, state: FSMContext):
    rusumi = message.text
    await state.update_data(
        {"rusumi": rusumi}
    )
    await message.answer(f"<b><i>🕹Pozitsiyasi:\nAvtomobilingiz nechinchi pozitsiya </i></b>:", parse_mode="html")
    await holat.pozitsiya.set()


@dp.message_handler(state=holat.pozitsiya)
async def pozit_send(message: types.Message, state: FSMContext):
    pozitsiya = message.text
    await state.update_data(
        {"pozitsiya": pozitsiya}
    )
    await message.answer(f"<b><i>📆Yili:\nAvtomobilingiz nechanchi yil? </i></b>:", parse_mode="html")
    await holat.yili.set()


@dp.message_handler(state=holat.yili)
async def yili_send(message: types.Message, state: FSMContext):
    yili = message.text
    await state.update_data(
        {"yili": yili}
    )
    await message.answer(f"<b><i>📟Yurgani:\nAvtomobilingiz necha km yurgan?\nMasalan 100 km </i></b>:",
                         parse_mode="html")
    await holat.yurgani.set()


@dp.message_handler(state=holat.yurgani)
async def yurgani_send(message: types.Message, state: FSMContext):
    yurgani = message.text
    await state.update_data(
        {"yurgani": yurgani}
    )
    await message.answer(f"<b><i>🎨Rangi:\nAvtomobilingiz rangi qanaqa? </i></b>:", parse_mode="html")
    await holat.rangi.set()


@dp.message_handler(state=holat.rangi)
async def rangi_send(message: types.Message, state: FSMContext):
    rangi = message.text
    await state.update_data(
        {"rangi": rangi}
    )
    await message.answer(f"<b><i>⛽️Yoqilg'isi:\nAvtomobilingiz yoqilg'i turi? </i></b>:", parse_mode="html")
    await holat.yoqilgi.set()


@dp.message_handler(state=holat.yoqilgi)
async def yoqilgi_send(message: types.Message, state: FSMContext):
    yoqilgi = message.text
    await state.update_data(
        {"yoqilgi": yoqilgi}
    )
    await message.answer(f"<b><i>💵Narxi:\nAvtomobilingiz narxini kiriting?\nMasalan 100 mln </i></b>:",
                         parse_mode="html")
    await holat.narxi.set()


@dp.message_handler(state=holat.narxi)
async def narxi_send(message: types.Message, state: FSMContext):
    narxi = message.text
    await state.update_data(
        {"narxi": narxi}
    )
    await message.answer(f"<b><i>☎️Telefon:\nTelefon nomeringizni quyidagi formatda +998xxxxxxxxx kiriting </i></b>:",
                         parse_mode="html")
    await holat.telefon.set()


@dp.message_handler(state=holat.telefon)
async def telefon_send(message: types.Message, state: FSMContext):
    telefon = message.text
    await state.update_data(
        {"telefon": telefon}
    )
    await message.answer(f"<b><i>📍Manzil:\nManzilingizni kiriting? </i></b>:", parse_mode="html")
    await holat.manzil.set()


@dp.message_handler(state=holat.manzil)
async def shahar_send(message: types.Message, state: FSMContext):
    manzil = message.text
    await state.update_data(
        {"manzil": manzil}
    )
    await message.answer(f"<b><i>🏞Rasm:\nAvtomobil Rasimini yuboring!\nFaqat bitta rasm yuboring! </i></b>:",
                         parse_mode="html")
    await holat.rasm.set()


@dp.message_handler(state=holat.rasm, content_types=["photo"])
async def rasm_send(message: types.Message, state: FSMContext):
    rasm = message.photo[-1].file_id
    await state.update_data(
        {"rasm": rasm}
    )
    data = await state.get_data()
    rusumi = data.get("rusumi")
    pozitsiya = data.get("pozitsiya")
    yili = data.get("yili")
    yurgani = data.get("yurgani")
    rangi = data.get("rangi")
    yoqilgi = data.get("yoqilgi")
    narxi = data.get("narxi")
    telefon = data.get("telefon")
    manzil = data.get("manzil")
    rasm = data.get("rasm")
    await message.answer_photo(photo=rasm,
                               caption=f"🚘{rusumi} sotiladi‼️\n🕹Pozitsiyasi - {pozitsiya}\n📆Yili - {yili}\n🎨Rangi - {rangi}\n📟Yurgani - {yurgani}\n⛽️Yoqilg'i - {yoqilgi}\n💵Narxi - {narxi}\n☎️Telefon - {telefon}\n📍Manzil - {manzil}\n\n<b><i>Quyidagi e`lonni kanalga yuborishni hohlaysizmi?</i></b>",
                               parse_mode="html", reply_markup=buttons.ruxsat)
    await holat.tanlash.set()


@dp.callback_query_handler(state=holat.tanlash)
async def tanlash(call: types.CallbackQuery, state: FSMContext):
    r = call.data
    data = await state.get_data()
    rusumi = data.get("rusumi")
    pozitsiya = data.get("pozitsiya")
    yili = data.get("yili")
    yurgani = data.get("yurgani")
    rangi = data.get("rangi")
    yoqilgi = data.get("yoqilgi")
    narxi = data.get("narxi")
    telefon = data.get("telefon")
    manzil = data.get("manzil")
    rasm = data.get("rasm")
    await call.message.delete()
    if r == "ha":
        await bot.send_photo(chat_id=kanal_id, photo=rasm,
                             caption=f"🚘 {rusumi} sotiladi ‼️\n\n🕹Pozitsiyasi - {pozitsiya}\n📆Yili - {yili}\n🎨Rangi - {rangi}\n📟Yurgani - {yurgani}\n⛽️Yoqilg'i - {yoqilgi}\n💵Narxi - {narxi}\n☎️Telefon - {telefon}\n📍Manzil - {manzil}\n\n<b><i>⬇️ E'lon Berish Uchun Bot ⬇️\nhttps://t.me/avtosotuvbot\n\n⬇️ Moshina Bozor Kanali ⬇️\nhttps://t.me/avtosotuvuzz</i></b>",
                             parse_mode="html", reply_markup=buttons.oxiri)
        await call.message.answer(
            f"<b><i>✅E`lon kanalga joylandi\n Pastdagi tugmani bosib kanalga kirib e'loningizni ko'rishingiz mumkin!</i></b>",
            parse_mode="html", reply_markup=kanal)
        await state.finish()
    elif r == "yoq":
        await call.message.answer(
            f"<b><i>❌E`lon kanalga joylanmadi.\nQayta e'lon berish uchun <u>/start</u> ni bosing!</i></b>",
            parse_mode="html")
        await state.finish()


@dp.callback_query_handler(state=holat.el)
async def tekshirish(call: types.CallbackQuery):
    await call.answer()
    final_status = True
    result = ''
    for channel in obunani_tek.kanalid:
        status = await obunani_tek.check(user_id=call.from_user.id,
                                         channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status
            result = f"<b><i>✅ {str(channel.title)} kanaliga obuna bo'lgansiz!</i></b>",

        else:
            final_status *= False
            result = f"❌{str(channel.title)} kanaliga obuna bo'lmagansiz"

    if final_status:
        await call.message.delete()
        await holat.kir.set()
        await call.message.answer(
            f"<b><i>Avtomobilingizni sotmoqchi bo'lsangiz <u>E'lon berish</u> tugmasini bosing! </i></b>",
            parse_mode="html",
            reply_markup=kirish)
    else:
        await call.message.delete()
        await call.message.answer(str(result), disable_web_page_preview=True, reply_markup=majburiyobuna)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)