##############################################################################
#
#     drop.gyp
#     Copyright (c) 2020 Raphael DINGE
#
#Tab=3########################################################################



{
   'variables': {
      'erbb_flash_lds': '../../../../../submodules/libDaisy/core/STM32H750IB_flash.lds',
   },

   'includes': [
      '../../eurorack-blocks.gypi',
   ],

   'targets' : [
      {
         'target_name': 'drop',
         'type': 'none',

         'direct_dependent_settings': {
            'sources': [
               'Drop.cpp',
               'Drop.h',
               'DropDsp.cpp',
               'DropDsp.h',
               'Drop.erbui',

               '../dsp/Filter2Poles.cpp',
               '../dsp/Filter2Poles.h',
               '../dsp/Filter2Poles.hpp',
               '../dsp/GainRamp.cpp',
               '../dsp/GainRamp.h',
               '../dsp/GainRamp.hpp',
            ],

            'include_dirs': [
               '..',
            ],
         },
      },

      {
         'target_name': 'drop-daisy',
         'type': 'executable',

         'dependencies': [ 'drop', 'erb-daisy' ],
      },

      {
         'target_name': 'drop-vcvrack',
         'type': 'shared_library',

         'dependencies': [ 'drop', 'erb-vcvrack' ],
      },
   ],
}
