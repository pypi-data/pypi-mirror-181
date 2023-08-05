
#ifndef _CONTAM_X_STATE_H_
#define _CONTAM_X_STATE_H_

#include "commonState.h"
#include "string-len-max.h"
#include "simdat.h"
#include "../sqlite-src/sqlite3.h"
#if( __GNUC__ )  // Linux
# include <unistd.h>
# include <netdb.h>
# include <sys/types.h>
# include <sys/socket.h>
# include <netinet/in.h>
# include <netinet/tcp.h>
# include <arpa/inet.h>
# include <errno.h> // for errno
typedef int SOCKET;
#elif( _MSC_VER )  // MS Windows (also needs Ws2_32.lib)
# include <winsock2.h>
# include <WS2tcpip.h>
#else  // allow some code testing on other systems
# define htonl(a) (a)
# define ntohl(a) (a)
#endif
#include <time.h>

#define NTYPE "zjt"  /* node types: zone, junction, terminal */
#define FTYPE "pdtl"  /* flow types: path, duct, terminal, leak */

// Return status for user interrupt.
enum simInterruptStatus
  {
  sis_none,
  sis_forceConverge,
  sis_quit
  };

struct fileBracket
{
  IX day0, day1;    // Day-of-year at start and end of current bracket.
  I4 time0, time1;  // Time-of-day at start and end of current bracket.  0 <= time <= SEC24H (as read from file).
  _Bool hitEOF;
};

struct wthFileVals  // Values from weather file.
{
  R8 data0[10], data1[10];  // Values at {day0,time0} and {day1,time1}:
    // 0 = tmpambt, 1 = barpres,
    // 2 = windspd, 3 = winddir, 4 = humidity ratio, 5 = solhtot,
    // 6 = solhdir, 7 = tskyeff, 8 = rain, 9 = snow
  R8 data[10];   // Values interpolated at simulation time.
  _Bool tempOK;  // 1 = Temperature error not previously noted.
};

struct ctmFileVals  // Values from ambient contaminant file.
{
  IX nspcs;    // Number of species on contaminant file.
  IX* spindx;  // Array indices for *Mf1 in .CTM order.
  R4* Mf0, * Mf1;  // Mass fractions at {day0,time0} and {day1,time1}, in .PRJ order [kg/kg].
};

struct wpcFileVals  // Values from wind pressure and contaminants file.
{
  IX npath;      // Number of paths on WPC file.
  IX nspcs;      // Number of species on WPC file.
  R8 Pbar0, Pbar1;    // Barometric press at {day0,time0} and {day1,time1}.
  R4 Dambt0, Dambt1;  // Density at {time0} and {time1}.
  R4* wP0, * wP1;      // Wind pressures at {time0} and {time1} [npath].  Only used if {cxs->weather.useWPCwp}.
  R4** Mf0, ** Mf1;    // Mass fractions at {time0} and {time1} [nspcs][npath].  Only used if {cxs->weather.useWPCmf}.
  _Bool difwP1;  // True if wP1 differ from wP0.
  R4* Z;         // Path elevations [m] [npath].
  R4* sign;      // Sign for path direction.
  IX* spindx;    // Array indices for *Mf in .CTM order.
  R4* Max;       // Maximum mass fractions [nspcs].
};

typedef struct weatherState
{
  FILE* uwth;      // Weather file.
  I1 WTHfile[_MAX_PATH];  // Full path for weather file.
  //
  FILE* uctm;      // Ambient contaminants file.
  I1 CTMfile[_MAX_PATH];  // Full path for contaminant file.
  //
  FILE* ucvf;      // Continuous values file.
  I1 CVFfile[_MAX_PATH];  // Full path for continuous values file.
  //
  FILE* udvf;      // Discrete values file.
  I1 DVFfile[_MAX_PATH];  // Full path for discrete values file.
  //
  FILE* uwpc;      // Wind pressure and contaminants file.
  I1 WPCfile[_MAX_PATH];  // Full path for WPC file.
  IX useWPC;              // If true, use WPC file (= cxs->weather.useWPCwp | cxs->weather.useWPCmf).
  IX useWPCmf;            // If true, use WPC file mass fraction values.
  IX useWPCwp;            // If true, use WPC file wind pressure values.

  struct fileBracket wthBracket;
  struct wthFileVals wthVals;
  I1* dyw;  // Vector of day-of-week numbers.
  I1* dyt;  // Vector of day-of-week types-- for schedule selection.
  I1* dst;  // Vector of Daylight Savings Time indicators.
  // static R4 *_Tg  = NULL;   // Vector of ground temperatures.  // Note R4 {_Tgrnd}, ground temperature [K], never used.
  // Ambient contaminant file.
  struct fileBracket ctmBracket;
  struct ctmFileVals ctmVals;

  // Wind pressure and contaminants file.
  struct fileBracket wpcBracket;
  struct wpcFileVals wpcVals;
  IX WPCversion;  // 2.1 = total pressures, 2.4 = wind pressures.
  I1* mp;             /* memory block for list structures */  // hoho dml  Not clear actually used to share global data; may just be local to multiple fcns.
  PATHLOC* PLDLoc0;   /* start of PLD path location linked list */
  PATHLOC** PLDlist;  /* vector of pointers to PLD linked list */
  PATHLOC* WPCLoc0;   /* start of WPC path location linked list */
  R4* WPC_wP;   // Vector [npath] of WPC wind pressures at {cxs->stepEndTime} [Pa].
  R8** WPC_Mf;  // Array [npath][cxs->nctm] of ambient mass fractions [-].

} WEATHERSTATE;

struct cvfFileVals  // Values from continuous values file.
{
  R4* V0, * V1;  // Values at {day0,time0} and {day1,time1}.
  R4* V;        // Values interpolated at simulation time.
};

struct dvfFileVals  // Values from discrete values file.
{
  R4* V0;       // Values at {day0,time0} (never uses interpolation).
  IX idx1;      // Index associated with first value at {day1,time1}.
  R4 val1;      // First value at {day1,time1}.
};

typedef struct ctrlState
{
  //--- Global variables.
  IX cvfNumNames;          // Number of node names in CVF file.
  IX dvfNumNames;          //   "      "     "        DVF file.
  I1** cvfNames;        // List of node names in CVF file.
  I1** dvfNames;        //   "      "     "      DVF file.
  struct cvfFileVals cvfVals;  // Current values from CVF file.
  struct dvfFileVals dvfVals;  //   "      "     "    DVF file.

  //--- File-scope variables.
  FILE* ulogc;  // Control node log file.

  // Continuous values file.
  struct fileBracket cvfBracket;

  // Discrete values file.
  struct fileBracket dvfBracket;
} CTRLSTATE;

