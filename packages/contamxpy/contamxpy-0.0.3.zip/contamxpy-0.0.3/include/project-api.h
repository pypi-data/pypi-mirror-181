/** @file project-api.h
 *  @brief contam project API.
 *  @author Brian J. Polidoro (NIST)
 *  @author W. Stuart Dols (NIST)
 *  @date 2022-10-20
 *
 *  Data and functions that provide an interface to project files of CONTAM.
 */
#ifndef _PROJECT_API_H_
#define _PROJECT_API_H_

 /** ambient zone number */
#define AMBT    -1

 /**
  * @defgroup ICON_TYPE_GROUP CONTAM Icon Types Group
  *
  * @{
  */

  /** Zone Icon Type */
#define ZONE_ICON_TYPE "zon"
 /** Path Icon Type */
#define PATH_ICON_TYPE "pth"
 /** Filter Icon Type */
#define FILTER_ICON_TYPE "flt"
 /** Contaminant Source/Sink Icon Type */
#define CSS_ICON_TYPE "css"
 /** Duct Icon Type */
#define DCT_ICON_TYPE "dct"
 /** Junction Icon Type */
#define JCT_ICON_TYPE "jct"
 /** Annotation Icon Type */
#define NOTE_ICON_TYPE "note"
 /** Personal Exposure Icon Type */
#define PEXP_ICON_TYPE "pexp"
 /** Simple Air Handler System Icon Type */
#define AHS_ICON_TYPE "ahs"
 /** Control Icon Type - future */
#define CTRL_ICON_TYPE "ctrl"

/** @} */

/**
 * @defgroup PRJ_ELEMENT_GROUP Project Element Group
 *
 * @{
 */

 /** Occupant Schedule Element Type */
#define OCC_SCHED_ELEMENT_TYPE "ods"

/** @} */

/**
 * @defgroup DIR_GROUP Direction group
 *
 * @{
 */

 /** Direction Minimum */
#define DIR_MIN 1
 /** North */
#define DIR_NORTH 1
 /** East */
#define DIR_EAST 2
 /** Up */
#define DIR_UP 3
 /** South */
#define DIR_SOUTH 4
 /** West */
#define DIR_WEST 5
 /** Down */
#define DIR_DOWN 6
 /** Direction Maximum */
#define DIR_MAX 6

/** @} */

/**
 * @defgroup VF_TYPE_GROUP VF group
 *
 * @{
 */

 /** VF type minimum */
#define VF_TYPE_MIN 0
 /** None */
#define VF_TYPE_NONE 0
 /** CVF */
#define VF_TYPE_CVF 1
 /** DVF */
#define VF_TYPE_DVF 2
 /** VF type maxmimum */
#define VF_TYPE_MAX 2

/** @} */


/**
 * @defgroup ICONS_GROUP CONTAM Sketchpad Icons
 *
 * @{
 */

 /* flow arrow - pointing east */
#define FLOW_E      1  
/* flow arrow - pointing west */
#define FLOW_W      2  
/* flow arrow - pointing north */
#define FLOW_N      3  
/* flow arrow - pointing south */
#define FLOW_S      4  
/* zone - standard */
#define ZONE_ST     5  
/* zone - phantom */
#define ZONE_PH     6  
/* zone - ambient */
#define ZONE_AM     7  
/* Sketch Origin */
#define ORIGIN      9  
/* wall - east/west */
#define WL_EW      11  
/* wall - north/south */
#define WL_NS      12  
/* wall - northwest corner */
#define WL_ES      14  
/* wall - northeast corner */
#define WL_SW      15  
/* wall - southeast corner */
#define WL_NW      16  
/* wall - southwest corner */
#define WL_NE      17  
/* walls - to north, east, and south */
#define WL_NES     18  
/* walls - to east, south, and west */
#define WL_ESW     19  
/* walls - to south, west, and north */
#define WL_NSW     20  
/* walls - to west, north, and east */
#define WL_NEW     21  
/* wall quad corner */
#define WL_NESW    22  
/* opening - 1-way airflow */
#define OPNG       23  
/* opening - 2-way airflow */
#define DOOR       24  
/* large 1-way opening */
#define LG_OPNG    25  
/* large 2-way opening */
#define LG_DOOR    27  
/* fan - flow to the east */
#define FAN_E      28  
/* fan - flow to the west */
#define FAN_W      29  
/* fan - flow to the north */
#define FAN_N      30  
/* fan - flow to the south */
#define FAN_S      31  
/* note - '*' */
#define NOTE       42  
/* box - AHS supply */
#define BOX_S     128  
/* box - AHS return */
#define BOX_R     129  
/* simple AHS zones/element */
#define S_AHS     130  
/* personal exposure */
#define PEXP      131  
/* personal activity (future) */
#define PERSON    132  
/* contaminant source/sink (C95) */
#define CONT_SS   133  
/* contaminant reaction (future) */
#define CONT_RX   134  
/* mass layers - east/west, floor */
#define WMS_EW    136  
/* mass layers - north/south */
#define WMS_NS    137  
/* window layers - east/west, floor */
#define WDW_EW    138  
/* window layers - north/south */
#define WDW_NS    139  
/* generic zone mass */
#define GEN_MASS  140  
/* radiant interchange */
#define RAD_INT   141  
/* heat source */
#define HEAT_SRC  142  
/* duct (not saved) - east/west */
#define DCT_EW    143  
/* duct (not saved) - north/south */
#define DCT_NS    144  
/* duct (saved) - east/west */
#define DCT_EWk   145  
/* duct (saved) - north/south */
#define DCT_NSk   146  
/* duct - east/south */
#define DCT_ES    147  
/* duct - south/west */
#define DCT_SW    148  
/* duct - north/west */
#define DCT_NW    149  
/* duct - north/east */
#define DCT_NE    150  
/* duct crossing */
#define DCT_X     151  
/* duct - east/west - grouping icon (future) */
#define DCT_EWg   152  
/* duct - north/south - grouping icon (future) */
#define DCT_NSg   153  
/* duct - north/south - north positive */
#define DCT_NSn   154  
/* duct - east/west - east positive */
#define DCT_EWe   155  
/* duct - north/south - south positive */
#define DCT_NSs   156  
/* duct - east/west - west positive */
#define DCT_EWw   157  
/* junction */
#define JCT       158  
/* junction - connected to level above */
#define JCT_CA    159  
/* junction - connected to level below */
#define JCT_CB    160  
/* junction - connected above & below */
#define JCT_CAB   161  
/* junction terminal */
#define IOJ       162  
/* terminal - connected to level above */
#define IOJ_CA    163  
/* terminal - connected to level below */
#define IOJ_CB    164  
/* control link (not saved) - east/west */
#define CL_EW     168  
/* control link (not saved) - north/south */
#define CL_NS     169  
/* control link (saved) - east/west */
#define CL_EWk    170  
/* control link (saved) - north/south */
#define CL_NSk    171  
/* control link - east/south */
#define CL_ES     172  
/* control link - south/west */
#define CL_SW     173  
/* control link - north/west */
#define CL_NW     174  
/* control link - north/east */
#define CL_NE     175  
/* control link - cross-over */
#define CL_X      176  
/* control actuator - point to north */
#define CA_N      177  
/* control actuator - point to east */
#define CA_E      178  
/* control actuator - point to south */
#define CA_S      179  
/* control actuator - point to west */
#define CA_W      180  
/* control sensor - point to north */
#define CS_N      181  
/* control sensor - point to east */
#define CS_E      182  
/* control sensor - point to south */
#define CS_S      183  
/* control sensor - point to west */
#define CS_W      184  
/* control node */
#define CTRLN     185  
/* phantom control node */
#define CTRLP     186  
/* super control node */
#define CTRLS     187  
/* super element output control node */
#define CTRLO     188  
/* super element input control node */
#define CTRLI     189  
/* Loop tail east */
#define LT_E      206  
/* Loop tail west */
#define LT_W      207  
/* Loop tail north */
#define LT_N      208  
/* Loop tail south */
#define LT_S      209  

/** @} */


/**
 * @defgroup COLOR_GROUP CONTAM colors
 *
 * @{
 */

 /** Color minimum */
#define CLR_MIN -1
 /** No Color */
#define CLR_NOCOLOR -1
 /** Black */
#define CLR_BLACK 0
 /** Dark Red */
#define CLR_DK_RED 1
 /** Red */
#define CLR_RED 2
 /** Hot Pink */
#define CLR_HOT_PINK 3
 /** Rose */
#define CLR_ROSE 4
 /** Brown */
#define CLR_BROWN 5
 /** Orange */
#define CLR_ORANGE 6
 /** Light Orange */
#define CLR_LT_ORANGE 7
 /** Gold */
#define CLR_GOLD 8
 /** Tan */
#define CLR_TAN 9
 /** Olive Green */
#define CLR_OL_GREEN 10
 /** Dark Yellow */
#define CLR_DK_YELLOW 11
 /** Lime */
#define CLR_LIME 12
 /** Yellow */
#define CLR_YELLOW 13
 /** Light Yellow */
#define CLR_LT_YELLOW 14
 /** Dark Green */
#define CLR_DK_GREEN 15
 /**  Green*/
#define CLR_GREEN 16
 /** Sea Green */
#define CLR_SEA_GREEN 17
 /** Bright Green */
