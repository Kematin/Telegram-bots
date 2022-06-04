from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Main menu
btn_now = KeyboardButton('📚 -> Текущая неделя')
btn_next = KeyboardButton('📚 -> Следующая неделя')
main_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btn_now, btn_next)

# Previous menu
btn_back = KeyboardButton('⬅️⬅️ Прошлое меню')

# Select Menu
monday = KeyboardButton('📅 -> Понедельник')
tuesday = KeyboardButton('📅 -> Вторник')
wednesday = KeyboardButton('📅 -> Среда')
thursday = KeyboardButton('📅 -> Четверг')
friday = KeyboardButton('📅 -> Пятница')
all_days = KeyboardButton('📅📅 -> Вся неделя')
select_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(monday, tuesday, wednesday, thursday, friday, all_days, btn_back)