// global variables for WPP calculations
typedef struct cpl_wpp      /* structure for WPP calculation */
{
  R4 Vmet; /*reference local wind velocity at Hmet */
  R4 Hmet;
  R4 Dmet;
  R4 amet;
  R4 Dlocal;
  R4 alocal;
  R4 InitA; /*initial calculation wind angle: 0-360, <LastA*/
  R4 LastA; /*last calculation wind angle: 0-360*/
  R4 StepA; /*calculaiton step of wind angle*/
  R4 CurtA; /*current angle*/
} CPL_WPP;

typedef struct cfdState
{

  I1* cplms;  // storage
  R8*** psaved;
  R8*** C1, *** C2, *** C3, *** C4, *** C5;
  R8*** P;  // P[NI][NJ][NK]
  R8* AIN, * AOU;  // areas of inlets, outlets  // AIN[11], AOU[11];
  IX NI, NJ, NK;
  I4 IM1, JM1, KM1;
  I4* INTY, * IOTY;  // plan postion identifier; inty:inlet; ioty:outlet;
    // INTY[11], IOTY[22];
    //     =1:xmin plane
    //      2:xmax plane
    //      3:ymin plane
    //      4:ymax plane
    //      5:zmin plane
    //      6:zmax plane
  // loca2
  I4 NBIN;    // NumCfdZones * NumInlets
  I4** LBIN;  // LBIN[1..NBIN][6], Set of CVs for each Inlet, 6 => x=1-2; y=2-3, z=4-5
  I4 NBOUT;   // NumCfdZones * NumOutlets
  I4** LBOUT; // LBOUT[1..NBOUT][6], Set of CVs for each Outlet, 6 => x=1-2; y=2-3, z=4-5
// local pressure for inlets and outlets
  R8* PIN1, * POUT1, * PIN2, * POUT2, ** CBIN, ** CBOUT;
  R8 cfdzonemp, cfdzonemp1;  // cfd zone mean pressure based on local pressures of the openings.
  I1** NMIN, ** NMOUT;
  R8 REFDENS, OPERDENS;
  //R8 FLOWIN;  //total inflow rate from inlets
  R8 NULLP;
  //variables at boundaries
  //bic
  R8* TBOUT, * VBOUT, * PBOUT;
  // EKBOU, *EDBOU,
  // TBOUT[22], QIN, QOUT, VBOUT[22], PBOUT[22], EKBOU[22], EDBOU[22], POUT[11];
  I4* OMTYPE;
  //bic2
  R8* TBIN, * UBIN, * VBIN, * WBIN, * PBIN, * AMASSIN;
  // TBIN[11], UBIN[11], VBIN[11], WBIN[11], PBIN[11], AMASSIN[11];
  I4* IMTYPE;
  R8 GRA;
  I4 NITER;
  // initial values
  R8 TINIT, TM;  // tm:reference temp
  I4 IMON, JMON, KMON;

  // OUTLET INLET DATA:
  R8* AMASSOUT;
  // AMASSOUT[11], AMASSOUTV[11];
  FILE* BA;
  FILE* uIN; // not allowed to be called IN
  // BA:balance.dat
  IX* PITYPE, * POTYPE, PBYN;  // Is it a pressure boundary? 1:yes; 0:no
  R8* COEOUT, * COEIN, * EXPOUT, * EXPIN;  // CMOUT[11];
  IX CONTAMINANT;
  IX NOC;
  IX VSTEADY, CSTEADY;
  R8 TIMESTEP, CFDTIME;
  I4 CRESTART;
  R8* cfdzoneMfi;  // contaminant initial values: 5 maximum;

  I1 cfdpdrive[_MAX_DRIVE];  // drive letter for file <project>_pext
  I1 cfdpdir[_MAX_DIR];      // directory path for file <project>_pext
  I1 cfdpname[_MAX_FNAME];   // project file name
  I1 cfdprj[_MAX_PATH];      // full path
  IX CACTIVE[6];
  IX cnctlt;
  R8*** opencoe, *** opencoesv;
  //R8 Pmean;
  R8 PHI_MIN[12];
  R8 PHI_MAX[12];
  IX LAMIN;  // >=1:laminar flow (true); 0:turbulence flow (false)
  IX STEP;   // >=1:use step change for false time step relaxation(true); 0: don't use it(false)
  I1 TITLE[LINELEN];
  //
  // velocity, pressure, pp??, temperature
  R8*** U, *** V, *** W;
  // U[NI][NJ][NK], V[NI][NJ][NK], W[NI][NJ][NK];
  R8*** PP, *** T;
  // PP[NI][NJ][NK], T[NI][NJ][NK];
  IX* FINALC;
  //
  // geometry
  R8 XX, YY, ZZ, * X, * Y, * Z;
  // X[NI], Y[NJ], Z[NK];
  // flow domain dimension, control volume centers coordinates
  R8** AREX, ** AREY, ** AREZ, *** VOL;
  // AREX[NJ][NK], AREY[NI][NK], AREZ[NI][NJ], VOL[NI][NJ][NK];
  // areas of control volumes
  R8* XF, * YF, * ZF;
  // XF[NI], YF[NJ], ZF[NK];
  // control volume surface coordinates
  //geo1
  R8* AWQ, ATOT;
  // AWQ[51], ATOT;
  // constant heat wall areas, total areas of all outlets
  //dem1
  I4 IMAX, JMAX, KMAX, IM2, JM2, KM2;
  //indices:imax=(total cv)+2=im1+1=im2+2
  //dem2
  R8* DELX, * DELY, * DELZ, * DELXC, * DELYC, * DELZC;
  // DELX[NI], DELY[NJ], DELZ[NK];
  // dimensions of each cv in 3 directions
  I4 IREF, JREF, KREF;
  //the grid number for the reference point
  I4 IIREF, JJREF, KKREF;
  //loca1
  I4* IQTY, * ITTY;  // plan postion identifier; iqty:q-wall; itty:t-wall;
    // IQTY[51], ITTY[51];
    // same codes as INTY, IOTY.
  I1** NMBL;
  //loca3
  I4 NBL, ** IBL;
  // IBL[51][7];
  //number of blockages and their posions defined as LBIN etc.
  //loca4-locations for non-adiabatic walls
  I4 NAWT, ** LNAW;  // LNAW[51][7];  //numbers and locations for t-wall
  I4 NAWQ, ** LNAWQ;  // LNAWQ[51][7];  //for q-wall
  //variables for the calculations of q-wall
  //properties of air
  R8*** VIS, *** ED, *** EK, ANU, ACP, AK, CIG[9], PRL;
  //VIS[NI][NJ][NK], ED[NI][NJ][NK], EK[NI][NJ][NK], ANU, DENS, ACP, AK, CIG[9], PRL;
  // dynamic viscosity, density, Cp,
  // thermal conductivity, Turbulent Prandtl number
  // prandtl number
  R8*** AN, *** AS, *** AE, *** AW, *** AT, *** AB, *** AP;  //linearization coefficents
  // AN[NI][NJ][NK], AS[NI][NJ][NK], AE[NI][NJ][NK],
  // AW[NI][NJ][NK], AT[NI][NJ][NK], AB[NI][NJ][NK], AP[NI][NJ][NK];
  R8*** DX, *** DY, *** DZ;
  //DX[NI][NJ][NK], DY[NI][NJ][NK], DZ[NI][NJ][NK];
  //false time
  R8 DTU, DTV, DTW, DTT, DTEK, DTED;  //false time steps for u,v,w etc.
  I4 ISTEP;  // the threshold for new time step change
  R8 CDTU, CDTV, CDTW, CDTT, CDTEK, CDTED;  // new time steps for u,v,w etc.
  //source term linear coefficients
  R8*** BS, *** SP, RESOU, RESOV, RESOW, RESOM, RESOT;
  // BS[NI][NJ][NK], SP[NI][NJ][NK], RESOU, RESOV, RESOW, RESOM,
  // coefficent b, dependent cofficent in source term
  // SPEKD[NI][NJ][NK],SPW[NI][NJ][NK],RESOT;
  // residual of u,v,w,mass
  //sour1
  R8* TSOUU, * HSOU, TAREA, ** CSOUU, ** CSOU, ** CSOUCUT;
  //TSOUU[50], HSOU[50], TAREA;
  //sour2
  R8* TNAW, * QNAW, ** CNAW, ** CNAWCUT;  // TNAW[50], QNAW[50];
  //oth1
  R8 BETA;
  I4 NITMAX, N1, N2, N3, CNITMAX;
  //oth2
  //R8 CFD_GREAT,CFD_TINY;
  //ind
  R8 CN, CCI;
  //prt
  I4 JP1, JP2, JPSTP, IP1, IP2, IPSTP;
  //urf
  R8 URFU, URFV, URFW, URFT, URFP, URFEK, URFED,
    UMAX, VMAX, WMAX, TMAX, UMIN, VMIN, WMIN, TMIN;
  //store
  R8*** US, *** VS, *** WS, *** STORE;
  // US[NI][NJ][NK], VS[NI][NJ][NK], WS[NI][NJ][NK], STORE[NI][NJ][NK];
  //turb1
  //const R8 CMU = 0.09;
  // static R8 CD, C1, C2, GEN[NI][NJ][NK], GEB[NI][NJ][NK];
  //turb2
  R8 XP, YP, ZP;
  // static R8 CMUQ, TAU, CAPA;  // Calculated but never used.
  R8*** UOLD, *** VOLD, *** WOLD, *** POLD, *** TOLD, *** TS;
  // ***DIFFU, ***DIFFV, ***DIFFW,
  // DIFFU[NI][NJ][NK], DIFFV[NI][NJ][NK], DIFFW[NI][NJ][NK],
  // UOLD[NI][NJ][NK], VOLD[NI][NJ][NK], WOLD[NI][NJ][NK];
  // resid
  R8 CRITE, PINTV;  // convergence criterion, printing frequency
  R8 CRITE_UVW, CRITE_T; // convergence criterion for UVW and T
  // length scale
  I4*** ICELL;
  // IX ***BLANK, ICELL[NI][NJ][NK];
  // static IX ***WFUNC;  // Calculated but never used.
  //indentifier of turbulence model
  IX ITUR;  // =0:zero equation; =1 k-e model(trivial)
  //nodevalues
  R8*** UP, *** VP, *** WP, *** VTT;
  // ***DENS, ***PPD;
  // UP[NI][NJ][NK], VP[NI][NJ][NK], WP[NI][NJ][NK], VTT[NI][NJ][NK], PPD[NI][NJ][NK];
  // in
  I4 ICOMPU, I2DX, I2DY, I2DZ;
  // icompu:=0:not restart;=1,restart
  // static const IALGO = 1;
  // ialgo: Type of applied algorithm: =1 for SIMPLE;=2 for SIMPLIEST;=3 for C (trivial)
  // OUTLET INLET DATA:
  // static R8 *OUTAVV, *OUTAV;
  // OUTAVV[11], OUTAV[11];
  // static R8 *INAVV, *INAV, *AMASS, *AMASSV;
  // INAVV[11], INAV[11], AMASS[11], AMASSV[11];
  // file pointers
  FILE* RE, * VA, * OUTPUT;
  // RE:result.dat; VA:vari.dat; TECP:tecp.dat
  R8 resomnr;
  // cell flow flux
  // static R8 ***FFLUX;  // FFLUX[NI][NJ][NK];
  IX*** OBJECTNM;
  // A switch to determine whether the statical procedure used or not
  R8 ppref;
  // TP[NI][NJ][NK], ppref, PROUT=0.0;
  //FILE *LOGFILE;
  FILE* TE;
  clock_t START;
  R8 RPP0, RPC0[6], RP0, RU0, RV0, RW0, RT0;
  IX BUOYML;
  IX ENERGY, TOTALCOM;
  R8 PAMB;
  IX EWCYN;  // is ewc required to be generated?
  IX DUMPLOG;  //=0,no dump anything;=1,dump input;=2,dump PP equation residues
  IX CINDEX;
  // static R8 RESOC;  // Calculated but never used.
  R8 RESOC, DTC, URFC, CDTC;
  R8 TIMEMAX;
  IX ENDSTEP;
  R8*** C1OLD, *** C2OLD, *** C3OLD, *** C4OLD, *** C5OLD;
  IX INITYN;  //initialize???
  //check the convergence of u,v,w and t
  //R8 CREU,CREV,CREW;
  // static IX cplyn;
  IX PrintGeo;  // switch of the output of the geometry
  IX PrintVel;  // switch of the output of the velocity and pressure etc.
  // fluid blockage or solid blockage
  IX* FSBLOC;
  R8 CRESIDU;
  I4 CMAXITER;
  I4 DIFFSMU, DIFFSMV, DIFFSMW, DIFFSMT, DIFFSMC;
  R8 SUMM, SUMMA;
  I4 TPLSTEP, TPLSTEP1, TPLSTEP2;
  R8 INCTM;
  FILE* UCD;
  //unsteady infor:
  struct inlet_ucd* UCDINLET;
  struct outlet_ucd* UCDOUTLET;
  struct blok_ucd* UCDBLOK;
  struct qcwall_ucd* UCDQCW;
  struct twall_ucd* UCDTW;
  I4 nnx, nny, nnz;
  // generate wdb file for wpp function
  R8* WVPL, *** Cp;
  // static R8 AirC;
  FILE* WDB;
  FILE* vartemp;
  // static FILE *PFL;
  IX COUPLEWPP;
  CPL_WPP ABWIND;  // AmBient wind
  IX CFDDONE;
  I4 WPPSTEP;
  R8 TDMAterm, * TDMAa, * TDMAb, * TDMAc, * TDMAd;
  R8*** pu, *** pus, *** pv, *** pvs, *** pw, *** pws;
  IX* WPPBC;
  IX NXSLCF, NYSLCF, NZSLCF, * XSLCF, * YSLCF, * ZSLCF;

  //Global variables for multi-grid solver
  //phiMGP_0,1,2,3 are the unknown variable on fine, average, coarse level
  // hoho wsd - replaced LN_SOLVER and SM_SOLVER with cxs->rcdat.cfd_solver and cxs->rcdat.cfd_smooth, respectively CW 3.4
  //static IX LN_SOLVER = 1; //Flag for linear solver: 0 = TDMA, 1 = MG
  //static IX SM_SOLVER = 1; //Flag for smoother: 0 = Gauss-Seidel, 1 = TDMA
  R8*** PHIMGP_0, *** PHIMGP_1, *** PHIMGP_2, *** PHIMGP_3;
  //coefficients for average grid
  R8*** AP_1, *** AE_1, *** AW_1, *** AN_1, *** AS_1, *** AB_1, *** AT_1;
  //coefficients for coarse grid
  R8*** AP_2, *** AE_2, *** AW_2, *** AN_2, *** AS_2, *** AB_2, *** AT_2;
  //fine grid--------A_fine*phiMGP_0=b_0, res_phiMG_0=b_0-A*phiMGP_0
  R8*** RES_PHIMG_0, *** ERR_PHIMG_0;
  //R8 ***B_0;
  //average grid-----(from restriction and res_phiMG_0 we will find res_phiMG_1)-----b_1=res_phiMG_1------A_ave*phiMGP_1=b_1, res_phiMG_1=b_1-A_ave*phiMGP_1
  R8*** RES_PHIMG_1, *** ERR_PHIMG_1, *** B_1;
  //coarse grid------(from restriction and res_phiMG_1 we will find res_phiMG_2)-----b_2=res_phiMG_2------A_coa*phiMGP_2=b_2, (from an interpolation phiMGP_2 will be transfered to phiMGP_3 on the average grid)
  R8*** RES_PHIMG_2, *** ERR_PHIMG_2, *** B_2;
  //these values are interpolation and restriction coefficients
  R8*** REST_AVEP, *** REST_COAP, *** REST_AVEU, *** REST_COAU, *** REST_AVEV, *** REST_COAV, *** REST_AVEW, *** REST_COAW;
  IX imax_ave, jmax_ave, kmax_ave, imax_coa, jmax_coa, kmax_coa, nn_mg;
  IX imaxGS, jmaxGS, kmaxGS, immaxGS, jmmaxGS, kmmaxGS, GSnum, BCnum;
  R8 err_mg;
  R8* xE_int1, * xW_int1, * xE_int2, * xW_int2, * yN_int1, * yS_int1, * yN_int2, * yS_int2, * zT_int1, * zB_int1, * zT_int2, * zB_int2;
  //Global variables for multi-grid solver

  IX nCFDzone;  // number of total CFD zones
  IX ctlctmcpl;  //control parameters of concentration coupling
  IX MAXCPL;  // max iterations for dynamic coupling
  IX cpliter;  // coupling iteration number
  IX tcpl; // Couple Type (0 for Quasi; 1 for dynamic; 2 for CFD post only)
  IX cpl;
  IX ctmcpl; // couple cfd concentration?
  IX cfdrunty; // CFD running type: 0=start from previous; 1=start as a new case
  IX crestart;  // concentration restart coupling
  IX doneflow;
  IX ufstart;
  IX donectm;
  IX cciter;
  FILE* MON, * CPLTE;
  IX COUPLE; // couple or not for building indoor air flow? Yes = 1; No = 0.

  struct cpl_node* cfdzone, * refzone;  // cfd zones
  IX readrst;
  // static CSE_DAT *pe;  // pointer to source/sink element data
  FILE* CONTAMOUT;
  IX dump, dumpR;  //=0,no dump intermediate;=1,dump intermediate;the dumping frequency to contamout file
  IX nctmcpl;  //coupled concentration number
  R8 convcpl;
  I4* cfdniter;
  IX finaliter;
  FILE* CPLRST;  // hardcopy of output and input data
  // static I1 temprj[_MAX_PATH];

} CFDSTATE;

