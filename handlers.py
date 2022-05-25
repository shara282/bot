from aiogram.dispatcher import FSMContext
import datetime
from main import bot, dp
from aiogram.types import Message, ReplyKeyboardRemove
from config import admin_id, WEATHER_TOKEN
from menu import menu_start, menu_selection_method, menu_selection_test_1, menu_selection_test_2, menu_selection_test_3
from states import SearchTest, Test
from getting_weather import get_weather, get_air_pollution


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.reply("\U0001F60A Приветствую вас в своем боте! \U0001F60A\nВыберите функцию:",
                        reply_markup=menu_start)


@dp.message_handler(text="Погода")
async def selection_weather(message: Message, state: FSMContext):
    choice = message.text
    await state.update_data({'choice1': choice})
    await message.reply("Выберите способ получения погоды:", reply_markup=menu_selection_method)


@dp.message_handler(text="По названию города", state=None)
async def selection_city(message: Message, state: FSMContext):
    await message.reply(text="Введите название города:", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    if data.get('choice1') == "Погода":
        await SearchTest.Q1.set()
    elif data.get('choice1') == "Загрязнение воздуха":
        await SearchTest.Q3.set()


@dp.message_handler(text="По координатам", state=None)
async def selection_coordinates(message: Message, state: FSMContext):
    await message.reply(text="Введите широту и долготу через пробел:", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    if data.get('choice1') == "Погода":
        await SearchTest.Q2.set()
    elif data.get('choice1') == "Загрязнение воздуха":
        await SearchTest.Q4.set()


@dp.message_handler(text="Загрязнение воздуха")
async def selection_air_pollution(message: Message, state: FSMContext):
    choice = message.text
    await state.update_data({'choice1': choice})
    await message.reply("Выберите способ получения данных о загрязнении воздуха:", reply_markup=menu_selection_method)


@dp.message_handler(state=SearchTest.Q1)
async def get_weather_city(message: Message, state: FSMContext):
    answer = message.text
    try:
        result = get_weather(answer, 1, WEATHER_TOKEN)
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {result['city_name']}\nКоординаты: {result['lat']} ш. {result['lon']} д.\n"
                            f"Температура: {result['temp']}C° {result['weather_description']}\nОщущается как {result['temp_feels']}C°\n"
                            f"Влажность: {result['humidity']}%\nДавление: {result['pressure']} мм.рт.ст\n"
                            f"Видимость: {result['visibility']} м\nВетер: {result['wind_speed']} м/с\n"
                            f"Порыв ветра: {result['wind_gust']} м/с\nОблачность: {result['clouds']}%\n"
                            f"Восход солнца: {result['sunrise_time']}\nЗакат солнца: {result['sunset_time']}\n"
                            f"Продолжительность дня: {result['day_length']}\n"
                            f"***Хорошего дня!***", reply_markup=menu_start
                            )
    except:
        await message.reply(text=f"\U0001F625 Не удалость получить данных по городу: {answer} \U0001F625\n"
                                 f"Проверьте название города и попробуйте еще раз.", reply_markup=menu_start)
    await state.finish()


@dp.message_handler(state=SearchTest.Q2)
async def get_weather_coordinates(message: Message, state: FSMContext):
    answer = message.text.split()
    try:
        result = get_weather(answer, 2, WEATHER_TOKEN)
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {result['city_name']}\nКоординаты: {result['lat']} ш. {result['lon']} д.\n"
                            f"Температура: {result['temp']}C° {result['weather_description']}\nОщущается как {result['temp_feels']}C°\n"
                            f"Влажность: {result['humidity']}%\nДавление: {result['pressure']} мм.рт.ст\n"
                            f"Видимость: {result['visibility']} м\nВетер: {result['wind_speed']} м/с\n"
                            f"Порыв ветра: {result['wind_gust']} м/с\nОблачность: {result['clouds']}%\n"
                            f"Восход солнца: {result['sunrise_time']}\nЗакат солнца: {result['sunset_time']}\n"
                            f"Продолжительность дня: {result['day_length']}\n"
                            f"***Хорошего дня!***", reply_markup=menu_start
                            )
    except:
        await message.reply(text=f"\U0001F625 Не удалость получить данных по координатам: {answer} \U0001F625\n"
                                 f"Проверьте координаты и попробуйте еще раз.", reply_markup=menu_start)
    await state.finish()


