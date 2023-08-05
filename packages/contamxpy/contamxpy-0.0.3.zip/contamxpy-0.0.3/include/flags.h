
// airflow node flags:
#define  VAR_P 0x0001   /* P varies */
#define NVAR_P 0xFFFE   /* flags & NVAR_P to clear the VAR_P flag */
#define  VAR_M 0x0002   /* Mf varies */
#define NVAR_M 0xFFFD   /* flags & NVAR_M to clear the VAR_M flag */
#define  VAR_T 0x0004   /* T varies */
#define NVAR_T 0xFFFB   /* flags & NVAR_T to clear the VAR_T flag */
#define  SYS_N 0x0008   /* AHS implicit node */
#define  UNCZN 0x0010   /* flags | UNCZN to set unconditioned space
                           flags & UNCZN to see if zone is unconditioned */
#define SETCZN 0xFFEF   /* flags & SETCZN to set conditioned zone */
#define  WMASS 0x0020   /* massive; V > 0 */
#define  NMASS 0xFFDF   /* flags & NMASS to clear the WMASS flag */
#define  F_DYN 0x0040   /* dynamic flow; cxs->dti > 0 */
#define  N_DYN 0xFFBF   /* flags & N_DYN to clear the F_DYN flag */
#define  F_PMD 0x0061   /* = VAR_P & WMASS & F_DYN */

#define  CFDZN 0x0020   /*Leon CFD Zone for checking if a ZONE_DSC is a CFD zone, not used for af_node */
#define FLAG_N 0x003F   /* P, M, T, S & U zone flag bits; used in PrjRead() */

// airflow path flags:
#define  WIND  0x0001   /* possible wind pressure */
#define  WPC_P 0x0002   /* this path uses WPC file pressure */
#define NWPC_P 0xFFFD     /* use to cancel WPC_P */
#define  WPC_C 0x0004   /* this path uses WPC file contaminants */
#define NWPC_C 0xFFFB     /* use to cancel WPC_C */
#define  WPC_F 0x0006   /* this path uses WPC pressure or contaminants */
#define  AHS_S 0x0008   /* system supply or return path */
#define  AHS_R 0x0010   /* recirculation flow path */
#define  AHS_O 0x0020   /* outside air flow path */
#define  AHS_X 0x0040   /* exhaust flow path */
#define  AHS_P 0x0078   /* any of the AHS paths */
#define  AHS_I 0x0070   /* implicit (R|O|X) AHS paths */
#define  LIM_P 0x0080   /* pressure limits */
#define  LIM_F 0x0100   /* flow limits */
#define  FAN_F 0x0200   /* constant flow fan path */
#define  JCT_L 0x0400   /* junction leak path; set in prjdata */
#define  N_DRV 0x0800   /* use numerical partial derivative, set in afesim */
#define FLAG_P 0x01FF   /* all path flag bits; used in PrjRead() */