#define RST_HDR_SIZE 10   // number of items in .rst file header

typedef struct restartState
{

  FILE* urst;    // Simulation restart file.
  I4 rhd[RST_HDR_SIZE]; // restart file header data.
  //   [0] cxs->nzone, [1] cxs->npath, [2] cxs->nctm, [3] cxs->njct, [4] cxs->ndct, 
  //   [5] cxs->ncss + cxs->nbls + cxs->ndvr
  //   [6] cxs->nctrl,
  //   [7] start date, [8] end date
  //   [9] number of bytes in header
  R8* rBuffer;   /* buffer to store R4 values for binary write */
  IX rMaxBuf;    /* max index of cxs->restart.rBuffer */
  IX rNrNode;    /* number of airflow node data values */
  IX rNrPath;    /* number of airflow path data values */
  IX rNrCtm;     /* number of airflow node contaminant data values */
  IX rNrCSS;     /* number of source/sink data values */
  IX rNrBLS;     /* number of boundary layer sink data values */  // hoho dml  Since {cxs->restart.rNrBLS} == {cxs->nbls}, why need this?  Ditto other static globals.
  IX rNrDVR;     /* number of deposition/resuspension sink data values */
  IX rNrFld;     /* number of filter loading values */
  IX rNrCtrl;    /* number of control node data values */
  IX rSizeData;  /* size (bytes) of one data group */

} RESTARTSTATE;

