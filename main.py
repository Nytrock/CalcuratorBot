from aiogram import Bot, Dispatcher
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
import json

with open('config.json') as file:
    config = json.load(file)
BOT_TOKEN: str = config['BOT_TOKEN']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class ArithmeticOperationInMessage(BaseFilter):
    def __init__(self):
        self.text: str

    async def __call__(self, message: Message) -> bool | dict[str, float]:
        self.text = message.text.replace(" ", "").replace(",", ".")
        if '+' in self.text:
            nums = self.get_nums('+')
            if not nums:
                return False
            return {'result': sum(nums)}
        elif '-' in self.text:
            nums = self.get_nums('-')
            if not nums:
                return False
            return {'result': nums[0] - nums[1]}
        elif '*' in self.text:
            nums = self.get_nums('*')
            if not nums:
                return False
            return {'result': nums[0] * nums[1]}
        elif '/' in self.text:
            nums = self.get_nums('/')
            if not nums:
                return False
            return {'result': nums[0] / nums[1]}
        elif '%' in self.text:
            nums = self.get_nums('%')
            if not nums:
                return False
            return {'result': nums[0] % nums[1]}
        return False

    def get_nums(self, operation: str) -> bool | tuple[float, float]:
        nums: list[str] = self.text.split(operation)
        if len(nums) != 2 or not nums[0].replace(".", "").isdigit() or not nums[1].replace(".", "").isdigit():
            return False
        if operation in ('/', '%') and float(nums[1]) == 0:
            return False
        return float(nums[0]), float(nums[1])


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Калькулятор!'
                         '\nНапиши мне арифметическую операцию с двумя числами (+, -, /, *, %) и я её решу')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напишите мне арифметическую операцию с двумя числами в формате "1+1" и я произведу вычисления. '
        'Можно вводить рациональные числа.')


@dp.message(ArithmeticOperationInMessage())
async def process_if_arithmetic_operation(message: Message, result: float):
    if result % 1 == 0:
        await message.reply(str(int(result)))
    else:
        await message.reply(str(result))


@dp.message(~ArithmeticOperationInMessage())
async def process_if_not_arithmetic_operation(message: Message):
    await message.answer("Некорректная арифмитическая операция")


if __name__ == '__main__':
    dp.run_polling(bot)
