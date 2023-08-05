/** @file library-api.h
 *  @brief contam library API.
 *  @author Brian J. Polidoro (NIST)
 *  @author W. Stuart Dols (NIST)
 *  @date 2022-10-20
 *
 *  Data and functions that provide an interface to library files of CONTAM. 
 *  CONTAM Library files contain elements that can be used in CONTAM projects.
 */
#ifndef _LIBRARY_API_H_
#define _LIBRARY_API_H_

 /**
  * @defgroup LIBTYPE_GROUP Library Type Group
  *
  * @{
  */

  /** Contaminant Library Type */
#define CTM_LIB_TYPE 0
  /** Schedule Library Type */
#define SCH_LIB_TYPE 1
  /** Wind Pressure Profile Library Type */
#define WPF_LIB_TYPE 2
  /** Path Airflow Element Library Type */
#define AFE_LIB_TYPE 3
  /** Duct Airflow Element Library Type */
#define DFE_LIB_TYPE 4
  /** Controls Library Type */
#define CTL_LIB_TYPE 5

  /** @} */

 /** @brief Used to get a state for a library.  A library state is needed to use the other library APIs.
  *
  *  @param[in] commonState This is a pointer to a state for common contam functionality.
  *  @return A pointer to a library state.
  */
void* cliGetNewLibraryState(void* commonState);

/** @brief Used to delete a state for a library. Delete a state when finished with it to avoid a memory leak.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliDeleteLibraryState(void* libraryState);

/** @brief Used to open an existing library file.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @param[in] libPath      This is the path to the exisiting library file.
 *  @param[in] type         This is the type of library file. See @ref LIBTYPE_GROUP.
 *  @param[in] tempPath     This is a path where temporary files are written. Must have write permission for that path.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliOpenLibrary(void* libraryState, char* libPath, int type, char* tempPath);

/** @brief Used to save a library to a file with an established path.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @param[in] description  This is description for the library file.  The description will be stored for that type.
 *  @param[in] type         This is the type of library file. See @ref LIBTYPE_GROUP.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliSaveLibrary(void* libraryState, char* description, int type);

/** @brief Used to save a library to a file with the given path.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @param[in] libPath      This is the path to a library file.
 *  @param[in] description  This is description for the library file. The description will be stored for that type.
 *  @param[in] type         This is the type of library file. See @ref LIBTYPE_GROUP.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliSaveLibraryAs(void* libraryState, char* libPath, char* description, int type);

/** @brief Used to get a description that is stored for a type of library.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] type                   This is the type of library file. See @ref LIBTYPE_GROUP.
 *  @param[in,out] descriptionBuffer  This is a char buffer where the description for the library file will be put.
 *  @param[in] descriptionBufferSize  This is the size of the descriptionBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliGetLibraryDescription(void* libraryState, int type, char* descriptionBuffer,
      unsigned int descriptionBufferSize);

/** @brief Used to delete an element from a library.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @param[in] elementType  This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementName  This is the name of the element to delete.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliDeleteLibraryElement(void* libraryState, char* elementType, char* elementName);

/** @brief Used to get the number of elements of a type in a library.
 *
 *  @param[in] libraryState This is a pointer to a state for a library.
 *  @param[in] elementType  This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @return The number of elements of the type specified. -1= if no project state given, -2= if element type is invalid
 */
int   cliGetNumberOfLibraryElements(void* libraryState, char* elementType);

/** @brief Used to get the default values of an element as a JSON string.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element default JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @param[in] elementSubType  This is the sub type of the element. This only used for elements with sub types.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliGetDefaultLibraryElement(void* libraryState, char* elementType, char* elementJSONbuffer,
      int elementJSONbufferSize, unsigned short elementSubType);

/** @brief Used to get the values of an element as a JSON string using its name.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementName            This is the name of the element to get. 
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element default JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliGetLibraryElementByName(void* libraryState, char* elementType, char* elementName,
      char* elementJSONbuffer, int elementJSONbufferSize);

/** @brief Used to get the values of an element as a JSON string using its number.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementNumber          This is the number of the element to get. It will be in the range 1 to Number of Elements.
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element default JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliGetLibraryElementByNumber(void* libraryState, char* elementType, int elementNumber,
      char* elementJSONbuffer, int elementJSONbufferSize);

/** @brief Used to replace the values of an element using its name.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] exisitngElementName    This is the name of the element to replace.
 *  @param[in] elementJSONBuffer      This is a char buffer where the element JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliReplaceLibraryElement(void* libraryState, char* elementType, char* existingElementName,
      char* elementJSONbuffer);

/** @brief Used to add an element of the type given.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementJSONBuffer      This is a char buffer where the element JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cliAddLibraryElement(void* libraryState, char* elementType, char* elementJSONbuffer);

/** @brief Used to check if a name is used in the library by an element type.
 *
 *  @param[in] libraryState           This is a pointer to a state for a library.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] newElementName         This is the name of the element to test.
 *  @return -1= no state given, 1 = name is used, 0 = name is not used
 */
int   cliCheckNewLibraryElementName(void* libraryState, char* elementType, char* newElementName);

#endif