#define CLR_BR_GREEN 18
 /** Light Green */
#define CLR_LT_GREEN 19
 /** Dark Teal */
#define CLR_DK_TEAL 20
 /** Teal */
#define CLR_TEAL 21
 /** Aqua */
#define CLR_AQUA 22
 /** Turquiose */
#define CLR_TURQUIOSE 23
 /** Light Turquoise */
#define CLR_LT_TURQUIOSE 24
 /** Dark Blue */
#define CLR_DK_BLUE 25
 /** Blue */
#define CLR_BLUE 26
 /** Light Blue */
#define CLR_LT_BLUE 27
 /** Sky Blue */
#define CLR_SKY_BLUE 28
 /** Pale Blue */
#define CLR_PALE_BLUE 29
 /** Indigo */
#define CLR_INDIGO 30
 /** Blue Gray */
#define CLR_BLUE_GRAY 31
 /** Violet */
#define CLR_VIOLET 32
 /** Plum */
#define CLR_PLUM 33
 /** Lavendar */
#define CLR_LAVENDER 34
 /** Gray 80 */
#define CLR_GRAY_80 35
 /** Gray 50 */
#define CLR_GRAY_50 36
 /** Gray 40 */
#define CLR_GRAY_40 37
 /** Gray 25 */
#define CLR_GRAY_25 38
 /** White */
#define CLR_WHITE 39
 /**Azure  */
#define CLR_AZURE 40
 /** Mariner */
#define CLR_MARINER 41
 /** Smalt */
#define CLR_SMALT 42
 /** Navy Blue */
#define CLR_NVY_BLUE 43
 /** Medium Blue */
#define CLR_MED_BLUE 44
 /** Blue Stone */
#define CLR_BLUE_STONE 45
 /** Bahama Blue */
#define CLR_BAHAMA_BLUE 46
 /** Pacific Blue */
#define CLR_PACIFIC_BLUE 47
 /** Science Blue */
#define CLR_SCIENCE_BLUE 48
 /** Klien Blue */
#define CLR_KLEIN_BLUE 49
 /** Royal Blue */
#define CLR_ROYAL_BLUE 50
 /** Pantina */
#define CLR_PANTINA 51
 /** Persian Green */
#define CLR_PERSIAN_GREEN 52
 /** Azure Radiance */
#define CLR_AZURE_RADIANCE 53
 /** Blue Ribbon */
#define CLR_BLUE_RIBBON 54
 /** Governor Blue */
#define CLR_GOVENOR_BLUE 55
 /** Carribean Green */
#define CLR_CARRIBEAN_GREEN 56
 /** Spring Green */
#define CLR_SPRING_GREEN 57
 /** Picton Blue */
#define CLR_PICTON_BLUE 58
 /** Boston Blue */
#define CLR_BOSTON_BLUE 59
 /** Sky Blue */
#define CLR_DP_SKY_BLUE 60
 /** Cornflower Blue */
#define CLR_CORNFLOWER_BLUE 61
 /**  Blue Violet */
#define CLR_BLUE_VIOLET 62
 /** Purple */
#define CLR_PURPLE 63
 /** Apple */
#define CLR_APPLE 64
 /** Jade */
#define CLR_JADE 65
 /** Aquamarine */
#define CLR_AQUAMARINE 66
 /** Malibu */
#define CLR_MALIBU 67
 /** Anakiwa */
#define CLR_ANAKIWA 68
 /** Melrose */
#define CLR_MELROSE 69
 /** Portage */
#define CLR_PORTAGE 70
 /** Dark Violet */
#define CLR_DK_VIOLET 71
 /** Electric Violet */
#define CLR_ELECTRIC_VIOLET 72
 /** Camarone */
#define CLR_CAMARONE 73
 /** Malchite */
#define CLR_MALCHITE 74
 /** Pastel Green */
#define CLR_PASTEL_GREEN 75
 /** Periwinkle */
#define CLR_PERIWINKLE 76
 /** Heliotrope */
#define CLR_HELIOTROPE 77
 /** Medium Purple */
#define CLR_MED_PURPLE 78
 /** Amethyst */
#define CLR_AMETHYST 79
 /** Purple Heart */
#define CLR_PURPLE_HEART 80
 /** Fun Green */
#define CLR_FUN_GREEN 81
 /** Lima */
#define CLR_LIMA 82
 /** Screaming Green */
#define CLR_SCREAMING_GREEN 83
 /** Mint Green */
#define CLR_MINT_GREEN 84
 /** Pink Lace */
#define CLR_PINK_LACE 85
 /** Lavendar Rose */
#define CLR_LAVENDER_ROSE 86
 /** Pink Flamingo */
#define CLR_PINK_FLAMINGO 87
 /** Magenta */
#define CLR_MAGENTA 88
 /** Purple Pizzazz */
#define CLR_PURPLE_PIZZAZZ 89
 /** Pompadour */
#define CLR_POMPADOUR 90
 /** Verdun Green */
#define CLR_VERDUN_GREEN 91
 /** Atlantis */
#define CLR_ATLANTIS 92
 /** Sulu */
#define CLR_SULU 93
 /** Reef */
#define CLR_REEF 94
 /** Cream */
#define CLR_CREAM 95
 /** Your Pink */
#define CLR_YOUR_PINK 96
 /** Carnation Pink */
#define CLR_CARNATION_PINK 97
 /** Hot Pink */
#define CLR_HT_PINK 98
 /** Hollywood Cerise */
#define CLR_HOLLYWOOD_CERISE 99
 /** Limeade */
#define CLR_LIMEADE 100
 /** Green Yellow */
#define CLR_GREEN_YELLOW 101
 /** Canary */
#define CLR_CANARY 102
 /** Mona Lisa */
#define CLR_MONA_LISA 103
 /** Wild Watermelon */
#define CLR_WILD_WATERMELON 104
 /** Wild Strawberry */
#define CLR_WILD_STRAWBERRY 105
 /** Medium Red Violet */
#define CLR_MED_RED_VIOLET 106
 /** Flirt */
#define CLR_FLIRT 107
 /** Costa Del Sol */
#define CLR_COSTA_DEL_SOL 108
 /** Electric Lime */
#define CLR_ELECTRIC_LIME 109
 /** laser Lemon */
#define CLR_LASER_LEMON 110
 /** Golden Tainoi */
#define CLR_GOLDEN_TAINOI 111
 /** Atomic Tangerine */
#define CLR_ATOMIC_TANGERINE 112
 /** Bittersweet */
#define CLR_BITTERSWEET 113
 /** Hopbush */
#define CLR_HOPBUSH 114
 /** Rouge */
#define CLR_ROUGE 115
 /** Avocado */
#define CLR_AVOCADO 116
 /** Rio Grande */
#define CLR_RIO_GRANDE 117
 /** Neon Carrot */
#define CLR_NEON_CARROT 118
 /** Sunset Orange */
#define CLR_SUNSET_ORANGE 119
 /** Lipstick */
#define CLR_LIPSTICK 120
 /** Tyiran Purple */
#define CLR_TYRIAN_PURPLE 121
 /** Potters Clay */
#define CLR_POTTERS_CLAY 122
 /** Buddha Gold */
#define CLR_BUDDHA_GOLD 123
 /** Chocolate */
#define CLR_CHOCOLATE 124
 /** Scarlet */
#define CLR_SCARLET 125
 /** Guardsman Red */
#define CLR_GUARDSMAN_RED 126
 /** Paprika */
#define CLR_PAPRIKA 127
 /** Metallic Copper */
#define CLR_METALLIC_COPPER 128
 /** Grenadier */
#define CLR_GRENADIER 129
 /** Oregon */
#define CLR_OREGON 130
 /** Red Berry */
#define CLR_RED_BERRY 131
 /** Stiletto */
#define CLR_STILETTO 132
 /** Crimson */
#define CLR_CRIMSON 133
 /** Dark Khaki */
#define CLR_DK_KHAKI 134
 /** Tundora */
#define CLR_TUNDORA 135
 /** Boulder */
#define CLR_BOUDLER 136
 /** Alto */
#define CLR_ALTO 137
 /** Alabaster */
#define CLR_ALABASTER 138
 /** Rosy Brown */
#define CLR_ROSY_BROWN 139
 /** Color Maximum */
#define CLR_MAX 139

/** @} */

/**
 * @defgroup SETTINGS_GROUP CONTAM settings
 *
 * @{
 */

 /** SketchPad Width */
#define SKWIDTH_INT_STG "skwidth"
 /** SketchPad Height */
#define SKHEIGHT_INT_STG "skheight"
 /** default units - 0= SI, 1= IP */
#define DEF_UNITS_INT_STG "defUnits"
 /** default flow units */
#define DEF_FLOWS_INT_STG "defFlows"
 /** default zon temperature */
#define DEF_T_FLT_STG "defT"
 /** default temperature units */
#define UDEF_T_INT_STG "udefT"
 /** relative north */
#define RELN_FLT_STG "relN"
 /** elevation for reference wind speed */
#define WINDH_FLT_STG "windH"
 /** Length units for elevation */
#define UWH_INT_STG "uwH"
 /** local terrain constant */
#define WINDAO_FLT_STG "windAo"
 /** velocity profile exponent */
#define WINDA_FLT_STG "winda"
 /** scaling factor */
#define SCF_FLT_STG "scf"
 /** Length Units fo scaling factor */
