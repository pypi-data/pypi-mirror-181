/** @file contam-x-cosim.h
 *  @brief contam-x-cosim API.
 *  @author Brian J. Polidoro (NIST)
 *  @author W. Stuart Dols (NIST)
 *  @date 2021-09-07
 *
 *  Data and function that provide an interface to dynamic link libray version of ContamX.
 */
#ifndef _CONTAM_X_COSIM_H_
#define _CONTAM_X_COSIM_H_

#include "types.h"
#include "string-len-max.h"

// if using windows then must define either CONTAM_EXPORT or CONTAM_IMPORT
// CONTAM_EXPORT is for building the contamx-lib library
// CONTAM_IMPORT is for using contamx-lib library
#ifdef _WIN32
#ifdef CONTAM_EXPORT
#define CONTAM_API __declspec(dllexport)
#elif CONTAM_IMPORT
#define CONTAM_API __declspec(dllimport)
#else
#define CONTAM_API
#endif
#else
#define CONTAM_API
#endif

/** The zone_cosim_dsc data structure contains zone information relavant to use
 *  of the contam-x-cosim API.  
 *  
 *  Each zone in a CONTAM PRJ (including implicit supply and return zones of each
 *  simple air-handling system) is represented by an <EM>airflow node</EM> during
 *  a ContamX simulation.
 */
typedef struct zone_cosim_dsc
{
  IX nr;                  /**< zone number */
  U2 flags;               /**< Airflow Node flags:
                               \li bit 0 (0x01) variable Pressure node
                               \li bit 1 (0x02) variable Mass fraction node
                               \li bit 2 (0x04) variable Temperature node
                               \li bit 3 (0x08) implicit Simple AHS node, i.e., supply or return
                               \li bit 4 (0x10) unconditioned node
                               \li bit 5 (0x20) node volume > 0, i.e., not massless */
  R4 Vol;                 /**< zone volume [m<SUP>3</SUP>] */
  I1 level_name[NAMELEN]; /**< level name */
  IX level_nr;            /**< level number */
  I1 name[NMLN2];         /**< zone name \n
                           * \b NOTE: Implicit supply and return zones of 
                           * simple air-handling systems (SAHS) will have either
                           * "(Sup)" or "(Ret)" appended to the name of the SAHS
                           * with which they are associated. */
} ZONE_COSIM_DSC;

/** The jct_cosim_dsc data structure contains duct junction information relavant to use
 *  of the contam-x-cosim API.  
 *
 *  Each duct junction, including terminals, in a CONTAM PRJ is represented by an 
 *  <EM>airflow node</EM> during a ContamX simulation. Therefore jct_cosim_dsc
 *  is similar to zone_cosim_dsc.
 */
typedef struct jct_cosim_dsc
{
  IX nr;              /**< junction number */
  U2 flags;           /**< Airflow Node flags:
                           \li bit 0 (0x01) variable Pressure node
                           \li bit 1 (0x02) variable Mass fraction node
                           \li bit 2 (0x04) variable Temperature node
                           \li bit 4 (0x10) unconditioned node
                           \li bit 5 (0x20) node volume > 0, i.e., not massless */
  IX containing_zone; /**< Zone number in which the junction is located */
  IX envIndex;        /**< Index identifies order of specifying values in WPC file and used to reference 
                       *   specific terminals located in ambient when using the contam-x-cosim API. 
                       *   This value will be zero for terminals not located in ambient. */
} JCT_COSIM_DSC;

/** The path_cosim_dsc data structure contains airflow path information for airflow paths 
 *  accessible via the contam-x-cosim API.
 *
 *  Each airflow path in a CONTAM PRJ is represented by an <EM>airflow link</EM> which connects 
 *  two <EM> airflow nodes </EM> during a ContamX simulation. a path_cosim_dsc structure
 *  will be associated with items on the SketchPad:
 *    \li each airflow path represented by an <EM>airflow path icon</EM>
 *    \li each supply or return airflow path associated with a simple air-handling system
 *    \li implicit flow paths associated with each simple air-handling system including: 
 *        an outdoor air intake, exhaust, and recirculation flow path
 *    \li a leakage flow path for each duct leakage associated with a duct junction
 * 
 *  COORDINATE SYSTEM: The coordinate system is user-defined and not validated via CONTAM.  
 *  It is the responsibility of the PRJ developer to establish the convention of the 
 *  coordinate system being used.
 */
typedef struct path_cosim_dsc 
{
  IX nr;        /**< Airflow path sequence number assigned by ContamX. */
  U2 flags;     /**< Airflow path flag values: 
                      \li 0x0001 possible wind pressure
                      \li 0x0002 path uses WPC file pressure
                      \li 0x0004 path uses WPC file contaminants
                      \li 0x0008 Simple air-handling system (SAHS) supply or return path
                      \li 0x0010 SAHS recirculation flow path
                      \li 0x0020 SAHS outside air flow path
                      \li 0x0040 SAHS exhaust flow path
                      \li 0x0080 path has associate pressure limits
                      \li 0x0100 path has associate flow limits
                      \li 0x0200 path has associated constant airflow element
                      \li 0x0400 junction leak path */
  IX from_zone; /**< Zone number, positive airflow when flow is from this zone. */
  IX to_zone;   /**< Zone number, positive airflow when flow is to this zone. */
  IX ahs_nr;    /**< The number of the Simple Air-handling System that the path serves - return/supply only. */
  R4 X;         /**< X coordinate of the airflow path, units [m]. This value is enterred directly in ContamW. */
  R4 Y;         /**< Y coordinate of the airflow path, units [m]. This value is enterred directly in ContamW. */
  R4 Z;         /**< Z coordinate of the airflow path, units [m]. 
                  *  This value is obtained from the Relative Elevation enterred in ContamW and 
                  *  the elevation of the level on which the path is defined. */
  IX envIndex;  /**< Index identifies order of specifying values in WPC file and used to reference 
                  * specific envelope paths when using the contam-x-cosim API. This value will be zero 
                  * for interior flow paths, i.e., those not connected to ambient. */
} PATH_COSIM_DSC;

