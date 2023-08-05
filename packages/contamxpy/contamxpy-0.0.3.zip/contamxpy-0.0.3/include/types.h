/** @file types.h */
#ifndef TYPES_H
# define TYPES_H

#if(_MSC_VER)
# include <stdint.h>
#elif(__GNUC__)
# include <inttypes.h>
#endif

typedef char I1;           /**< 1 byte signed integer */
typedef int16_t I2;        /**< 2 byte signed integer */
typedef int32_t I4;        /**< 4 byte signed integer */
typedef int64_t I8;        /**< 8 byte signed integer */
typedef int32_t IX;        /**< 4 byte signed integer to
                               maintain /32bit/64bit/cross-platform consistancy */
typedef unsigned char U1;  /**< 1 byte unsigned integer */
typedef uint16_t U2;       /**< 2 byte unsigned integer */
typedef uint32_t U4;       /**< 4 byte unsigned integer */
typedef uint32_t UX;       /**< 4 byte unsigned integer */
typedef float R4;          /**< 4 byte real value */
typedef double R8;         /**< 8 byte real value */
typedef long double RX;    /**< 10 byte real value (extended precision) */

// hoho dml  Using "I1" where truly mean "char" (for instance, in string
//   fcns) is a bad idea, because it obscures meaning.  Only reason to
//   use these typedefs is in cases where might have a machine dependency
//   of interest, e.g., where need to do something special to make R8
//   have the expected precision.  But calling standard library fcns
//   that expect a char, don't want to label the char an "I1", because
//   that would prevent you from ever redefining "I1" in the typedef... and
//   if you can't change the typedef, then there's no reason to use it.


#endif  // End #ifndef _TYPES_H_.