#define USCF_INT_STG "uscf"
 /** origin row */
#define ORG_ROW_INT_STG "orgRow"
 /** origin column */
#define ORG_COL_INT_STG "orgCol"
 /** invert Y axis */
#define INV_YAX_INT_STG "invYaxis"
 /** show geometry */
#define SH_GEO_INT_STG "showGeom"
 /** ambient temperature steady-state */
#define TA_ST_FLT_STG "TaStdy"
 /** ambient pressure steady-state */
#define PB_ST_FLT_STG "PbStdy"
 /** wind speed steady-state */
#define WS_ST_FLT_STG "WsStdy"
 /** wind direction steady-state */
#define WD_ST_FLT_STG "WdStdy"
 /** reltive humidity steady-state */
#define RH_ST_FLT_STG "rhStdy"
 /** day of year steady-state */
#define DAYT_ST_INT_STG "dayStdy"
 /** Temperature  units steady-state */
#define UTA_ST_INT_STG "uTaStdy"
 /** Pressure units steady-state */
#define UPB_ST_INT_STG "uPbStdy"
 /** Speed units for wind steady-state */
#define UWS_ST_INT_STG "uwsStdy"
 /** units wind direction steady-state */
#define UWD_ST_INT_STG "uwdStdy"
 /** ambient temperature wind-pressure */
#define TA_WND_FLT_STG "TaWind"
 /** ambient pressure wind-pressure */
#define PB_WND_FLT_STG "PbWind"
 /** wind speed wind-pressure */
#define WS_WND_FLT_STG "WsWind"
 /** wind direction wind-pressure */
#define WD_WND_FLT_STG "WdWind"
 /** relative humidity wind-pressure */
#define RH_WND_FLT_STG "rhWind"
 /** day of year wind-pressure */
#define DAYT_WND_INT_STG "dayWind"
 /** Temperature units wind-pressure */
#define UTA_WND_INT_STG "uTaWind"
 /** Pressure units wind-pressure */
#define UPB_WND_INT_STG "uPbWind"
 /** Speed units for wind wind-pressure */
#define UWS_WND_INT_STG "uwsWind"
 /** units wind direction wind-pressure */
#define UWD_WND_INT_STG "uwdWind"
 /** weather file path */
#define WTH_PATH_STG "wth"
 /** contaminant file path */
#define CTM_PATH_STG "ctm"
 /** CVF file path */
#define CVF_PATH_STG "cvf"
 /** DVF file path */
#define DVF_PATH_STG "dvf"
 /** WPC file path */
#define WPC_PATH_STG "wpc"
 /** EWC file path */
#define EWC_PATH_STG "ewc"
 /** WPC origin X */
#define XREF_PLD_FLT_STG "Xref"
 /** WPC origin Y */
#define YREF_PLD_FLT_STG "Yref"
 /** WPC origin Z */
#define ZREF_PLD_FLT_STG "Zref"
 /** Coordinate rotation */
#define ANGL_PLD_FLT_STG "angle"
 /** X,Y,Z length units */
#define UXYZ_PLD_INT_STG "uXYZ"
 /** tolerance for matching path locations */
#define EPSP_PLD_FLT_STG "epsP"
 /** tolerance for matching species */
#define EPSS_PLD_FLT_STG "epsS"
 /** Data time shift */
#define TSHFT_PLD_INT_STG "tShift"
 /** date WPC starts */
#define DSTRT_PLD_INT_STG "dStart"
 /** date WPC ends */
#define DEND_PLD_INT_STG "dEnd"
 /** Use WPC wind pressure */
#define WP_PLD_INT_STG "wpcWP"
 /** Use WPC mass frasctions */
#define MF_PLD_INT_STG "wpcMF"
 /** if true, Only allow WPC and DVF files to trigger airflow calculations */
#define TRIG_PLD_INT_STG "wpctrig"
 /** latitude */
#define LAT_LOC_FLT_STG "latd"
 /** longitude */
#define LGT_LOC_FLT_STG "longtd"
 /** time zone number */
#define TZ_LOC_FLT_STG "tznr"
 /** altitude */
#define ALT_LOC_FLT_STG "altd"
 /** ground temperature */
#define TGR_LOC_FLT_STG "Tgrnd"
 /** Length units for altitude */
#define UALT_LOC_INT_STG "uAlt"
 /** Tempeature units for ground */
#define UTG_LOC_INT_STG "uTg"
 /** airflow simulation: 0=steady, 1 = dynamic, 2 = balance duct flows */
#define SIMAF_INT_STG "simAf"
 /** N-R method for non-linear eqns: 0=SUR, 1=STR */
#define AF_CALC_INT_STG "afcalc"
 /** maximum number of airflow iterations */
#define AF_MAXI_INT_STG "afmaxi"
 /** relative airflow convergence factor */
#define AF_RCNVG_FLT_STG "afrcnvg"
 /** absolute airflow convergence factor [1/s] */
#define AF_ACNVG_FLT_STG "afacnvg"
 /** flow under-relaxation coefficient (SUR) */
#define AF_RELAX_FLT_STG "afrelax"
 /** units for airflow convergence */
#define AF_UAC_INT_STG "uac"
 /** Building Pressurization value */
#define PBLDG_FLT_STG "Pbldg"
 /** Prssure units for building pressurization */
#define UPBLDG_INT_STG "uPb"
 /** method for airflow SLAE: 0=SKY, 1=PCG */
#define AF_SLAE_INT_STG "afslae"
 /** if true, resequence the linear equations */
#define AF_RSEQ_INT_STG "afrseq"
 /** maximum number of iterations (PCG) */
#define AF_LMAXI_INT_STG "aflmaxi"
 /** relative convergence factor for (PCG) */
#define AF_LCNVG_FLT_STG "aflcnvg"
 /** if true, do linear airflow initialization */
#define AF_LINIT_INT_STG "aflinit"
 /** if true, use temperature adjustment */
#define AF_TADJ_INT_STG "afTadj"
 /** mass fraction (contaminant) simulation: 0 = none, 1=steady, 2 = transient, 3 = cyclic */
#define SIMMF_INT_STG "simMf"
 /** maximum number of iterations (cyclic) */
#define MF_CY_MAXI_INT_STG "maxiCy"
 /** relative convergence factor (cyclic) */
#define MF_CY_RCNVG_FLT_STG "rcnvgCy"
 /** absolute convergence factor [kg/kg] (cyclic) */
#define MF_CY_ACNVG_FLT_STG "acnvgCy"
 /** over-relaxation coefficient (cyclic) */
#define MF_CY_RELAX_FLT_STG "relaxCy"
 /** units for ccacnvg */
#define MF_CY_UCC_INT_STG "uccCy"
 /** 0 = SKY, 1 = BCG, 2 = SOR, 3 = LU, ... (non-trace) */
#define MF_NT_MTH_INT_STG "mthdNt"
/** if true, resequence the linear equations (non-trace) */
#define MF_NT_RSEQ_INT_STG "rseqNt"
 /** maximum iterations (non-trace) */
#define MF_NT_MAXI_INT_STG "maxiNt"
 /** relative convergence (non-trace) */
#define MF_NT_RCNVG_FLT_STG "rcnvgNt"
 /** absolute convergence (non-trace) */
#define MF_NT_ACNVG_FLT_STG "acnvgNt"
 /** realxation coefficient (non-trace) */
#define MF_NT_RELAX_FLT_STG "relaxNt"
 /** trapezoidal integration factor (non-trace) */
#define MF_NT_GAMMA_FLT_STG "gammaNt"
 /** units for mfnacnvg (non-trace) */
#define MF_NT_UCCN_INT_STG "uccNt"
 /** 0 = SKY, 1 = BCG, 2 = SOR, 3 = LU, ... (trace) */
#define MF_TR_MTH_INT_STG "mthdTr"
 /** if true, resequence the linear equations (trace) */
#define MF_TR_RSEQ_INT_STG "rseqTr"
 /** maximum iterations (trace) */
#define MF_TR_MAXI_INT_STG "maxiTr"
 /** relative convergence  (trace) */
#define MF_TR_RCNVG_FLT_STG "rcnvgTr"
 /** absolute convergence  (trace) */
#define MF_TR_ACNVG_FLT_STG "acnvgTr"
 /** relaxation coefficient (trace)  */
#define MF_TR_RELAX_FLT_STG "relaxTr"
 /** trapezoidal integration factor (trace) */
#define MF_TR_GAMMA_FLT_STG "gammaTr"
 /** units for ucct (trace) */
#define MF_TR_UCCT_INT_STG "uccTr"
 /** 0 = SKY, 1 = BCG, 2 = SOR, 3 = LU, ... BCG not allowed (cvode) */
#define MF_CV_MTH_INT_STG "LMthdCv"
 /** if true, resequence the linear equations (cvode) */
#define MF_CV_RSEQ_INT_STG "rseqCv"
 /** maximum iterations (cvode) */
#define MF_CV_MAXI_INT_STG "maxiCv"
 /** relative convergence (cvode) */
#define MF_CV_RCNVG_FLT_STG "rcnvgCv"
 /** absolute convergence (cvode) */
#define MF_CV_ACNVG_FLT_STG "acnvgCv"
 /** relaxation coefficient  (cvode) */
#define MF_CV_RELAX_FLT_STG "relaxCv"
 /** units uccv (cvode) */
