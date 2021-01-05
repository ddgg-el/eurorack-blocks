/*****************************************************************************

      AnalogControlBase.cpp
      Copyright (c) 2020 Raphael DINGE

*Tab=3***********************************************************************/



/*\\\ INCLUDE FILES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

#include "erb/AnalogControlBase.h"

#include "erb/Module.h"

namespace erb
{



/*\\\ PUBLIC \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

/*
==============================================================================
Name : ctor
==============================================================================
*/

AnalogControlBase::AnalogControlBase (Module & module, const AdcPin & pin)
{
   module.add (*this, pin.pin);
}



/*
==============================================================================
Name : norm_val
==============================================================================
*/

float AnalogControlBase::norm_val () const
{
   return _norm_val;
}



/*\\\ INTERNAL \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

/*
==============================================================================
Name : impl_bind
==============================================================================
*/

void  AnalogControlBase::impl_bind (uint16_t * val_u16_ptr)
{
   _val_u16_ptr = val_u16_ptr;
}



/*
==============================================================================
Name : impl_process
==============================================================================
*/

void  AnalogControlBase::impl_process ()
{
   constexpr float u16_to_norm = 1.f / 65535.f;
   _norm_val = 1.f - float (*_val_u16_ptr) * u16_to_norm;
}



/*\\\ PROTECTED \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/



/*\\\ PRIVATE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/



}  // namespace erb



/*\\\ EOF \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/