@dp.message_handler(state=SearchTest.Q3)
async def get_air_pollution_city(message: Message, state: FSMContext):
    answer = message.text
    try:
        result = get_air_pollution(answer, 1, WEATHER_TOKEN)
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Качество воздуха в городе: {result['city_name']}\n"
                            f"Координаты: {result['lat']} ш. {result['lon']} д.\n"
                            f"Индекс качества воздуха: {result['aqi']}\n"
                            f"Концентрация СО: {result['co']}  мкг/м³\n"
                            f"Концентрация NO: {result['no']}  мкг/м³\n"
                            f"Концентрация NO2: {result['no2']}  мкг/м³\n"
                            f"Концентрация O3: {result['o3']}  мкг/м³\n"
                            f"Концентрация SO2: {result['so2']}  мкг/м³\n"
                            f"Концентрация РМ 2,5(мелкодисперсное вещество): {result['pm2_5']}  мкг/м³\n"
                            f"Концентрация РМ 10(крупнодисперсных частиц): {result['pm10']}  мкг/м³\n"
                            f"Концентрация NH3: {result['nh3']}  мкг/м³\n"
                            f"***Хорошего дня!***", reply_markup=menu_start
                            )
    except:
        await message.reply(text=f"\U0001F625 Не удалость получить данных по городу: {answer} \U0001F625\n"
                                 f"Проверьте название города и попробуйте еще раз.", reply_markup=menu_start)
    await state.finish()


@dp.message_handler(state=SearchTest.Q4)
async def get_air_pollution_coordinates(message: Message, state: FSMContext):
    answer = message.text.split()
    try:
        result = get_air_pollution(answer, 2, WEATHER_TOKEN)
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Качество воздуха по координатам: {result['lat']} ш. {result['lon']} д.\n"
                            f"Индекс качества воздуха: {result['aqi']}\n"
                            f"Концентрация СО: {result['co']}  мкг/м³\n"
                            f"Концентрация NO: {result['no']}  мкг/м³\n"
                            f"Концентрация NO2: {result['no2']}  мкг/м³\n"
                            f"Концентрация O3: {result['o3']}  мкг/м³\n"
                            f"Концентрация SO2: {result['so2']}  мкг/м³\n"
                            f"Концентрация РМ 2,5(мелкодисперсное вещество): {result['pm2_5']}  мкг/м³\n"
                            f"Концентрация РМ 10(крупнодисперсных частиц): {result['pm10']}  мкг/м³\n"
                            f"Концентрация NH3: {result['nh3']}  мкг/м³\n"
                            f"***Хорошего дня!***", reply_markup=menu_start
                            )
    except:
        await message.reply(text=f"\U0001F625 Не удалость получить данных по координатам: {answer} \U0001F625\n"
                                 f"Проверьте координаты и попробуйте еще раз.", reply_markup=menu_start)
    await state.finish()


@dp.message_handler(text="Тест", state=None)
async def selection_test(message: Message):
    await message.reply("Вы начали тестирование.\n"
                        "Вопрос №1\n\n"
                        "В чем главная причина изменения погоды?\n\n"
                        "A - Постоянное перемещение воздушных масс\n"
                        "B - Фазы Луны\n"
                        "C - Воля Богов", reply_markup=menu_selection_test_1)
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer1': answer})
    await message.reply("Вопрос №2\n\n"
                        "В Гидрометцентре составляют синоптические карты с информацией о погоде, процессах и явлениях в атмосфере. Где нужны такие карты?\n\n"
                        "A - В авиации\n"
                        "B - В сельском хозяйстве\n"
                        "C - На флоте\n"
                        "D - Во всех вышеперечисленных областях", reply_markup=menu_selection_test_2)
    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer2': answer})
    await message.reply("Вопрос №3\n\n"
                        "Слово «климат» произошло от греческого klima. Как это переводится?\n\n"
                        "A - Перемена\n"
                        "B - Наклон\n"
                        "C - Облако", reply_markup=menu_selection_test_1)
    await Test.Q3.set()