#define MF_CV_UCCV_INT_STG "uccCv"
 /** 0=trapezoid, 1=STS, 2=CVODE */
#define MF_SOLV_INT_STG "mfSolver"
 /** if true, use 1D zones */
#define SIM_1DZ_INT_STG "sim1dz"
 /** if true, use 1D ducts */
#define SIM_1DD_INT_STG "sim1dd"
 /** length of duct cells for C-D modeling [m] */
#define CELL_DX_FLT_STG "celldx"
 /** if true, compute variable junction temperatures */
#define SIM_VJT_INT_STG "simVtj"
 /** Length units for cell length */
#define CELL_UDX_INT_STG "udx"
 /** 0=BDF, 1=AM */
#define CVODE_MTH_INT_STG "NLMthCv"
 /** relative convergence */
#define CVODE_RCNVG_FLT_STG "cvRcnvg"
 /** absolute convergence */
#define CVODE_ACNVG_FLT_STG "cvAcnvg"
 /** maximum time step */
#define CVODE_DT_MAX_FLT_STG "cvDtMax"
 /** if true, vary density during time step */
#define TSDENS_INT_STG "tsdens"
 /** under-relaxation factor for calculating dM/dt */
#define TSRELAX_FLT_STG "tsrelax"
 /** maximum number of time step iterations (density changes) */
#define TSMAXI_INT_STG "tsmaxi"
 /** if true (default), converge S.S. flows varying air density */
#define CNVG_SS_INT_STG "cnvgSS"
 /** if true (default), use zone pressure to compute air density */
#define DENS_ZP_INT_STG "densZP"
 /** if true (not def), vary D with H in stack calculation */
#define STACKD_INT_STG "stackD"
 /** if true (not def), include dMdt in airflow calculation */
#define DO_DMDT_INT_STG "dodMdt"
 /** simulation date (steady-state) */
#define STDYD_INT_STG "datest"
 /** simlation time (steady-state) */
#define STDYT_INT_STG "timest"
 /** simulation start date (transient) */
#define STRTD_INT_STG "date0"
 /** simulation start time (transient) */
#define STRTT_INT_STG "time0"
 /** simulation end date (transient) */
#define ENDD_INT_STG "date1"
 /** simulation end time (transient) */
#define ENDT_INT_STG "time1"
 /** calculation time step */
#define CTS_INT_STG "tstep"
 /** output time step */
#define LTS_INT_STG "tlist"
 /** screen time step */
#define STS_INT_STG "tscrn"
 /** use restart */
#define RST_INT_STG "restart"
 /** restart date */
#define RSTD_INT_STG "rstDate"
 /** restart time */
#define RSTT_INT_STG "rstTime"
 /** output logging */
#define LIST_INT_STG "list"
 /** use window dialog */
#define DO_DLG_INT_STG "doDlg"
 /** save flow data */
#define PF_SAVE_INT_STG "pfsave"
 /** save node data */
#define ZF_SAVE_INT_STG "zfsave"
 /** save mass fraction data */
#define ZC_SAVE_INT_STG "zcsave"
 /** 1 = ACH based on true volumes instead of std volumes */
#define ACH_VOL_INT_STG "achvol"
 /** 1 = save building air exchange rate transient data */
#define ACH_SAVE_INT_STG "achsave"
 /** 1 = save air exchange rate box-whisker data */
#define ABW_SAVE_INT_STG "abwsave"
 /** 1 = save contaminant box-whisker data */
#define CBW_SAVE_INT_STG "cbwsave"
 /** 1 = save exposure transient data */
#define EXP_SAVE_INT_STG "expsave"
 /** 1 = save exposure box-whisker data */
#define EBW_SAVE_INT_STG "ebwsave"
 /** 1 = save zones age-of-air transient data */
#define ZAA_SAVE_INT_STG "zaasave"
 /** 1 = save zones age-of-air box-whisker data */
#define ZBW_SAVE_INT_STG "zbwsave"
 /** 1 = save zone flow file */
#define RZF_SAVE_INT_STG "rzfsave"
 /** 1 = save zone mass file */
#define RZM_SAVE_INT_STG "rzmsave"
 /** 1 = save zone 1D file */
#define RZ1_SAVE_INT_STG "rz1save"
 /** 1 = save csm file */
#define CSM_SAVE_INT_STG "csmsave"
 /** 1 = save surface file */
#define SRF_SAVE_INT_STG "srfsave"
 /** 1 = save controls log file */
#define CLG_SAVE_INT_STG "clgsave"
 /** 1 = save basic cex  file */
#define BCEX_SAVE_INT_STG "bcexsave"
 /** 1 = save detaild cex files */
#define DCEX_SAVE_INT_STG "dcexsave"
 /** 1 = save path flow results to SQL */
#define PFSQL_SAVE_INT_STG "pfsqlsave"
 /** 1 = save zone flow results to SQL */
#define ZFSQL_SAVE_INT_STG "zfsqlsave"
 /** 1 = save zone mass (contaminant) results to SQL */
#define ZCSQL_SAVE_INT_STG "zcsqlsave"
 /** density used for ACH calculation (default 1.2041) [kg/m^3] */
#define DENS_ACH_FLT_STG "densACH"
 /** acceleration of gravity (default 9.8055) [m/s^2] */
#define GRAV_FLT_STG "grav"
 /** extra variables */
#define EXTRA0_INT_STG "extra0"
 /** extra variables */
#define EXTRA1_INT_STG "extra1"
 /** extra variables */
#define EXTRA2_INT_STG "extra2"
 /** extra variables */
#define EXTRA3_INT_STG "extra3"
 /** extra variables */
#define EXTRA4_INT_STG "extra4"
 /** extra variables */
#define EXTRA5_INT_STG "extra5"
 /** extra variables */
#define EXTRA6_INT_STG "extra6"
 /** extra variables */
#define EXTRA7_INT_STG "extra7"
 /** extra variables */
#define EXTRA8_INT_STG "extra8"
 /** extra variables */
#define EXTRA9_INT_STG "extra9"
 /** extra variables */
#define EXTRA10_INT_STG "extra10"
 /** extra variables */
#define EXTRA11_INT_STG "extra11"
 /** extra variables */
#define EXTRA12_INT_STG "extra12"
 /** extra variables */
#define EXTRA13_INT_STG "extra13"
 /** extra variables */
#define EXTRA14_INT_STG "extra14"
 /** extra variables */
#define EXTRA15_INT_STG "extra15"
 /** if true, do building airflow test (zones) */
#define VAL_Z_INT_STG "valZ"
 /** if true, do building airflow test (ducts) */
#define VAL_D_INT_STG "valD"
 /** if true, do building airflow test (classified flows */
#define VAL_C_INT_STG "valC"
 /** Couple type (0=contam only,1=post-process,2=quasi,3=dynamic) */
#define CFD_CTYP_INT_STG "cfd"
 /** Convergence Factor for Airflow Coupling */
#define CFD_CNVG_FLT_STG "cfdcnvg"
 /** Use var file (0=no, 1=yes) */
#define CFD_VAR_INT_STG "cfdvar"
 /** reference zone (not used) */
#define CFD_ZREF_INT_STG "cfdzref"
 /** Max number of couple iterations */
#define CFD_MAXI_INT_STG "cfdmaxi"
 /** CMO output step (0 – imax?) */
#define CFD_DTCMO_INT_STG "dtcmo"
 /** linear solver: 0=TDMA, 1=multigrid */
#define CFD_SOLV_INT_STG "cfdsolv"
 /** multigrid smoother: 0=Gauss-Seidel, 1=TDMA */
#define CFD_SMOOTH_INT_STG "cfdsmooth"
 /** convergence criterion for velocity */
#define CFD_CUVM_FLT_STG "cnvgUVM"
 /** convergence criterion for energy/temperature */
#define CFD_CONVT_FLT_STG "cfdcnvgT"

/** @} */

/**
 * @defgroup ZONE_GROUP CONTAM zones
 *
 * @{
 */

 /** zone name  */
#define ZONE_NAME_STR "name"
 /** axial dispersion coefficient */
#define ZONE_AXIALD_FLT "axialD"
 /** 0=none, 1=1d zone */
#define ZONE_CDAXIS_SHT "cdaxis"
 /** length of c/d cell [m] */
#define ZONE_CELLDX_FLT "celldx"
 /** CFD zone ID */
#define ZONE_CFD_NAME_STR "cfd_name"
 /** zone color */
#define ZONE_COLOR_SHT "color"
 /** 1= vary zone pressure */
#define ZONE_VARP_SHT "varP"
 /** 1= vary zone contaminant mass fraction */
#define ZONE_VARM_SHT "varM"
 /** 1= include inbuilding volume */
#define ZONE_BVOL_SHT "bldgVol"
 /** 1= cfd zone */
#define ZONE_CFD_SHT "cfd"
 /** zone elevation point 1 (1d zone) */
#define ZONE_H1_FLT "H1"
 /** zone elevation point 2 (1d zone) */
#define ZONE_H2_FLT "H2"
 /** zone number (output only) */
#define ZONE_NR_INT "nr"
 /** zone constant pressure */
#define ZONE_P0_FLT "P0"
 /** zone control number */
#define ZONE_CTRL_INT "ctrl"
 /** zone kinteic reaction name */