typedef struct summaryState
{
  FILE* uach;  // Building air exchange rate output file.
  FILE* ucbw;  // Contamiant box-whisker output file.
  FILE* uage;  // Zones age-of-air output file.

  // For .csm and .cex ambient interaction files 
  IX nEnvPaths_All;            // Number of paths, terminals and leaks connected to ambient
                                    //   including AHS_X and AHS_O paths
  AF_PATH** EnvPaths_All;   // Vector of all Envelope paths

  // Mass or Rate of species entering/leaving building:
  R8* Env_MassIn_sum;    // kg into building over entire simulation, VECT[ctm].
  R8* Env_MassOut_sum;    // kg out of  " .
  R8* Env_MdotIn_step;    // kg/s during simulation time step, VECT[ctm].
  R8* Env_MdotOut_step;    //  " .
  // For .cex file
  R8* Env_MassOut_list;    // kg out of whole building over listing time step, VECT[ctm].
  R8** Env_MassPath_list;    // kg out of each path      over listing time step, ARR[ctm][path].
  //R8* Env_MassPath;    // Total kg for path->Flow[0/1] for a single path, VECT[ctm].

  R8** flows;  /* flow matrix for computing age of air */
  R8** times;  /* time constant matrix */
  R8* ident;   /* identity vector for matrix inversion */
  R8* mass;    /* mass matrix for computing age of air */
  R8 cnvrtACH;  // kg/s * cxs->summary.cnvrtACH = ACH  2006/06/07
    // Contam 3.0 will provide a density value, _DensACH, for the ACH calc.

  // For box-and-whisker summaries of air exchange rate.
  IX ach_dayCt;  // Number of steps done in one day.
  I4 ach_runCt; // Number of steps done in the run.
  BOX_CALC ach_day[3]; // Box-whisker exchange rate data for the day.
  BOX_CALC ach_run[3]; // Box-whisker exchange rate data for the run.

  // For box-and-whisker summaries of contaminant concentrations.
  IX ctm_dayCt;  // Number of steps done in one day.
  I4 ctm_runCt; // Number of steps done in the run.
  BOX_CALC** ctm_day; /* box-whisker contaminant data for the day */
  BOX_CALC** ctm_run; /* box-whisker contaminant data for the run */

  // For box-and-whisker summaries of age-of-air.
  IX age_dayCt;  // Number of steps done in one day.
  I4 age_runCt; // Number of steps done in the run.
  BOX_CALC* age_day; // Box-whisker age-of-air data for the day.
  BOX_CALC* age_run; // Box-whisker age-of-air data for the run.

  // For whole-building air exchange rate.
  R8 bldgACR_inOutRelDiff_max;  // maximum relative in/out imbalance
  IX bldgACR_date;
  I4 bldgACR_time;

  // For functions sum_filter_compute() AND writeCsm_FilterReport().
  AF_PATH** Fpath; // Vector of pointers to paths with filters
  IX nFpath;         // Number of paths with filters

  // For functions sum_ambient_compute() AND writeCsm_AmbientReport().
  I4 ttime;        // total time simulated [s]
} SUMMARYSTATE;