@dp.message_handler(state=Test.Q3)
async def answer_q3(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer3': answer})
    await message.reply("Вопрос №4\n\n"
                        "Главный климатообразующий фактор — это...\n\n"
                        "A - Высота над уровнем моря\n"
                        "B - Географическая широта местности\n"
                        "C - Удаленность от океанов", reply_markup=menu_selection_test_1)
    await Test.Q4.set()


@dp.message_handler(state=Test.Q4)
async def answer_q4(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer4': answer})
    await message.reply("Вопрос №5\n\n"
                        "Воздушные массы в умеренном поясе России движутся в основном ...\n\n"
                        "A - С востока на запад\n"
                        "B - С запада на восток\n"
                        "C - С юга на север", reply_markup=menu_selection_test_1)
    await Test.Q5.set()


@dp.message_handler(state=Test.Q5)
async def answer_q5(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer5': answer})
    await message.reply("Вопрос №6\n\n"
                        "Как связаны климат и погода?\n\n"
                        "A - Климат — многолетний режим погоды\n"
                        "B - Это одно и то же\n"
                        "C - Не связаны", reply_markup=menu_selection_test_1)
    await Test.Q6.set()


@dp.message_handler(state=Test.Q6)
async def answer_q6(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer6': answer})
    await message.reply("Вопрос №7\n\n"
                        "В каких регионах погода меняется особенно часто?\n\n"
                        "A - В приморских\n"
                        "B - В засушливых\n"
                        "C - В пустынных", reply_markup=menu_selection_test_1)
    await Test.Q7.set()


@dp.message_handler(state=Test.Q7)
async def answer_q7(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer7': answer})
    await message.reply("Вопрос №8\n\n"
                        "Среди главных факторов климата нет...\n\n"
                        "A - Географической широты\n"
                        "B - Близости морей и океанов\n"
                        "C - Направлений господствующих ветров\n"
                        "D - Рельефа и высоты над уровнем моря\n"
                        "E - Морских течений\n"
                        "F - Движения тектонических плит", reply_markup=menu_selection_test_3)
    await Test.Q8.set()


@dp.message_handler(state=Test.Q8)
async def answer_q8(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer8': answer})
    await message.reply("Вопрос №9\n\n"
                        "Где на Земле дождь идет каждый день?\n\n"
                        "A - На экваторе\n"
                        "B - На Крите\n"
                        "C - В Петербурге", reply_markup=menu_selection_test_1)
    await Test.Q9.set()


@dp.message_handler(state=Test.Q9)
async def answer_q9(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer9': answer})
    await message.reply("Вопрос №10\n\n"
                        "За погодой наблюдают...\n\n"
                        "A - В метеорологических центрах\n"
                        "B - В метрологических центрах\n"
                        "C - Дома из окна", reply_markup=menu_selection_test_1)
    await Test.Q10.set()


@dp.message_handler(state=Test.Q10)
async def answer_q10(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data({'answer10': answer})
    data = await state.get_data()
    cnt = 0
    if data.get('answer1') == "A":
        cnt += 1
    if data.get('answer2') == "D":
        cnt += 1
    if data.get('answer3') == "B":
        cnt += 1
    if data.get('answer4') == "B":
        cnt += 1
    if data.get('answer5') == "B":
        cnt += 1
    if data.get('answer6') == "A":
        cnt += 1
    if data.get('answer7') == "A":
        cnt += 1
    if data.get('answer8') == "F":
        cnt += 1
    if data.get('answer9') == "A":
        cnt += 1
    if data.get('answer10') == "A":
        cnt += 1
    await message.reply("\U0001F618 Спасибо за ваши ответы! \U0001F618\n"
                        f"Вы ответили правильно на {cnt} вопрос(ов)", reply_markup=menu_start)
    await state.finish()