#define ZONE_KINR_STR "kinr"
 /** zone level name */
#define ZONE_LEVEL_STR "level"
 /** zone schedule name */
#define ZONE_SCHED_STR "sched"
 /** zone height relative to level [m] */
#define ZONE_RELHT_FLT "relHt"
 /** initial zone temperature */
#define ZONE_T0_FLT "T0"
 /** MOL_DIFF units for axial dispersal */
#define ZONE_U_AD_SHT "u_aD"
 /** Length units for relHt */
#define ZONE_U_HT_SHT "u_Ht"
 /** Length units for XYZ */
#define ZONE_U_L_SHT "u_L"
 /** Pressure units */
#define ZONE_U_P_SHT "u_P"
 /** Tempertaure units */
#define ZONE_U_T_SHT "u_T"
 /** Volume units */
#define ZONE_U_V_SHT "u_V"
 /** Value file node name */
#define ZONE_VF_NODE_NAME_STR "vf_node_name"
 /** Value file type */
#define ZONE_VF_TYPE_SHT "vf_type"
 /** Zone volume */
#define ZONE_VOL_FLT "Vol"
 /** Zone X1 (1d zone) */
#define ZONE_X1_FLT "X1"
 /** Zone X2 (1d zone) */
#define ZONE_X2_FLT "X2"
 /** Zone Y1 (1d zone) */
#define ZONE_Y1_FLT "Y1"
 /** Zone Y2 (1d zone) */
#define ZONE_Y2_FLT "Y2"
 /** Zone initial concentration array */
#define ZONE_CC0_ARR "CC0"

/** @} */

/**
 * @defgroup PATH_GROUP CONTAM paths
 *
 * @{
 */

 /** Type of BC in CFD (0 Mdot, 1 Press) */
#define PATH_CFD_BTYP_SHT "cfd_btyp"
 /** Type of BC in CONTAM (0 Mass flow Rate, 1 Pressure) */
#define PATH_CFD_CAPP_SHT "cfd_capp"
 /** CFD ID of path from PRJ file */
#define PATH_CFD_PNAME_STR "cfd_pname"
 /** Type of path for CFD treatment (1=powerlaw, 2=pressure) */
#define PATH_CFD_PTYP_SHT "cfd_ptyp"
 /** path color */
#define PATH_COLOR_SHT "color"
 /** path direction */
#define PATH_DIR_BYT "dir"
 /** return/supply flow rate */
#define PATH_FAHS_FLT "Fahs"
 /** use limits 0=none, 1=press, 2=flow */
#define PATH_LIM_SHT "lim" 
 /** use wind 0=no wind, 1=wind*/
#define PATH_WIND_SHT "wind"
 /** path icon */
#define PATH_ICON_SHT "icon"
 /** path multiplier */
#define PATH_MULT_FLT "mult"
 /** path nunber (output only) */
#define PATH_NR_INT "nr"
 /** path AHS name */
#define PATH_AHS_STR "ahs"
 /** path control number */
#define PATH_CTRL_INT "ctrl"
 /** path aiflow element name */
#define PATH_ELEMENT_STR "element"
 /** path filter number */
#define PATH_FILTER_INT "filter"
 /** path level name */
#define PATH_LEVEL_STR "level"
 /** path schdeule name */
#define PATH_SCHED_STR "sched"
 /** path wind pressure profile name  */
#define PATH_WPP_STR "wpp"
 /** path connected zone M number */
#define PATH_ZM_INT "zm"
 /** path connected zone N number */
#define PATH_ZN_INT "zn"
 /** path relative height to level */
#define PATH_RELHT_FLT "relHt"
 /** Pressure units for constant wind pressure  */
#define PATH_U_DP_SHT "u_dP"
 /** Flow Rate units for return/supply */
#define PATH_U_F_SHT "u_F"
 /** Length units for relative height */
#define PATH_U_HT_SHT "u_Ht"
 /** Length units for XY values */
#define PATH_U_XY_SHT "u_XY"
 /** path values file node name */
#define PATH_VF_NODE_NAME_STR "vf_node_name"
 /** path values file node type */
#define PATH_VF_TYPE_SHT "vf_type"
 /** path wall azimuth angle */
#define PATH_WAZM_FLT "wazm"
 /** path wind speed modifier */
#define PATH_WP_MOD_FLT "wPmod"
 /** path constant wind pressure */
#define PATH_WP_SET_FLT "wPset"
 /** path X value (wpc or 1d zone) */
#define PATH_X_FLT "X"
 /** path limit maximum  */
#define PATH_X_MAX_FLT "Xmax"
 /** path limit minimum */
#define PATH_X_MIN_FLT "Xmin"
 /** path Y value (wpc or 1d zone) */
#define PATH_Y_FLT "Y"

/** @} */

/**
 * @defgroup PATH_LIMIT_GROUP Limit values for paths
 *
 * @{
 */

 /** No path limits */
#define PATH_LIM_NONE 0
 /** use path pressure limit */
#define PATH_LIM_PRES 1
 /** use path flow limit */
#define PATH_LIM_FLOW 2

 /** @} */

/**
 * @defgroup LEVEL_GROUP CONTAM levels
 *
 * @{
 */

 /** level name */
#define LEV_NAME_STR "name"
 /** level reference height */
#define LEV_REFHT_FLT "refht"
 /** level delta height  */
#define LEV_DELHT_FLT "delht"
 /** Length units for ref height */
#define LEV_U_RFHT_SHT "u_rfht"
 /**  Length units for delta height */
#define LEV_U_DLHT_SHT "u_dlht"
 /** level icons array - see @ref ICONS_GROUP */
#define LEV_ICONS_ARR "icons"
 /** icon column */
#define LEV_IC_COL_SHT "col"
 /** icon row */
#define LEV_IC_ROW_SHT "row"
 /** icon number */
#define LEV_IC_NR_INT "nr"
 /** icon icon number */
#define LEV_IC_ICON_BYT "icon"

/** @} */

/**
 * @defgroup CONSS_GROUP CONTAM contaminant source/sink
 *
 * @{
 */

 /** Source/Sink initial concentration  */
#define CSS_CC0_FLT "CC0"
 /** name to couple with CFD model */
#define CSS_CFD_PNAME_STR "cfd_pname"
 /** Source/Sink color */
#define CSS_COLOR_SHT "color"
 /** Relative Elevation Maximum (1d zone) */
#define CSS_HMAX_FLT "Hmax"
 /** Relative Elevation Minimum (1d zone) */
#define CSS_HMIN_FLT "Hmin"
 /** Source/Sink multiplier */
#define CSS_MULT_FLT "mult"
 /** Source/Sink number (output only) */
#define CSS_NR_INT "nr"
 /** Source/Sink control number */
#define CSS_CTRL_INT "ctrl"
 /** Source/Sink element name */
#define CSS_ELEMENT_STR "element"
 /** Source/Sink schedule name */
#define CSS_SCHED_STR "sched"
 /** Source/Sink zone number */
#define CSS_ZONE_INT "zone"
 /** Length units for XYZ */
#define CSS_U_XYZ_SHT "u_XYZ"
 /** Source/Sink Values file node name */
#define CSS_VF_NODE_NAME_STR "vf_node_name"
 /** Source/Sink Values file type */
#define CSS_VF_TYPE_SHT "v_type"
 /** Source/Sink X maximum (1d zone) */
#define CSS_XMAX_FLT "Xmax"
 /** Source/Sink X minimum (1d zone) */
#define CSS_XMIN_FLT "Xmin"
 /** Source/Sink Y maximum (1d zone */
#define CSS_YMAX_FLT "Ymax"
 /** Source/Sink Y minimum (1d zone) */
#define CSS_YMIN_FLT "Ymin"

/** @} */

/**
 * @defgroup JUNCTION_GROUP CONTAM junction/terminals
 *
 * @{
 */

 /** Area of duct */
#define JCT_AD_FLT "Ad"
 /** free area of face */
#define JCT_AF_FLT "Af"
 /** if true, this terminal is (to be) balanced  */
#define JCT_BAL_SHT "bal"
 /** loss coefficient for balanced flows [-] */
#define JCT_CB_FLT "Cb"
 /** maximum Cb desired [-] */
#define JCT_CBMAX_FLT "Cbmax"
 /** junction color */
#define JCT_COLOR_SHT "color"
 /** loss coefficient of basic terminal [-] */
#define JCT_CT_FLT "Ct"
 /** direction of terminal duct - to show wP */
#define JCT_DDIR_BYT "ddir"
 /** design flow rate [kg/s] */
#define JCT_FDES_FLT "Fdes"
 /** positive flow direction - to show flow */
#define JCT_FDIR_BYT "fdir"
 /** use wind pressure */
#define JCT_WIND_SHT "wind"
 /** junction icon */
#define JCT_ICON_BYT "icon"
 /** junction number (output only) */
#define JCT_NR_INT "nr"
 /** junction initial pressure */
#define JCT_P0_FLT "P0"
 /** junction control number */
#define JCT_CTRL_INT "ctrl"
 /** junction kinetic reaction name */
#define JCT_KINR_STR "kinr"
 /** junction level name */
#define JCT_LEVEL_STR "level"
 /** junction schedule name */
#define JCT_SCHED_STR "sched"
 /** junction relative height */
#define JCT_RELHT_FLT "relHt"
 /** junction initial temperature */
