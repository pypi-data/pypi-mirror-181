import logging
import random
import re

from pyplanet.apps.config import AppConfig
from pyplanet.contrib.command import Command
from pyplanet.utils.style import style_strip

logger = logging.getLogger(__name__)

class RollDiceApp(AppConfig):
	game_dependencies = []
	app_dependencies = ['core.maniaplanet', 'core.trackmania', 'core.shootmania']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	async def on_start(self):
		await self.instance.command_manager.register(
			Command(command='roll', aliases=[], target=self.roll,
				description='Roll a die or dice and print the result. Use "/roll 2d6" for example to roll 2 six-sided dice.')
				.add_param(name='die', nargs=1, type=str, default='1d20', required=False)
		)


	async def roll(self, player, data, **kwargs) -> None:
		roll_count = 1
		roll_max = 20
		match_result = re.match('(\d+)?[dD](\d+)?', data.die)
		if match_result:
			count, die = match_result.groups()
			logger.debug(f'Input argument parsed as count:{str(count)}, die:{str(die)}')
			try:
				roll_max = int(die) if int(die) > 0 else roll_max
				roll_count = int(count) if int(count) > 0 else roll_count
			except ValueError:
				pass
			except TypeError:
				pass
		logger.debug(f'Rolling with roll_count:{str(roll_count)}, roll_max:{str(roll_max)}')
		rolls = []	# type: list[str]
		while len(rolls) < roll_count:
			current_roll = random.randint(1, roll_max)
			rolls.append(current_roll)
			logger.debug('Rolled: ' + str(current_roll))
		await self.instance.chat(f'$ff0$<$fff{player.nickname}$> rolls $<$fff{str(roll_count)}d{str(roll_max)}$>...')
		await self.instance.chat(f'$ff0Dice: $<$fff{", ".join([str(r) for r in rolls])}$> Total: $<$fff{str(sum(rolls))}$>')