/** The term_cosim_dsc data structure contains duct terminal information relavant to the use
 *  of the contam-x-cosim API. ContamX creates an <EM>airflow link</EM> to represent the
 *  connectivity of the terminal between <EM>airflow nodes</EM> associated with the terminal
 *  (represented by jct_cosim_dsc) and the zone in which the terminal is located. Therefore,
 *  this data structure is similar to path_cosim_dsc.
 *
 *  COORDINATE SYSTEM: The coordinate system is user-defined and not validated via CONTAM. 
 *  It is the responsibility of the PRJ developer to establish the convention of the
 *  coordinate system being used.
 */
typedef struct term_cosim_dsc
{
  IX nr;        /**< junction number */
  U2 flags;     /**< Airflow path flag values:  
                     \li 0x01 terminal has wind pressure associated with it
                     \li 0x02 terminal uses WPC file pressure */
  R4 X;         /**< X coordinate of the airflow terminal, units [m]. This value is enterred directly in ContamW. */
  R4 Y;         /**< Y coordinate of the airflow terminal, units [m]. This value is enterred directly in ContamW. */
  R4 Z;         /**< Z coordinate of the airflow terminal, units [m]. 
                 *   This value is obtained from the Relative Elevation enterred in ContamW and 
                 *   the elevation of the level on which the terminal is defined. */
  R4 relHt;     /**< terminal height relative to level [m] */
  IX to_zone;   /**< Zone number in which the terminal is located */
  IX envIndex;  /**< Index identifies order of specifying values in WPC file and used to reference 
                 *   specific terminals located in ambient when using the contam-x-cosim API. 
                 *   This value will be zero for terminals not located in ambient. */
} TERM_COSIM_DSC;

/** The control_cosim_dsc data structure contains control information relavant to use
 *  of the contam-x-cosim API.
 *
 *  Two types of controls can be used to pass Input to and Output from ContamX via
 *  the API: Constant (CT_SET) and Signal Split or pass-through (CT_PAS), respectively.
 *  The number of each control type in a project can be obtained by cxiGetNumInputControlNodes()
 *  and cxiGetNumOutputControlNodes(), respectively. This data structure can then be populated
 *  with control data by iterating through the list of controls and using cxiGetControlInfo() to
 *  create local lists of controls as needed. Control values can then be Set and Get via 
 *  cxiSetInputControlValue() and cxiGetOutputControlValue(), respectively.
 *
 *  SEE ALSO: cxiGetNumInputControlNodes(), cxiGetNumOutputControlNodes(), cxiGetInputControlInfo(), \n
 *  cxiGetOutputControlInfo(), cxiSetInputControlValue(), cxiGetOutputControlValue()
 */
typedef struct control_cosim_dsc
{
  IX nr;                  /**< control number */
  I1 name[NAMELEN];       /**< control name   */
} CONTROL_COSIM_DSC;

void* cxiGetContamState();

/** @brief Set ContamX to return INFIL and MIX flow rates as volumetric airflows [m<SUP>3</SUP>/s]
  *  as opposed to mass flow rates [kg/s]. 
  * @return N/A 
  *
  * This feature of ContamX was incorporated for co-simulation between 
  * EnergyPlus and CONTAM. ContamX will convert the mass flows using the EnergyPlus 
  * psychromatric function PsyRhoAirFnPbTdbW() according to the rules for
  * calcuating interzone, infiltration, and ventilation system flows in EnergyPlus. 
  *
  * SEE ALSO: cxiGetPathFlows(), cxiGetTermFlow(), cxiGetLeakFlow()
  */
CONTAM_API void cxiSetUseVolumeFlows(void* contamXState);

/** @brief Set wind pressure calculation mode.
 *  This function must be called in the beginning of a simulation prior to cxiSetupSimulation() to
 *  set the wind pressure calculation mode for the entire simulation period.
 *  @param[in] useWP  The wind pressure calculation method.
 *    0 = CONTAM computes wind pressures using WTH-like messages
 *        and ambient Mass Fractions using CTM-like messages, i.e., cxiSetAmbtXXX messages.
 *    1 = Use envelope-related functions of the contam-x-cosim API to 
 *        set wind pressure of individual envelope flow paths (default), i.e., cxiSetEnvelopeXXX.
 *  @return N/A
 */
CONTAM_API void cxiSetWindPressureMode(void* contamXState, IX useWP);

