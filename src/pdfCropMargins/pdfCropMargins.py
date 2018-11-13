#!/usr/bin/python
# -*- coding: utf-8 -*-
# Note that using the shebang "usr/bin/env python" does not set the process
# name to pdfCropMargins in Linux (for things like top, ps, and killall).
"""

pdfCropMargins -- a program to crop the margins of PDF files
Copyright (C) 2014 Allen Barker (Allen.L.Barker@gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Project web site: https://abarker.github.io/pdfCropMargins
Source code site: https://github.com/abarker/pdfCropMargins

=====================================================================

A command-line application to crop the margins of PDF files.  Cropping the
margins can make it easier to read the pages of a PDF document -- whether the
document is printed or displayed on a screen -- because the fonts appear
larger.  Margin-cropping is also useful at times when one PDF is included in
another as a graphic.  Many options are available.

To see the formatted documentation, run::
   pdfCropMargins -h | more
or::
   python pdfCropMargins -h | more

This is the initial starting script, but it just calls `mainCrop` from
`main_pdfCropMargins.py`, which does the real work.  Its only purpose is to
handle errors and make sure that any temp directories are cleaned up.  It tries
to gracefully handle ^C characters from the user (`KeyboardInterrupt`) to stop
the program and clean up.

"""

# TODO: Consider defining a command-line option which will print out either a
# bash script or a DOS script that they can modify and use.

from __future__ import print_function, division, absolute_import
import sys

def main(stdin_file):
    """Run main, catching any exceptions and cleaning up the temp directories."""

    cleanup_and_exit = sys.exit # Function to do cleanup and exit before the import.
    exit_code = 0

    # Imports are done here inside the try block so some ugly (and useless)
    # traceback info is avoided on user's ^C (KeyboardInterrupt, EOFError on Windows).
    try:
        from . import external_program_calls as ex # Creates tmp dir as side effect.
        cleanup_and_exit = ex.cleanup_and_exit # Switch to the real one, deletes temp dir.

        from . import main_pdfCropMargins # Imports external_program_calls, don't do first.
        main_pdfCropMargins.main_crop(stdin_file) # Run the actual program.

    except (KeyboardInterrupt, EOFError): # Windows raises EOFError on ^C.
        print("\nGot a KeyboardInterrupt, cleaning up and exiting...\n",
              file=sys.stderr)

    except SystemExit:
        exit_code = sys.exc_info()[1]
        print()

    except:
        # Echo back the unexpected error so the user can see it.
        print("\nCaught an unexpected exception in the pdfCropMargins program.",
                                                               file=sys.stderr)
        print("Unexpected error: ", sys.exc_info()[0], file=sys.stderr)
        print("Error message   : ", sys.exc_info()[1], file=sys.stderr)
        print()
        exit_code = 1
        import traceback
        max_traceback_length = 30
        traceback.print_tb(sys.exc_info()[2], limit=max_traceback_length)
        # raise # Re-raise the error.

    finally:
        # Some people like to hit multiple ^C chars, which kills cleanup.
        # Call cleanup again each time.
        for i in range(30): # Give up after 30 tries.
            try:
                cleanup_and_exit(exit_code)
            except (KeyboardInterrupt, EOFError):
                continue


#
# Run when invoked as a script.
#

if __name__ == "__main__":

    main()