typedef struct      /* structure for extreme values */
{
  R4 value;    /* current extreme value */
  IX nr;       /* source number */
  I4 time;     /* time of extreme */
  IX date;     /* date of extreme */
} EXTREME;

typedef struct simoutState
{
  FILE* usim;      // SIMulation results file (.sim).
  FILE* usrf;      // SuRFace results file for source/sinks (.srf).
  FILE* ucex;      // Contaminant EXfiltration file for building as a whole (.cex).
  FILE** udcexList;  // Detailed Contaminant EXfiltration files,
                                  //   one for each contaminant (.cex).
  R4 Tamax;  // Maximum ambient temperature during day [K].
  R4 Tamin;  // Minimum ambient temperature during day [K].
  R4 wsmax;  // Maximum wind speed during day [m/s].
  R4 wsmin;  // Minimum wind speed during day [m/s].

  EXTREME maxACH;
  EXTREME maxZP;
  EXTREME minZP;
  EXTREME maxJP;
  EXTREME minJP;
  // STS results
  FILE* urxr;  // cross reference file
  FILE* urzf;  // zone airflow data
  FILE* urzm;  // zone mass fraction data
  FILE* urz1;  // 1-D zone cell mass fraction data
  IX nZ1D;  // number of 1-D zones
  IX nC1D;  // number of 1-D zone cells
  CD_ZONE** Z1D;  // vector of pointers to 1-D C-D zone structures
  R4* concVec;  // Vector of contaminant concentrations.
  R4** ZC1D; // array of 1-D zone/cell mass fractions
  R4** ZMfd; // array of mixed zone mass fractions
  R4** Ztpd; // array of zone temperature, pressure, and density data

  IX nccnd;  // for matching Contam96

} SIMOUTSTATE;

typedef struct exposState
{
  FILE* uexp;  // Exposure output file.
  // For box-and-whisker summaries of exposure.
  IX exp_dayCt;  // Number of steps done in one day.
  I4 exp_runCt; // Number of steps done in the run.
  BOX_CALC** exp_day;  // Box-whisker exposure data for the day.
  BOX_CALC** exp_run;  // Box-whisker exposure data for the run.

} EXPOSSTATE;

typedef struct cosimState
{

  AF_NODE** cosim_zone_list;  // list of pointers to zones [1:cxs->nzone]
  AF_PATH** cosim_path_list;  // list of pointers to path links [1:cxs->npath]
  CT_NODE** cosim_inode_list; // list of pointers to input control nodes [1:cxs->cosim.num_cosim_inodes]
  CT_NODE** cosim_onode_list; // list of pointers to output control nodes [1:cxs->cosim.num_cosim_onodes]
  AF_PATH** cosim_term_list;  // list of pointers to terminal links [1:cxs->cosim.num_cosim_terms]
  AF_NODE** cosim_jct_list;   // list of pointers to junction nodes [1:cxs->njct]
  AF_PATH** cosim_leak_list;  // list of pointers to terminal links [1:cxs->cosim.num_cosim_leaks]
  AF_PATH** cosim_oap_list;   // list of pointers to AHS outdoor air path [1:cxs->cosim.num_cosim_ahs_oap]
  R4* cosim_oap_values_list;  // list of values to use for outdoor air control values [1:cxs->cosim.num_cosim_ahs_oap]
  //IX* env_list;               // list of cxs->ENV_Mf indices of envelope paths [1:nEnvPaths_Wpc]
  IX num_cosim_inodes;    // number of intput control nodes (CT_SET w/ names)
  IX num_cosim_onodes;    // number of output control nodes (CT_PAS w/ names)
  IX num_cosim_terms;     // number of terminals
  IX num_cosim_leaks;     // number of junction leaks
  IX num_cosim_ahs_oap;   // number of AHS outdoor air paths
  IX cosim_use_vol_flows; // if tue then flows are returned in m^3/s
  //IX num_envp;                // number of and index of last envelope path

} COSIMSTATE;
/*  state data for contam-x  */