/** @brief Set a function pointer to a user-defined callback function.
 *  The cxiRegisterCallback_PrjDataReady() function should be called at the 
 *  very beginning of a co-simulation. Then the cxiSetupSimulation() function should 
 *  be called which will in turn cause the user-defined function to be called. 
 *
 *  The user-defined callback function can be used to obtain project-related information 
 *  that will be needed for other functions during the transient simulation. For example, 
 *  cxiGetNumPaths() and cxiGetPathInfo() can be called to obtain path-related information.
 *
 *  \b NOTE: The following functions must not be called prior to calling cxiRegisterCallback_PrjDataReady() :
 *  cxiDoCoSimStep(), cxiEndSimulation(), cxiGetAHSNumber(), cxiGetCtmName(), cxiGetCurrentDate(), 
 *  cxiGetCurrentTime(), cxiGetEnvelopeExfil(), cxiGetInputControlNumber(), cxiGetLeakFlow(), cxiGetLeakInfo(), 
 *  cxiGetLeakNumber(), cxiGetNumAHS(), cxiGetNumCtms(), cxiGetNumInputCtrlNodes(), cxiGetNumJunctions(), 
 *  cxiGetNumLeaks(), cxiGetNumOutputCtrlNodes(), cxiGetNumPaths(), cxiGetNumTerminals(), cxiGetNumZones(), 
 *  cxiGetOutputControlNumber(), cxiGetOutputControlValue(), cxiGetPathFlows(), cxiGetSimulationEndDate(), 
 *  cxiGetSimulationEndTime(), cxiGetSimulationStartDate(), cxiGetSimulationStartTime(), cxiGetSimulationTimeStep(), 
 *  cxiGetTermFlow(), cxiGetTermInfo(), cxiGetZoneMF(), cxiGetZoneNumber(), cxiGetZoneVolume(), cxiSetAHSPercentOA(), 
 *  cxiSetAmbtHumRatio(), cxiSetAmbtPressure(), cxiSetAmbtTemperature(), cxiSetAmbtWndDir(), cxiSetAmbtWndSpd(), 
 *  cxiSetEnvelopeMF(), cxiSetEnvelopeWP(), cxiSetInputControlValue(), cxiSetJunctionTemperature(), 
 *  cxiSetSupplyReturnPathFlow(), cxiSetZoneHumRatio(), cxiSetZoneTemperature(), cxiSetZoneAddMass().
 *
 *  \b NOTE: The following functions may only be called within the user-defined callback function :
 *  cxiGetJunctionInfo(), cxiGetPathInfo(), cxiGetZoneInfo().
 *
 *  @param prjDataReadyFcnP pointer to user-defined callback function.
 */
CONTAM_API void cxiRegisterCallback_PrjDataReady( void* contamXState, void* pUserData, void ( *prjDataReadyFcnP )( void*, void* ) );

// set the function to call when errors occur
/** @todo */
CONTAM_API void cxiSetErrorFunction(void* contamXState, void (*errorAuxFcnP)(void *cxs,const char* const headerStr,
  char* const messageStr, int* const nonFatalErrorCt));

/** @brief Setup the simulation including the option to run ContamX in the co-simulation mode.
 *  Calling cxiSetupSimulation() with \p useCosim set to \e 1 results in the calling of the 
 *  user-defined callback function as set by cxiRegisterCallback_PrjDataReady().
 *  This must be done in order to run a co-simulation with ContamX.
 *
 *  @param[in] projectPath The file system path to the CONTAM PRJ file on which to run
 *             the simulation.
 *  @param[in] useCosim Select ContamX run mode: 
 *             0 = run a CONTAM only simulation, 
 *             1 = run ContamX in co-simulation mode.
 */
CONTAM_API void cxiSetupSimulation(void* contamXState, char* projectPath, IX useCosim);

//=============================================================================
// The following functions must NOT be called before the project data ready 
// callback function has been called. 
//=============================================================================

//=============================================================================
// Date & Time
//=============================================================================

/** @brief Get the starting date of a transient simulation.
 *  @return Day of year (1 - 365).
 */
CONTAM_API IX cxiGetSimulationStartDate(void* contamXState);

/** @brief Get the starting time of a transient simulation.
 *  @return Time of day (0 - 86400) [s].
 */
CONTAM_API IX cxiGetSimulationStartTime(void* contamXState);

/** @brief Get the end date of a transient simulation.
 *  @return Day of year (1 - 365).
 */
CONTAM_API IX cxiGetSimulationEndDate(void* contamXState);

/** @brief Get the end time of a transient simulation.
 *  @return Time of day (0 - 86400) [s].
 */
CONTAM_API IX cxiGetSimulationEndTime(void* contamXState);

/** @brief Get calculation time step from the simulation parameters.
 *
 *  ContamW enforces entry of the calculation time step so that it divides evenly into 3600.
 *  @return Simulation time step, t_step, as defined in PRJ file (1 - 3600) [s]
 */
CONTAM_API IX cxiGetSimulationTimeStep(void* contamXState);

/** @brief Get the current simulation day of the year.
 *  @return Day of the year (1 - 365: 1 = Jan01, 365 = Dec31)
 */
CONTAM_API IX cxiGetCurrentDate(void* contamXState);

/** @brief Get the current simulation time of day.
 *  @return Time of day (0 - 86400) [s]
 */
CONTAM_API IX cxiGetCurrentTime(void* contamXState);

//=============================================================================
// Simulation Control
//=============================================================================

/** @brief Perform calculations for a single simulation time step.
 *  
 *  \b NOTE: Currently this should only be run with \p stepForward set to 1.
 *  @param[in] stepForward 0 = rerun the current time step, 1 = run next time step.
 */
CONTAM_API void cxiDoCoSimStep(void* contamXState, IX stepForward);

/** @brief This function must be called at the end of a co-simulation.
 *  This should only be called once all timesteps of the co-simulation
 *  have been completed, i.e., after cxiDoCoSimStep() has been called for
 *  the values obtained for the ending date and time of the simulation.
 *  
 *  SEE ALSO: cxiGetSimulationEndDate(), cxiGetSimulationEndTime()
 */
CONTAM_API void cxiEndSimulation(void* contamXState);

/** @brief Get version string for contam-x-cosim.
 *  Example version string: "3.4.0.1-64bit"
 *  @param[out] strVersion Pointer to string of _MAX_FNAME (typically 256) characters.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 2 => error, \p strVersion == NULL
 */
CONTAM_API IX cxiGetVersion(void* contamXState, char* strVersion);

//=============================================================================
// Contaminant info
//=============================================================================

/** @brief Get the number of contaminants in the PRJ file.
 *  The list of contaminants in the PRJ file refers to species defined in the PRJ file by number.
 *  @return Number of contaminants being simulated (cxs->nctm).
 */
CONTAM_API IX cxiGetNumCtms(void* contamXState);

