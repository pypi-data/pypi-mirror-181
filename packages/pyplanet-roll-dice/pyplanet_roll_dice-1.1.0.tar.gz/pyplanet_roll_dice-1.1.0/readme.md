# Roll Dice

A plugin for [PyPlanet](https://pypla.net/).

This plugin allows you to simulate dice rolls.

## Commands

|Command    |Description|
|-----------|-----------|
| /roll die | Use this command to simulate a dice roll. If the 'die' argument is omitted a 1d20 die will be rolled. The die argument can be any 2 integer numbers separated by the letter 'd'. The first number indicates the number of dice to roll and the second number indicates the max value of the die to roll. |

Examples of commands:

```
$> /roll

Player rolls 1d20...
Dice: 19 Total: 19
```

```
$> /roll 2d6

Player rolls 2d6...
Dice: 1, 4 Total: 5
```

```
$> /roll 3d8

Player rolls 3d8...
Dice: 8, 6, 3 Total: 17
```