#define JCT_T0_FLT "T0"
 /** junction dowward duct number */
#define JCT_DDNR_INT "ddnr"
 /** terminal filter number */
#define JCT_FILT_INT "filt"
 /** terminal wind pressure profile name */
#define JCT_WPP_STR "wpp"
 /** junction zone number */
#define JCT_ZN_INT "pzn"
 /** Area units */
#define JCT_U_A_SHT "u_A"
 /** Pressure units */
#define JCT_U_DP_SHT "u_dP"
 /** Flow Rate units */
#define JCT_U_F_SHT "u_F"
 /** Length units for relative height */
#define JCT_U_HT_SHT "u_Ht"
 /** Temperature units */
#define JCT_U_T_SHT "u_T"
 /** Length units for XY  */
#define JCT_U_XY_SHT "u_XY"
 /** Junction Values file node name */
#define JCT_VF_NODE_NAME_STR "vf_node_name"
 /** Junction Value file type */
#define JCT_VF_TYPE_SHT "vf_type"
 /** Junction volume */
#define JCT_VOL_FLT "Vol"
 /** Terminal azimuth angle */
#define JCT_WAZM_FLT "wazm"
 /** Terminal wind pressure modifier */
#define JCT_WPMOD_FLT "wPmod"
 /** Terminal constant wind pressure [Pa] */
#define JCT_WPSET_FLT "wPset"
 /** Junction X (wpc or 1d zone) */
#define JCT_X_FLT "X"
 /** Junction Y (wpc or 1d zone) */
#define JCT_Y_FLT "Y"
 /** Jucntion initial Contaminant concentration array */
#define JCT_CC0_ARR "CC0"

/** @} */

/**
 * @defgroup DUCT_GROUP CONTAM ducts
 *
 * @{
 */

 /** flow area at inlet end [m^2] - future */
#define DCT_AIN_FLT "Ain"
 /** flow area at outlet end [m^2] - future */
#define DCT_AOUT_FLT "Aout"
 /** duct color */
#define DCT_COLOR_SHT "color"
 /** positive flow direction on sketchpad */
#define DCT_DIR_BYT "dir"
 /** length of the duct segment [m] */
#define DCT_LENGTH_FLT "length"
 /** duct number (output only) */
#define DCT_NR_INT "nr"
 /** duct control number */
#define DCT_CTRL_INT "ctrl"
 /** duct airflow element name */
#define DCT_ELEMENT_STR "element"
 /** duct filter number */
#define DCT_FILTER_INT "filter"
 /** duct connected junction M number */
#define DCT_JCTM_INT "jctm"
 /** duct connnected junction N number */
#define DCT_JCTN_INT "jctn"
 /** duct schedule name */
#define DCT_SCHED_STR "sched"
 /** sum of local loss coefficients */
#define DCT_SLLC_FLT "sllc"
 /** Area units */
#define DCT_U_A_SHT "u_A"
 /** Length units */
#define DCT_U_L_SHT "u_L"
 /** duct Values file node name */
#define DCT_VF_NODE_NAME_STR "vf_node_name"
 /** duct Values file type */
#define DCT_VF_TYPE "vf_type"

/** @} */
/**
 * @defgroup AHS_GROUP CONTAM simple air handling system
 *
 * @{
 */

 /** AHS number (output only) */
#define AHS_NR_INT "nr"
 /** AHS name */
#define AHS_NAME_STR "name"
 /** AHS description */
#define AHS_DESC_STR "desc"
 /** AHS color */
#define AHS_COLOR_SHT "color"
 /** AHS minimum outdoor air flow */
#define AHS_MIN_OA_FLOW_FLT "minOA"
 /** outdoor air location X (wpc) */
#define AHS_OAI_X_FLT "oaX"
 /** outdoor air location Y (wpc) */
#define AHS_OAI_Y_FLT "oaY"
 /** outdoor air loaction (wpc) */
#define AHS_OAI_Z_FLT "oaZ"
 /** supply zone volume */
#define AHS_SUP_VOL_FLT "svol"
 /** supply zone initial contaminant concentration array */
#define AHS_SUP_CC0_ARR "sCC0"
 /** supply zone kinetic reaction name */
#define AHS_SUP_KNR_STR "sKinr"
 /** return zone volume */
#define AHS_RET_VOL_FLT "rvol"
 /** return zone initial contaminant concentration array */
#define AHS_RET_CC0_ARR "rCC0"
 /** return zone kinetic reaction name */
#define AHS_RET_KNR_STR "rKinr"
 /** outdoor air schdeule name */
#define AHS_OA_SCHED_STR "oaSched"
 /** outdoor air filter number */
#define AHS_OA_FILT_STR "oaFilt"
 /** recirculation filter number */
#define AHS_REC_FILT_STR "recFilt"
 /** AHS Values file node name */
#define AHS_VF_NODE_NAME_STR "vf_node_name"
 /** AHS Values file type */
#define AHS_VF_TYPE "vf_type"
 /** Flow Rate units */
#define AHS_U_F_SHT "u_F"
 /** Length units for XYZ  */
#define AHS_U_XYZ_SHT "u_XYZ"
 /** Volume units for supply zone */
#define AHS_U_SUP_VOL_SHT "u_sV"
 /** Volume units for return zone */
#define AHS_U_RET_VOL_SHT "u_rV"

/** @} */

/**
 * @defgroup FILTER_GROUP CONTAM filters
 *
 * @{
 */

 /** filter number (output only) */
#define FLT_NR_INT "nr"
 /** filter element name */
#define FLT_ELEMENT_STR "element"
 /** filter loading array */
#define FLT_LOADING_ARR "loadings"
 /** loading point - total loading */
#define FLT_PT_TLOAD_FLT "tload"
 /** loading point - number of individual loadings = 0 - future */
#define FLT_PT_NILOADS_SHT "niloads"

/** @} */

/**
 * @defgroup OCC_SCHEDULE_GROUP CONTAM occuapnt schedule
 *
 * @{
 */

 /** occupant schdeule name */
#define OCS_NAME_STR "name"
 /** occupant schedule description */
#define OCS_DESC_STR "desc"
 /** Length units for XYZ */
#define OCS_U_XYZ_SHT "u_XYZ"
 /** Is schedule used? (output only) */
#define OCS_USED_SHT "used"
 /** schedule data array */
#define OCS_DATA_ARR "data"
 /** schedule data - reative height */
#define OCS_PT_RELHT_FLT "relHt"
 /** schedule data - time of day [sec] */
#define OCS_PT_TIME_INT "time"
 /** schedule data - X */
#define OCS_PT_X_FLT "X"
 /** schedule data - Y */
#define OCS_PT_Y_FLT "Y"
 /** schedule data - Zone Number */
#define OCS_PT_ZONE_INT "zone"

/** @} */

/**
 * @defgroup PEXP_GROUP CONTAM personal exposure
 *
 * @{
 */

 /** personal exposure number (output only) */
#define PEXP_NR_INT "nr"
 /** personal exposure contaminant generation multiplier  */
#define PEXP_CGMLT_FLT "cgmlt"
 /** personal exposure color */
#define PEXP_COLOR_SHT "color"
 /** personal exposure decsription */
#define PEXP_DESC_STR "desc"
 /** personal exposure - generates contaminants? */
#define PEXP_GEN_SHT "gen"
 /** personal exposure - array of 12 occupant day schedules */
#define PEXP_OCS_ARR "odsch"
 /** personal exposure - occupant contaminant generation array */
#define PEXP_OCG_ARR "ocg"
 /** personal exposure data point - species name */
#define PEXP_PT_SPCS_STR "spcs"
 /** personal exposure data point - schedule name */
#define PEXP_PT_SCHED_STR "wsched"
 /** personal exposure data point - generation rate */
#define PEXP_PT_CGMAX_FLT "cgmax"
 /** personal exposure data point - Values file node name */
#define PEXP_PT_VF_NODE_NAME_STR "vf_node_name"
 /** personal exposure data point - Value file type */
#define PEXP_PT_VF_TYPE_SHT "vf_type"
 /** personal exposure data point - generation rate units */
#define PEXP_PT_U_G_SHT "u_G"

/** @} */

/**
 * @defgroup NOTES_GROUP CONTAM Annotations
 *
 * @{
 */

 /** Note text */
#define NOTE_TEXT_STR "note"
 /** Note color */
#define NOTE_COLOR_SHT "color"

/** @} */

/**
 * @defgroup CONTROLS_TYPE_GROUP CONTAM Control Types
 *
 * @{
 */

/* value from schedule */
#define CT_SCH  1     
/* constant value */
#define CT_SET  2    
 /* value from continuous values file - CVF */
