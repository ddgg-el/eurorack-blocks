/*****************************************************************************

      SubmoduleDaisySeed.cpp
      Copyright (c) 2020 Raphael DINGE

*Tab=3***********************************************************************/



/*\\\ INCLUDE FILES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

#include "erb/daisy/SubmoduleDaisySeed.h"

#undef erb_DAISY_HEARTBEAT



namespace erb
{



/*\\\ PUBLIC \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

/*
==============================================================================
Name : ctor
==============================================================================
*/

SubmoduleDaisySeed::SubmoduleDaisySeed ()
{
   enable_fz ();

   _this_ptr = this;

   _seed.Configure ();
   _seed.Init (true /* boost */);

   _seed.SetAudioBlockSize (erb_BUFFER_SIZE);
}



/*\\\ INTERNAL \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/



/*\\\ PROTECTED \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/



/*\\\ PRIVATE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/

/*
==============================================================================
Name : enable_fz
Description :
   Enable FZ (flush-to-zero) denormal behavior
==============================================================================
*/

void  SubmoduleDaisySeed::enable_fz ()
{
   uint32_t fpscr = __get_FPSCR ();
   fpscr |= 0x01000000; // FZ bit
   __set_FPSCR (fpscr);
}



/*
==============================================================================
Name : do_run
==============================================================================
*/

void  SubmoduleDaisySeed::do_run ()
{
   _seed.adc.Start ();
   _seed.StartAudio (audio_callback_proc);

   for (;;) {}
}



/*
==============================================================================
Name : audio_callback_proc
==============================================================================
*/

void  SubmoduleDaisySeed::audio_callback_proc (float ** in, float ** out, size_t size)
{
   _this_ptr->audio_callback (in, out, size);
}



/*
==============================================================================
Name : audio_callback
==============================================================================
*/

void  SubmoduleDaisySeed::audio_callback (float ** in, float ** out, size_t /* size */)
{
   raw_audio_inputs = in;
   raw_audio_outputs = out;

   _run ();

   _clock.tick ();

#if defined (erb_DAISY_HEARTBEAT)
   static uint16_t phase = 0;
   phase += 100;
   _seed.SetLed (phase < 32000);
#endif
}



SubmoduleDaisySeed * SubmoduleDaisySeed::_this_ptr = nullptr;



}  // namespace erb



/*\\\ EOF \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\*/
