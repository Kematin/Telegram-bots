from aiogram import Bot, Dispatcher, executor, types
import markup as mark

from data import data_list
from main import Parsing
token = data_list['token']
days_to_check = ['📅 -> Понедельник', '📅 -> Вторник', '📅 -> Среда', '📅 -> Четверг', '📅 -> Пятница', '📅📅 -> Вся неделя']
weak_to = 'None'

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)
pars = Parsing()



# Functions
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, это бот Kem`a\nВыбери с какой недели взять дз", reply_markup=mark.main_menu)


@dp.message_handler()
async def main_functions(message: types.Message):
	if message.text == '📚 -> Текущая неделя':
		weak_to = message.text[5:]
		pars.get_weak(weak_to)
		await bot.send_message(message.from_user.id, 'Теперь выбери день недели', reply_markup=mark.select_menu)

	elif message.text == '📚 -> Следующая неделя':
		weak_to = message.text[5:]
		pars.get_weak(weak_to)
		await bot.send_message(message.from_user.id, 'Теперь выбери день недели', reply_markup=mark.select_menu)

	elif message.text == '⬅️⬅️ Прошлое меню':
		await bot.send_message(message.from_user.id, 'Окей', reply_markup=mark.main_menu)




	#for pars
	elif message.text in days_to_check[:5]:
		day = message.text[5:].lower()
		await bot.send_message(message.from_user.id, f'Окей возьму дз за {day}\nПримерное ожидание 1 минута')
		pars.get_day(day)
		days, hometasks = pars.main_method('https://cop.admhmao.ru/')		

		flag = -1
		w_day = {
			'понедельник': 0,
			'вторник': 1,
			'среда': 2,
			'четверг': 3,
			'пятница': 4
		}
		true_day = w_day[day.lower()]

		await bot.send_message(message.from_user.id, days[true_day])
		for h in hometasks:
			if h[-2] == '2':
				flag += 1

			if flag == true_day:
				homework = ' '.join(hometasks[h])
				await bot.send_message(message.from_user.id, f'{h[:-1]}: {homework}')

			else: continue		


	elif message.text == days_to_check[5]:
		day = message.text[6:].lower()
		await bot.send_message(message.from_user.id, f'Окей возьму дз за всю неделю\nПримерное ожидание 1 минута')
		pars.get_day(day)
		days, hometasks = pars.main_method('https://cop.admhmao.ru/')

		flag = 0
		for h in hometasks:
			if h[-2] == '2':
				await bot.send_message(message.from_user.id, days[flag] + '\n')
				flag += 1

			homework = ' '.join(hometasks[h])
			await bot.send_message(message.from_user.id, f'{h[:-1]}: {homework}')		


	else:
		await bot.send_message(message.from_user.id, 'Неизвестная команда')


# Run bot
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)




def run(check_week, day, days, hometasks):
	if check_week:
		flag = 0
		for h in hometasks:
			if h[-2] == '2':
				print(days[flag] + '\n')
				flag += 1

			homework = ' '.join(hometasks[h])
			print(f'{h[:-1]}: {homework}')
	else:
		flag = -1
		w_day = {
			'понедельник': 0,
			'вторник': 1,
			'среда': 2,
			'четверг': 3,
			'пятница': 4
		}
		true_day = w_day[day.lower()]

		print(days[true_day])
		for h in hometasks:
			if h[-2] == '2':
				flag += 1

			if flag == true_day:
				homework = ' '.join(hometasks[h])
				print(f'{h[:-1]}: {homework}')

			else: continue		