/** @brief Get name of contaminant by number.
 *  The number of contaminants in the PRJ can be obtained from cxiGetNumCtms().
 *  @param[in] ctmNumber Zero-based index of contaminant being used in the simulation.
 *  @param[out] *strName Pointer to character buffer into which contaminant name will be copied.
 *   The buffer should be at least #NAMELEN characters long.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p ctmNumber out of range
 *    \li 2 => error, \p strName == NULL
*/
CONTAM_API IX cxiGetCtmName(void* contamXState, IX ctmNumber, char* strName);

//=============================================================================
// Ambient
//=============================================================================

/** @brief Set the ambient temperature.
 *  This function is used when simulating weather in a manner similar to a WTH file.
 *  cxiSetWindPressureMode(0) should be called in at the beginning of the simulation
 *    in order to utilize this method.
 *  @param[in] ambtTemp Ambient temperature [K].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, ambtTemp < 0
 *
 *  @todo Clarify use of this function in relation to the cxiSetEnvelopeXXX() functions,
 *        i.e., can they be used together. Seems they can but need to verify performance
 *        when mixing the Ambt and Envelope functions. Likely, users should use one
 *        or the other for now to avoid confilicting behavior.
 */
CONTAM_API IX cxiSetAmbtTemperature(void* contamXState, R4 ambtTemp);

/** @brief Set the ambient pressure.
 *  This function is used when simulating weather in a manner similar to a WTH file.
 *  cxiSetWindPressureMode(0) should be called in at the beginning of the simulation 
 *    in order to utilize this method.
 *  @param[in] ambtPres Ambient pressure [Pa].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, ambtPres < 0
 * 
 *  SEE ALSO: cxiSetWindPressureMode()
 *  @todo Clarify use of this function in relation to the cxiSetEnvelopeXXX() functions,
 *        i.e., can they be used together. Seems they can but need to verify performance
 *        when mixing the Ambt and Envelope functions. Likely, users should use one
 *        or the other for now to avoid confilicting behavior.
 */
CONTAM_API IX cxiSetAmbtPressure(void* contamXState, R4 ambtPres);

/** @brief Set the wind speed.
 *  This function is used when simulating weather in a manner similar to a WTH file.
 *
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(0)" should be called at the
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize
 *        this method.
 *
 *  @param[in] wndSpd Wind speed [m/s].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, wndSpd < 0
 */
CONTAM_API IX cxiSetAmbtWndSpd(void* contamXState, R4 wndSpd);

/** @brief Set the wind direction.
 *
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(0)" should be called at the
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize
 *        this method.
 *
 *  @param[in] wndDir Wind direction from North (0 - 360) [degrees].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, wndDir < 0 OR > 360
 */
CONTAM_API IX cxiSetAmbtWndDir(void* contamXState, R4 wndDir);

/** @brief Set the ambient humidity ratio.
 *  This function is used when simulating weather in a manner similar to a WTH file.
 *
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(0)" should be called at the
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize
 *        this method.
*   @todo
*/
CONTAM_API IX cxiSetAmbtHumRatio(void* contamXState, R4 humRatio);

/** @brief Set the ambient mass fraction of selected contaminant.
 *
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(0)" should be called at the
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize
 *        this method.
 *
 *  @param[in] ctmNumber  Contaminant number of mass to add (0 - cxs->nctm-1).
 *  @param[in] Mf         Mass fraction (>= 0.0) [kg_contaminant/kg_air].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p ctmNumber out of range
 *    \li 2 => error, \p Mf less than zero
 *    \li 3 => error, incorrect wind pressure mode
 *  @todo
 */
CONTAM_API IX cxiSetAmbtMassFraction(void* contamXState, I4 ctmNumber, R8 Mf);

//=============================================================================
// Zones
//=============================================================================

/** @brief Get the number of zones in the PRJ file.
 *  @return Number of zones in the project (cxs->nzone).
 */
CONTAM_API IX cxiGetNumZones(void* contamXState);

/** @brief Get the numeric identifier of a zone based on its name and level on which it is located. 
 *  @param[in] *zoneName String that provides the name of the zone for which to
 *             obtain the numeric identifier.
 *  @param[in] zoneLevelNumber Level number on which the desired zone is located.
 *  @param[out] *pZoneNumber Pointer to data to be populated by the numeric zone identifier.
 *
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p zoneName == NULL OR length == 0 \n
 *    \li 2 => error, \p zoneLevelNumber out of range \n
 *    \li 3 => error, \p *pZoneNumber == NULL
 *    \li 4 => error, \b cxs->ZoneList == NULL. \n 
 *          \b cxs->ZoneList is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *
 *  SEE ALSO: cxiGetNumZones(), cxiRegisterCallback_PrjDataReady()
 *
 *  @todo Currently the only way to obtain the number of levels in a PRJ is
 *        by using cxiGetZoneInfo() to obtain all the zone information and 
 *        checking all the level numbers.
 *
 */
CONTAM_API IX cxiGetZoneNumber(void* contamXState, const char* zoneName, IX zoneLevelNumber, IX* pZoneNumber);

/** @brief Get information about selected zone.
 *  This function should only be called from within the projectDataReady callback function.
 *  @param[in] zoneNumber Zone number assigned by ContamW.
 *  @param[out] *pZoneInfo Pointer to structure to be populated with zone information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \b cxs->ZoneList == NULL.\n 
 *          \b cxs->ZoneList is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 2 => error, \p pZoneInfo == NULL \n
 *    \li 3 => error, \p zoneNumber out of range (1 - cxs->nzone)
 *
 *  SEE ALSO: cxiGetNumZones(), cxiRegisterCallback_PrjDataReady()
 */
CONTAM_API IX cxiGetZoneInfo(void* contamXState, IX zoneNumber, ZONE_COSIM_DSC* pZoneInfo);

