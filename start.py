from aiogram import Bot, Dispatcher, executor, types, filters, executor
import aiogram.utils.markdown as md
from aiogram.dispatcher.filters import Text
import config
import logging
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import rest
import article
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import re
from aiogram.types import ParseMode


storage = MemoryStorage()

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    add_article = State()

class Form_1(StatesGroup):
    del_article = State()


class Form_ma_test(StatesGroup):
    ticker = State()
    ma = State()



""" Main menu"""
@dp.message_handler(commands=["start"])
@dp.message_handler(Text(equals="Back"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Momentum", "Dividends", "Links", "Tests"]
    keyboard.add(*buttons)
    await message.answer("Choose", reply_markup=keyboard)



""" Momentum menu"""
@dp.message_handler(Text(equals="Momentum"))
async def cmd_momentum(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["SP500", "DJ30", "ETF", "Strategy", "Back"]
    keyboard.add(*buttons)
    await message.answer("Momentum", reply_markup=keyboard)


@dp.message_handler(Text(equals="SP500"))
async def cmd_sp500(message: types.message):
    await message.answer(f"<b>{rest.get_etf('SP500')}</b>\n\n"
                         f"{rest.get_avg_momentum('sp500')}", parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="DJ30"))
async def cmd_dj30(message: types.Message):
    await message.answer(f"<b>{rest.get_etf('DJ30')}</b>\n\n"
                         f"{rest.get_avg_momentum('dj30')}", parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="ETF"))
async def cmd_momentum(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["GEM", "GEM Strategy", "Back"]
    keyboard.add(*buttons)
    await message.answer("ETF", reply_markup=keyboard)


@dp.message_handler(Text(equals="GEM Strategy"))
async def process_photo_command(message: types.Message):
    with open("GEM.png", "rb") as photo:
        await message.reply_photo(photo, caption="Global equity momentum")

@dp.message_handler(Text(equals="GEM"))
async def cmd_gem(message: types.Message):
    await message.answer(rest.get_etf_momentum())


@dp.message_handler(Text(equals="Strategy"))
async def cmd_momentum_strategy(message: types.Message):
    await message.answer(f"<b>Momentum 12_2 portfolios of the time-series stock momentum (TSMOM)</b>\n"
                         f"<i>The time-series stock momentum strategy sorts stocks based"
                         f"on their prior 11-month returns, skips one-month,"
                         f"and holds the winner portfolio for the subsequent one-month"
                         f"stocks with positive Excess return* in the past 11 months."
                         f"further ranked into quintiles based on returns,"
                         f" value-weighted portfolio of stocks in the best-performing 20 percent."
                         f"The dual momentum strategy buys the strongest winner portfolio</i>\n\n"
                         f"<u>1) Excess return = total return over past 12 months less return of T-bill.</u>\n"
                         f"<u>2) If Excess return > 0, go long risky assets. Otherwise, go alternative assets (T-Bills))</u>",
                         parse_mode=types.ParseMode.HTML)



"""Dividends menu"""
@dp.message_handler(Text(equals="Dividends"))
async def cmd_dividends_aristocrats(message: types.Message):
    await message.answer(f"<u>Dividend aristocrats from SP500</u>\n\n"
                         f"<b><i>Average dividends for last 5 years / last close price.</i></b>\n\n"
                         f"{rest.get_div()}", parse_mode=types.ParseMode.HTML)


"""Links menu"""
@dp.message_handler(Text(equals="Links"))
async def cmd_links(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Sites", "Articles", "Back", "Add_Note", "Last_Notes", "Del_Note"]
    keyboard.add(*buttons)
    await message.answer("Links", reply_markup=keyboard)

@dp.message_handler(Text(equals="Sites"))
async def cmd_sites(message: types.Message):
    buttons = [
    types.InlineKeyboardButton(text="SSRN", url="https://www.ssrn.com/index.cfm/en/"),
        types.InlineKeyboardButton(text="Dual Momentum", url="https://dualmomentum.net"),
        types.InlineKeyboardButton(text="Alpha Architect", url="https://alphaarchitect.com"),
        types.InlineKeyboardButton(text="FollowingtheTrend", url="https://www.followingthetrend.com"),
        types.InlineKeyboardButton(text="InvestServices", url="https://journal.tinkoff.ru/short/invest-services/"),
        types.InlineKeyboardButton(text="InvestAccount", url="https://journal.tinkoff.ru/investment-accounting/"),
        types.InlineKeyboardButton(text="SeekingAlpha", url="https://seekingalpha.com/article/4249370-momentum-strategies-applied-to-djia-stocks"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Links", reply_markup=keyboard)

@dp.message_handler(Text(equals="Articles"))
async def cmd_articles(message: types.Message):
    await message.answer(article.articles_, parse_mode="HTML")

@dp.message_handler(Text(equals="Tests"))
async def cmd_tests(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["MA", "Momentum", "Cash trigger"]
    keyboard.add(*buttons)
    await message.answer("Links", reply_markup=keyboard)


@dp.message_handler(Text(equals="MA"))
async def cmd_ma_test(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Cancel", "Back"]
    keyboard.add(*buttons)
    await Form_ma_test.ticker.set()
    await message.answer(f"Please type a ticker to test MA strategy",reply_markup=keyboard, parse_mode="HTML")

@dp.message_handler(state=Form_ma_test.ticker)
async def cmd_ma_ticker(message: types.Message, state: FSMContext):
    message_raw = str(message.text)
    async with state.proxy() as data:
        data["ticker"] = message_raw
    await Form_ma_test.next()
    await message.reply("Now, choose MA period to test")

@dp.message_handler(state=Form_ma_test.ma)
async def cmd_ma_num(message: types.Message, state: FSMContext):
    message_raw = int(message.text)
    async with state.proxy() as data:
        data["ma"] = message_raw
    markup = types.ReplyKeyboardRemove()
    await bot.send_message(
        message.chat.id,
        md.text(
            f"Results:\n{rest.test(data['ticker'], data['ma'])}"
        ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
    )

    await state.finish()


@dp.message_handler(Text(equals="Add_Note"))
async def cmd_add_article(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Cancel", "Back"]
    keyboard.add(*buttons)
    await Form.add_article.set()
    await message.answer(f"Please type a note",reply_markup=keyboard, parse_mode="HTML")


@dp.message_handler(Text(equals="Del_Note"))
async def cmd_del_article(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Cancel", "Back"]
    keyboard.add(*buttons)
    await Form_1.del_article.set()
    await message.answer(f"Please type id",reply_markup=keyboard, parse_mode="HTML")


@dp.message_handler(state=Form_1.del_article)
async def cmd_del_article_state(message: types.Message, state:FSMContext):
    message_raw = int(message.text)
    del_ = rest.del_article(message_raw)
    await state.finish()
    await message.answer(del_)

@dp.message_handler(Text(equals="Cancel", ignore_case=True), state="*", )
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.finish()
    await message.answer("Cancel")

@dp.message_handler(state=Form.add_article)
async def cmd_add_article_state(message: types.Message, state:FSMContext):
    message_raw = str(message.text)
    username = message.chat.username
    add_ = rest.add_article(message_raw, username)
    await state.finish()
    await message.answer(add_)


@dp.message_handler(Text(equals="Last_Notes"))
async def cmd_last_notes(message: types.Message):
    await message.answer(rest.last_article())


if __name__ == "__main__" :
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
