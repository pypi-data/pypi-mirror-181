/** @file element-api.h
 *  @brief contam library API.
 *  @author Brian J. Polidoro (NIST)
 *  @author W. Stuart Dols (NIST)
 *  @date 2022-10-20
 *
 *  Defines for element APIs
 */
#ifndef _ELEMENT_API_H_
#define _ELEMENT_API_H_

/**
 * @defgroup ELEMENT_TYPE_GROUP Types of elements
 *
 * @{
 */

 /** Species element type */
#define SPECIES_ELEMENT_TYPE "spc"
 /** Day Schedule element type */
#define DYSCH_ELEMENT_TYPE "dys"
 /** Contaminant Source/Sink element type */
#define CSE_ELEMENT_TYPE "cse"
 /**Filter element type */
#define FTE_ELEMENT_TYPE "fte"
 /** Path Airflow element type */
#define AFE_ELEMENT_TYPE "afe"
 /** Duct Airflow element type */
#define DFE_ELEMENT_TYPE "dfe"
 /** Week Schdeule element type */
#define WKSCH_ELEMENT_TYPE "wks"
 /** Wind Pressure Profile element type */
#define WPF_ELEMENT_TYPE "wpf"
 /** Kinetic Raction element type */
#define KNR_ELEMENT_TYPE "knr"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_TYPE_GROUP airflow element data types
 *
 * @{
 */

 /** Powerlaw Orifice */
#define PL_ORFC   0 
 /** Powerlaw Leak per item */
#define PL_LEAK1  1
 /** Powerlaw leak per unit length */
#define PL_LEAK2  2
 /** Powerlaw leak per unit area */
#define PL_LEAK3  3
 /** Powerlaw Connection (ASCOS) Data */
#define PL_CONN   4
 /** Powerlaw Q = C(dP)^n */
#define PL_QCN    5
 /** Powerlaw F = C(dP)^n */
#define PL_FCN    6
 /** Powerlaw Test Data (1-point) */
#define PL_TEST1  7
 /** Powerlaw Test Data (2-point) */
#define PL_TEST2  8
 /** Powerlaw Crack Description */
#define PL_CRACK  9
 /** Powerlaw Stairwell */
#define PL_STAIR 10
 /** Powerlaw Shaft */
#define PL_SHAFT 11
 /** Backdraft Damper Flow Q = C(dP)^n */
#define PL_BDQ   12
 /** Backdraft Damper Flow F = C(dP)^n */
#define PL_BDF   13
 /** Self-Regulating Vent */
#define SR_JWA   14   // Self Regulating - JW Axley  3.0a
 /** Quadratic dP = aQ + bQ^2 */
#define QF_QAB   15
 /** Quadratic dP = aF + bF^2 */
#define QF_FAB   16
 /** Quadratic Crack Description */
#define QF_CRACK 17
 /** Quadratic Test Data (2-point) */
#define QF_TEST2 18
 /** Two-way One Opening */
#define DR_DOOR  19
 /** Two-way Two Opening */
#define DR_PL2   20
 /** Fan Constant Mass Flow */
#define FN_CMF   21
 /** Fan Constant Volume Flow */
#define FN_CVF   22
 /** Fan Performance Curve */
#define FN_FAN   23
 /** Cubic Spline Flow F vs P */
#define CS_FSP   24
 /** Cubic Spline Flow Q vs P */
#define CS_QSP   25
 /** Cubic Spline Flow P vs F */
#define CS_PSF   26
 /** Cubic Spline Flow P vs Q */
#define CS_PSQ   27
 /** Super Airflow element */
#define AF_SUP   28
 /** Duct  Darcy-Colebrook */
#define DD_DWC   29
 /** Duct Orifice */
#define DD_PLR   30
 /** Duct F = C(dP)^n */
#define DD_FCN   31
 /** Duct Q = C(dP)^n */
#define DD_QCN   32 
 /** Duct Fan Performance Curve */
#define DD_FAN   33
 /** Duct Fan Constant Mass Flow */
#define DD_CMF   34
 /** Duct Fan Constant Volume Flow */
#define DD_CVF   35
 /** Duct Backdraft Damper Flow Q = C(dP)^n */
#define DD_BDQ   36
 /** Duct Backdraft Damper Flow F = C(dP)^n */
#define DD_BDF   37
 /** Duct Cubic Spline Flow F vs P */
#define DD_FSP   38
 /** Duct Cubic Spline Flow Q vs P */
#define DD_QSP   39
 /** Duct Cubic Spline Flow P vs F */
#define DD_PSF   40
 /** Duct Cubic Spline Flow P vs Q */
#define DD_PSQ   41

 /** @} */

/**
 * @defgroup SRC_SINK_ELEMENT_TYPE_GROUP S/S Element types
 *
 * @{
 */

 /** Constant Coefficient */
#define CS_CCF   0
 /** Pressure Driven */
#define CS_PRS   1
 /** Cutoff Concentration */
#define CS_CUT   2
 /** Decaying Source */
#define CS_EDS   3
 /** Boundary Layer Diffusion Controlled */
#define CS_BLS   4
 /** Burst Source */
#define CS_BRS   5    /* 1999/03/20 */
 /** Deposition Velocity */
#define CS_DVS   6
 /** Deposition Rate */
#define CS_DRS   7    /* 2004/06/03 */
 /** Deposition with Resuspension */
#define CS_DVR   8    /* 2009/04/01 */
 /** Super Source/Sink */
#define CS_SUP   9    /* 2006/03/30 */
 /** NRCC Power Law */
#define CS_PLM  10
 /** NRCC Peak */
#define CS_PKM  11
 /** SXD */
#define CS_SXD  12    /* 2005/09/23 No CW interface yet */
 /** DXD */
#define CS_DXD  13

 /** @} */

/**
 * @defgroup FILTER_ELEMENT_TYPE_GROUP filter element data types
 *
 * @{
 */

 /** Constant Efficiency Filtration */
#define FL_CEF   0
 /** Simple Particle Filtration */
#define FL_PF0   1
 /** Simple Gaseous Filtration */
#define FL_GF0   2
 /** Penn State UVGI */
#define FL_UV1   3
 /** Super Element */
#define FL_SPF   4

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_GROUP airflow and ductflow element data fields
 *
 * @{
 */

 /** element name */
#define AFE_NAME_STR "name"
 /**  */
#define AFE_DESC_STR "desc"
 /** element description */
#define AFE_DTYPE_SHT "dtype"
 /** element icon */
#define AFE_ICON_BYT "icon"
 /** element used - output only */
#define AFE_USED_SHT "used"
 /** element number - output only */
#define AFE_NR_INT "nr"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_ORFC_GROUP orifice element data fields
 *
 * @{
 */

 /** Flow Exponent */
#define AFE_ORFC_EXPT_FLT "expt"
 /** Cross-sectional Area */
#define AFE_ORFC_AREA_FLT "area"
 /** Hydraulic Diameter */
#define AFE_ORFC_DIA_FLT "dia"
 /** Discharge Coefficient */
#define AFE_ORFC_COEF_FLT "coef"
 /** Reynolds Number */
#define AFE_ORFC_RE_FLT "Re"
 /** area units */
#define AFE_ORFC_U_A_SHT "u_A"
 /** length units for diameter */
#define AFE_ORFC_U_D_SHT "u_D"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_LEAK_GROUP leakage element data fields
 *
 * @{
 */

 /** Flow Exponent */
#define AFE_LEAK_EXPT_FLT "expt"
 /** Discharge Coefficient */
#define AFE_LEAK_COEF_FLT "coef"
 /** Pressure Difference */
#define AFE_LEAK_PRES_FLT "pres"
 /** area per item */
#define AFE_LEAK_A1_FLT "area1"
 /** area per unit length */
#define AFE_LEAK_A2_FLT "area2"
 /** area per unit area */
#define AFE_LEAK_A3_FLT "area3"
 /** area units per item */
#define AFE_LEAK_U_A1_SHT "u_A1"
 /** area units per unit length */
#define AFE_LEAK_U_A2_SHT "u_A2"
 /** area units per area */
#define AFE_LEAK_U_A3_SHT "u_A3"
 /** pressure difference units */
#define AFE_LEAK_U_DP_SHT "u_dP"

 /** @} */

 /**
 * @defgroup AIRFLOW_ELEMENT_CONN_GROUP Connection element data fields
 *
 * @{
 */

 /** Flow Area */
#define AFE_CONN_AREA_FLT "area"
 /** Flow Coefficent */
#define AFE_CONN_COEF_FLT "coef"
 /** Area units */
#define AFE_CONN_U_A_SHT "u_A"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_CRACK_GROUP crack element data fields
 *
 * @{
 */

 /** Crack Length */
#define AFE_CRACK_LEN_FLT "length"
 /** Crack Width */
#define AFE_CRACK_WIDTH_FLT "width"
 /** Length Units */
#define AFE_CRACK_U_L_SHT "u_L"
 /** Width Units */
#define AFE_CRACK_U_W_SHT "u_W"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_TEST1_GROUP test 1 point element data fields
 *
 * @{
 */
 
 /** Flow Exponent */
#define AFE_TEST1_EXPT_FLT "expt"
 /** Pressure Difference */
#define AFE_TEST1_DP_FLT "dP"
 /** Flow Rate */
#define AFE_TEST1_FLOW_FLT "Flow"
 /** Pressure Units */
#define AFE_TEST1_U_P_SHT "u_P"
 /** Flow Units */
#define AFE_TEST1_U_F_SHT "u_F"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_TEST2_GROUP test 2 point element data fields
 *
 * @{
 */

 /** Pressure Drop 1 */
#define AFE_TEST2_DP1_FLT "dP1"
 /** Flow Rate 1 */
#define AFE_TEST2_F1_FLT "F1"
 /** Pressure Drop 2 */
#define AFE_TEST2_DP2_FLT "dP2"
 /** Flow Rate 2 */
#define AFE_TEST2_F2_FLT "F2"
 /** Pressure Units 1 */
#define AFE_TEST2_U_P1_SHT "u_P1"
 /** Flow Units 1 */
#define AFE_TEST2_U_F1_SHT "u_F1"
 /** Pressure Units 2 */
#define AFE_TEST2_U_P2_SHT "u_P2"
 /** Flow Units 2 */
#define AFE_TEST2_U_F2_SHT "u_F2"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_STAIR_GROUP Strairwell element data fields
 *
 * @{
 */

 /** Distance between Levels */
#define AFE_STAIR_HT_FLT "Ht"
 /** Cross-secionyal Area */
#define AFE_STAIR_AREA_FLT "area"
 /** Density of People */
#define AFE_STAIR_PEO_FLT "peo"
 /** Stair Tread - 0 = Open, 1 = Closed */
#define AFE_STAIR_TREAD_SHT "tread"
 /** Area Units */
#define AFE_STAIR_U_A_SHT "u_A"
 /** Length Units for distance */
#define AFE_STAIR_U_D_SHT "u_D"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_SHAFT_GROUP shaft element data fields
 *
 * @{
 */

 /** Distance between Levels */
#define AFE_SHAFT_HT_FLT "Ht"
 /** Cross-sectional Area */
#define AFE_SHAFT_AREA_FLT "area"
 /** Perimeter */
#define AFE_SHAFT_PERIM_FLT "perim"
 /** Roughness */
#define AFE_SHAFT_ROUGH_FLT "rough"
 /** Area Units */
#define AFE_SHAFT_U_A_SHT "u_A"
 /** Length Units for distance */
#define AFE_SHAFT_U_D_SHT "u_D"
 /** Length Units for perimeter */
#define AFE_SHAFT_U_P_SHT "u_P"
 /** Length Units for roughness */
#define AFE_SHAFT_U_R_SHT "u_R"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_QCN_GROUP QCN element data fields
 *
 * @{
 */

 /** Flow Coeffient */
#define AFE_QCN_TURB_FLT "turb"
 /** Flow Exponent */
#define AFE_QCN_EXPT_FLT "expt"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_FCN_GROUP FCN element data fields
 *
 * @{
 */

 /** Flow Coefficient */
#define AFE_FCN_TURB_FLT "turb"
 /** Flow Exponent */
#define AFE_FCN_EXPT_FLT "expt"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_QAB_GROUP QAB element data fields
 *
 * @{
 */

 /** Coefficient a */
#define AFE_QAB_A_FLT "a"
 /**  Coefficient b*/
#define AFE_QAB_B_FLT "b"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_CRACK_GROUP crack element data fields
 *
 * @{
 */

 /** Coefficient a */
#define AFE_FAB_A_FLT "a"
 /** Coefficient b */
#define AFE_FAB_B_FLT "b"

 /** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_QCR_GROUP QF crack element data fields
 *
 * @{
 */

 /** Crack Length */
#define AFE_QCR_LEN_FLT "length"
 /** Crack Width */
#define AFE_QCR_WIDTH_FLT "width"
 /** Crack Depth */
#define AFE_QCR_DEPTH_FLT "depth"
 /** Number of Bends */
#define AFE_QCR_NB_SHT "nB"
 /** Length Units */
#define AFE_QCR_U_L_SHT "u_L"
 /** Length Units for width */
#define AFE_QCR_U_W_SHT "u_W"
 /** Length Units for depth */
#define AFE_QCR_U_D_SHT "u_D"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_QFT2_GROUP QF Test 2 element data fields
 *
 * @{
 */

 /** Pressure Drop 1 */
#define AFE_QT2_DP1_FLT "dP1"
 /** Flow Rate 1 */
#define AFE_QT2_F1_FLT "F1"
 /** Pressure Drop 2 */
#define AFE_QT2_DP2_FLT "dP2"
 /** Flow Rate 2 */
#define AFE_QT2_F2_FLT "F2"
 /** Pressure Diff Units */
#define AFE_QT2_U_P1_SHT "u_P1"
 /** Flow Units */
#define AFE_QT2_U_F1_SHT "u_F1"
 /** Pressure Diff Units 2 */
#define AFE_QT2_U_P2_SHT "u_P2"
 /** Flow Rate Units 2 */
#define AFE_QT2_U_F2_SHT "u_F2"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DOOR_GROUP Door element data fields
 *
 * @{
 */

 /** Height */
#define AFE_DOOR_HT_FLT "Ht"
 /** Width */
#define AFE_DOOR_WD_FLT "wd"
 /** Discharge Coeficient */
#define AFE_DOOR_CD_FLT "cd"
 /** Length Units for height */
#define AFE_DOOR_U_H_SHT "u_H"
 /** Length Units for width */
#define AFE_DOOR_U_W_SHT "u_W"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DPL_GROUP Door Two Opening element data fields
 *
 * @{
 */

 /** Height */
#define AFE_DPL_HT_FLT "Ht"
 /** Width */
#define AFE_DPL_WD_FLT "wd"
 /** Discharge Coefficient */
#define AFE_DPL_CD_FLT "cd"
 /** Length Units for height */
#define AFE_DPL_U_H_SHT "u_H"
 /**  Length Units for width */
#define AFE_DPL_U_W_SHT "u_W"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_BDQ_GROUP BDQ element data fields
 *
 * @{
 */

 /** Flow Coefficient - dP > 0 */
#define AFE_BDQ_CP_FLT "Cp"
 /** Flow Exponent - dP > 0 */
#define AFE_BDQ_XP_FLT "xp"
 /** Flow Coefficient - dP < 0 */
#define AFE_BDQ_CN_FLT "Cn"
 /** Floe Exponent - dP < 0 */
#define AFE_BDQ_XN_FLT "xn"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_BDF_GROUP BDF element data fields
 *
 * @{
 */

 /** Flow Coefficient - dP > 0 */
#define AFE_BDF_CP_FLT "Cp"
 /** Flow Exponent - dP > 0 */
#define AFE_BDF_XP_FLT "xp"
 /** Flow Coefficient - dP < 0 */
#define AFE_BDF_CN_FLT "Cn"
 /** Flow Exponent - dP < 0 */
#define AFE_BDF_XN_FLT "xn"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_SRJWA_GROUP SR JWA element data fields
 *
 * @{
 */

 /** Max Flow Rate */
#define AFE_SR_F0_FLT "F0"
 /** Regulating Pressure */
#define AFE_SR_P0_FLT "P0"
 /** Reverse Flow Fraction */
#define AFE_SR_F_FLT "f"
 /** Flow Rate Units */
#define AFE_SR_U_F0 "u_F0"
 /** Pressure Units */
#define AFE_SR_U_P0 "u_P0"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_CMF_GROUP Constant Mass Fan element data fields
 *
 * @{
 */

 /** Flow Rate */
#define AFE_CMF_FLOW_FLT "Flow"
 /** Flow Rate Units */
#define AFE_CMF_U_F_SHT "u_F"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_CVF_GROUP Constant Volume Fan element data fields
 *
 * @{
 */

 /** Volume Flow Rate */
#define AFE_CVF_FLOW_FLT "Flow"
 /** Volume Flo Rate Units */
#define AFE_CVF_U_F_SHT "u_F"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_PFAN_GROUP Performance Fan Curve element data fields
 *
 * @{
 */

 /** Cutt-off Ratio */
#define AFE_FAN_OFF_FLT "off"
 /** Equivalent Orifice Area */
#define AFE_FAN_SAREA_FLT "Sarea"
 /** Area Units */
#define AFE_FAN_U_SA_SHT "u_Sa"
 /** Curve Data Point Array */
#define AFE_FAN_CDATA_ARR "cdata"
 /** Data Point Flow Rate */
#define AFE_FAN_PT_MF_FLT "mF"
 /** Data Point Pressure Rise */
#define AFE_FAN_PT_DP_FLT "dP"
 /** Data Point Revised dP */
#define AFE_FAN_PT_RP_FLT "rP"
 /** Flow Rate Units */
#define AFE_FAN_PT_U_MF_SHT "u_mF"
 /** Pressure Units for Pressure Rise */
#define AFE_FAN_PT_U_DP_SHT "u_dP"
 /** Pressure Units for Revised dP */
#define AFE_FAN_PT_U_RP_SHT "u_rP"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_CSF_GROUP Cubis Spline Flow element data fields
 *
 * @{
 */

 /** Length Units for X */
#define AFE_CSF_U_X_SHT "u_X"
 /** Length Units for Y */
#define AFE_CSF_U_Y_SHT "u_Y"
 /** XY data point array */
#define AFE_CSF_YXDATA_ARR "xydata"
 /** Data Point X */
#define AFE_CSF_PT_X_FLT "X"
 /** Data Point Y */
#define AFE_CSF_PT_Y_FLT "Y"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_SUPER_GROUP Super element data fields
 *
 * @{
 */

 /** Length Units for height */
#define AFE_SUP_U_HT_SHT "u_Ht"
 /** Array of sub-element data */
#define AFE_SUP_LIST_ARR "list"
 /** Data Point - Sub-element name */
#define AFE_SUP_PT_ELM_STR "element"
 /** Data Point - Sub-element Relative Height */
#define AFE_SUP_PT_RELHT_FLT "relHt"
 /** Data Point - Sub-element Is Filtered */
#define AFE_SUP_PT_FILT_SHT "Filtered"
 /** Data Point - Sub-element Schedule Name */
#define AFE_SUP_PT_SCHED_SHT "Sched"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DWC_GROUP Duct DWC element data fields
 *
 * @{
 */

 /** Roughness */
#define DFE_DWC_ROUGH_FLT "rough"
 /** Length Units for roughness */
#define DFE_DWC_U_R_SHT "u_R"

/** @} */
/**
 * @defgroup AIRFLOW_ELEMENT_DPL_GROUP DPLR element data fields
 *
 * @{
 */

 /** Flow Exponent */
#define DFE_PL_EXPT_FLT "expt"
 /** Cross-sectional Area */
#define DFE_PL_AREA_FLT "area"
 /** Hydraulic Diameter */
#define DFE_PL_DIA_FLT "dia"
 /** Discharge Coefficient */
#define DFE_PL_COEF_FLT "coef"
 /** Are Units */
#define DFE_PL_U_A_SHT "u_A"
 /** Length Units for diameter */
#define DFE_PL_U_D_SHT "u_D"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DFCN_GROUP Duct FCN element data fields
 *
 * @{
 */

 /** Flow Coefficient */
#define DFE_FCN_TURB_FLT "turb"
 /** Flow Exponent */
#define DFE_FCN_EXPT_FLT "expt"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DQCN_GROUP Duct QCN element data fields
 *
 * @{
 */

 /** Flow Coefficent */
#define DFE_QCN_TURB_FLT "turb"
 /** Flow Exponent */
#define DFE_QCN_EXPT_FLT "expt"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DPFAN_GROUP Duct Perf Fan Curve element data fields
 *
 * @{
 */

 /** Cutt-off Ratio */
#define DFE_FAN_OFF_FLT "off"
 /** Equivalent Orifice Area */
#define DFE_FAN_SAREA_FLT "Sarea"
 /** Area Units */
#define DFE_FAN_U_SA_SHT "u_Sa"
 /** Curve Data Point Array */
#define DFE_FAN_CDATA_ARR "cdata"
 /** Data Point - Flow Rate */
#define DFE_FAN_PT_MF_FLT "mF"
 /** Data Point - Presure Rise */
#define DFE_FAN_PT_DP_FLT "dP"
 /**  Data Point - Revised dP */
#define DFE_FAN_PT_RP_FLT "rP"
 /** Flow Rate Units */
#define DFE_FAN_PT_U_MF_SHT "u_mF"
 /** Pressure Units for Pressure Rise */
#define DFE_FAN_PT_U_DP_SHT "u_dP"
 /** Pressure Units for Rvised dP */
#define DFE_FAN_PT_U_RP_SHT "u_rP"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DCMF_GROUP Duct Constant Mass Fan element data fields
 *
 * @{
 */

 /** Flow Rate */
#define DFE_CMF_FLOW_FLT "Flow"
 /** Flow Rate units */
#define DFE_CMF_U_F_SHT "u_F"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DCVF_GROUP Duct Constant Volume Fan element data fields
 *
 * @{
 */

 /** Flow Rate */
#define DFE_CVF_FLOW_FLT "Flow"
 /** Flow Rate units */
#define DFE_CVF_U_F_SHT "u_F"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DBDQ_GROUP Duct BDQ element data fields
 *
 * @{
 */

 /** Flow Coefficient - dP > 0 */
#define DFE_BDQ_CP_FLT "Cp"
 /** Flow Exponent - dP > 0 */
#define DFE_BDQ_XP_FLT "xp"
 /** Flow Coefficient - dP < 0 */
#define DFE_BDQ_CN_FLT "Cn"
 /** Flow Exponent - dP < 0 */
#define DFE_BDQ_XN_FLT "xn"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DBDF_GROUP Duct BDF element data fields
 *
 * @{
 */

 /** Flow Coefficient - dP > 0 */
#define DFE_BDF_CP_FLT "Cp"
 /** Flow Exponent - dP > 0 */
#define DFE_BDF_XP_FLT "xp"
 /** Flow Coefficient - dP < 0 */
#define DFE_BDF_CN_FLT "Cn"
 /** Flow Exponent - dP < 0 */
#define DFE_BDF_XN_FLT "xn"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DCSF_GROUP Duct Cubis Spline Flow element data fields
 *
 * @{
 */

 /** Length Units for X */
#define DFE_CSF_U_X_SHT "u_X"
 /** Length Units for Y */
#define DFE_CSF_U_Y_SHT "u_Y"
 /** XY data point array */
#define DFE_CSF_YXDATA_ARR "xydata"
 /** X */
#define DFE_CSF_PT_X_FLT "X"
 /** Y */
#define DFE_CSF_PT_Y_FLT "Y"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DCT_GROUP duct element data fields
 *
 * @{
 */

 /** Diameter */
#define DFE_HDIA_FLT "hdia"
 /** Perimeter */
#define DFE_PERIM_FLT "perim"
 /** Cross-sectional Area */
#define DFE_AREA_FLT "area"
 /** Major Dimension */
#define DFE_MAJOR_FLT "major"
 /** Minor Dimension */
#define DFE_MINOR_FLT "minor"
 /** Surface Area */
#define DFE_AS_FLT "As"
 /** Leakage Rate */
#define DFE_QR_FLT "Qr"
 /** Pressure Difference */
#define DFE_PR_FLT "Pr"
 /** Duct Shape - See AIRFLOW_ELEMENT_DFE_SHAPE_GROUP */
#define DFE_SHAPE_SHT "shape"
 /** Length Units for diameter */
#define DFE_U_D_SHT "u_D"
 /** Length Units for perimeter */
#define DFE_U_P_SHT "u_P"
 /** Area Units */
#define DFE_U_A_SHT "u_A"
 /** Length Units for major dimension */
#define DFE_U_MJ_SHT "u_mj"
 /** Length Units fir minor dimension */
#define DFE_U_MN_SHT "u_mn"
 /** Units for Leakage Rate - 0= SI, 1= IP */
#define DFE_U_QR_SHT "u_Qr"
 /** Units for Pressure Difference - 0= SI, 1= IP */
#define DFE_U_PR_SHT "u_Pr"

/** @} */

/**
 * @defgroup AIRFLOW_ELEMENT_DFE_SHAPE_GROUP Duct element shape options
 *
 * @{
 */

 /** Circular Duct */
#define DFE_SHAPE_CIR 0
 /** Rectangular Duct */
#define DFE_SHAPE_RECT 1
 /** Oval Duct */
#define DFE_SHAPE_OVAL 2
 /** Other Shaoed Duct */
#define DFE_SHAPE_OTHER 3

/** @} */

/**
 * @defgroup DAY_SCHEDULE_GROUP Day Schedule data fields
 *
 * @{
 */

 /** Name */
#define DSH_NAME_STR "name"
 /** Decription */
#define DSH_DESC_STR "desc"
 /** Shape - See DAY_SCHEDULE_SHAPE_GROUP */
#define DSH_SHAPE_SHT "shape"
 /** Unit Conversion */
#define DSH_UCNV_SHT "ucnv"
 /** Unit Type - NOUNITS, TEMPERATURE */
#define DSH_UTYP_SHT "utyp"
 /** data points array */
#define DSH_POINTS_ARR "points"
 /** data point - time (secs) */
#define DSH_PT_TIME_INT "time"
 /** data point - control value */
#define DSH_PT_CTRL_FLT "ctrl"

/** @} */

/**
 * @defgroup DAY_SCHEDULE_SHAPE_GROUP Day Schedule shape options
 *
 * @{
 */

 /** Rectangular */
#define DSH_SHAPE_RECT_SHT 0
 /** Trapezoidal */
#define DSH_SHAPE_TRAP_SHT 1

/** @} */

/**
 * @defgroup WEEK_SCHEDULE_GROUP Week Schedule data fields
 *
 * @{
 */

 /** Name */
#define WSH_NAME_STR "name"
 /** Description */
#define WSH_DESC_STR "desc"
 /** Unit Conversion */
#define WSH_UCNV_SHT "ucnv"
 /** Unit Type - NOUNITS, TEMPERATURE */
#define WSH_UTYP_SHT "utyp"
 /** Day Schedule array - size=12 */
#define WSH_DSH_ARR "dss"

/** @} */

/**
 * @defgroup SPECIES_GROUP Species data fields
 *
 * @{
 */

 /** Name */
#define SPCS_NAME_STR "name"
 /** Default Concentration */
#define SPCS_CCDEF_FLT "ccdef"
 /** Specific Heat */
#define SPCS_CP_FLT "Cp"
 /** Decay Rate */
#define SPCS_DECAY_FLT "decay"
 /** Description */
#define SPCS_DESC_STR "desc"
 /** Diffusion Coefficient */
#define SPCS_DM_FLT "Dm"
 /** Effective Density */
#define SPCS_EDENS_FLT "edens"
 /** UVGI Susceptibility Constant */
#define SPCS_KUV_FLT "Kuv"
 /** Mean Diameter */
#define SPCS_MDIAM_FLT "mdiam"
 /** Molar Mass */
#define SPCS_MOLWT_FLT "molwt"
 /** Non-trace Flag - 0= False, 1 = True */
#define SPCS_NT_SHT "ntflag"
 /** Simulate Flag - 0= False, 1 = True */
#define SPCS_SIM_SHT "sflag"
 /** Concentration Units */
#define SPCS_U_CC_SHT "ucc"
 /** Specifc Heat Units */
#define SPCS_U_CP_SHT "ucp"
 /** Diffusion Coefficient Units */
#define SPCS_U_DM_SHT "udm"
 /** Effective Density Units */
#define SPCS_U_ED_SHT "ued"
 /** Length Units for Mean Diameter */
#define SPCS_U_MD_SHT "umd"

/** @} */

/**
 * @defgroup SOURCE_SINK_ELEMENT_GROUP Source/Sink element data fields
 *
 * @{
 */

 /** Name */
#define CSE_NAME_STR "name"
 /** Description */
#define CSE_DESC_STR "desc"
 /** Species Name */
#define CSE_SPCS_STR "spcs"
 /** Element Type - ee SRC_SINK_ELEMENT_TYPE_GROUP */
#define CSE_CTYPE_SHT "ctype"

/** @} */

/**
 * @defgroup CSE_CCF_ELEMENT_GROUP Constant Coefficient element data fields
 *
 * @{
 */

 /** Generation Rate */
#define CSE_CCF_G_FLT "G"
 /** Removal Rate */
#define CSE_CCF_D_FLT "D"
 /** CONSS Units */
#define CSE_CCF_U_G_SHT "u_G"
 /** DEP_FLOW Units */
#define CSE_CCF_U_D_SHT "u_D"

/** @} */

/**
 * @defgroup CSE_PRS_ELEMENT_GROUP Presure driven element data fields
 *
 * @{
 */

 /** Generation Rate */
#define CSE_PRS_G_FLT "G"
 /** Pressure Exponent */
#define CSE_PRS_X_FLT "x"
 /** CONSS Units */
#define CSE_PRS_U_G_SHT "u_G"
 
/** @} */

/**
 * @defgroup CSE_CUT_ELEMENT_GROUP Cutoff Concentration element data fields
 *
 * @{
 */
 
 /** Generation Rate */
#define CSE_CUT_G_FLT "G"
 /** Cutoff Concentration */
#define CSE_CUT_CO_FLT "Co"
 /** CONSS Units */
#define CSE_CUT_U_G_SHT "u_G"
 /** Concentraion Units */
#define CSE_CUT_U_C_SHT "u_C"

/** @} */

/**
 * @defgroup CSE_EDS_ELEMENT_GROUP Decaying source element data fields
 *
 * @{
 */

 /**Initial Emmision Rate  */
#define CSE_EDS_G0_FLT "G0"
 /** Decay Constant */
#define CSE_EDS_K_FLT "k"
 /** CONSS Units */
#define CSE_EDS_U_G_SHT "u_G"
 /** Time Constant Units */
#define CSE_EDS_U_K_SHT "u_k"

/** @} */

/**
 * @defgroup CSE_BLS_ELEMENT_GROUP Boundary Layer element data fields
 *
 * @{
 */

 /** Film Transfer Coefficient */
#define CSE_BLS_HM_FLT "hm"
 /** Partition Coefficient */
#define CSE_BLS_KP_FLT "Kp"
 /** Surface Mass */
#define CSE_BLS_M_FLT "M"
 /** Film Density of Air */
#define CSE_BLS_RHO_FLT "rho"
 /** Speed Units for Film Transfer */
#define CSE_BLS_U_H_SHT "u_h"
 /** Mass Units */
#define CSE_BLS_U_M_SHT "u_M"
 /** Density Units */
#define CSE_BLS_U_R_SHT "u_r"

/** @} */

/**
 * @defgroup CSE_BRS_ELEMENT_GROUP Burst element data fields
 *
 * @{
 */

 /** Mass Added */
#define CSE_BRS_M_FLT "M"
 /** Mass Units */
#define CSE_BRS_U_M_SHT "u_M"

/** @} */

/**
 * @defgroup CSE_DVS_ELEMENT_GROUP Deposition Velocity element data fields
 *
 * @{
 */

 /** Deposition Surface Area */
#define CSE_DVS_DA_FLT "dA"
 /** Deposition Velocity */
#define CSE_DVS_DV_FLT "dV"
 /** Area Units */
#define CSE_DVS_U_A_SHT "u_A"
 /** Speed Units */
#define CSE_DVS_U_V_SHT "u_V"
 
/** @} */

/**
 * @defgroup CSE_DRS_ELEMENT_GROUP Deposition Rate element data fields
 *
 * @{
 */

  /** Depostion Rate */
#define CSE_DRS_KD_FLT "kd"
 /** Time Constant Units */
#define CSE_DRS_U_K_SHT "u_k"

/** @} */

/**
 * @defgroup CSE_DVR_ELEMENT_GROUP Deposition with Resuspension element data fields
 *
 * @{
 */

 /** Deposition Surface Area */
#define CSE_DVR_DA_FLT "dA"
 /** Deposition Velocity */
#define CSE_DVR_DV_FLT "dV"
 /** Resuspension Rate */
#define CSE_DVR_R_FLT "R"
 /** Resuspension Area */
#define CSE_DVR_RA_FLT "rA"
 /** Area Units for Deposition */
#define CSE_DVR_U_DA_SHT "u_dA"
 /** Time Constant Units for Resuspension */
#define CSE_DVR_U_R_SHT "u_R"
 /** Area Units for Resuspension */
#define CSE_DVR_U_RA_SHT "u_RA"
 /** Speed Units for Deposition Velocity */
#define CSE_DVR_U_V_SHT "u_V"
 
/** @} */

/**
 * @defgroup CSE_SUP_ELEMENT_GROUP Super S/S element data fields
 *
 * @{
 */

 /** Array of Sub-Element Names */
#define CSE_SUP_SS_ARR "ss"

/** @} */

/**
 * @defgroup CSE_PLM_ELEMENT_GROUP Powerlaw element data fields
 *
 * @{
 */

 /** Initial Emission Factor */
#define CSE_PLM_A_FLT "a"
 /** Exponent */
#define CSE_PLM_B_FLT "b"
 /** PL MOdel Time */
#define CSE_PLM_TP_FLT "tp"
 /** CONSS Units */
#define CSE_PLM_U_A_SHT "u_a"
 /** Time Units */
#define CSE_PLM_U_TP_SHT "u_tp"

/** @} */

/**
 * @defgroup CSE_PKM_ELEMENT_GROUP Peak element data fields
 *
 * @{
 */

 /** Peak Emission Rate */
#define CSE_PKM_A_FLT "a"
 /** Fititng  Parameter */
#define CSE_PKM_B_FLT "b"
 /** Time of Peak */
#define CSE_PKM_TP_FLT "tp"
 /** CONSS Units */
#define CSE_PKM_U_A_SHT "u_a"
 /** Time Units */
#define CSE_PKM_U_TP_SHT "u_tp"

/** @} */

/**
 * @defgroup WPF_GROUP Wind Pressure Profile data fields
 *
 * @{
 */

 /** Name */
#define WPF_NAME_STR "name"
 /** Description */
#define WPF_DESC_STR "desc"
 /** Profile Type - See WPF_TYPE_GROUP */
#define WPF_TYPE_SHT "type"
 /** data points array */
#define WPF_ADATA_ARR "adata"
 /** data point - Azimuth Angle */
#define WPF_PT_AZM_FLT "azm"
 /** data point - Coefficient */
#define WPF_PT_COEF_FLT "coef"
 /** Is Element Used - output only */
#define WPF_USED_SHT "used"

/** @} */

/**
 * @defgroup WPF_TYPE_GROUP Wind pressure profile type options
 *
 * @{
 */

 /** Linear Profile */
#define WPF_TYPE_LINEAR 1
 /** Cubic Spline Fit Profile */
#define WPF_TYPE_CSF 2
 /** Trigonometric Profile */
#define WPF_TYPE_TRIG 3

/** @} */

/**
 * @defgroup KNR_GROUP crack element data fields
 *
 * @{
 */

 /** Name */
#define KNR_NAME_STR "name"
 /** Description */
#define KNR_DESC_STR "desc"
 /** Is KNR Used - output only */
#define KNR_USED_SHT "used"
 /** reaction data array */
#define KNR_KRD_ARR "krd"
 /** data point - Coefficient */
#define KNR_PT_COEF_FLT "coef"
 /** data point - product species name */
#define KNR_PT_PROD_STR "product"
 /** data point - source species name */
#define KNR_PT_SRC_STR "source"

/** @} */

/**
 * @defgroup FILTER_ELEMENT_GROUP Filter element data fields
 *
 * @{
 */

 /** Area */
#define FTE_AREA_FLT "area"
 /** Density */
#define FTE_DENS_FLT "dens"
 /** Depth */
#define FTE_DEPTH_FLT "depth"
 /** Filter Type - See FILTER_ELEMENT_TYPE_GROUP */
#define FTE_FTYPE_SHT "ftype"
 /** Name */
#define FTE_NAME_STR "name"
 /** Description */
#define FTE_DESC_STR "desc"
 /** Is Filter Element Used - output only */
#define FTE_USED_SHT "used"
 /** Area and Length Units */
#define FTE_U_AL_SHT "u_al"
 /** Density Units */
#define FTE_U_D_SHT "u_D"

/** @} */

/**
 * @defgroup FTE_CEF_ELEMENT_GROUP Constant Efficieny filter element data fields
 *
 * @{
 */

 /** efficiency array */
#define FTE_CEF_EFFS_ARR "effs"
 /** data point - Species Anme */
#define FTE_CEF_PT_SPCS "spcs"
 /** data point - efficiency */
#define FTE_CEF_PT_EFF "eff"

/** @} */

/**
 * @defgroup FTE_PF0_ELEMENT_GROUP Simple Particle filter element data fields
 *
 * @{
 */

 /** Length Units for particle size */
#define FTE_PF0_U_SZ_SHT "usz"
 /** efficiency array */
#define FTE_PF0_EFFS_ARR "effs"
 /** data point - particle size */
#define FTE_PF0_PT_SZ_FLT "size"
 /** data point - filter efficiency */
#define FTE_PF0_PT_EF_FLT "eff"

/** @} */

/**
 * @defgroup FTE_GF0_ELEMENT_GROUP Simple gaseous filter element data fields
 *
 * @{
 */

 /** filter data array */
#define FTE_GF0_FDATA_ARR "fdata"
 /** data point - species name */
#define FTE_GF0_PT_SPCS_STR "spcs"
 /** data point - breathru efficiency */
#define FTE_GF0_PT_BTHRU_FLT "bthru"
 /** data point - efficiency array */
#define FTE_GF0_PT_EFFS_ARR "effs"
 /** sub data point - particle loading */
#define FTE_GF0_PT_EFFS_PT_LD_FLT "load"
 /** sub data point - particle filter efficiency */
#define FTE_GF0_PT_EFFS_PT_EFF_FLT "eff"

/** @} */

/**
 * @defgroup FTE_UV1_ELEMENT_GROUP Penn State UVGI filter element data fields
 *
 * @{
 */

 /** Design Survivability */
#define FTE_UV1_SDES_FLT "Sdes"
 /** Design Velocity */
#define FTE_UV1_UDES_FLT "Udes"
 /** Design Mass Flow Rate */
#define FTE_UV1_FDES_FLT "Fdes"
 /** Design Organism-Specific Rate Constant */
#define FTE_UV1_KDES_FLT "Kdes"
 /** Uses Age Model */
#define FTE_UV1_AGE_SHT "age"
 /** TU Constant C0 */
#define FTE_UV1_C0_FLT "C0"
 /** TU Constant C1 */
#define FTE_UV1_C1_FLT "C1"
 /** TU Constant C2 */
#define FTE_UV1_C2_FLT "C2"
 /** TU Constant C3 */
#define FTE_UV1_C3_FLT "C3"
 /** TU Constant C4 */
#define FTE_UV1_C4_FLT "C4"
 /** Age Constant K0 */
#define FTE_UV1_K0_FLT "K0"
 /** Age Constant K1 */
#define FTE_UV1_K1_FLT "K1"
 /** Flow Rate Units */
#define FTE_UV1_U_FDES_SHT "u_Fdes"
 /** Speed Units */
#define FTE_UV1_U_UDES_SHT "u_Udes"
 /** Area Units for Cross-sectional Flow Area */
#define FTE_UV1_U_ADES_SHT "u_Ades"

/** @} */

/**
 * @defgroup FTE_SUP_ELEMENT_GROUP Super Filter element data fields
 *
 * @{
 */

 /** Sub-Filter Element Name Array */
#define FTE_SUP_SF_ARR "sf"

/** @} */


#endif