/** @brief Get the volume of the specified zone. 
 *  @param[in] zoneNumber Zone number assigned by ContamW.
 *  @param[out] *pVolume Pointer to structure to be populated with zone volume, units [m<SUP>3</SUP>].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \b cxs->cosim.cosim_zone_list == NULL.\n 
 *          \b cxs->cosim.cosim_zone_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 2 => error, \p pVolume == NULL \n
 *    \li 3 => error, \p zoneNumber out of range (1 - cxs->nzone)
 *
 *  SEE ALSO: cxiGetNumZones(), cxiRegisterCallback_PrjDataReady()
 *
 *  @todo BJP why does this use cxs->cosim.cosim_zone_list but other functions use cxs->ZoneList?
 */
CONTAM_API IX cxiGetZoneVolume(void* contamXState, IX zoneNumber, R4 *pVolume);

/** @brief Set the temperature of the specified zone.
 *  @param[in] zoneNumber Zone number assigned by ContamW.
 *  @param[in] temperature Value of zone temperature, units [K].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p zoneNumber out of range (1 - cxs->nzone)\n 
 *    \li 2 => error, \p temperature < 0\n
 *
 *  SEE ALSO: cxiGetNumZones(), cxiGetZoneInfo()
 */
CONTAM_API IX cxiSetZoneTemperature(void* contamXState, IX zoneNumber, R8 temperature);

/** @brief Set the humidity ratio of the specified zone.
 *  @param[in] zoneNumber Zone number assigned by ContamW.
 *  @param[in] humRatio Value of zone humidity ratio, units [kg_H2O/kg_air].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p zoneNumber out of range (1 - cxs->nzone)\n 
 *    \li 2 => error, \p temperature < 0\n
 *
 *  This feature of ContamX was incorporated for co-simulation between 
 *  EnergyPlus and CONTAM. ContamX utilizes the humidity ratio to convert 
 *  the mass flows using the EnergyPlus psychromatric function PsyRhoAirFnPbTdbW()
 *  which requires the humidity ratio as a parameter. 
 *
 *  SEE ALSO: cxiGetNumZones(), cxiGetZoneInfo()
 */
CONTAM_API IX cxiSetZoneHumRatio(void* contamXState, IX zoneNumber, R8 humRatio);

/** @brief Add mass to the specified zone.
 *  @param[in] zoneNumber Zone number assigned by ContamW (1 - cxs->nzone).
 *  @param[in] ctmNumber  Contaminant number of mass to add (0 - cxs->nctm-1).
 *  @param[in] addMass Amount of mass to add to the zone, units [kg_contaminant].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p zoneNumber out of range  
 *    \li 2 => error, \p addMass < 0  
 *    \li 3 => error, \p ctmNumber out of range  
 *
 *  SEE ALSO: cxiGetNumZones(), cxiGetZoneInfo(), cxiGetNumCtms()
 *
 *  @todo cxiSetZoneAddMass: WSD Does not currently work with massless nodes, and
 *        Need to test for 1D convection\diffusion zones.
 *  @todo cxiSetZoneAddMass check use of doBridgeMf flag when using this function.
 *  @todo cxiSetZoneAddMass Investigate differences between use of this function compared
 *        to using a source. There appears to be some discrepancies in resulting max
 *        concentrations after release.
 *
 */
IX cxiSetZoneAddMass(void* contamXState, IX zoneNumber, IX ctmNumber, R8 addMass);

/** @brief Get contaminant mass fraction of a zone.
 *  @param[in] zoneNumber The zone number for which to obtain the current mass fraction (1 - cxs->nzone).
 *  @param[in] ctmNumber Zero-based index of contaminant (0 - cxs->nctm-1).
 *  @param[out] *pMassFraction Pointer to variable in which to place the mass fraction, units [kg_cont/kg_air].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pMassFraction == NULL
 *    \li 2 => error, \p zoneNumber out of range
 *    \li 3 => error, \p ctmNumber out of range
 *
 *  SEE ALSO: cxiGetNumCtms(), cxiGetCtmName(), cxiGetNumZones()
 */
CONTAM_API IX cxiGetZoneMF(void* contamXState, IX zoneNumber, IX ctmNumber, R8* pMassFraction);

//=============================================================================
// Airflow Paths
//=============================================================================

/** @brief Get number of airflow paths in the PRJ file. 
 *  This is the total number of airflow paths in the project
 *  including simple air-handling system paths.
 *  @return Number of airflow paths (cxs->npath).
 * 
 */
CONTAM_API IX cxiGetNumPaths(void* contamXState);

/** @brief Get information about an airflow path.
 *  This function should only be called from within the projectDataReady callback function.
 *  @param[in] pathNumber Airflow path number assigned by ContamW.
 *  @param[out] *pPath Pointer to structure to be populated with path information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \b cxs->cosim.cosim_path_list == NULL \n
 *          \b cxs->cosim.cosim_path_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p pathNumber out of range (1 - cxs->npath)
 *
 *  SEE ALSO: cxiGetNumPaths()
 */
CONTAM_API IX cxiGetPathInfo(void* contamXState, IX pathNumber, PATH_COSIM_DSC* pPath);

/** @brief Get airflow rate of selected airflow path.
 *  @param[in] pathNumber Number of airflow path for which to obtain airflow rate.
 *  @param[out] *pFlow0 Pointer to data to which primary airflow rate is to be written.
 *              All airflow paths will have at least one airflow rate associated
 *              with them as provided by \p pFlow0. The sign of the airflow rate will
                be releative to the positive direction established for the specified 
                airflow path. This information is available via the cxiGetPathInfo()
                function.
 *  @param[out] *pFlow1 Pointer to data to which secondary airflow rate is to be written.
 *              Two-way airflow paths can have flow in both directions. In which
 *              case the flow in the negative direction will be provided by this value.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p ppath == NULL
 *    \li 2 => error, \b cxs->cosim.cosim_path_list == NULL \n
 *          \b cxs->cosim.cosim_path_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady()
 *    \li 3 => error, \p pathNumber out of range (1 - cxs->npath)
 * 
 *  \b NOTE: Airflow units are provided in units of [kg/s] unless the cxiSetUseVolumeFlows()
 *  function is used to specify that ContamX should provide them as volumentric
 *  airflows in units of [m<SUP>3</SUP>/s].
 *
 *  SEE ALSO: cxiGetNumPaths(), cxiGetPathInfo(), cxiSetUseVolumeFlows()
 */
