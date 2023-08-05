/** @file string-len-max.h */
/* Define max lengths for strings. */

#ifndef _STRING_LEN_MAX_H_
#define _STRING_LEN_MAX_H_


#include <limits.h>
#include <stdio.h>
#include <stdlib.h>


//--- Preprocessor definitions.
#define LINELEN 4096 // TODO wsd - this was 256 but issues with getcwd() in contam-x-main on Linux where MAX_PATH = 4096
#define NOTELEN 72   /* > CONTAM96 (67) */
#define NMLN   5
#define NMLN1 16     /**< maximum length of level names. */
#define NMLN2 32     /**< Maximum length of zone names. */
#define NAMELEN 16   /**< Maximum length of other named items, e.g., airflow elements. */ 

#ifndef _MAX_PATH    // Windows/DOS defined in <stdlib.h>
//
# ifdef PATH_MAX     // GNUC parameter defined in <limits.h>
#  define _MAX_PATH  PATH_MAX  // PATH_MAX = max bytes in a pathname.
#  define _MAX_DIR   PATH_MAX
# elif defined FILENAME_MAX  // Should always be defined in <stdio.h>.
#  define _MAX_PATH  FILENAME_MAX
#  define _MAX_DIR   FILENAME_MAX
# else
#  define _MAX_PATH  260  // VisualC++ value
#  define _MAX_DIR   256  // VisualC++ value
# endif  // End #ifdef PATH_MAX.
//
# ifdef NAME_MAX     // GNUC parameter defined in <limits.h>
#  define _MAX_FNAME NAME_MAX  // NAME_MAX = max bytes in a filename.
# elif defined FILENAME_MAX  // Should always be defined in <stdio.h>.
#  define _MAX_FNAME FILENAME_MAX
# else
#  define _MAX_FNAME 256  // VisualC++ value
# endif  // End #ifdef NAME_MAX.
//
# define _MAX_DRIVE 4    // 3 minimum (3 VisualC++)
# define _MAX_EXT   8    // 5 minimum (256 VisualC++)
//
#endif  // End #ifndef _MAX_PATH


#endif  // End #ifndef _STRING_LEN_MAX_H_.
