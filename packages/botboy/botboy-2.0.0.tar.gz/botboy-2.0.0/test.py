"""Tests the core module"""

from botboy import BotBoy

bot = BotBoy('Adder', lambda x, y: x + y, silent=False)

def test_one():
  global bot

  # Test initialization info
  bot.info()

  # Test setter and getter
  new_bot = BotBoy()

  new_bot.name = 'Subtracter'
  assert new_bot.name == 'Subtracter'

  def subtractor(x, y): return x - y

  new_bot.task = subtractor
  assert new_bot.task == subtractor

  # Test getter and setter info
  new_bot.info()

  # All tests passed
  return True

def test_two():
  global bot

  # Test default execution
  bot.execute(1, 2)

  if bot.result:
    assert bot.result == 3

  # Test waiting for result execution
  bot.execute(10, 20, wait=True)
  assert bot.result == 30

  # Test execution on separate process
  # Cannot wait on process
  bot.execute(30, 40, process=True)

  if bot.result:
    assert bot.result == 70

  return True

def test_three():
  global bot

  # Test store result in file
  bot.save('test.txt')

  import os
  assert os.path.exists(os.getcwd() + '/test.txt')

  # Test store result at path
  bot.save(os.getcwd() + '/test2.txt')
  assert os.path.exists(os.getcwd() + '/test2.txt')

  return True

if __name__ == '__main__':
  tests = [test_one, test_two, test_three]
  i = 1

  for test in tests:
    if test(): print(f'Test {i} passed')
    else: print(f'Test {i} failed')
    i += 1