CONTAM_API IX cxiGetPathFlows(void* contamXState, IX pathNumber, R8* pFlow0, R8* pFlow1);

/** @brief Set the supply or return airflow rate of a specified airflow path
 *         of a simple air-handling system (SAHS).
 *  @param[in] pathNumber Airflow path number assigned by ContamW.
 *  @param[in] flow Value to which the airflow rate should be set, units [kg/s]. 
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pathNumber out of range (1 - cxs->npath)
 *    \li 2 => error, \p flow less than 0.0
 *    \li 3 => error, \p cxs->cosim.cosim_path_list == NULL
            \b cxs->cosim.cosim_path_list is populated by ContamX upon initialization 
 *          of a co-simulation prior to calling the user-defined callback function 
 *          established by cxiRegisterCallback_PrjDataReady().
 *    \li 4 => error, \p pathNumber is not a supply or return airflow path.
 *
 *  NOTE: cxiGetZoneInfo() can be used to determine which zones are implicit SAHS
 *        supply and return zones using the \b flags and \b Name fields of the zone_cosim_dsc
 *        data structure. cxiGetPathInfo() can then be used to determine if a SAHS
 *        supply or return path is connected to either an SAHS supply or return.  
 *
 *  SEE ALSO: cxiGetNumPaths(), cxiGetPathInfo(), cxiGetZoneInfo(), cxiRegisterCallback_PrjDataReady()
 *
 * @todo WSD This function sets the control value pointer \em pcv to \em &_one in
 *       order to override any schedules that might be associated with the
 *       supply/return airflow path being set. The airflow rate set by this
 *       function call will be maintained until it is changed by another
 *       call to this funtion.\n
 *       NEED TO VERIFY THIS BEHAVIOUR.
 */
CONTAM_API IX cxiSetSupplyReturnPathFlow(void* contamXState, IX pathNumber, R4 flow);

/** @brief Get number of Simple Air-handling Systems in the PRJ file. 
 *  @return Number of Simple AHSs (cxs->nahs).
 */
CONTAM_API IX cxiGetNumAHS(void* contamXState);

/** @brief Get the numeric identifier of a simple air-handling system (SAHS) 
 *         based on its name. 
 *  @param[in] *ahsName String that provides the name of the AHS for which to
 *             obtain the numeric identifier.
 *  @param[out] *pAhsNumber Pointer to data to be populated by the numeric SAHS identifier.
 *              This value will be set to -1 if \p ahsName can't be found.
 *
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p ahsName == NULL OR length == 0
 *    \li 2 => error, \p pAhsNumber == NULL
 *    \li 3 => error, \b cxs->AhsList == NULL 
 *          \b cxs->AhsList is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *
 *  SEE ALSO: cxiGetNumAHS(), cxiSetAHSPercentOA(), cxiRegisterCallback_PrjDataReady()
 */
CONTAM_API IX cxiGetAHSNumber(void* contamXState, const char* ahsName, IX* pAhsNumber);

/** @brief Set the outdoor airflow fraction of a simple air-handling system (SAHS).
 *  @param[in] ahsNumber Numeric identifier of the SAHS.
 *  @param[in] OAValue   Fraction of outdoor air to be deliverd by the supply airflow 
 *                       of the specified SAHS, (0.0 - 1.0). 
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p ahsNumber out of range (1 - cxs->nahs)
 *    \li 2 => error, \p OAValue out of range (0.0 - 1.0)
 *    \li 3 => error, \p cxs->cosim.cosim_oap_values_list == NULL
            \b cxs->cosim.cosim_oap_values_list is populated by ContamX upon initialization 
 *          of a co-simulation prior to calling the user-defined callback function 
 *          established by cxiRegisterCallback_PrjDataReady().
 *
 *  SEE ALSO: cxiGetNumAHS(), cxiGetAHSNumber(), cxiRegisterCallback_PrjDataReady()
 *
 * @todo WSD Will this fraction of outdoor air be maintained until it is changed
 *       by another message and/or another schedule value? Are schedule values
 *       overridden by this function?
 */
CONTAM_API IX cxiSetAHSPercentOA(void* contamXState, IX ahsNumber, R4 OAValue);

//=============================================================================
// Controls
//=============================================================================

/** @brief Get the number of input control nodes in the project.
 *  @return The number of input control nodes (cxs->cosim.num_cosim_inodes).
 *
 *  Input control nodes include those <EM>Constant</EM> type controls
 *  that have been provided with a name. Input controls can be used
 *  to pass user-defined information into ContamX during runtime.
 *
 *  SEE ALSO: cxiSetInputControlValue()
 */
CONTAM_API IX cxiGetNumInputCtrlNodes(void* contamXState);

/** @brief Get the number of output control nodes in the project.
 *  @return The number of output control nodes (cxs->cosim.num_cosim_onodes).
 *
 *  Output control nodes include those <EM>Signal Split</EM> type controls
 *  that have been provided with a name. Output controls can be used
 *  to pass user-defined information out of ContamX during runtime.
 *
 *  SEE ALSO: cxiGetOutputControlValue()
 */
CONTAM_API IX cxiGetNumOutputCtrlNodes(void* contamXState);

