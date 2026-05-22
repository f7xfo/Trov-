"""Telegram bot — entry point and handlers.

This is a minimal but working bot that demonstrates the full vertical slice:
1. /start — onboarding, asks role (candidate or employer)
2. Free-text from candidate — treated as raw CV input, run through the
   CV extraction agent, profile saved to DB
3. Free-text from employer — treated as a search query, run through the
   query parsing agent, structured criteria returned

This is intentionally a v0.1 surface. Full handlers (PDF parsing, search
results UI, ratings, alerts) come in subsequent PRs.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from trov.agents.cv_extraction import extract_cv
from trov.agents.query_parsing import parse_query
from trov.core.config import settings
from trov.core.logging import log
from trov.db.models import Language
from trov.i18n import t
from trov.services.users import get_or_create_user_from_telegram

# In-memory role pick state. Will move to DB / Redis in v0.2.
_pending_role: dict[int, None] = {}


async def cmd_start(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Onboarding: ask whether the user is a candidate or employer."""
    if not update.effective_user or not update.message:
        return

    user = await get_or_create_user_from_telegram(update.effective_user)
    lang = user.preferred_language

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t("role_candidate", lang), callback_data="role:candidate")],
            [InlineKeyboardButton(t("role_employer", lang), callback_data="role:employer")],
        ]
    )
    await update.message.reply_text(t("ask_role", lang), reply_markup=keyboard)


async def on_role_picked(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data or not query.from_user:
        return

    await query.answer()
    user = await get_or_create_user_from_telegram(query.from_user)
    lang = user.preferred_language

    role = query.data.split(":")[1]
    if role == "candidate":
        _pending_role[query.from_user.id] = None
        await query.edit_message_text(t("start_candidate", lang), parse_mode=ParseMode.MARKDOWN)
    else:
        await query.edit_message_text(t("start_employer", lang), parse_mode=ParseMode.MARKDOWN)


async def cmd_help(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    user = await get_or_create_user_from_telegram(update.effective_user)
    await update.message.reply_text(t("help", user.preferred_language))


async def on_text(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Route free text based on context.

    v0.1 heuristic: if message is short and looks like a search ("I need", "ត្រូវការ"),
    parse as a search query. Otherwise, treat as CV input.

    v0.2 will use proper conversation state (Redis) instead of heuristics.
    """
    if not update.message or not update.message.text or not update.effective_user:
        return

    user = await get_or_create_user_from_telegram(update.effective_user)
    text = update.message.text.strip()
    lang = user.preferred_language

    looks_like_search = (
        len(text) < 200
        and any(
            marker in text.lower()
            for marker in ["i need", "looking for", "hire", "ត្រូវការ", "រកបុគ្គលិក"]
        )
    )

    try:
        if looks_like_search:
            await update.message.chat.send_action("typing")
            parsed = await parse_query(text)
            log.info("query_parsed", user_id=str(user.id), parsed=parsed.model_dump())
            await update.message.reply_text(
                f"🔍 Role: *{parsed.role or '?'}*\n"
                f"📍 Location: *{parsed.location or '?'}*\n"
                f"💰 Max: *${parsed.max_salary_usd or '?'}*\n\n"
                f"_(v0.1: search results coming in v0.2)_",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await update.message.reply_text(t("cv_received", lang))
            await update.message.chat.send_action("typing")
            cv = await extract_cv(text)
            log.info("cv_extracted", user_id=str(user.id), cv=cv.model_dump())
            await update.message.reply_text(
                t(
                    "cv_extracted",
                    lang,
                    headline=cv.headline or "—",
                    location=cv.location or "—",
                    years=cv.years_experience or "?",
                    salary=cv.desired_salary_usd or "?",
                    skills=", ".join(cv.skills) or "—",
                    languages=", ".join(cv.languages) or "—",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
    except Exception as e:
        log.error("handler_error", error=str(e))
        await update.message.reply_text(t("error_generic", lang))


def build_application() -> Application:
    """Build the python-telegram-bot Application with all handlers registered."""
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(on_role_picked, pattern=r"^role:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    return app
