
import string, sys, time, types, socket, re, os;
import ErrLog, select, time, EComponent, copy;
#import cx_Oracle, cx2Oracledb;
#from TrakConfig import *;

#CR51494
import operator;
from datetime import datetime;
from collections import OrderedDict;

SECS_PER_DAY = 24.0 * 60 * 60;

class MMTransactions_Jija:

    def createTrakLot_Jija(self,
        transUserId    = None,
        lotNumber      = None,
        lotQty         = None,
        masterProcess  = None,
        tgtDevcNumber  = None,
        tgtMatlOwner   = None,
        tgtCustSrc     = None,
        tgtBank        = None,
        srcDevcNumber  = None,
        srcMatlOwner   = None,
        srcCustSrc     = None,
        srcBank        = None,
        trakRouting    = None,
        trakOper       = None,
        stepName       = None,
        trakShift      = None,
        nextDevcNumber = None,
        pkgKit         = None,
        hostName       = None,
        maskSet        = None,
        traceCode      = None,
        topMark        = None,
        backMark       = None,
        waferLotNumber = None,
        activateLotFlag= None,
        trakLotClass   = None,
        validateLotFlag= None,
        bypassUsedEntitiesFlag = None,
        actualWlotNumber = None,
        npiStatus        = None,
        moveOvrdFlag     = None,
        dieSource        = None,
        rawstockPartNumber = None,
        isLotStartFromMWI = None,
        woNumber = None, 
        processSpec = None):
        
        """Parameters: transUserId, lotNumber, lotQty, masterProcess, tgtDevcNumber, tgtMatlOwner, tgtCustSrc, tgtBank, srcDevcNumber, srcMatlOwner, srcCustSrc, srcBank, trakRouting, trakOper, stepName, trakShift, nextDevcNumber, pkgKit, hostName, maskSet, traceCode, topMark, backMark, waferLotNumber, activateLotFlag, trakLotClass, validateLotFlag, bypassUsedEntitiesFlag, actualWlotNumber, npiStatus, moveOvrdFlag, dieSource, rawstockPartNumber,isLotStartFromMWI,woNumber,processSpec"""
        if not rawstockPartNumber:
            rawstockPartNumber  = None;
        if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
            self._validateRequiredArgs(
                srcBank    = srcBank); 
        #ENHC0011605 - ABI Project - Added rawstockPartNumber
        return self._createTrakLot_Jija("createTrakLot", transUserId, lotNumber, lotQty, masterProcess, tgtDevcNumber, tgtMatlOwner, tgtCustSrc, tgtBank, srcDevcNumber, srcMatlOwner, srcCustSrc, srcBank, trakRouting, trakOper, trakShift, nextDevcNumber, waferLotNumber, pkgKit, hostName, maskSet, traceCode, topMark, backMark, None, stepName, activateLotFlag, trakLotClass, validateLotFlag, bypassUsedEntitiesFlag, actualWlotNumber, npiStatus, moveOvrdFlag, dieSource,rawstockPartNumber,isLotStartFromMWI,woNumber,processSpec);



    def _createTrakLot_Jija(self, transType, transUserId, lotNumber, lotQty, masterProcess, tgtDevcNumber, tgtMatlOwner, tgtCustSrc, tgtBank, srcDevcNumber, srcMatlOwner, srcCustSrc, srcBank, trakRouting, trakOper, trakShift, nextDevcNumber = None, waferLotNumber = None, pkgKit = None, hostName= None, maskSet = None, traceCode = None, topMark = None, backMark = None, assyLoc = None, stepName = None, activateLotFlag = None, trakLotClass = None, validateLotFlag = None, bypassUsedEntitiesFlag = None, actualWlotNumber = None, npiStatus = None, moveOvrdFlag = None, dieSource = None, rawstockPartNumber = None, isLotStartFromMWI = None, woNumber = None, processSpec = None):

        tranLogSeq = 1;
        requireUpdateFFCode = 1; 
        self._validateRequiredArgs(
            transType     = transType,
            transUserId   = transUserId,
            lotQty        = lotQty,
            tgtDevcNumber = tgtDevcNumber);
        self._validateStringArgs(
            transType      = transType,
            transUserId    = transUserId,
            lotNumber      = lotNumber,
            masterProcess  = masterProcess,
            tgtDevcNumber  = tgtDevcNumber,
            tgtMatlOwner   = tgtMatlOwner,
            tgtCustSrc     = tgtCustSrc,
            tgtBank        = tgtBank,
            srcDevcNumber  = srcDevcNumber,
            srcMatlOwner   = srcMatlOwner,
            srcCustSrc     = srcCustSrc,
            srcBank        = srcBank,
            trakRouting    = trakRouting,
            trakOper       = trakOper,
            stepName       = stepName,
            trakShift      = trakShift,
            nextDevcNumber = nextDevcNumber,
            waferLotNumber = waferLotNumber,
            maskSet        = maskSet,
            traceCode      = traceCode,
            pkgKit         = pkgKit,
            topMark        = topMark,
            hostName       = hostName,
            assyLoc        = assyLoc,
            trakLotClass   = trakLotClass,
            actualWlotNumber = actualWlotNumber,
            dieSource        = dieSource);
        self._validateNumberArgs(1, 0, 1, 1,
            lotQty = lotQty);
        self._validateSequenceArgs(1, 1, 1, [], 0,
            backMark = backMark);
        self._validateYesArgs(
            bypassUsedEntitiesFlag = bypassUsedEntitiesFlag,
            activateLotFlag = activateLotFlag,
            validateLotFlag = validateLotFlag,
            moveOvrdFlag    = moveOvrdFlag);
        print ("_createTrakLot_Jija")
        #isLotStartFromMWI = "Y";
        toBank = None
        if stepName:
            self._validateStepName(1, ("stepName", stepName));

        if trakOper:
            self._validateTrakOper(1, ("trakOper", trakOper));

        if trakRouting:
            lenTrakRouting = len(trakRouting);
            if len(trakRouting) == 6:
                trakRouting = self.getLatestTrakRouting(trakRouting)[0][0];
            if lenTrakRouting == 9:
                self._checkTrakRouting(trakRouting);
            if lenTrakRouting <> 6 and lenTrakRouting <> 9:
                self._raiseError("Trak routing (:1) is invalid. Routing does not exists.",(trakRouting,)); 

        if npiStatus:
            self._validateNpiStatus(npiStatus);

        eventTime = self._sysdate();
        self._getUserTransLevel(transType, transUserId);
        #find parent bank for srcBank. do not do try except, becase srcBank will be validate in VB code.added by Chen Ming for CR53272
        if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
            if srcBank:
                parentBank = self._dbExecute("select PARENT_BANK_CC from BANKTABL where BANK = :1",(srcBank,))[0][0];        

        returnLotNumber, lotNumber, trakLotClass = self._validateLotGenerationRule(lotNumber, trakLotClass, validateLotFlag, "ALOT", bypassUsedEntitiesFlag)[0];
        if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
            if srcBank and len(srcBank) > 4:
                self._raiseError("Source Bank (:1) length must be 4 character", (srcBank,));
        if tgtBank and len(tgtBank) > 4:
            self._raiseError("Target Bank (:1) length must be 4 character", (tgtBank,));
        if tgtBank:
            self._validateTrakBank(1, ("tgtBank", tgtBank));
        
        if srcMatlOwner:
            if not self._dbExecute("select 1 from OPOWNER where MATL_OWNER = :1 and rownum = 1", (srcMatlOwner,)):
                self._raiseError("srcMatlOwner (:1) is not valid.", (srcMatlOwner,));
        if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
            if srcCustSrc:
            #Added by Chen Ming for CR53272
                if not parentBank and srcBank:
                    if not self._dbExecute("select 1 from CUSTOMST where ISO_COUNTRY_CODE_05 = :1 and rownum = 1",(srcCustSrc,)):
                       self._raiseError("srcCustSrc (:1) is not valid ISO Country Code.",(srcCustSrc, ));
                else:
                    if not self._dbExecute("select 1 from CUSTOMST where CUST_SRC = :1 and rownum = 1", (srcCustSrc,)):
                        self._raiseError("srcCustSrc (:1) is not valid.", (srcCustSrc,)); 
            #end CR53272

        if tgtMatlOwner:
            if not self._dbExecute("select 1 from OPOWNER where MATL_OWNER = :1 and rownum = 1", (tgtMatlOwner,)):
                self._raiseError("tgtMatlOwner (:1) is not valid.", (tgtMatlOwner,));
        if tgtCustSrc:
            if not self._dbExecute("select 1 from CUSTOMST where CUST_SRC = :1 and rownum = 1", (tgtCustSrc,)):
                self._raiseError("tgtCustSrc (:1) is not valid.", (tgtCustSrc,));

        if tgtDevcNumber == "DEFAULT":
            self._validateRequiredArgs(
                nextDevcNumber = nextDevcNumber);
            tgtDevcNumberInfo = self._dbExecute(
                "select SOURCE_DEVC_NUMBER from DEVICE_NETWORKS where TARGET_DEVC_NUMBER = :1",
                (nextDevcNumber,));
            if len(tgtDevcNumberInfo) <> 1:
                self._raiseError("Unable to determine default Current Device for Next Device (:1)", (nextDevcNumber,));
            tgtDevcNumber = tgtDevcNumberInfo[0][0];
        else:
            self._validateDevcNumber(1, ("tgtDevcNumber", tgtDevcNumber));
        if srcDevcNumber == "DEFAULT":
            srcDevcNumberInfo = self._dbExecute(
                "select SOURCE_DEVC_NUMBER from DEVICE_NETWORKS where TARGET_DEVC_NUMBER = :1",
                (tgtDevcNumber,));
            if len(srcDevcNumberInfo) <> 1:
                self._raiseError("Unable to determine default Source Device for Current Device (:1)", (tgtDevcNumber,));
            srcDevcNumber = srcDevcNumberInfo[0][0];
        if nextDevcNumber:
            if nextDevcNumber == tgtDevcNumber:
                self._raiseError("Next Device (:1) must be different from Target Device", (nextDevcNumber,));
            self._validateDevcNumber(1, ("nextDevcNumber", nextDevcNumber));
            self._validateDevcDevcCombination(1, ("tgtDevcNumber", tgtDevcNumber), ("nextDevcNumber", nextDevcNumber));

        if self._getTransParmValue(transType, None, "autoActivateLot") or activateLotFlag:
            lotStatus = "AC";
            autoActivateLot = 1;
        else:
            lotStatus = "ST";
            autoActivateLot = 0;

        if waferLotNumber:
            #self._validateWaferLotNumber(1, ("waferLotNumber", waferLotNumber));
            try:
                maskSetWafer = self.getWaferLotAttributes(
                    attributes = "maskSet",
                    lotNumber = waferLotNumber)[0][0];
            except IndexError:
                maskSetWafer = None;
            checkMaskSetOvrd = self._getTransParmValue(transType, None, "checkMaskSetOvrd");
            if not maskSet:
               maskSet = maskSetWafer;
            if maskSetWafer and maskSetWafer <> maskSet and not checkMaskSetOvrd:
                self._raiseError("Mask Set (:1) does not match value in database (:2)", (maskSet, maskSetWafer)); 

        doNotUpdateAssyLoc = 0;
        if not assyLoc:
            if trakOper:
                assyLoc = self._getAssemblySiteCode(trakOper);

            if not assyLoc:
                assyLoc = self._getMESParmValue(parmOwnerType='APPL', parmName='assemblyLocation', parmOwner='MaterialMgr');
                if trakOper:
                    if self._getMESParmValue("OPER", trakOper, "updateAssyLoc"):
                        doNotUpdateAssyLoc = 0;
                else:
                    doNotUpdateAssyLoc = 1;
        
        if trakOper:
            testLoc = self._getTestSiteCode(trakOper);
        else:
            testLoc = None;
        defaultTrakRouting = None;
        if trakOper:
            defaultTrakRouting =  self._checkRoutingRequired(trakLotClass, tgtDevcNumber, trakRouting, trakOper, None)[0][0];

        if not maskSet:
            maskSet = srcDevcNumber
        else:
            try:
                self._dbExecute("select devc_number from devices where devc_number = :1",(maskSet,))[0][0];   
            except IndexError:
                self._raiseError("The maskset value is not valid.");

        if masterProcess:
            self._validateProcName(1, ("masterProcess", masterProcess));
            self._validateDevcProcCombination(1, ("tgtDevcNumber", tgtDevcNumber), ("masterProcess", masterProcess));
            dbTrakRouting = self.getProcessAttributes(
                attributes = "trakRouting",
                procName = masterProcess)[0][0];
            if not trakRouting:
                trakRouting = dbTrakRouting;
            elif dbTrakRouting <> trakRouting:
                self._raiseError("Master Process (:1) and TRAK Routing (:2) combination is invalid", (masterProcess, trakRouting));
        else:
            if isLotStartFromMWI and isLotStartFromMWI == "Y":
                masterProcess = self._getMasterProcessMWI(tgtDevcNumber, maskSet,assyLoc, trakRouting, stepName, trakOper, pkgKit, woNumber, processSpec);
            else:
                masterProcess = self._getMasterProcess(tgtDevcNumber, maskSet, assyLoc, trakRouting, stepName, trakOper, pkgKit);
            #self._raiseError(masterProcess);
            if autoActivateLot and not masterProcess:
                autoActivateLot = 0;
                lotStatus = "ST";
                #if trakRouting:
                #    if stepName:
                #        self._raiseError("Unable to find default Master Process for Device (:1) with TRAK Routing (:2), step name (:3) and trak operation (:4)", (tgtDevcNumber, trakRouting, stepName, trakOper));
                #    else:
                #        self._raiseError("Unable to find default Master Process for Device (:1) with TRAK Routing (:2) and trak operation (:3)", (tgtDevcNumber, trakRouting, trakOper));

                #    # self._raiseError("Unable to find default Master Process for Device (:1) corresponding to TRAK Routing (:2)", (tgtDevcNumber, trakRouting));
                #else:
                #    # self._raiseError("Unable to find default Master Process for Device (:1)", (tgtDevcNumber,));
                #    if stepName:
                #        self._raiseError("Unable to find default Master Process for Device (:1) with no TRAK Routing, step name (:2) and trak operation (:3)", (tgtDevcNumber, stepName, trakOper));
                #    else:
                #        self._raiseError("Unable to find default Master Process for Device (:1) with no TRAK Routing and trak operation (:2)", (tgtDevcNumber, trakOper));

            if masterProcess and not trakRouting:
                trakRouting = self.getProcessAttributes(
                    attributes = "trakRouting",
                    procName = masterProcess)[0][0];

        if not trakOper and masterProcess:
            try:
                #trakOper = self._dbExecute("select TRAK_OPERATION from PROCESS_SEQS where PROC_NAME= :1 and PSEQ_NUMBER=10",(masterProcess,))[0][0];
                trakOperList = self.getProcSeqAttr(attributes='stepName,stepSeq,trakOper', procName = masterProcess);        
                if trakOperList:
                    stepName,stepSeq,trakOper = trakOperList[0];
            except:
                self._raiseError("Master Process (:1) does not have a process seqs defined",(masterProcess,));

        if trakOper:
            if not trakRouting and defaultTrakRouting:
                self._raiseError("Master Process (:1) and default TRAK Routing (:2) combination is invalid", (masterProcess, defaultTrakRouting));      
        checkLogicMoveValid = None;
        if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
            checkLogicMoveValid = self._getMESParmValue('APPL','MaterialMgr','checkLogicMoveValid');
            if checkLogicMoveValid:
                if moveOvrdFlag <> "Y" and checkLogicMoveValid <> "0":
                    if not self._checkLogicMovValid(srcBank, tgtBank, None, None):
                        self._raiseError("Illogical move from sourceBank (:1) to targetBank (:2)",(srcBank, tgtBank));
        
        #ENHC0011984 and ENHC0011985
        palCode, productClass = self.getDeviceAttributes(attributes = "palCode,prodClass", devcNumber = tgtDevcNumber)[0];

        try:
            palCodeForCuFlush = self.getMESParmValues(attributes='parmValue',parmOwnerType='PALC',parmOwner=palCode[0],parmName='palCodeForCuFlush')[0][0];
        except IndexError:
            palCodeForCuFlush = None;
        #ENHC0011984 and ENHC0011985
        
        rawstockProdClassList = [];
        rawstockProdClassList = self._getMESParmValue('APPL','MaterialMgr','rawstockProductClass');        

        if pkgKit:
            self._validatePkgKit(1, ("pkgKit", pkgKit));
            
            if rawstockProdClassList:
                if productClass in rawstockProdClassList:
                    self._validateDevcPkitCombination(1, ("tgtDevcNumber", tgtDevcNumber), ("pkgKit", pkgKit));
            else:
                self._validateDevcPkitCombination(1, ("tgtDevcNumber", tgtDevcNumber), ("pkgKit", pkgKit)); 

        else:
            if not isLotStartFromMWI and not isLotStartFromMWI == "Y": #by Aish
                #ENHC0011985 added by Fuji, check if pkgKit empty and device palCode is J, then it requires pkg kit
                if palCodeForCuFlush == "1":
                    self._raiseError("This Device Number (:1) with palCode (:2) is require package kit. Please enter the package kit.",(tgtDevcNumber,palCode));
                #ENHC0011985 end
            
            pkgKit = self._getDefaultPkgKit(tgtDevcNumber, maskSet, trakRouting);
        self._createLot(lotNumber, tgtDevcNumber, masterProcess, pkgKit, lotStatus, lotQty, eventTime);
        origTraceCode = None;
        if not doNotUpdateAssyLoc:
            assyLoc2 = assyLoc;
        else:
            assyLoc2 = "";
        #if isLotStartFromMWI and isLotStartFromMWI == "Y":
        r3State = None;
        #CR31863:Fiena
        if trakOper:
            #get bank type
            try:
                r3State = self._dbExecute("select SAP_TRACKING_TYPE_Z5 from OPERTABL O, BANKTABL B where O.TRAK_OPER= :1 and O.BANK_EE = B.BANK", (trakOper,))[0][0];
            except IndexError:
                r3State = None;

        bondDiagram = None;
        bondDiagramRev = None;
        #ENHC0011605 - ABI Project Start
        prodClass = None;
        #ENHC0011605 - ABI Project End
        if self._getMESParmValue("APPL", "MaterialMgr", "generateBondingDiagram"):
            prodClass = self.getDeviceAttributes(attributes = "prodClass", devcNumber = tgtDevcNumber)[0][0];
            if prodClass == "99" and r3State == "W" and not dieSource and transType == "createTrakLot":
                if isLotStartFromMWI <> "Y":
                    self._raiseError("dieSource is required");

            if prodClass == "99" and r3State == "W" and transType == "createTrakLot":
                #fiena change to use new API : CR31863
                if isLotStartFromMWI <> "Y":
                    bondDiagram = self.generateBondingDiagram(tgtDevcNumber, dieSource, assyLoc, pkgKit)[0][0];

        if bondDiagram:
                    try:
                        bondDiagramRev = self.generateBondingDiagramRev(bondDiagram)[0][0];
                    except IndexError:
                        pass;

        #Start of ENHC0012559:Shobana
        #need to check whether there is any value of configuration for lotClassPriorityAutoUpdate
        try:
            lotClassPriorityValue = self._getMESParmValue('TLCL', lotNumber[:2] ,'lotClassPriorityAutoUpdate');
        except IndexError:
            lotClassPriorityValue = None;
                
        if lotClassPriorityValue:
            priority = lotClassPriorityValue;
        else:
            priority = 1; 
        self._updateLotAttributes(transUserId, lotNumber,
            {"waferLotNumber":waferLotNumber, "maskSet":maskSet, "trakMatlOwner":tgtMatlOwner, "trakCustSrc":tgtCustSrc, "srcMatlOwner":srcMatlOwner, "srcCustSrc":srcCustSrc, "nextDevcNumber":nextDevcNumber, "originalStartDate":eventTime, "sourceBank":srcBank, "targetBank":tgtBank, "origTrakLotClass":trakLotClass, "priority":priority, "topMark" : topMark,"backMark": backMark, "startOper":trakOper, "actualLotStartDate":eventTime, "origTrakRouting": trakRouting, "testLoc" : testLoc, "assyLoc" : assyLoc2, "actualWlotNumber" : actualWlotNumber, "reqdPriority":1, "trakRouting":trakRouting, "irabActualStartDate":eventTime, "npiStatus" : npiStatus, "dieSource" : dieSource, "bondingDiagram" : bondDiagram, "bondingDiagramRevision" : bondDiagramRev, "woNumber" : woNumber}, eventTime);
        #End of ENHC0012559:Shobana
                    
        if transType <> "createNonTrakLot":
            self._updateLotAttributes(transUserId, lotNumber,
                {"trakLotClass":trakLotClass},
                eventTime);
        #ENHC0011605 - ABI Project Start
        if not rawstockPartNumber:
            if not prodClass:
                prodClass = self.getDeviceAttributes(attributes = "prodClass", devcNumber = tgtDevcNumber)[0][0];
            rawstockProductClassList = [];
            rawstockProductClassList = self._getMESParmValue('APPL','MaterialMgr','rawstockProductClass');
            
            if rawstockProductClassList :
                if prodClass in rawstockProductClassList:
                    rawstockPartNumber = tgtDevcNumber;
                #else:
                    #if trakLotClass:
                        #self._raiseError("rawstockPartNumber is empty");
        if rawstockPartNumber:
            self._updateLotAttributes(transUserId, lotNumber,{"rawstockPartNumber":rawstockPartNumber},eventTime);       
        #ENHC0011605 - ABI Project End

        tsqQty = 0;
        phyTraceCode = "";        
                
        if autoActivateLot:
            self._queueNewLot(transUserId, lotNumber, masterProcess, stepName, eventTime);
            if not pkgKit:
                stepName = self.getCurrentStepContext(
                    attributes = "stepName",
                    lotNumber = lotNumber)[0][0];
                if not self._getMESParmValue("STEP", stepName, "optionalPkgKitFlag"):
                    self._raiseError("Unable to find default Package Kit for Device (:1)", (tgtDevcNumber,));
            #can only generate tracecode if lot is auto-activated, ie has ALOT_OPER_HIST entry
       # ERP traceCode issue changes start -Jija
            try:
                autoGenTraceCode = self._checkAutoTraceCodeGenerate(transType);
            except IndexError:
                autoGenTraceCode = None;
       # ERP traceCode issue changes end -Jija
            if not traceCode and autoGenTraceCode:
                #CR53940-To overcome duplicate recrod insertion in the table MES_ATTRIBUTE_HISTORIES, we added the flag requireUpdateFFCode.
                #        This flag says whether the traceCode has been generated or not.
                requireUpdateFFCode = 0;                
                traceCode = self.generateTraceCode(transUserId, lotNumber);
                #print "traceCodeTT:%s"%(traceCode);                
                origTraceCode = traceCode;
                #FCode generation was added for Trace Improvement for CR53940
                fCode=traceCode[:2];
                if fCode=="" or fCode=="  ":
                  self._dbExecute("update AO_LOTS set ACTUALWLOTNUMBER = :1 where ALOT_NUMBER = :2", (waferLotNumber, lotNumber));
                  fCode="";
                  fCode = self.generateFFAATTCode(attributes = "fCode", lotNumber = lotNumber)[0];
                  fCode = fCode[0];
                  if len(fCode)==1:
                    fCode= fCode + " ";
                  elif len(fCode)==0:
                    fCode= fCode + "  " ;
                  traceCode= fCode + traceCode[2:]
                
                fatCode, wlCode, dateCode, zCode = self._extractTraceCodeFields(traceCode);
                self._updateLotAttributes(transUserId, lotNumber,
                {"traceCode":traceCode, "fatCode":fatCode, "dateCode":dateCode, "wlCode":wlCode}, eventTime);
                #get Physical Trace Code based on configuration    
                phyTraceCode = self.populatePhysicalTraceCode(transUserId, lotNumber, traceCode);
                #print "phyTraceCode2:%s"%(phyTraceCode);
                if phyTraceCode:
                    self._updateLotAttributes(transUserId, lotNumber,
                        {"physicalTraceCode":phyTraceCode}, eventTime);
                
       # ERP traceCode changes start -Jija


            #autoGenTraceCode = None;
            print "autoGenTraceCode:%s"%(autoGenTraceCode);
            if not traceCode and not autoGenTraceCode and (isLotStartFromMWI and isLotStartFromMWI == "Y"):
                print "transType:%s"%(transType);
                srcLotNumber = "";
                try:
                    srcLotNumber = self._dbExecute("select SRCLOTNUMBER from AO_LOTS A where A.ALOT_NUMBER= :1",(lotNumber,))[0][0];
                except IndexError:
                    srcLotNumber = None;
                print "srcLotNumber:%s"%(srcLotNumber);
                if srcLotNumber: 
                    #select traceCode of SRCLOTNUMBER
                    try:
                        traceCode = self.getLotAttributes(attributes = "traceCode",lotNumber = srcLotNumber)[0];
                    except IndexError:
                        traceCode = None;
                print "traceCode-SRC LOT:%s"%(traceCode);
                if not traceCode:
                    #traceCode = select traceCode from WDT
                    try:
                        traceCode = self.getWDTAOLotData(attributes = "traceCode", lotNumber = lotNumber)[0][0];
                    except IndexError:
                        traceCode = None;
                print "traceCode-WDT:%s"%(traceCode);
                if not traceCode:
                    #traceCode = select traceCode from batch chars in GEN_MWI_MESLOTSTART and GEN_SS_MESLOTSTARTDETAILS
                    try:
                        traceCode = self._dbExecute("select TRACECODE from LOTSTARTDIFFBATCHLIST where LOTNUMBER= :1",(lotNumber,))[0][0];
                    except IndexError:
                        traceCode = None;
                print "traceCode-batch chars:%s"%(traceCode);
                if traceCode:

                    fatCode, wlCode, dateCode, zCode = self._extractTraceCodeFields(traceCode);
                    print "fatCode-updating..:%s"%(fatCode);
                    self._updateLotAttributes(transUserId, lotNumber,
                    {"traceCode":traceCode, "fatCode":fatCode, "dateCode":dateCode, "wlCode":wlCode}, eventTime);
                self._raiseError("traceCode (:1) fatCode(:2) ", (traceCode, fatCode));
        # ERP traceCode changes end - jija

            currTrakOper = self.getCurrentStepContext(
                attributes = "trakOper",
                lotNumber = lotNumber)[0][0];
            if not trakOper:
                self._updateLotAttributes(transUserId, lotNumber,
                    {"startOper": currTrakOper},
                    eventTime);
                defaultTrakRouting =  self._checkRoutingRequired(trakLotClass, tgtDevcNumber, trakRouting, currTrakOper, None)[0][0];
                if not trakRouting and defaultTrakRouting:
                    self._raiseError("Master Process (:1) and default TRAK Routing (:2) combination is invalid", (masterProcess, defaultTrakRouting));
            #populate irab attributes
            if self._isTestOperation(currTrakOper):
                tsqQty = lotQty;
        irabQtyDict = {"accumRejQty" : 0, "testStartQty" : tsqQty, "currBalanceDue" : lotQty, "origOrderQty" : lotQty, "orderAdjustQty" : 0};
        self._updateLotIrabQtyParameters(lotNumber, "ALOT", irabQtyDict);
        self._raiseError("traceCode (:1) autoGenTraceCode. (:2) .",(traceCode,autoGenTraceCode)); 
        #TraceCode validation should take place after the lot assigned to oper - CR53940
        if traceCode and requireUpdateFFCode == 1 and autoActivateLot:
            privUpdtTcode = self._checkPrivForUpdateAttribute(transUserId, "traceCode");
            origTraceCode = traceCode;
            #FCode generation was added for Trace Improvement for CR53940
            fCode=traceCode[:2];
            if fCode=="" or fCode=="  ":
              fCode="";
              fCode = self.generateFFAATTCode(attributes = "fCode", lotNumber = lotNumber)[0];
              fCode = fCode[0];
              if len(fCode)==1:
                  fCode= fCode + " ";
              elif len(fCode)==0:
                  fCode= fCode + "  ";
              traceCode= fCode + traceCode[2:]            
            traceCode, fatCode, wlCode, dateCode = self._parseTraceCode(traceCode, eventTime, lotNumber, "N", "N", privUpdtTcode, "Y", None, None);
            self._updateLotAttributes(transUserId, lotNumber,
                {"traceCode":traceCode, "fatCode":fatCode, "dateCode":dateCode, "wlCode":wlCode}, eventTime);
            #get Physical Trace Code based on configuration    
            phyTraceCode = self.populatePhysicalTraceCode(transUserId, lotNumber, traceCode);
            #print "phyTraceCode1:%s"%(phyTraceCode);
            if phyTraceCode:
                self._updateLotAttributes(transUserId, lotNumber,
                    {"physicalTraceCode":phyTraceCode}, eventTime);

        elif traceCode and not autoActivateLot:
            privUpdtTcode = self._checkPrivForUpdateAttribute(transUserId, "traceCode");
            origTraceCode = traceCode;
            traceCode, fatCode, wlCode, dateCode = self._parseTraceCode(traceCode, eventTime, lotNumber, "N", "N", privUpdtTcode, "Y", None, None);
            self._updateLotAttributes(transUserId, lotNumber,
                {"traceCode":traceCode, "fatCode":fatCode, "dateCode":dateCode, "wlCode":wlCode}, eventTime);
            phyTraceCode = self.populatePhysicalTraceCode(transUserId, lotNumber, traceCode);
            if phyTraceCode:
                self._updateLotAttributes(transUserId, lotNumber,
                     {"physicalTraceCode":phyTraceCode}, eventTime); 

        if transType <> "createNonTrakLot":
            if autoActivateLot:
                trakOperHist = self._getLotTrakOperHist(lotNumber);
                if not trakOper:
                    trakOper = trakOperHist[0];
                elif trakOperHist[0] <> trakOper:
                    self._raiseError("TRAK Operation (:1) does not match Operation (:2) of first process step of Master Process (:3)", (trakOper, trakOperHist[0], masterProcess));

            if not tgtBank:
                tgtBank = self._getDefaultTrakTgtBank(trakLotClass);
            auditorTrakId = self._getMESParmValue("USER", transUserId, "auditorTrakId");
            #if srcBank and srcBank <> "0000" and srcBank <> "0007":
                #self._updateBankInventory(srcBank, srcDevcNumber, srcMatlOwner, srcCustSrc, eventTime, 0, -lotQty);

            if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
                trakCmd = "bulkStrt(lotNumber = %s, lotQty = %d, tgtDevcNumber = %s, tgtMatlOwner = %s, tgtCustSrc = %s, tgtBank = %s, srcDevcNumber = %s, srcMatlOwner = %s, srcCustSrc = %s, srcBank = %s, routing = %s, oper = %s, shiftCode = %s, originator = %s, auditorTrakId = %s, topMark = %s, unitOfIssue = 'EA', lotStartDate = %s)"%(`lotNumber`, lotQty, `tgtDevcNumber`, `tgtMatlOwner`, `tgtCustSrc`, `tgtBank`, `srcDevcNumber`, `srcMatlOwner`, `srcCustSrc`, `srcBank`, `trakRouting`, `trakOper`, `trakShift`, `transUserId`, `auditorTrakId`, `topMark`, `eventTime`);
                self._addTrakTrans(transUserId, lotNumber, trakCmd, "bulkStrt", eventTime);
            else:
                smiInvokedMsg='1'
                trakCmd = "bulkStrt(lotNumber = %s, lotQty = %d, tgtDevcNumber = %s, tgtMatlOwner = %s, tgtCustSrc = %s, tgtBank = %s, srcDevcNumber = %s, srcMatlOwner = %s, srcCustSrc = %s, srcBank = %s, routing = %s, oper = %s, shiftCode = %s, originator = %s, auditorTrakId = %s, topMark = %s, unitOfIssue = 'EA', lotStartDate = %s, smiInvokedMsg = %s)"%(`lotNumber`, lotQty, `tgtDevcNumber`, `tgtMatlOwner`, `tgtCustSrc`, `tgtBank`, `srcDevcNumber`, `srcMatlOwner`, `srcCustSrc`, `srcBank`, `trakRouting`, `trakOper`, `trakShift`, `transUserId`, `auditorTrakId`, `topMark`, `eventTime`,`smiInvokedMsg`);

            self._addTrakTrans(transUserId, lotNumber, trakCmd, "bulkStrt", eventTime);  
            
            if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
                if traceCode or (assyLoc and not doNotUpdateAssyLoc) or testLoc:
                    trakCmd = "updtCode(lotNumber = %s,"%(`lotNumber`,);
                    if traceCode:
                        trakCmd  = trakCmd + "traceCode = %s,"%(`origTraceCode`,);
                    if assyLoc and not doNotUpdateAssyLoc:
                        trakCmd  = trakCmd + "assyLoc = %s,"%(`assyLoc`,);
                    if testLoc:
                        trakCmd  = trakCmd + "testLoc = %s,"%(`testLoc`,);

                    trakCmd  = trakCmd + "shiftCode = %s, originator = %s, oper = %s, srcDevcNumber = %s, transUserId = %s)"%(`trakShift`, `transUserId`, `trakOper`, `tgtDevcNumber`, `transUserId`);

                    self._addTrakTrans(transUserId, lotNumber, trakCmd, "updtCode", eventTime);

                    self._insertTranlog(eventTime, hostName, transUserId, "UPDTCODE", trakLotClass, lotNumber[2:], tgtDevcNumber, "N", lotQty, trakOper, "1", trakOper, "1", trakLotClass, lotNumber[2:], tgtDevcNumber, trakRouting, trakRouting, tgtMatlOwner, tgtCustSrc, tgtMatlOwner, tgtCustSrc, None, None, traceCode, None, None, None, None, None, trakShift, transUserId, tranLogSeq);
                    tranLogSeq = tranLogSeq + 1;
                try:
                    toBank = self._dbExecute("select BANK_EE from OPERTABL where TRAK_OPER= :1",(trakOper,))[0][0];
                except:
                    self._raiseError("Error Getting to Bank");
            if not isLotStartFromMWI or isLotStartFromMWI <> "Y":
                self._updateBankInventory(toBank, tgtDevcNumber, tgtMatlOwner, tgtCustSrc, eventTime, lotQty, 0);
                if self._checkCompTrackingRequired(toBank, tgtMatlOwner):
                    self._updateCompLotInfo(lotNumber, srcDevcNumber, 1, srcMatlOwner, srcCustSrc, srcBank, None, None, None);
        
        if autoActivateLot:
            holdCondition = self._getHoldCondition(lotNumber);
            if holdCondition:
                stepName, holdUserId, reasonCode, comment, holdTypes = holdCondition;
                tranLogSeq = self._holdLot(holdUserId, lotNumber, stepName, reasonCode, comment, holdTypes, None, None, None, eventTime, hostName, None, None, trakShift, tranLogSeq);

       
        ##CR43950: Fiena check futureShipHoldFlag. If exist, copy to lotNumber
        srcFutureShipHoldFlag = 0;
        lotCondition = "";
        if waferLotNumber:
            try:
                srcFutureShipHoldFlag = self.getWaferLotAttributes(
                    attributes = "futureShipHoldFlag",
                    lotNumber = waferLotNumber)[0][0];
            except IndexError:
                srcFutureShipHoldFlag = 0;
        if srcFutureShipHoldFlag == 1:
            lotCondition = "WLOT_NUMBER = %s"%`waferLotNumber`;        
        else:
            #srcFutureShipHoldFlag = 0. check by device
            exist = None;
            if srcDevcNumber:
                try:
                    exist = self.getFutureShipHoldCond(
                        attributes = "devcNumber",
                        devcNumber = srcDevcNumber)[0][0];
                except IndexError:
                    exist = None;
                
            if exist:
                lotCondition = "DEVC_NUMBER = %s"%`srcDevcNumber`;
                srcFutureShipHoldFlag = 1;
            else:
                if tgtDevcNumber:
                    try:
                        exist = self.getFutureShipHoldCond(
                            attributes = "devcNumber",
                            devcNumber = tgtDevcNumber)[0][0];
            
                    except IndexError:
                        exist = None;
                if exist:
                    lotCondition = "DEVC_NUMBER = %s"%`tgtDevcNumber`;
                    srcFutureShipHoldFlag = 1;
                    
        if srcFutureShipHoldFlag == 1:
            self._updateLotAttributes(transUserId, lotNumber,
                {"futureShipHoldFlag":srcFutureShipHoldFlag}, eventTime);
            data = self._dbExecute(
                "select distinct STEP_NAME, SET_TIME, SET_USER_ID, RCDE_ID, COMMENTS, RESET_TIME from FUTURE_SHIP_HOLD_COND where  %s order by STEP_NAME, SET_TIME"%lotCondition);
            if data:
                for fsStepName, fsSetTime, fsSetUserId, fsReasonCode, fsComment, fsResetTime in data:
                    self._dbExecute(
                        "delete FUTURE_SHIP_HOLD_COND where ALOT_NUMBER = :1",
                        (lotNumber,));
                    if not self._dbExecute("select 1 from FUTURE_SHIP_HOLD_COND where ALOT_NUMBER = :1 and STEP_NAME = :2 and RCDE_ID = :3 and COMMENTS = :4", (lotNumber, fsStepName, fsReasonCode, fsComment)):
                         self._dbExecute(
                              "insert into FUTURE_SHIP_HOLD_COND (ALOT_NUMBER, STEP_NAME, SET_TIME, SET_USER_ID, RCDE_ID, COMMENTS) values (:1, :2, :3, :4, :5, :6)",
                              (lotNumber, fsStepName, fsSetTime, fsSetUserId, fsReasonCode, fsComment));
        ###--    


        #if trakLotClass:
        #    self._initializeQadsLotHeader(lotNumber);

        #CR60137 start to check lot nettable
        if lotNumber and tgtDevcNumber and lotQty:
            if tgtDevcNumber <> "DEFAULT" and lotQty > 0:
                if self._checkLotNettable(lotNumber = lotNumber) == 1 and self._checkLotInTbeOper(lotNumber = lotNumber) == 1:
                    self._deductRemainingDcrQtyFromFo(tgtPartNumber = tgtDevcNumber, adjustQty = lotQty);
        #CR60137 end

        #ENHC0011984 copper CR start, added by Fuji
        try:
            palCodeForCuFlush = self.getMESParmValues(attributes='parmValue',parmOwnerType='PALC',parmOwner=palCode[0],parmName='palCodeForCuFlush')[0][0];
        except IndexError:
            palCodeForCuFlush = None;
        
        if palCodeForCuFlush == "1":
            try:
                lotWireType = self.getLotWireType(lotNumber = lotNumber)[0][0];
            except IndexError:
                lotWireType = None;
            
            if lotWireType:
                if lotWireType in ("COPPER","THINNER WIRE"):
                    try:
                        tempRawstockPartNumber = self.getLotAttributes(attributes='rawstockPartNumber',lotNumber=lotNumber)[0][0];
                    except IndexError:
                        tempRawstockPartNumber = None;

                    if tempRawstockPartNumber:
                        #first, check is it logged in CONVERTED_COPPER
                        try:
                            copperDevc, copperStartLotNumber, copperLotStartDate = self.getConvertedCopper(attributes='devcNumber,startLotNumber,startDate', devcNumber = tempRawstockPartNumber)[0];
                        except IndexError:
                            copperDevc = None;
                            copperStartLotNumber = None;
                            copperLotStartDate = None;
                        
                        firstCopperLotStart = 0;
                    
                        if copperDevc:
                            if copperStartLotNumber == None and copperLotStartDate == None: #if startDate is empty, then insert date
                                self._dbExecute("update CONVERTED_COPPER set START_ALOT_NUMBER = :1, START_DATE = :2 where DEVC_NUMBER = :3", (lotNumber,eventTime, tempRawstockPartNumber));
                                firstCopperLotStart = 1;
                    
                        elif not copperDevc: #if not record in converted_copper, it will be the first copper lot to start
                            self.addConvertedCopper(transUserId = transUserId, startLotNumber = lotNumber, devcNumber = tempRawstockPartNumber, startDate = eventTime);
                            firstCopperLotStart = 1;                            
    
                        if firstCopperLotStart == 1:
                            #and then, get the list of gold lot, tag all the gold lot firstCuThinStart
                            listOfGoldLot = self.getListOfGoldLot(lotNumber = lotNumber);
                            if listOfGoldLot:
                                for eachGoldLot in listOfGoldLot:
                                    self._updateLotAttributes(transUserId = transUserId, lotNumber = eachGoldLot[0], attrDict = {"firstCuThinStart":"Y"}, eventTime = eventTime);
        #ENHC0011984 end

        
        if returnLotNumber:
            lotNumberList = [];
            lotNumberList.append(tuple([lotNumber, tgtDevcNumber, lotQty]));
            return lotNumberList;