#define CT_CVF  3    
/* value from discrete values file - DVF */
#define CT_DVF  4     
/* write value to log file */
#define CT_LOG  5     
/* pass signal (splitter) */
#define CT_PAS  6     
/* modify signal */
#define CT_MOD  7     
/* hysteresis parameter */
#define CT_HYS  8     
/* absolute value of signal */
#define CT_ABS  9     
/* convert signal to binary */
#define CT_BIN 10     
/* delay by schedule */
#define CT_DLS 11     
/* delay by exponential */
#define CT_DLX 12     
/* time integral of in1; in2 as control */
#define CT_INT 13     
/* running average */
#define CT_RAV 14     
/* invert (NOT) signal */
#define CT_INV 15     
/* AND 2 signals */
#define CT_AND 16     
/* OR 2 signals */
#define CT_OR  17     
/* XOR 2 signals */
#define CT_XOR 18     
/* add 2 signals */
#define CT_ADD 19     
/* subtract signals: out = in1 - in2 */
#define CT_SUB 20     
/* multiple 2 signals */
#define CT_MUL 21     
/* divide signals: out = in1 / in2 */
#define CT_DIV 22     
/* sum multiple signals */
#define CT_SUM 23     
/* average multiple signals */
#define CT_AVG 24     
/* maximum of multiple signals */
#define CT_MAX 25     
/* minimum of multiple signals */
#define CT_MIN 26     
/* lower limit switch */
#define CT_LLS 27     
/* upper limit switch */
#define CT_ULS 28     
/* lower band switch */
#define CT_LBS 29     
/* upper band switch */
#define CT_UBS 30     
/* lower limit control */
#define CT_LLC 31     
/* upper limit control */
#define CT_ULC 32     
/* proportional control */
#define CT_PC1 33     
/* proportional-integral control */
#define CT_PI1 34     
/*  super node */
#define CT_SUP 35
/* sensor type */
#define CT_SEN 36
/* exp() */
#define CT_EXP 37     
/* natural log */
#define CT_LGN 38
/* log base 10 */
#define CT_LG1 39
/* pow() */
#define CT_POW 40     
/* square root */
#define CT_SQT 41
/* polynomial */
#define CT_PLY 42
/* sine */
#define CT_SIN 43    
/* cosine */
#define CT_COS 44     
/* tangent */
#define CT_TAN 45     
/* modulo */
#define CT_MDU 46     
/* ceiling */
#define CT_CEL 47     
/* floor */
#define CT_FLR 48     
/* phantom sub-node of super element */
#define CT_SPH 49     
/* integrate over reporting time step */
#define CT_IRS 50    
/* average over reporting time step */
#define CT_ARS 51    

/** @} */


/**
 * @defgroup CONTROLS_GROUP CONTAM Controls
 *
 * @{
 */

 /** Control Number (output only) */
#define CTRL_NR_INT "nr"
 /** Control Sequence Number (output only) */
#define CTRL_SEQNR_INT "seqnr"
 /** Control Type - See @ref CONTROL_TYPE_GROUP */
#define CTRL_TYPE_SHT "ctype"
 /** Control Name */
#define CTRL_NAME_STR "name"
 /** Control Description */
#define CTRL_DESC_STR "desc"
 /** Control Input Number 1 */
#define CTRL_CI1_INT "ci1"
 /** Control Input Number 2 */
#define CTRL_CI2_INT "ci2"
 /** Control Sensor offset */
#define CTRL_SN_OFFSET_FLT "soffset"
 /** Control Sensor scale */
#define CTRL_SN_SCALE_FLT "sscale"
 /** Control Sensor Time Constant */
#define CTRL_SN_TAU_FLT "tau"
 /** Control Sensor X */
#define CTRL_SN_X_FLT "X"
 /** Control Sensor Y */
#define CTRL_SN_Y_FLT "Y"
 /** Control Sensor relative elevation */
#define CTRL_SN_RELHT_FLT "relHt"
 /** Control Sensor Species */
#define CTRL_SN_SPCS_STR "spcs"
 /** Control Sensor Type - See @ref CONTROLS_SENSOR_TYPE_GROUP */
#define CTRL_SN_TYPE_SHT "stype"
 /** Control Sensor Measure - SEE @ref CONTROLS_SENSOR_MEASURE_GROUP */
#define CTRL_SN_MEASURE_SHT "measure"
 /** Control Sensor Source Number */
#define CTRL_SN_SRC_NR_INT "source"
 /** Control Week Schedule Name */
#define CTRL_WK_SCH_NAME_STR "wsched"
 /** Control Set Value */
#define CTRL_SET_VAL_FLT "set"
 /** Control CVF/DVF node name */
#define CTRL_CDVF_NODE_NAME_STR "cdvf"
 /** Control Modify Offset */
#define CTRL_MOD_OFFSET_FLT "moffset"
 /** Control Modify scale */
#define CTRL_MOD_SCALE_FLT "mscale"
 /** Control Scheduled Delay increasing signal schedule */
#define CTRL_SCHED_DELAY_INC_STR "dsincr"
 /** Control Scheduled Delay decreasing signal schedule */
#define CTRL_SCHED_DELAY_DEC_STR "dsdecr"
 /** Control Exponential Delay increasing signal */
#define CTRL_EXP_DELAY_INC_INT "tauincr"
 /** Control Exponential Delay decreasing signal */
#define CTRL_EXP_DELAY_DEC_INT "taudecr"
 /** Control Integration over time shape - See @ref INTEGRATION_SHAPE_GROUP */
#define CTRL_INTG_SHAPE_SHT "ishape"
 /** Control Running Average time span (10-86400) */
#define CTRL_RAVG_TSPAN_INT "tspan"
 /** Control Report Offset */
#define CTRL_RPT_OFFSET_FLT "roffset"
 /** Control Report Scale */
#define CTRL_RPT_SCALE_FLT "rscale"
 /** Control Report Header */
#define CTRL_RPT_HDR_STR "rheader"
 /** Control Report Units */
#define CTRL_RPT_UNITS_STR "runits"
 /** Control Propotional Controller kp */
#define CTRL_PCT_KP_FLT "pkp"
 /** Control Propotional/Integral Controller kp */
#define CTRL_PICT_KP_FLT "pikp"
 /** Control Propotional/Integral Controller ki */
#define CTRL_PICT_KI_FLT "piki"
 /** Control Hysteresis */
#define CTRL_HYST_SLACK_FLT "slack"
 /** Control Polynomial Coefficients Array */
#define CTRL_POLY_COEFS_ARR "polycoefs"
 /** Control Lower Band Switch Bandwidth */
#define CTRL_LBS_BWIDTH_FLT "band"
 /** Control Upper Band Switch Bandwidth */
#define CTRL_UBS_BWIDTH_FLT "band"
 /** Control Sum Control node number array */
#define CTRL_SUM_NODE_NR_ARR "nodes"
 /** Control Avg Control node number array */
#define CTRL_AVG_NODE_NR_ARR "nodes"
 /** Control Max Control node number array */
#define CTRL_MAX_NODE_NR_ARR "nodes"
 /** Control Min Control node number array */
#define CTRL_MIN_NODE_NR_ARR "nodes"

 /** @} */

/**
 * @defgroup CONTROLS_SENSOR_TYPE_GROUP CONTAM Sensor Types
 *
 * @{
 */

 /** Control Zone Sensor */
#define CTRL_SN_TYPE_ZONE 1
 /** Control Path Sensor */
#define CTRL_SN_TYPE_PATH 2
 /** Control Junction Sensor */
#define CTRL_SN_TYPE_JCT 3
 /** Control DUCT Sensor */
#define CTRL_SN_TYPE_DUCT 4
 /** Control Personal Exposure Sensor */
#define CTRL_SN_TYPE_PEXP 5
 /** Control Terminal Sensor */
#define CTRL_SN_TYPE_TERM 6

 /** @} */

/**
 * @defgroup CONTROLS_SENSOR_MEASURE_GROUP CONTAM Control Sensor Measure Types
 *
 * @{
 */
 
 /** Control Sensor Measure Conatmiant Mass Fraction */
#define CTRL_SN_MEASURE_CTM 0
 /** Control Sensor Measure Temperature */
#define CTRL_SN_MEASURE_TEMP 1
 /** Control Sensor Measure Flow Rate */
#define CTRL_SN_MEASURE_FLRT 2
 /** Control Sensor Measure Pressure Difference */
#define CTRL_SN_MEASURE_DP 3
 /** Control Sensor Measure Absolute Pressure */
#define CTRL_SN_MEASURE_PRESS 4
 /** Control Sensor Measure Zone Occupancy  */
#define CTRL_SN_MEASURE_ZOCC 5

 /** @} */

 /** @brief Used to get a state for a project.  A project state is needed to use the other project APIs.
  *
  *  @param[in] commonState This is a pointer to a state for common contam functionality.
  *  @return A pointer to a project state.
  */
void* cpiGetNewProjectState(void* commonState);

/** @brief Used to delete a state for a project. Delete a state when finished with it to avoid a memory leak.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiDeleteProjectState(void* projectState);

/** @brief Used to open an existing project file.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] projectPath  This is the path to the exisiting project file.
 *  @param[in] tempPath     This is a path where temporary files are written. Must have write permission for that path.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiOpenProject(void* projectState, const char* projectPath, char* tempPath);

/** @brief Used to save a project to a file with an established path.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] tempPath     This is a path where temporary files are written. Must have write permission for that path.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSaveProject(void* projectState, char* tempPath);

/** @brief Used to save a project to a file with the given path.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] prjPath      This is the path to a project file.
 *  @param[in] tempPath     This is a path where temporary files are written. Must have write permission for that path.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSaveProjectAs(void* projectState, const char* prjPath, char* tempPath);

/** @brief Perform a check on the building model to determine if it is ready for a simulation. This must be done before running a simulation of the model.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @return See @ref RETURN_GROUP for return values
 */
int cpiDoBuildingCheck(void* projectState);

