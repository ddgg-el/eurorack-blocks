##############################################################################
#
#     vcvrack.gyp
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
         'target_name': 'vcvrack',
         'type': 'shared_library',

         'dependencies': [ 'erb-vcvrack' ],

         'sources': [
            'VcvRack.cpp',
            'VcvRack.h',
            'VcvRack.erbui',
         ],

         'copies': [{
            'destination': '<(PRODUCT_DIR)/res',
            'files': [ 'artifacts/vcvrack.svg' ],
         }],
      },
   ],
}
