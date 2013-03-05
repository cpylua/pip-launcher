#! py -3
# -*- coding: utf-8 -*-

from winreg import OpenKey, QueryInfoKey, QueryValue, CloseKey, \
  EnumKey, HKEY_LOCAL_MACHINE
import sys
import re
import subprocess
import os


def enum_pythons():
  """ Find all installed pythons in Windows registry. """
  regpath = r'SOFTWARE\Python\Pythoncore'
  reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
  skcount, _, _ = QueryInfoKey(reg)
  subkeys = [EnumKey(reg, i) for i in range(skcount)]
  CloseKey(reg)
  subpaths = [r'{0}\{1}'.format(regpath, key) for key in subkeys]
  return {key: install_path(path) for key, path in zip(subkeys, subpaths)}


def install_path(regpath):
  """ Find the install path for this python version. """
  reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
  path = QueryValue(reg, 'InstallPath')
  CloseKey(reg)
  return path


def find_latest_py(pythons, series):
  """ Find the latest python version under series. """
  key = max(k for k in pythons.keys() if k.startswith(str(series)))
  return pythons[key]


def find_py(pythons, ver):
  """ Find the install path of specified python version. """
  py = pythons.get(ver)
  if not py:
    raise ValueError('Python {0} not found on this system'.format(ver))
  return py


def launch(launcher, args):
  pythons = enum_pythons()
  if launcher == '-2':
    py = find_latest_py(pythons, 2)
  elif launcher == '-3':
    py = find_latest_py(pythons, 3)
  else:
    py = find_py(pythons, launcher[1:])

  cmd = os.path.join(py, 'Scripts\\pip.exe')
  args.insert(0, cmd)
  return subprocess.call(args)


def pr_help():
  """ Print usage. """
  print('usage: pips [launcher arguments] [pip arguments]\n'
        '\nLauncher arguments:\n\n'
        '-2    Launch the latest pip 2.x version\n'
        '-3    Launch the latest pip 3.x version(default)\n'
        '-X.Y  Launch the specified pip version')
  sys.exit(0)


def main():
  if len(sys.argv) < 2:
    launcher = '-3'
    args = []
  elif sys.argv[1].lower() == '--help':
    pr_help()
  elif not re.match(r'-\d(.\d)?', sys.argv[1]):
    launcher = '-3'
    args = sys.argv[1:]
  else:
    launcher = sys.argv[1]
    args = sys.argv[2:]
  return launch(launcher, args)


if __name__ == '__main__':
  main()