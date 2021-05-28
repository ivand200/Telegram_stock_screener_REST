from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import aiogram.utils.markdown as fmt
from aiogram.dispatcher.filters import Text
import config
import logging
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import rest
import article


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

""" Main menu"""
@dp.message_handler(commands=["start"])
@dp.message_handler(Text(equals="Back"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Momentum", "Dividends", "ETF", "Links"]
    keyboard.add(*buttons)
    await message.answer("Choose", reply_markup=keyboard)


""" Momentum menu"""
@dp.message_handler(Text(equals="Momentum"))
async def cmd_momentum(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["SP500", "DJ30", "Strategy", "Low range", "Back"]
    keyboard.add(*buttons)
    await message.answer("Momentum", reply_markup=keyboard)

@dp.message_handler(Text(equals="SP500"))
async def cmd_sp500(message: types.message):
    await message.answer(f"<b>{rest.get_etf('SPY')}</b>\n\n"
                         f"{rest.get_mom('sp500')}", parse_mode=types.ParseMode.HTML)

@dp.message_handler(Text(equals="DJ30"))
async def cmd_dj30(message: types.Message):
    await message.answer(f"<b>{rest.get_etf('^DJI')}</b>\n\n"
                         f"{rest.get_mom('dj30')}", parse_mode=types.ParseMode.HTML)

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

@dp.message_handler(Text(equals="Low range"))
async def cmd_dj30(message: types.Message):
    await message.answer(f"Stocks which trade at low range for last 5 year\n"
                         f"SP500:\n{rest.get_low_range('sp500')}\n\n"
                         f"DJ30:\n{rest.get_low_range('dj30')}")


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
    buttons = ["Sites", "Articles", "Back"]
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


"""ETF menu"""
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


if __name__ == "__main__" :
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