typedef struct sqliteState
{
  sqlite3* sqldb;                  // Database file
  sqlite3_stmt* TimeInsert;
  sqlite3_stmt* AmbientInsert;
  sqlite3_stmt* ZoneCCInsert;
  sqlite3_stmt* DuctCCInsert;
  sqlite3_stmt* ZoneFlowInsert;
  sqlite3_stmt* DuctFlowInsert;
  sqlite3_stmt* PathLinkInsert;
  sqlite3_stmt* DuctLinkInsert;

} SQLITESTATE;

typedef struct bridgeState
{
  SOCKET sockfd;        // socket 'file description' identifier
  I1* msgbuf;           // buffer for message to/from ACATS bridge
  IX maxbuf;            // size of cxs->bridge.msgbuf - sufficient for all valid messages
  IX num_afpaths;       // number of flow paths
  IX num_elmts;         // number of airflow elements
  IX num_ahsp;          // number of ahs paths
  IX num_ducts;         // number of duct segments
  IX num_terms;         // number of terminals
  IX num_leaks;         // number of duct leaks
  IX num_inodes;        // number of intput control nodes (CT_SET w/ names)
  IX num_onodes;        // number of output control nodes (CT_PAS w/ names)
  IX num_agents;        // number of agents (contaminants)
  IX num_envp;          // number of and index of last envelope path

  IX* env_list;         // list of cxs->ENV_Mf indices of envelope paths [1:nEnvPaths_Wpc]
  IX* ctm_list;         // list of indices of envelope contaminants [1:cxs->nctm]
  // CTM_DAT *ctm;             //   vector of data for each agent (see sxtrn.h) [0:cxs->nctm-1]
  AF_NODE** zone_list;  // list of pointers to zones [1:cxs->nzone]
  AF_PATH** path_list;  // list of pointers to path links [1:_num_paths]
  AFE_DAT** elmt_list;  // list of pointers to path elements [1:cxs->bridge.num_elmts]
  AF_NODE** jct_list;   // list of pointers to jcts  [1:cxs->njct]
  CT_NODE** inode_list; // list of pointers to input control nodes [1:cxs->bridge.num_inodes]
  CT_NODE** onode_list; // list of pointers to output control nodes [1:cxs->bridge.num_onodes]
  R4* poa_list;         // vector of percent outdoor air values [0:cxs->nahs]

} BRIDGESTATE;