/** @brief Get information about an Input control.
 *  This function should only be called from within the projectDataReady callback function.
 *  @param[in] inputControlIndex Index into array of named Input controls.
 *  @param[out] *pControl Pointer to CONTROL_COSIM_DSC structure to be populated with Input control information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \b pControl == NULL \n
 *    \li 2 => error, \b cxs->cosim.cosim_inode_list == NULL \n
 *          \b cxs->cosim.cosim_inode_list is populated by ContamX upon initialization of a co-simulation
 *          prior to calling the user-defined callback function established by
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p inputControlIndex out of range (1 - cxs->cosim.num_cosim_inodes)
 *
 *  SEE ALSO: cxiGetNumInputCtrlNodes(), cxiSetInputControlValue()
 */
CONTAM_API IX cxiGetInputControlInfo(void* contamXState, IX inputControlIndex, CONTROL_COSIM_DSC* pControl);

/** @brief Get information about an Output control.
 *  This function should only be called from within the projectDataReady callback function.
 *  @param[in] outputControlIndex Index into array of named Output controls.
 *  @param[out] *pControl Pointer to CONTROL_COSIM_DSC structure to be populated with Input control information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \b pControl == NULL \n
 *    \li 2 => error, \b cxs->cosim.cosim_inode_list == NULL \n
 *          \b cxs->cosim.cosim_onode_list is populated by ContamX upon initialization of a co-simulation
 *          prior to calling the user-defined callback function established by
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p outputControlIndex out of range (1 - cxs->cosim.num_cosim_onodes)
 *
 *  SEE ALSO: cxiGetNumOutputCtrlNodes(), cxiGetOutputControlValue()
 */
CONTAM_API IX cxiGetOutputControlInfo(void* contamXState, IX outputControlIndex, CONTROL_COSIM_DSC* pControl);

/** @brief Set the value of an input control node.
 *  @param[in] inputCtrlNumber Control number assigned by ContamW.
 *  @param[in] ctrlValue Value to which control is to be set, units [-].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p inputCtrlNumber out of range (1 - cxs->cosim.num_cosim_inodes)\n
 */
CONTAM_API IX cxiSetInputControlValue(void* contamXState, IX inputCtrlNumber, R4 ctrlValue);

/** @brief Get the value of a specified output control node.
 *  @param[in] outputCtrlNumber The control number assigned by ContamW.
 *  @param[out] *pCtrlValue Pointer to data to be populated with the control value.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pCtrlValue == NULL
 *    \li 2 => error, there are no input control nodes
 *    \li 3 => error, \p outputCtrlNumber is out of range (1 - cxs->cosim.num_cosim_onodes)
 *
 *  SEE ALSO: cxiGetNumOutputCtrlNodes()
 */
CONTAM_API IX cxiGetOutputControlValue(void* contamXState, IX outputCtrlNumber, R4* pCtrlValue);

//=============================================================================
// Ducts
//=============================================================================

/** @brief Get the number of duct terminals in the project.
 *  @return The number of duct terminals (cxs->cosim.num_cosim_terms).
 */
CONTAM_API IX cxiGetNumTerminals(void* contamXState);

/** @brief Get information about a specified duct terminal.
 *  @param[in] termNumber The terminal number assigned by ContamW.
 *  @param[out] *pTerm Pointer to structure to be populated with duct terminal
 *              information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pTerm == NULL
 *    \li 2 => error, \b cxs->cosim.cosim_term_list == NULL \n
 *          \b cxs->cosim.cosim_term_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p termNumber out of range (1 - cxs->cosim.num_cosim_terms)
 *
 *  SEE ALSO: cxiGetNumTerminals()
 */
CONTAM_API IX cxiGetTermInfo(void* contamXState, IX termNumber, TERM_COSIM_DSC* pTerm);

/** @brief Get airflow rate of selected duct terminal.
 *  @param[in] termNumber Number of duct terminal for which to obtain airflow rate.
 *  @param[out] *pFlow Pointer to data to which the airflow rate is to be written.
 *              Duct terminals will have only one airflow rate associated
 *              with them. The airflow rate will be positive for airflows out of 
 *              the terminal and into the zone in which it is located and negative 
 *              for flows into the terminal from the zone.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pFlow == NULL
 *    \li 2 => error, \em cxs->cosim.cosim_term_list == NULL \n
 *          \em cxs->cosim.cosim_term_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p termNumber out of range (1 - cxs->cosim.num_cosim_terms).
 * 
 *  \b NOTE: Airflow units are provided in units of [kg/s] unless the cxiSetUseVolumeFlows()
 *  function is used to specify that ContamX should provide them as volumentric
 *  airflows in units of [m<SUP>3</SUP>/s].
 *
 *  SEE ALSO: cxiGetNumTerminals(), cxiGetTermInfo(), cxiSetUseVolumeFlows()
 */CONTAM_API IX cxiGetTermFlow(void* contamXState, IX termNumber, R8* pFlow);

/** @brief Get the number of duct junction in the project.
 *  @return The number of duct junctions (cxs->njct).
 */
CONTAM_API IX cxiGetNumJunctions(void* contamXState);

/** @brief Get information about selected duct junction.
 *  This function should only be called from within the \em projectDataReady callback function.
 *  @param[in] jctNumber Junction number assigned by ContamW.
 *  @param[out] *pJct Pointer to structure to be populated with junction information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pJct == NULL
 *    \li 2 => error, \p cxs->JctList == NULL \n
 *          \b cxs->JctList is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p jctNumber out of range (1 - cxs->njct)
 *
 *  SEE ALSO: cxiGetNumJunctions(), cxiRegisterCallback_PrjDataReady()
 */
CONTAM_API IX cxiGetJunctionInfo(void* contamXState, IX jctNumber, JCT_COSIM_DSC* pJct);

