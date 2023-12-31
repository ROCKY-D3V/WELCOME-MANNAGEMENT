from enum import Enum
from cachetools import TTLCache
from time import perf_counter

from telegram import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Update, Message
from telegram.constants import ParseMode

from IRO import DEV_USERS, DEV_USERS, DEMONS, DRAGONS

# stores admin in memory for 10 min.
ADMINS_CACHE = TTLCache(maxsize = 512, ttl = (60 * 30), timer=perf_counter)

# stores bot admin status in memory for 10 min.
BOT_ADMIN_CACHE = TTLCache(maxsize = 512, ttl = (60 * 10), timer=perf_counter)

DEV_USERS = DEV_USERS + DEV_USERS

DRAGONS = DRAGONS + DEV_USERS

DEMONS = DEMONS + DEV_USERS


class AdminPerms(Enum):
	CAN_RESTRICT_MEMBERS = 'Can Restrict Members'
	CAN_PROMOTE_MEMBERS = 'Can Promote Members'
	CAN_INVITE_USERS = 'Can Invite Users'
	CAN_DELETE_MESSAGES = 'Can Delete Messages'
	CAN_CHANGE_INFO = 'Can Change Info'
	CAN_PIN_MESSAGES = 'Can Pin Messages'
	IS_ANONYMOUS = 'Is Anonymous'


class ChatStatus(Enum):
	CREATOR = "Creator"
	ADMIN = "Administrator"


# class SuperUsers(Enum):
# 	Owner = [OWNER_ID]
# 	SysAdmin = [OWNER_ID, SYS_ADMIN]
# 	Devs = DEV_USERS
# 	Sudos = DEV_USERS
# 	Supports = DEMONS
# 	Whitelist = DRAGONS
# 	Mods = MOD_USERS


def anon_reply_markup(cb_id: str) -> InlineKeyboardMarkup:
	return InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
							text = 'Prove identity',
							callback_data = cb_id
					)
				]
			]
	)


anon_reply_text = "Seems like you're anonymous, click the button below to prove your identity"


def edit_anon_msg(msg: Message, text: str):
	"""
	edit anon check message and remove the button
	"""
	msg.edit_text(text, parse_mode = ParseMode.MARKDOWN, reply_markup = None)


async def user_is_not_admin_errmsg(msg: Message, permission: AdminPerms = None, cb: CallbackQuery = None):
	errmsg = f"You are missing the following rights to use this command:\n*{permission.value}*"
	if cb:
		return cb.answer(errmsg, show_alert = True)
	return await msg.reply_text(errmsg, parse_mode = ParseMode.MARKDOWN)

def button_expired_error(u: Update):
	errmsg = "This button has expired!"
	if u.callback_query:
		u.callback_query.answer(errmsg, show_alert = True)
		u.effective_message.delete()
		return
	return u.effective_message.edit_text(errmsg, parse_mode = ParseMode.MARKDOWN)

anon_callbacks = {}
