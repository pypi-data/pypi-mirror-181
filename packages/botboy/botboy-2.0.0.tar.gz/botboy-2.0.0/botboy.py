"""Multithreading & processing worker that executes functions and prints the result"""
__version__ = '2.0.0'

import threading
import multiprocessing

class BotBoy:
  def __init__(self, name=None, task=None, silent=True):
    self._name = name
    self._task = task
    self._silent = silent
    self._result = None
    self._process = None
    self._thread = None

  @property
  def name(self):
    """Name getter"""
    return self._name

  @name.setter
  def name(self,name):
    """Name setter"""
    self._name = name

  @property
  def task(self):
    """Task getter"""
    return self._task

  @task.setter
  def task(self, task):
    """Task setter"""
    self._task = task

  @property
  def silent(self):
    """Silent getter"""
    return self._silent

  @silent.setter
  def silent(self, is_silent):
    """Silent setter"""
    self._silent = is_silent

  @property
  def result(self):
    """Result getter"""
    return self._result

  @result.setter
  def result(self, result):
    """Result setter"""
    self._result = result

  @property
  def process(self):
    """Process getter"""
    return self._process

  @process.setter
  def process(self, process):
    """Process setter"""
    self._process = process

  @property
  def thread(self):
    """Thread getter"""
    return self._thread

  @thread.setter
  def thread(self, thread):
    """Thread setter"""
    self._thread = thread

  def info(self):
    """Displays the bot's name and task"""
    print(f'Name: {self.name}\nTask: {self.task}\nResult: {self.result}\nProcess: {self.process}\nThread: {self.thread}')

  def __str__(self):
    """Returns a string representation of the bot"""
    return self.info()

  def _wrapper(self, *args):
    """Task wrapper"""
    self.log(f'{self.name} is executing task: {self.task}')
    self.result = self.task(*args)
    self.log(f'Retrieved result from {self.name}: {self.result}')

  def execute(self, *args, wait=False, process=False):
    """Runs the assigned task

    wait (Boolean) - Pause execution until task is finished running
    process (Boolean) - Run task on a separate process instead of default thread
    file (Dictionary) - Stores result in file (provided name or path)
    """
    if process:
      self.process = multiprocessing.Process(target=self._wrapper, name=self.name, args=args)
      self.log(f'Running {self.task} on separate process: {self.process}')
      self.process.run()
      self.process = None
    else:
      self.thread = threading.Thread(target=self._wrapper, name=self.name, args=args)
      self.run_thread(wait)

  def run_thread(self, wait):
    """Executes the task on a separate thread

    wait (Boolean) - Pause execution until task is finished running
    """
    if wait:
      self.log(f'Waiting for {self.task} to finish')
      self.thread.run()
    else:
      self.thread.start()
    self.thread = None

  def save(self, filename):
    """Save the result in a file

    filename (String) - The name of the file or the path to store the result in
    """
    self.log(f'Storing result at {filename}')

    with open(filename, 'w') as f:
      f.write(f'{self.result}')

  def log(self, msg):
    """Logs a message to output"""
    if not self.silent: print(msg)
