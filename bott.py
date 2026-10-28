#!/usr/bin/env python3
"""
Telegram Bot - Minimal and functional
Uses python-telegram-bot v20+
Run: python3 bot.py
"""

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ---------------- CONFIG ----------------
# Get your bot token from @BotFather on Telegram:
#   https://t.me/BotFather -> /newbot
# Your bot username: @Gta2027_bot
BOT_TOKEN = "9279252211:AAFO3K3UYYfBb2GgouEzStiVEPcYu8mDzug"  # <-- your token from @BotFather
ADMIN_IDS = [123456789]  # <-- replace with your Telegram user ID


# ---------------- HELPER ----------------
def get_admin_filter():
    async def filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        return update.effective_user.id in ADMIN_IDS
    return filter


# ---------------- COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome = (
        "👋 *Welcome to Gta2027_bot!* \n\n"
        "I am your trading assistant bot.\n\n"
        "*Commands:*\n"
        "/help — show this help\n"
        "/price — get crypto price (BTC/USDT)\n"
        "/add <amount> — add funds (demo)\n"
        "/balance — check your balance\n"
        "/trade <coin> — quick trade demo\n"
        "/ping — check if bot is alive\n\n"
        "Type /help any time!"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start — greet the bot\n"
        "/price — BTC/USDT demo price\n"
        "/add <amount> — demo deposit\n"
        "/balance — your demo balance\n"
        "/trade <coin> — quick trade demo\n"
        "/ping — alive check",
        parse_mode="Markdown",
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("pong 🏓")


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return a demo/live-ish crypto price (fetches from Binance public API)"""
    import asyncio
    try:
        import httpx
    except Exception:
        httpx = None

    if httpx:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                    timeout=5.0,
                )
                data = resp.json()
                price = float(data.get("price", 0))
                await update.message.reply_text(
                    f"📈 BTC/USDT = ${price:,.2f}\n"
                    f"(from Binance public API)"
                )
                return
        except Exception:
            pass
    # Fallback demo value
    await update.message.reply_text("📈 BTC/USDT = $62,000.00 (demo value)")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        amount = float(context.args[0]) if context.args and context.args[0].replace(".","").isdigit() else 100
    except Exception:
        amount = 100
    user_id = update.effective_user.id
    context.user_data["balance"] = context.user_data.get("balance", 0) + amount
    await update.message.reply_text(
        f"✅ +${amount:,.2f} added to your demo balance!\n"
        f"Total: ${context.user_data['balance']:,.2f}"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    b = context.user_data.get("balance", 0)
    await update.message.reply_text(f"💰 Your demo balance: ${b:,.2f} USDT")


async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    coin = context.args[0].upper() if context.args else "BTC"
    b = context.user_data.get("balance", 0)
    if b < 100:
        await update.message.reply_text("❌ Insufficient balance! Use /add first.")
        return
    context.user_data["balance"] -= 100
    context.user_data[f"holdings_{coin}"] = context.user_data.get(f"holdings_{coin}", 0) + 1
    await update.message.reply_text(
        f"✅ Bought 1 {coin}\n"
        f"Remaining balance: ${context.user_data['balance']:,.2f} USDT\n"
        f"Holdings: {context.user_data.get(f'holdings_{coin}', 1)} {coin}"
    )


# ---------------- MESSAGE HANDLER ----------------
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"You said: {update.message.text}\n"
        "Try /help to see available commands.",
        parse_mode="Markdown",
    )


# ---------------- MAIN ----------------
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("trade", trade))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    
  application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()

