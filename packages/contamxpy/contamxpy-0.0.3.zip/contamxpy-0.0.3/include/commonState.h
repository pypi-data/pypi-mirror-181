#ifndef _COMMONSTATE_H_
#define _COMMONSTATE_H_

#include "types.h"
#include "string-len-max.h"
#include <stdio.h>

/*
// Note: the error-output module exposes common state variables that allow the
// programmer to modify the destination and handling of errors.
//   Unless specific action is taken, the error-output module reports
// all errors to {stderr}, and a fatal error terminates the program
// without taking any action (e.g. to shut down open files).
//   To change this behavior, attach a file or function to an appropriate
// cpommon state variable.
//   Note that attaching a file or function, rather than calling it directly,
// decouples the error-output module from the particulars of the program
// using it.  This makes it easier to write unit tests of other code modules
// that report errors, by:
// (1) reducing the number of functions and variables that must be
// defined in order to link the unit test code; and
// (2) allowing the unit test code to customize the error reports.

// {errorAuxFcnP}: Ptr to an auxiliary fcn for reporting errors.  If set, all
// error reports go to this fcn.  If not set, all error reports go to {stderr}.
void (* errorAuxFcnP)
  (const char *const headerStr,
  char *const messageStr, int *const nonFatalErrorCt) = NULL;

// {errorLogFileFcnP}: Ptr to a auxiliary fcn for writing to a log.  If set, and the file open, all
// error reports logged to the file (in addition to the regular error output).
// Caller is responsible for opening, closing, and otherwise managing the file.
int (*errorLogFileFcnP)(FILE *ulog, const char* fmt, ...) = NULL;

// {errorFinishFcnP}: Ptr to an auxiliary fcn for closing down the program
// after a fatal error.  If not set, no special action is taken.
void (* errorFinishFcnP)
  (const IX flag) = NULL;
  //   Arg {flag}:
  // 0 for successful termination;
  // 1 for termination due to excessive severe errors, or at user request;
  // 2 for termination due to a fatal error.
  */

#ifdef _DEBUG
#define MEMTEST_GUARD_BYTES  1
#define MEMTEST_LEAKS        1
#define MEMTEST_LOG_ACTIONS  1
#else
#define MEMTEST_GUARD_BYTES  0
#define MEMTEST_LEAKS        0
#define MEMTEST_LOG_ACTIONS  0
#endif

#if( MEMTEST_LEAKS )
  // Record each memory allocation.
typedef struct memlist
{
  struct memlist* next;  // Pointer to next struct.
  void* allocMemP;       // Pointer to allocated memory.
  size_t allocSize;      // Number of bytes allocated (including guard bytes).
  char name[20];         // Name of variable allocated.
}  MEMLIST;
#endif

typedef struct commonState
{
  
  FILE* ulog; //pointer to log file
  void (*errorAuxFcnP)
    (struct commonState *cs,const char* const headerStr,
      char* const messageStr, int* const nonFatalErrorCt);
  int (*errorLogFileFcnP)(FILE* ulog, const char* fmt, ...);
  void (*errorFinishFcnP)
    (struct commonState*cs, const IX flag);
  int nonFatalErrorCt;
  // Directory separator character.
  char dirchr;
#if( MEMTEST_LEAKS )
  MEMLIST* memList;
#endif
  size_t bytesAllocated;
  size_t bytesFreed;
  FILE* unxt;
  IX    echo;  
  I1 lastError[LINELEN]; // buffer to hold the last error message from the error function
} CommonState;

void initCommonState(CommonState* cs);

#endif