/** @brief Used to get a setting which uses a floating point value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the FLT_STG defines)
 *  @param[in,out] value    This is pointer to a float value which will be set by the API to the value of the setting.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetFloatSetting(void* projectState, char* setting, float* value);

/** @brief Used to set a setting which uses a floating point value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the FLT_STG defines)
 *  @param[in] value        This is a float value which will be used for the setting.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSetFloatSetting(void* projectState, char* setting, float value);

/** @brief Used to get a setting which uses an integer value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the INT_STG defines)
 *  @param[in,out] value    This is pointer to an integer value which will be set by the API to the value of the setting.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetIntegerSetting(void* projectState, char* setting, int* value);

/** @brief Used to set a setting which uses an integer value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the INT_STG defines)
 *  @param[in] value        This is an integer value which will be used for the setting.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSetIntegerSetting(void* projectState, char* setting, int value);

/** @brief Used to get a setting which uses an path value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the PATH_STG defines)
 *  @param[in,out] path     This is pointer to an char array which will be set by the API to the value of the setting.
 *  @param[in] pathSize     This is size of the path char array.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetFilePathSetting(void* projectState, char* setting, char* path, unsigned int pathSize);

/** @brief Used to set a setting which uses a path value.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] setting      This is the indentifier for the setting. See @ref SETTINGS_GROUP. (use with the PATH_STG defines)
 *  @param[in] value        This is a char array value which will be used for the setting.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSetFilePathSetting(void* projectState, char* setting, char* path);

/** @brief Used to get the project's description
 *
 *  @param[in] projectState     This is a pointer to a state for a project.
 *  @param[in, out] description This is a char array to where the project description will be copied.
 *  @param[in] descriptionSize  This is size of the description char array.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetProjectDescription(void* projectState, char* description, unsigned int descriptionSize);

/** @brief Used to set the project's description
 *
 *  @param[in] projectState    This is a pointer to a state for a project.
 *  @param[in] description     This is a char array to that contains the new project description.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSetProjectDescription(void* projectState, char* description);

/** @brief Used to get the WPC's description
 *
 *  @param[in] projectState     This is a pointer to a state for a project.
 *  @param[in, out] description This is a char array to where the WPC description will be copied.
 *  @param[in] descriptionSize  This is size of the description char array.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetWPCDescription(void* projectState, char* description, unsigned int descriptionSize);

/** @brief Used to set the WPC's description
 *
 *  @param[in] projectState    This is a pointer to a state for a project.
 *  @param[in] description     This is a char array to that contains the new WPCs description.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiSetWPCDescription(void* projectState, char* description);

/** @brief Used to delete an element from a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] elementType  This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementName  This is the name of the element to delete.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiDeleteProjectElement(void* projectState, char* elementType, char* elementName);

/** @brief Used to get the number of elements of a type in a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] elementType  This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @return The number of elements of the type specified. -1= if no project state given, -2= if element type is invalid
 */
int   cpiGetNumberOfElements(void* projectState, char* elementType);

/** @brief Used to get the default values of an element as a JSON string.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element default JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @param[in] elementSubType  This is the sub type of the element. This only used for elements with sub types.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetDefaultProjectElement(void* projectState, char* elementType, char* elementJSONbuffer, unsigned int elementJSONbufferSize, unsigned short elementSubType);

/** @brief Used to get the values of an element as a JSON string using its name.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementName            This is the name of the element to get.
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetProjectElementByName(void* projectState, char* elementType, char* elementName, char* elementJSONbuffer, unsigned int elementJSONbufferSize);

/** @brief Used to get the values of an element as a JSON string using its number.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementNumber          This is the number of the element to get. It will be in the range 1 to Number of Elements.
 *  @param[in,out] elementJSONBuffer  This is a char buffer where the element JSON string will be put.
 *  @param[in] elementJSONBufferSize  This is the size of the elementJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetProjectElementByNumber(void* projectState, char* elementType, int elementNumber, char* elementJSONbuffer, unsigned int elementJSONbufferSize);

/** @brief Used to replace the values of an element using its name.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] exisitngElementName    This is the name of the element to replace.
 *  @param[in] elementJSONBuffer      This is a char buffer where the element JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiReplaceProjectElement(void* projectState, char* elementType, char* existingElementName, char* elementJSONbuffer);

/** @brief Used to add an element of the type given.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] elementJSONBuffer      This is a char buffer where the element JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiAddProjectElement(void* projectState, char* elementType, char* elementJSONbuffer);

/** @brief Used to check if a name is used in the project by an element type.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] elementType            This is the type of element. See @ref ELEMENT_TYPE_GROUP.
 *  @param[in] newElementName         This is the name of the element to test.
 *  @return -1= no state given, 1 = name is used, 0 = name is not used
 */
int cliCheckNewProjectElementName(void* projectState, char* elementType, char* newElementName);

/** @brief Used to get the values of an icon as a JSON string using its number.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @param[in] iconNumber             This is the number of the icon to get. It will be in the range 1 to number of icons.
 *  @param[in,out] iconJSONBuffer     This is a char buffer where the icon JSON string will be put.
 *  @param[in] iconJSONBufferSize     This is the size of the iconJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetIcon(void* projectState, char* iconType, int iconNumber, char* iconJSONbuffer, unsigned int iconJSONbufferSize);

/** @brief Used to get the number of icons of a type in a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @return The number of icons of the type specified. -1= if no project state given, -2= if icon type is invalid
 */
int   cpiGetNumberOfIcons(void* projectState, char* iconType);

/** @brief Used to get the default values of an icon as a JSON string.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @param[in,out] iconJSONBuffer     This is a char buffer where the icon JSON string will be put.
 *  @param[in] iconJSONBufferSize     This is the size of the iconJSONBuffer in bytes.
 *  @param[in] subIconType            This is the sub icon type which is only used to indicate the type of control to get. See @ref CONTROLS_TYPE_GROUP
 *  @return See @ref RETURN_GROUP for return values
 */
int cpiGetDefaultIcon(void* projectState, char* iconType, char* iconJSONbuffer, unsigned int iconJSONbufferSize, unsigned int subIconType);

/** @brief Used to delete an icon from a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @param[in] iconNumber             This is the number of the icon to get. It will be in the range 1 to number of icons.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiDeleteIcon(void* projectState, char* iconType, int iconNumber);

/** @brief Used to replace the values of an icon using its number.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @param[in] exisitngIconNumber     This is the number of the icon to replace.
 *  @param[in] iconJSONBuffer         This is a char buffer where the icon JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiReplaceIcon(void* projectState, char* iconType, int existingIconNumber, char* iconJSONbuffer);

/** @brief Used to add an icon of the type given.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] iconType               This is the type of icon. See @ref ICON_TYPE_GROUP.
 *  @param[in] iconJSONBuffer         This is a char buffer where the icon JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiAddIcon(void* projectState, char* iconType, char* iconJSONbuffer, unsigned int* icon_nr);

/** @brief Used to get the number of levels of a type in a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @return The number of levels of the type specified. -1= if no project state given
 */
int   cpiGetNumberOfLevels(void* projectState);

/** @brief Used to get the values of an level as a JSON string using its name.
 *
 *  @param[in] projectState         This is a pointer to a state for a project.
 *  @param[in] levelName            This is the name of the level to get.
 *  @param[in,out] levelJSONBuffer  This is a char buffer where the level JSON string will be put.
 *  @param[in] levelJSONBufferSize  This is the size of the levelJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetLevelByName(void* projectState, char* levelName, char* levelJSONbuffer, unsigned int levelJSONbufferSize);

/** @brief Used to get the values of a level as a JSON string using its number.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] levelNumber            This is the number of the level to get. It will be in the range 1 to number of levels.
 *  @param[in,out] levelJSONBuffer    This is a char buffer where the level JSON string will be put.
 *  @param[in] levelJSONBufferSize    This is the size of the levelJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetLevelByNumber(void* projectState, unsigned int levelNumber, char* levelJSONbuffer, unsigned int levelJSONbufferSize);

/** @brief Used to delete a level from a project.
 *
 *  @param[in] projectState This is a pointer to a state for a project.
 *  @param[in] levelName    This is the name of the level to delete.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiDeleteLevel(void* projectState, char* levelName);

/** @brief Used to add a level to the project.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] levelJSONBuffer        This is a char buffer where the level JSON string is passed in.
 *  @param[in] iconType               This is the number that the level should become starting with zero for the bottom level.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiAddLevel(void* projectState, char* levelJSONbuffer, unsigned int levelNumber);

/** @brief Used to replace the values of an level using its name.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in] oldLevelName           This is the name of the level to replace.
 *  @param[in] levelJSONBuffer        This is a char buffer where the level JSON string is passed in.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiReplaceLevel(void* projectState, char* oldLevelName, char* levelJSONbuffer);

/** @brief Used to get the default values of an level as a JSON string.
 *
 *  @param[in] projectState           This is a pointer to a state for a project.
 *  @param[in,out] levelJSONBuffer    This is a char buffer where the level JSON string will be put.
 *  @param[in] levelJSONBufferSize    This is the size of the levelJSONBuffer in bytes.
 *  @return See @ref RETURN_GROUP for return values
 */
int   cpiGetDefaultLevel(void* projectState, char* levelJSONbuffer, unsigned int levelJSONbufferSize);
#endif