/** @brief Set the temperature of the specified duct junction.
 *  @param[in] jctNumber Junction number assigned by ContamW.
 *  @param[in] temperature Value of junction temperature, units [K].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p jctNumber out of range (1 - cxs->njct)\n 
 *    \li 2 => error, \p temperature < 0\n
 *
 *  SEE ALSO: cxiGetNumJunctions(), cxiGetJunctionInfo()
 */
CONTAM_API IX cxiSetJunctionTemperature(void* contamXState, IX jctNumber, R8 temperature);

/** @brief Get the number of duct leakages in the project.
 *  @return The number of duct junctions having leakage (cxs->cosim.num_cosim_leaks).
 */
CONTAM_API IX cxiGetNumLeaks(void* contamXState);

/** @brief Get the numeric identifier of a duct leak based on the duct junction with
 *         which it is associated. 
 *  @param[in] jctNumber Numeric identifier of duct junction.
 *  @param[out] *pLeakNumber Pointer to data to be populated by the numeric duct leak identifier. This value will be set to -1 if \p jctNumber can't be found.
 *
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pLeakNumber == NULL  
 *    \li 2 => error, \p jctNumber out of range (1 - cxs->njct)
 *
 *  SEE ALSO: cxiGetNumJunctions()
 */
CONTAM_API IX cxiGetLeakNumber(void* contamXState, IX jctNumber, IX* pLeakNumber);

/** @brief Get information about a duct leakage component.
 *  @param[in] leakNumber The duct leakage number assigned by ContamW.
 *  @param[out] *pLeak Pointer to structure to be populated with duct junction
 *              leakage information.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pLeak == NULL
 *    \li 2 => error, \p leakNumber out of range (1 - cxs->cosim.num_cosim_leaks)
 *
 *  SEE ALSO: cxiGetNumLeaks()
 */
CONTAM_API IX cxiGetLeakInfo(void* contamXState, IX leakNumber, TERM_COSIM_DSC* pLeak);

/** @brief Get airflow rate of selected duct leakage path.
 *  @param[in] leakNumber Number of duct leakage path for which to obtain airflow rate.
 *  @param[out] *pFlow Pointer to data to which the airflow rate is to be written.
 *              Duct leakage paths will have only one airflow rate associated
 *              with them. The airflow rate will
                be positive for airflows out of the duct and into the zone in which
                the leak is located and negative for flows into the duct system from 
                the zone.
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pFlow == NULL
 *    \li 2 => error, \em cxs->cosim.cosim_leak_list == NULL \n
 *          \em cxs->cosim.cosim_leak_list is populated by ContamX upon initialization of a co-simulation 
 *          prior to calling the user-defined callback function established by 
 *          cxiRegisterCallback_PrjDataReady().
 *    \li 3 => error, \p leakNumber out of range (1 - cxs->cosim.num_cosim_leaks).
 * 
 *  \b NOTE: Airflow units are provided in units of [kg/s] unless the cxiSetUseVolumeFlows()
 *  function is used to specify that ContamX should provide them as volumentric
 *  airflows in units of [m<SUP>3</SUP>/s].
 *
 *  SEE ALSO: cxiGetNumLeaks(), cxiGetLeakInfo(), cxiSetUseVolumeFlows()
 */
CONTAM_API IX cxiGetLeakFlow(void* contamXState, IX leakNumber, R8* pFlow);

//=============================================================================
// Envelope flow paths - WPC-like interface
//=============================================================================

/** @brief Set the wind pressure of an envelope path.
 *  @param[in] envIndex Index into envelope path list.
 *  @param[in] wP Wind pressure value to set for path, units [Pa].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 2 => error, \p envIndex out of range
 */
CONTAM_API IX cxiSetEnvelopeWP(void* contamXState, IX envIndex, R4 wP);

/** @brief Set the mass fraction of an envelope airflow path.
 *
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(1)" should be called at the 
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize 
 *        this method.
 * 
 *  @param[in] envIndex  Index into envelope path list.
 *  @param[in] ctmNumber  Contaminant number of mass fraction to set (0 - cxs->nctm-1).
 *  @param[in] Mf  Value of mass fraction of \p ctmNumber to set for path \p envIndex, units [kg_contaminant/kg_air]
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p Mf < 0  
 *    \li 2 => error, \p envIndex out of range  
 *    \li 3 => error, \p ctmNumber out of range  
 */
CONTAM_API IX cxiSetEnvelopeMF(void* contamXState, IX envIndex, IX ctmNumber, R8 Mf);

/** @brief Get exfiltration of contaminant mass during the current time step.
 * 
 *   @ref cxiSetWindPressureMode(IX useWP) "cxiSetWindPressureMode(1)" should be called at the
 *        beginning of the simulation prior to @ref cxiSetupSimulation() in order to utilize
 *        this method.
 *
 *  @param[in] envIndex Index into envelope path list.
 *  @param[in] ctmNumber Contaminant number of mass fraction to get.
 *  @param[out] *pMass Pointer to varaible in which to place mass of contaminant [kg]. 
 *   Mass = MassFraction [kg_cont/kg_air] * MassFlow [kg_air/s] * dt [s].
 *  @return success or error value:
 *    \li 0 => success
 *    \li 1 => error, \p pMass == NULL
 *    \li 2 => error, \p envIndex out of range
 *    \li 3 => error, \p ctmNumber out of range (0 - cxs->nctm-1)
 */
CONTAM_API IX cxiGetEnvelopeExfil(void* contamXState, IX envIndex, IX ctmNumber, R8* pMass);

/** @todo bridge equivalent bridge functionality:
 *  \li ELEMENT_INFO_MSGTYPE
 *  \li DUCT_INFO_MSGTYPE
 *  \li INPUT_CTRL_INFO_MSGTYPE
 *  \li OUTPUT_CTRL_INFO_MSGTYPE
 *  \li DUCT_FLOW_UPDATE_MSGTYPE
 */

#endif //_CONTAM_X_COSIM_H_
