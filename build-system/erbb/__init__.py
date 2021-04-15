##############################################################################
#
#     __init__.py
#     Copyright (c) 2020 Raphael DINGE
#
#Tab=3########################################################################

from __future__ import print_function
from builtins import input
import fileinput
import multiprocessing
import os
import platform
import shutil
import subprocess
import sys

from . import ast
from .parser import Parser
from .generators.vcvrack.panel import Panel as vcvrackPanel
from .generators.vcvrack.manifest import Manifest as vcvrackManifest
from .generators.vcvrack.code import Code as vcvrackCode
from .generators.vcvrack.deploy import Deploy as vcvrackDeploy
from .generators.front_panel.milling import Milling as front_panelMilling
from .generators.front_panel.printing import Printing as front_panelPrinting

PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ROOT = os.path.abspath (os.path.dirname (os.path.dirname (PATH_THIS)))

sys.path.insert (0, os.path.join (PATH_ROOT, 'submodules', 'gyp', 'pylib'))
import gyp



"""
==============================================================================
Name: configure
==============================================================================
"""

def configure (name, path):
   configure_native (name, path)
   configure_daisy (name, path)



"""
==============================================================================
Name: configure_native
==============================================================================
"""

def configure_native (name, path):
   path_artifacts = os.path.join (path, 'artifacts')

   gyp_args = [
      '--depth=.',
      '--generator-output=%s' % path_artifacts,
   ]

   cwd = os.getcwd ()
   os.chdir (path)
   gyp.main (gyp_args + ['%s.gyp' % name])
   os.chdir (cwd)

   if platform.system () == 'Darwin':
      file = os.path.join (path_artifacts, '%s.xcodeproj' % name, 'project.pbxproj')

      for line in fileinput.input (file, inplace = 1):
         print (line, end = '')

         if 'BuildIndependentTargetsInParallel' in line:
            print ('\t\t\t\tLastUpgradeCheck = 1000;')



"""
==============================================================================
Name: configure_daisy
==============================================================================
"""

def configure_daisy (name, path):
   path_artifacts = os.path.join (path, 'artifacts')

   gyp_args = [
      '--depth=.',
      '--generator-output=%s' % path_artifacts,
      '--format', 'ninja-linux',
      '-D', 'OS=daisy',
      '-D', 'GYP_CROSSCOMPILE',
   ]

   os.environ.update ({
      'CC': 'arm-none-eabi-gcc',
      'CXX': 'arm-none-eabi-g++',
      'AR': 'arm-none-eabi-ar',
   })

   cwd = os.getcwd ()
   os.chdir (path)
   gyp.main (gyp_args + ['%s.gyp' % name])
   os.chdir (cwd)



"""
==============================================================================
Name: parse_ui
==============================================================================
"""

def parse_ui (name, path):
   filepath = os.path.join (path, name)

   with open (filepath, "r") as data:
      input_text = data.read ()

   parser = Parser ()
   return parser.parse (input_text, filepath)



"""
==============================================================================
Name: generate_vcvrack_panel
==============================================================================
"""

def generate_vcvrack_panel (name, path, module):
   generator = vcvrackPanel ()
   generator.generate (name, path, module)



"""
==============================================================================
Name: generate_vcvrack_manifest
==============================================================================
"""

def generate_vcvrack_manifest (name, path, module):
   generator = vcvrackManifest ()
   generator.generate (name, path, module)



"""
==============================================================================
Name: generate_vcvrack_code
==============================================================================
"""

def generate_vcvrack_code (name, path, module):
   generator = vcvrackCode ()
   generator.generate (name, path, module)



"""
==============================================================================
Name: generate_vcvrack_deploy
==============================================================================
"""

def generate_vcvrack_deploy (name, path, module):
   generator = vcvrackDeploy ()
   generator.generate (name, path, module)



"""
==============================================================================
Name: generate_front_panel_milling
==============================================================================
"""

def generate_front_panel_milling (name, path, module):
   generator = front_panelMilling ()
   generator.generate (name, path, module)



"""
==============================================================================
Name: generate_front_panel_printing
==============================================================================
"""

def generate_front_panel_printing (name, path, module):
   generator = front_panelPrinting ()
   generator.generate (name, path, module)



"""
==============================================================================
Name : build
==============================================================================
"""

def build (name, path):
   path_artifacts = os.path.join (path, 'artifacts')
   configuration = 'Release'

   cmd = [
      'ninja',
      '-C', os.path.join (path_artifacts, 'out', configuration),
   ]

   subprocess.check_call (cmd)



"""
==============================================================================
Name : build_target
==============================================================================
"""

def build_target (name, target, path):
   path_artifacts = os.path.join (path, 'artifacts')
   configuration = 'Release'

   cmd = [
      'ninja',
      '-C', os.path.join (path_artifacts, 'out', configuration),
      target
   ]

   subprocess.check_call (cmd)



"""
==============================================================================
Name : build_native_target
==============================================================================
"""

def build_native_target (name, target, path):
   path_artifacts = os.path.join (path, 'artifacts')
   configuration = 'Release'

   if platform.system () == 'Darwin':
      conf_dir = os.path.join (path_artifacts, 'build', configuration)

      if not os.path.exists (conf_dir):
         os.makedirs (conf_dir)

      xcodebuild_path = '/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild'

      if not os.path.exists (xcodebuild_path):
         # fallback to selected Xcode
         developer_path = subprocess.check_output (['xcode-select', '-p']).decode ('utf-8').rstrip ()
         xcodebuild_path = developer_path + '/usr/bin/xcodebuild'

      cmd = [
         xcodebuild_path,
         '-project', os.path.join (path_artifacts, '%s.xcodeproj' % name),
         '-configuration', configuration,
         '-target', target,
         '-parallelizeTargets',
         'SYMROOT=%s' % os.path.join (path_artifacts, 'build')
      ]

      subprocess.check_call (cmd)

   elif platform.system () == 'Linux':
      cmd = [
         'make',
         '-k',
         '-C', path_artifacts,
         '-j', '%d' % multiprocessing.cpu_count (),
         target
      ]

      subprocess.check_call (cmd)



"""
==============================================================================
Name : objcopy
==============================================================================
"""

def objcopy (name, path):
   path_artifacts = os.path.join (path, 'artifacts')
   configuration = 'Release'

   print ('OBJCOPY %s' % name)

   file_elf = os.path.join (path_artifacts, 'out', configuration, name)
   file_bin = os.path.join (path_artifacts, 'out', configuration, '%s.bin' % name)

   shutil.copyfile (file_elf, file_bin)

   cmd = [
      'arm-none-eabi-objcopy',
      '-O', 'binary',
      '-S', file_bin,
   ]

   subprocess.check_call (cmd)



"""
==============================================================================
Name : deploy
==============================================================================
"""

def deploy (name, path):
   path_artifacts = os.path.join (path, 'artifacts')
   file_bin = os.path.join (path_artifacts, 'out', 'Release', '%s.bin' % name)

   if not os.path.exists (file_bin):
      sys.exit ('Unknown target %s' % name)

   print ('Enter the system bootloader by holding the BOOT button down,')
   print ('and then pressing, and releasing the RESET button.')

   input ("Press Enter to continue...")

   print ('Flashing...')

   cmd = [
      'dfu-util',
      '-a', '0',
      '-i', '0',
      '-s', '0x08000000:leave',
      '-D', file_bin,
      '-d', '0483:df11',
   ]

   subprocess.check_call (cmd)

   print ('OK.')