struct mf_mem;
struct ctm_dat;
typedef struct contamXState
{
  CommonState commonState;
  IX list;          // data dump parameter:
                    //   > 0  dump matrix analysis,
                    //   = 2  dump .SIM output,
                    //   > 2  dump lognotes.
  IX doDialog;      /* if true, create windows dialog box */
  IX doDOSwdw;      /* if true, create interactive DOS window */
  _Bool doInput;    /* if true, test input, then exit */
  IX quiet;         /* if true, minimize output to console */
//
// tcp/ip bridge communication flags
  IX doBridge;      // tcp/ip bridge communication mode flag:
                          //   0 = no bridge connection
                          //   2 = bridge mode fully active
                          //   1 = bridge shutting down
  IX wPBridge;      // tcp/ip bridge wind pressure flag
                          //   1 = wind pressure and contaminants obtained via ADJ_WPC_MSGTYPE,
                          //   0 = ADJ_WTH_MSGTYPE and CTM file, set to 0 w/ "-w" command line option
                          //   Can also be set using cxiSetUseWindPressureMode() 0 => WTH & CTM-like api, 1 => WPC-like api.
                          //   TODO WSD (currently WTH file cannot be used in bridge mode - see bug 405).
  _Bool vFBridge;   // tcp/ip bridge volume flow units flag for _FLOW_UPDATE_MSGTYPEs
                          //   0 = send flows in [kg/s]
                          //   1 = send flows in [m3/s], because EnergyPlus wants 
                          //       Vdot = Mdot / (Density Of Destination Zone).
  _Bool doBridgeMf; // tcp/ip bridge mass fraction flag
                          //   1 = Server, e.g. ACATS, has reset a mass fraction.
//
  _Bool doOccSens;  /* if true, an occupancy sensor is present  CW 2.4b */
  I2 defUnits;     /* default units: 0 = SI, 1 = US (IP) */
  I2 defFlows;     /* default flows */

  I1 prjname[_MAX_FNAME];  /* project file name */
  I1 pdrive[_MAX_DRIVE];   /* drive letter for file <project>_pext */
  I1 pdir[_MAX_DIR];       /* directory path for file <project>_pext */
  I1 pext[_MAX_EXT];       /* extension for project file: ".prj"=>ContamX, ".prjl"=>LoopDA */
  I1 prjPRJ[_MAX_PATH];    /* full path for <project>_pext */
  RCDAT rcdat;   /* run control data */
  WTHDAT wthdat; /* steady state weather data */
  LOCDAT locdat; /* location data */
  IX newSTSaf;  /* if true, recompute STS airflows */
  R4* ENV_wP;  /* vector [nloc] of ENV wind pressures at cxs->time_scrn [Pa] */
  R4* ENV_wPs;   /* vector [nloc] of ENV wind pressure signs */
  R8** ENV_Mf; /* ENV ambient mass fractions [kgc/kga], _ENV_Mf[1:nloc][0:nctm-1] */
  IX nEnvPaths_Wpc; /* number of envelope paths and terminals */

// Simulation day-time.
  IX dayofy;       // Current day-of-year (1-365; 1=1Jan, 365=31Dec).
  IX dayofw;       // Current day-of-week (1-7; 1=Sunday).  // hoho dml  {_dayofw} only assigned values if have a weather file, but may be used without a weather file.
  IX daytyp;       // Current day type (1-12) (==> 0 - 11 for schedules); from PRJ or WTH files.
  IX DSTind;       // 1 = daylight savings time.
  I4 stepStartTime;  // Time-of-day, on date {dayofy}, at start of current time step [s] (0 - 86400).  Use 0h of day N+1, rather than 24h of day N.
  I4 stepEndTime;    // Time-of-day, on date {dayofy}, at end of current time step [s]   (0 - 86400).  // hoho dml  Since only runs up to SEC24H, why not just IX?
  IX simEndDate;  // Day-of-year to end transient simulation.
  I4 simEndTime;  // Time-of-day to end transient simulation [s].
  I4 time_scrn;   // Screen display time step [s].
  I4 time_list;   // Listing time step [s].
  IX time_step;   // Simulation time step [s].
  R4 dt;          // Simulation time step [s].
  R4 dti;         // Inverse of simulation time step [1/s].

// Other.
  IX nafnd;    /* number of airflow nodes */
  IX nafpt;    /* number of airflow paths */
  AF_NODE* afnd0;  /* pointer to first airflow node structure */
  AF_PATH* pafp0;  /* pointer to first path structure */
  CD_ZONE* cdzn0;  /* pointer to first C-D zone structure */
  AF_NODE* pambt;  /* pointer to ambient airflow node */
  CNV_NODE* jctn0; /* point to first junction */
  CNV_DUCT* duct0; /* pointer to first duct */
  CNV_LEAK* leak0; /* pointer to first leak */
  CNV_TERM* term0; /* pointer to first terminal */
  IX nZnode;     /* number of nodes that are zones */
  AF_NODE** Znode; /* vector of pointers to nodes that are zones */
  R4** Mfmax;  // Maximum contaminant concentrations (reset each day).
  R4** Mftst;  /* convergence test contaminant concentrations */
  AF_MAT* AF_mat;  /* airflow calculation sparse matrix */
  struct mf_mem* MFn_mem;  // Values for mass fraction calculations (non-trace, or combined system).
  struct mf_mem* MFt_mem;  // Values for mass fraction calculations (trace).
  I1* ms;   /* memory block for small structures - during simulation */
  I1* mb;   /* memory block for small structures - during input only */
// Contaminant data.
  IX nctm;  // Total number of contaminants simulated.
  IX nntc;  // Number of non-trace contaminants.
  R8* Rs;   /* vector of gas constants for non-trace contaminants [0:cxs->nntc-1] */
  R8* Cp;   /* vector of specific heats (const P) for non-trace contaminants */
  // R8 *_Cv;   // Vector of specific heats (const V) for non-trace contaminants.
  struct ctm_dat* ctm;  /* vector of data for each contaminant [0:cxs->nctm] */
  R4* penf; /* default filter penetration fractions (1 - eff) */
  IX nZctm; /* number of zones * number of contaminants (incl ambt) */
  IX nJctm; /* number of junctions * number of contaminants */
  IX nCmctm; /* number of cells in fully mixed zones * number of contaminants */
  IX nCcctm; /* number of cells in CDZ zones * number of contaminants */
  R8* MfJi;  // junction mass fractions @ start of step [0:cxs->nJctm-1]
  R8* MfJ;   // junction mass fractions @ end of step [0:cxs->nJctm-1]
  R8* sFMfJ; // junction STS mass flow sums [0:cxs->nJctm-1]
  R8* MfZi;  // Zone mass fractions @ start of step [0:cxs->nZctm-1].  Organization matches {cxs->MfZ}.
  R8* MfZ;   // Zone mass fractions [0:cxs->nZctm-1].  Organized by zone (ambient first).  Within a zone,
  // arranged non-trace, then trace contaminants.
  R8* sFMfZ; // mixed zone STS mass flow sums [0:cxs->nCmctm-1]
  R8* MfCi;  // C-D cell mass fractions @ start of step[0:cxs->nCcctm-1]
  R8* MfC;   // C-D cell mass fractions @ end of step [0:cxs->nCcctm-1]
  R8* sFMfC; // C-D cell mass flow sums [0:cxs->nCcctm-1]
  // Building level data.
  IX nlev;         /* number of levels; for read or save */
  LEV_DATA* Lev0;  /* pointer to lowest (first) level */
  LEV_DATA* LevH;  /* pointer to highest level */
  LEV_DATA** LevList;   /* list of pointers to levels - during input */
  // Library elements.
  IX ndsch;        /* number of day-schedules; for read or save */
  DY_SCHD* Dsch0;  /* pointer to first day-schedule structure */
  DY_SCHD** DschList;  // Array of pointers to day-scheds - used at input.
  IX nwsch;        /* number of week-schedules; for read or save */
  WK_SCHD* Wsch0;  /* pointer to first week-schedule structure */
  WK_SCHD** WschList;  // Array of pointers to week-scheds - used at input.
  IX nwpf;         /* number of wind profiles; for read or save */
  WIND_PF* Wpf0;   /* pointer to first Wind Profile structure */
  WIND_PF** WpfList;  /* list of pointers to WP - used at input */
  IX nafe;         /* number of airflow elements; for read or save */
  AFE_DAT* Afe0;   /* pointer to first AirFlow Elmt structure */
  AFE_DAT** AfeList;  /* list of pointers to afe - used at input */
  IX ndfe;         /* number of duct elements; for read or save */
  AFE_DAT* Dfe0;   /* pointer to first duct Elmt structure */
  AFE_DAT** DfeList;  /* list of pointers to dfe - used at input */
  IX ncse;         /* number of source elements; for read or save */
  CSE_DAT* Cse0;   /* pointer to first Cont Source Elmt structure */
  CSE_DAT** CseList;  /* list of pointers to CSE - used at input */
  IX nfilt;        /* number of filters; for read or save */
  FLT_DSC* Filt0;  /* pointer to first Filter structure */
  FLT_DSC** FiltList; /* list of pointers to Filt - used at input */
  IX nflte;        /* number of filter elements; for read or save */
  FLT_ELT* Flte0;  /* pointer to first Filter structure */
  FLT_ELT** FlteList; /* list of pointers to Filt - used at input */
  IX nkinr;        /* number of kinetic reactions; for read or save */
  KNR_DSC* Kinr0;  /* pointer to first Kinetic Reaction structure */
  KNR_DSC** KinrList;   /* list of pointers to KR - used at input */
  IX nzone;       /* number of airflow zones */
  ZONE_DSC** ZoneList;  /* list of pointers to zone data structures */
  ZONE_DSC ambt;  /* the "ambient" zone */

  IX npath;       /* number of airflow paths */
  PATH_DSC** PathList;  /* list of pointers to flow path data structures */

  IX njct;         /* number of junctions */
  JCT_DSC** JctList;    /* list of pointers to junction data structures */

  IX ndct;         /* number of duct segmentss */
  DCT_DSC** DctList;    /* list of pointers to duct data structures */

  IX nahs;        /* number of simple air handling systems icons */
  AHS_DSC* Ahs0;   /* pointer to first used AHS structure */
  AHS_DSC** AhsList;    /* list of pointers to AHS elements in cxs->mb */

  IX nctrl;       /* number of control nodes */
  IX nlogc;     /* number of log control nodes */
  CT_NODE* Ctrl0; /* pointer to first control node */
  CT_NODE** CtrlList;   /* list of pointers to control nodes */
  CT_NODE** CtrlLogs;   /* list of pointers to control log nodes CW 2.4b */

  IX ncss;                // Number of contaminant source/sinks.
  CSS_DSC* Css0;   // Ptr to first CSS structure (unless divided into trace/non-trace).
  CSS_DSC* Csst0;  // Ptr to first (trace) mass source/sink.
  CSS_DSC* Cssnt0; // Ptr to first (non-trace) mass source/sink.

  IX nbls;            // Number of boundary layer source/sinks (including inactive ones).
  BLS_DAT* Bls0;   // Ptr to first BLS source/sink structure (unless divided into trace/non-trace).
  BLS_DAT* Blst0;  // Ptr to first (trace) BLS source/sink.
  BLS_DAT* Blsnt0; // Ptr to first (non-trace) BLS source/sink.
  BLS_DAT* BlsInactive0; // Ptr to first inactive BLS source/sink.

  IX ndvr;            // Number of deposition/resuspension source/sinks (including inactive ones).
  DVR_DAT* Dvr0;   // Ptr to first DVR source/sink structure (unless divided into trace/non-trace).
  DVR_DAT* Dvrt0;  // Ptr to first (trace) DVR source/sink.
  DVR_DAT* Dvrnt0; // Ptr to first (non-trace) DVR source/sink.
  DVR_DAT* DvrInactive0; // Ptr to first inactive DVR source/sink.

  PXS_DAT* Pxs0;   // Ptr to first personal source PXS structure (unless divided into trace/non-trace).
  PXS_DAT* Pxst0;  // Ptr to first (trace) personal source.
  PXS_DAT* Pxsnt0; // Ptr to first (non-trace) personal source.

  IX nosch;       /* number of occupancy schedules; for read or save */
  OD_SCHD* Osch0;  /* pointer to first occupancy structure */
  OD_SCHD** OschList;   /* list of pointers to Osch - used at input */

  IX npexp;       /* number of personal exposures */
  PEXP_DSC* Pexp0; /* pointer to first exposure structure */
  PEXP_DSC** PexpList;  /* list of pointers to exposures in cxs->mb */

//CoSim globals

  IX useCosim; // if true use cosim mode
  IX cosim_stepForward;  // if true then stepping to the next time step
  IX simloop_day;  // Number of days simulated.
  IX SetupSimCount;  // Number of times SetupSimultion() is called.

  // this function pointer is used to call a function when the project data is ready and before it is freed
  void (*prjDataReadyFcnP)();

  I4 NrLufSkyN;  // Number of calls to fcn luf_sky_n().
  I4 NrLusSkyN;  // Number of calls to fcn lus_sky_n().
  I4 NrLufSkyS;  // Number of calls to fcn luf_sky_s().
  I4 NrLusSkyS;  // Number of calls to fcn lus_sky_s().
  I4 NrTimeSteps;  // Total number of time steps.
  I4 NrTStepIter;  // Total number of time step iterations.
  I4 NrSolveAf;    // Number of calls to solve_Af().
  R4 aftime;       // Time to compute airflows [s].
  IX* facBins;  // Jacobian factoring bins.
  I4 NrFillAf;  // Number of calls to FillAf().
  I4 NrCubicN;  // Number of calls to cubic(N).
  I4 NrCubicA;  // Number of calls to cubic(A).
  I4 rangeDWC[3];  // Range (lam, trns, turb) in afe_dwc().
  I4 NrPCG;      // Number of calls to sa_pcg().
  I4 NrPCGiter;  // Number of sa_pcg() iterations.
  I4 NrLufGE;    // Number of calls to luf_ge().
  I4 NrLusGE;    // Number of calls to lus_ge().
  I4 NrSolveMft;  // Number of calls to solve_Mft().
  I4 NrSolveMfn;  // Number of calls to solve_Mfn().
  I4 NrSolveSTS;   // Number of calls to solve_STS().
  I4 NrCDZsim;     // Number of calls to CDZsim().
  I4 NrDuctEulr;   // Number of ducts by STS Eulerian method.
  I4 NrDuctLagr;   // Number of ducts by STS Lagrangian method.
  R4 dtMaxStab;  // Maximum stable STS time step.
  // hoho dml  Consider keeping counts in the data structs that use these fcns.
  I4 NrBCG;      // Number of calls to fcn sa_bcg().
  I4 NrBCGiter;  // Number of iterations in fcn sa_bcg().
  I4 NrSOR;      // Number of calls to fcn sa_sor().
  I4 NrSORiter;  // Number of iterations in fcn sa_sor().

  FILE* ubal;  // Duct balance file.
  struct baldata* BalDat0; // start of linked list
  enum simInterruptStatus quit;  // User response to query.
  // hoho dml  Why keep sts-init fcns separate from fcns that rely on those
  // initialized data?  Fact that many extern vars shared just with solv-sts.c
  // indicates problem.
  R8** Atd;   // matrix for trigiagonal equations
  R8* Bxtd;   // RHS/solutions vector for trigiagonal equations
  R8** Akr;   // square matrix for chemical reactions [cxs->nctm * cxs->nctm]
  //R8 *_Bxkr = NULL;   // RHS/solutions vector for chemical reactions
  IX Ntdmxr;     // maximum number of rows in Atd & _Bxtd
  IX Ntdmxc;     // maximum number of cols in Atd (also used in EulerSet( ))
  IX daytypeLastSeek;
  #ifdef _MSC_VER 
  HWND hSimWnd;
  #endif
  int bSimAbort; // Set to TRUE when user clicks "Stop Simulation"
  int bSimConverge; // Set to TRUE when user checks "Assume convergence..."
  _Bool ignore;  // if true, log convergence data

  //function specific variables
  IX lint1d_i;
  const R4* lint1d_xold;
  IX splint_i;
  R4** splint_aold;
  IX PLDlist_count;
  R8* flow_time_rowchk,
    * flow_time_colchk,  /* row and column checks */
    * flow_time_maxdif;  /* max difference between row and column sums */
#ifdef _DEBUG
  IX calc_sP_first;
#endif

  struct weatherState weather;
  CTRLSTATE ctrl;
  RESTARTSTATE restart;
  SUMMARYSTATE summary;
  SIMOUTSTATE simout;
  EXPOSSTATE exp;
  COSIMSTATE cosim;
  SQLITESTATE sqlite;
  BRIDGESTATE bridge;
  CFDSTATE cfd;

  IX CDZsim_first;
  IX LagDuct_first;
  IX flow_time_balchk;
} ContamXState;

void initContamXState(ContamXState* cxs);
#endif
