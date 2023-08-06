from . import restClient,query,digitalCommerceUtil,file,utils,objectUtil,Sobjects
import simplejson,logging

import colorama
import sys,time
import ansi2html,re
import threading
from queue import Queue

def _queryLogRecords(logUserId=None,limit=50,whereClause=None):
    where = f" where {whereClause} " if whereClause != None else ''
    where = f" where logUserId='{logUserId}' " if logUserId is not None else where

    call = query.query(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog  {where} order by LastModifiedDate desc limit {limit}")
    return call

def _logRecord_toString(logRecord):
    log = logRecord
    logLine = f"""LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']}    Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}    lenght: {log['LogLength']}    duration: {log['DurationMilliseconds']}    startTime: {log['StartTime']} 
LOGDATA:    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}
    """     
    return logLine

def _queryLogData(logId):
    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog where Id ='{logId}' limit 1")

    if logRecords == None or len(logRecords)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLogwith Id {logId}")    
    logRecord = logRecords[0]

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
    return logRecord,logbody

def _parseTail(loguser=None,level=None,whereClause=None,deleteLogs=True):
    deleteList = []
    def deleteRecords(q):
      while True:
        Id = q.get()
        res = Sobjects.delete('ApexLog',Id)
        restClient.glog().debug(f"deleted records {Id}")
        q.task_done()


    timefield = "StartTime"

    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog order by {timefield} desc limit 1")
    if len(logRecords) > 0:
        _time = logRecords[0][timefield]
        _timez = _time.split('.')[0] + "Z"
    else:
        _timez = '2000-12-12T17:19:35Z'

    waitingPrinted = False
    q= None
    restClient.glog().debug(f"deleteLogs-->{deleteLogs}")
    if deleteLogs==True:
        if loguser==None:
            username = restClient.getCurrentThreadConnection()['username']
            loguser = f"Username:{username}"
        
        restClient.glog().debug("Starting queue")
        q = Queue(maxsize=0)
        threading.Thread(target=deleteRecords,args=(q,), daemon=True).start()
        threading.Thread(target=deleteRecords,args=(q,), daemon=True).start()
    
    logUserId = _getLogUserId(loguser=loguser) if loguser != None else None

    try:
        while (True):
            where = f" {timefield} > {_timez} "
            where = f" {whereClause} and {where}" if whereClause is not None else where
            where = f" logUserId='{logUserId}'and {where} " if logUserId is not None else where

            fields = "Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier"
            logRecords = query.queryRecords(f"Select {fields} FROM ApexLog where {where} ")
            if len(logRecords) > 0:
                waitingPrinted = False

                for record in logRecords:

                    parseLog(logId=record['Id'], loguser=loguser,level=level)                
                    _time = record[timefield]
                    _timez = _time.split('.')[0] + "Z"
                    if q!=None:
                        q.put(record['Id'])
                        restClient.glog().debug(f"{record['Id']} into queue...")
                    
            else:
                if waitingPrinted == False:
                    print()
                    if loguser != None:
                        print(f"waiting for debug logs for user {loguser}")
                    else:
                        print(f"waiting for debug logs ")

                    waitingPrinted = True

            time.sleep(2)
    except KeyboardInterrupt as e:
        print()
        print("Terminating -tail..., cleaning up")
        if q != None:
            while q.empty()==False:
                time.sleep(1)
        print('Terminated')
        return

   # except Exception as e:
def _parseLogs_LastN(lastN,loguser=None,whereClause=None,printLimits=True,writeToFile=False):
    where = f" where {whereClause} " if whereClause is not None else ''
    where = f" where logUserId='{_getLogUserId(loguser)}' " if loguser is not None else where

    q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
    if lastN == None:
        lastN = 1
    logIds = query.queryFieldList(f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}")
    if logIds == None or len(logIds)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)
    for logId in logIds:
        parseLog(logId,printLimits=printLimits,writeToFile=writeToFile)

def _getLogUserId(loguser):
    chunks = loguser.split(":")
    key = chunks[0] if len(chunks)>1 else 'Id'
    value = chunks[1] if len(chunks)>1 else chunks[0]
    if key.lower() == 'id':
        return value
    id = query.queryField(f"Select Id from User where {key}='{value}'") if key.lower()!='id' else value
    if id == None:
        utils.raiseException('QUERY',f"User with field {key} = {value} does not exist in the User Object.")    
    return id

def parseLog(logId=None,filepath=None,printLimits=True,lastN=1,loguser=None,level=None,whereClause=None,writeToFile=False,tail=False,deleteLogs=False):
    body = None

    if tail == True:
        return _parseTail(loguser=loguser,level=level,whereClause=whereClause,deleteLogs=deleteLogs)

    elif filepath != None:
        body = file.read(filepath)

    elif logId != None:  #check if already downloaded
        filename = f"{restClient.logFolder()}{logId}.log"
        if file.exists(filename) == True:
            body = file.read(filename)
            filepath = filename
        else:
           logRecord,body = _queryLogData(logId) 
           body = _logRecord_toString(logRecord=logRecord) + body

    else:
        return _parseLogs_LastN(lastN,loguser,whereClause=whereClause,printLimits=printLimits,writeToFile=writeToFile)

    if body == None :
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found. ')

    if len(body)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{logId}> is empty. ')

    if filepath == None:
        filename = f"{restClient.logFolder()}{logId}.log"
        file.write(filename,body)

    print('___________________________________________________________________________________________________________________________________________________________________')
    if logId != None:
        print(logId)

    return parse(logId,body,printLimits=printLimits,level=level,writeTofile=writeToFile)

def printLogRecords(loguser=None,limit=50,whereClause=None):
    logUserId = _getLogUserId(loguser) if loguser != None else None
    logs = _queryLogRecords(logUserId,limit=limit,whereClause=whereClause)
    logs = utils.deleteNulls(logs,systemFields=False)
    utils.printFormated(logs,rename="LogLength%Len:DurationMilliseconds%ms")

def delta(obj,field):
    return obj[field][1] - obj[field][0] if len(obj[field]) > 1 else 0

def setTimes(line,obj=None,field=None,value=None,chunkNum=None,type=None):
    def addList(obj,field,val):
        if field in obj:
            obj[field].append(val)
        else:
            obj[field] = [val]

    chunks = line.split('|')

    if obj == None:
        obj = {
            'type' : type,
            'ident' : _context['ident'],
            'exception' :False
        }
       
        if len(chunks)>3:
            obj['Id'] = chunks[3]

    addList(obj,'lines',line)
    addList(obj,'CPUTime',_context['DEF:CPU time'])
    addList(obj,'SOQLQueries',_context['DEF:SOQL queries'])
    addList(obj,'cmtCPUTime',_context['CMT:CPU time'])
    addList(obj,'cmtSOQLQueries',_context['CMT:SOQL queries'])
    addList(obj,'totalQueries',_context['totalQueries'])
    addList(obj,'time',chunks[0].split(' ')[0])
    addList(obj,'timeStamp',int ((chunks[0].split('(')[1]).split(')')[0]))

  #  if _context['exception'] == True and obj['exception'] == False:
  #      obj['exception'] = True
  #      _context['exception'] = False

    if obj['type'] is None:
        print()

    if field is not None:
        obj[field] = chunks[chunkNum] if value is None else value

    if _context['timeZero'] == 0:
        _context['timeZero'] = obj['timeStamp'][0]

    obj['elapsedTime'] = obj[f'timeStamp'][0] #- _context['timeZero']

    return obj

_context = {
    'totalQueries' : 0,
    'timeZero':0,
    'ident':0,
    'DEF:SOQL queries' : 0,
    'DEF:CPU time' : 0,
    'CMT:SOQL queries' : 0,
    'CMT:CPU time' : 0,
    "exception":False
}

def resetContext():
    _context['totalQueries'] = 0
    _context['timeZero'] = 0
    _context['ident'] = 0
    _context['DEF:SOQL queries'] = 0
    _context['DEF:CPU time']=0
    _context['CMT:SOQL queries'] = 0
    _context['CMT:CPU time']=0
    _context['exception'] = False
    _context['previousElapsedTime'] = 0
    _context['previousCPUTime'] = 0
    _context['previousIsLimit'] = False
    _context['prevTimes'] = {
        0:[0,0]
    }
    _context['prevLevel'] = 0
    _context['firstLineIn'] = True
    _context['firstLineOut'] = True

def parse(logId,logData,printLimits=True,userDebug=True,level=None,writeTofile=False):
    _context['printLimits'] = printLimits
    _context['userDebug'] = userDebug
    _context['logLevel'] = level

    lines = logData.splitlines()

    ident = 0

    SOQL = {}

    onGoingCalls = []
    methodsList = onGoingCalls
    constructorList = onGoingCalls
    codeUnitsList = onGoingCalls
    constructorList = onGoingCalls
    dmlList=onGoingCalls

    methodsList = []
    constructorList = []
    codeUnitsList = []
    constructorList = []
    dmlList=[]

    limits = None

    exceptionDict = None

    limitsDict = {}

    debugList = []
    multiLine = None #for multiline commands

    resetContext()

    print()

    _context['debugList'] = debugList
    _context['openItemsList'] = []

    for num,line in enumerate(lines):
   #     print(num)

        chunks = line.split('|')
        _context['chunks'] = chunks
        _context['line'] = line
        _context['num'] = num

        if _context['firstLineIn'] == True:
            if 'LOGDATA:' in line:
                obj = {
                    'type':'LOGDATA',
                    'output':line
                }
                debugList.append(obj)
             #   print(line)
                continue
            else:
                _context['firstLineIn'] = False
                levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                obj = {
                    'type':'LOGDATA',
                    'output':levels
                }
             #   print(levels)
            #    print()
                continue

        if len(chunks)>1 and chunks[1] in ['HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_BEGIN']:
            continue

        if '|SYSTEM_MODE_EXIT|' in line:
            nop=1

        parseUserInfo(_context)

       # if '|' in line:   #This is a new line always. 
       #     multiLine = None
        
        parseExceptionThrown(_context)
        parseVariableAssigment(_context)
        parseLimits(_context) 
        parseUserDebug(_context)
        parseNamedCredentials(_context)
        parseCallOutResponse(_context)
        parseWfRule(_context)
        parseConstructor(_context)
        parseFlow(_context)
        parseCodeUnit(_context) 
        parseDML(_context)
        parseSOQL(_context)
        parseMethod(_context)

    repDebugList = processRepetition(debugList)
    printDebugList(repDebugList,logId,writeTofile)

    print()

    return _context

#openItemsList = []
def append_and_increaseIdent(context,obj,increase=True):
    context['openItemsList'].append(obj)
    if increase == True:
        increaseIdent(context)
    context['debugList'].append(obj)

def decreaseIdent_pop_setFields(context,type,value,key='key',endsWith=None,decrease=True):
    if decrease == True:
        decreaseIdent(context)
    obj = popFromList(context,type=type,key=key,value=value,endsWith=endsWith)
    setTimes(context['line'],obj)
    return obj

def parseUserInfo(context):
    if '|USER_INFO|' in context['line']:
        obj = setTimes(context['line'],field='output',value=context['chunks'][4],type='USER_INFO')
        context['openItemsList'].append(obj)

def parseSOQL(context):
    line = context['line']
    chunks = context['chunks']

    if '|SOQL_EXECUTE_BEGIN|' in line:
        obj = setTimes(line,type="SOQL")
        obj['query'] = chunks[4]
        obj['object'] = chunks[4].lower().split(' from ')[1].strip().split(' ')[0]
        obj['apexline'] = chunks[2][1:-1]
        append_and_increaseIdent(context,obj,increase=False)

    if '|SOQL_EXECUTE_END|' in line:
        context['totalQueries'] = context['totalQueries'] + 1
        obj = decreaseIdent_pop_setFields(context,type="SOQL",key='type',value='SOQL',decrease=False)
        obj['rows'] = chunks[3].split(':')[1]

        soql = obj['query'].lower()
        _from = soql.split(' from ')[-1].strip()
        _from = _from.split(' ')[0]

        obj['output'] = f"Select: {_from} --> {obj['rows']} rows"


def parseLimits(context):
    line = context['line']
    chunks = context['chunks'] 

    if '*** getCpuTime() ***' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:CPU time'] = chs[4]
    if 'CPU Time:' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:CPU time'] = chs[2]      
    if '*** getQueries() ***' in line:
        chs = chunks[4].split(' ')
        context[f'DEF:SOQL queries'] = chs[4]

    if '|LIMIT_USAGE|' in line:
        if '|SOQL|' in line:
            _context[f'DEF:SOQL queries'] = chunks[4]

    if '|LIMIT_USAGE_FOR_NS|' in line:
        limits = chunks[2]
        if limits == '(default)':
            context['limits'] = 'DEF:'
        elif limits == 'vlocity_cmt':
            context['limits'] = 'CMT:'
        else:
            context['limits'] = f"{limits}:"

        limitsDict = setTimes(line,type='LIMITS')
        limitsDict['limitType'] = limits
        limitsDict['output'] = limitsDict['limitType']

    if 'limits' in context and context['limits']!=None and line == '':
        context['limits'] = None
    
    if 'limits' in context and  context['limits'] is not None:
        chunks = line.split(' ')
        limits = context['limits']
        if 'SOQL queries' in line:
            _context[f'{limits}SOQL queries'] = chunks[6]
        if 'CPU time' in line:
            _context[f'{limits}CPU time'] = chunks[5]

    if 'limits' in context and  context['limits'] is not None and line =='':
        setTimes(limitsDict['lines'][0],limitsDict)
        s = f"limits-{limits.lower()} {limitsDict['time'][0]}"
        if _context['printLimits'] == True:
            context['debugList'].append(limitsDict)
        context['limits'] = None   

def parseUserDebug(context):
    line = context['line']
    chunks = context['chunks']

    if '|' in line:   #This is a new line always. 
        context['debug_multiLine'] = False

    if '|USER_DEBUG|' in line:
        context['debug_multiLine'] = True
    if 'debug_multiLine' in context and context['debug_multiLine'] == True:
        if '|' in line:
            obj = setTimes(line,type='DEBUG')
            obj['type'] = 'DEBUG'
            obj['subType'] = chunks[3]
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1]

        else:
            obj = context['debugList'][-1].copy()
            obj['string'] = line
    #    if _context['userDebug'] == True:
        context['debugList'].append(obj)
        obj['output'] = obj['string'] 

def parseExceptionThrown(context):
    line = context['line']
    chunks = context['chunks']

    if '|' in line:   #This is a new line always. 
        context['exception_multiline'] = False

    if context['exception'] == True:
        if context['exception_multiline'] == True:   #This is a new line without the exeption
            if line != '':
                obj = context['debugList'][-1]
                obj['line'] = obj['line'] + line

    if '|EXCEPTION_THROWN|' in line or 'FATAL_ERROR' in line:
        obj = setTimes(line,type='EXCEPTION',field='output',value=chunks[3])
        context['exception'] = True
        context['exception_multiline'] = True
        context['debugList'].append(obj)


def parseWfRule(context):
    workflow = {}
    line = context['line']
    chunks = context['chunks'] 
    if '|WF_RULE_EVAL' in line:
        if 'BEGIN' in chunks[1]:
            obj = setTimes(line,field='output',value='Workflow',type='RULE_EVAL')
            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            decreaseIdent_pop_setFields(context,type='RULE_EVAL',key='output',value='Workflow')
        #    obj = getFromList(context['openItemsList'],'output','Workflow')
        #    setTimes(line,obj)

    if '|WF_CRITERIA_' in line:
        if 'BEGIN' in chunks[1]:
            obj = setTimes(line,type='WF_CRITERIA')
            obj['nameId'] = chunks[2]
            obj['rulename'] = chunks[3]
            obj['rulenameId'] = chunks[4]

            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            obj =decreaseIdent_pop_setFields(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
            obj['result'] = chunks[2]
            obj['output'] = f"{obj['rulename']} --> {obj['result']}"

    if '|WF_ACTION|' in line:
        obj = getFromList(context['openItemsList'],'output','Workflow',delete=False)
        obj['action'] = chunks[2]

def parseMethod(context):
    line = context['line']
    chunks = context['chunks'] 
    if '|METHOD_' in line:
        if len(chunks)<4:
            print(line)
            return

        operation = chunks[1]
        method = getMethod(line)

        if 'ENTRY' in operation:
            obj = setTimes(line,type='METHOD')
            obj['method'] = method
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
            obj['output'] = obj['method']
            context['debugList'].append(obj)

            if '.getInstance' in method:
                pass
            else:
                context['openItemsList'].append(obj)
                increaseIdent()
        else:
            obj = getFromList(context['openItemsList'],'method',method)
            if obj == None:
                obj = getFromList(context['openItemsList'],'method',f"{method}",endsWith=True)

            if obj is not None:
                decreaseIdent()
                setTimes(line,obj)

            else:
                obj = setTimes(line,type='NO_ENTRY')
                obj['method'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
                context['debugList'].append(obj)

            if 'method' in obj:
                obj['output']=obj['method']
            else:
                obj['output']=obj['Id']
            
def parseVariableAssigment(context):
    line = context['line']
    chunks = context['chunks'] 

    if 'EXP_VAR' in _context and _context['EXP_VAR'] == True:
        if chunks[1] == 'VARIABLE_ASSIGNMENT' and chunks[2] == '[EXTERNAL]':
            obj = setTimes(line,type='VAR_ASSIGN')
            obj['type'] = 'VAR_ASSIGN'
            obj['subType'] = 'EXCEPTION'
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

            context['debugList'].append(obj)         
            obj['output'] = obj['string'] 

        else:
            _context['EXP_VAR'] = False
    if '|VARIABLE_ASSIGNMENT|' in line:
        if len(chunks) >= 5:

            if 'ExecutionException' in chunks[4] or 'ExecutionException' in chunks[4]:
                obj = setTimes(line,type='VAR_ASSIGN')
                obj['type'] = 'VAR_ASSIGN'
                obj['subType'] = 'EXCEPTION'
                obj['string'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

                context['debugList'].append(obj)
                obj['output'] = obj['string'] 

                _context['EXP_VAR'] = True

def parseDML(context):
    line = context['line']
    chunks = context['chunks']

    if '|DML_BEGIN|' in line:
        obj = setTimes(line,type="DML")
        obj['OP'] = chunks[3]
        obj['Type'] = chunks[4]
        obj['Id'] = chunks[2]
        obj['apexline'] = chunks[2][1:-1]
        obj['output'] = f"{obj['OP']} {obj['Type']}" 
        append_and_increaseIdent(context,obj)

    if '|DML_END|' in line:
        decreaseIdent_pop_setFields(context,'DML',key='Id',value=chunks[2])

def parseCallOutResponse(context):
    line = context['line']
    chunks = context['chunks']

    if 'CALLOUT_RESPONSE' in line:
        obj = setTimes(line,type='CALLOUT')
        #  obj['type'] = 'DEBUG'
        #  obj['subType'] = chunks[3]
        obj['string'] = chunks[3]
        obj['apexline'] = chunks[2][1:-1]

        context['debugList'].append(obj)  
        obj['output'] = obj['string'] 

def parseConstructor(context):
    line = context['line']
    chunks = context['chunks']

    if '|CONSTRUCTOR_ENTRY|' in line:
        obj = setTimes(line,field='output',value=chunks[5],type='CONSTRUCTOR')
        append_and_increaseIdent(context,obj)

    if '|CONSTRUCTOR_EXIT|' in line:
        decreaseIdent_pop_setFields(context,type='CONSTRUCTOR',key='output',value=chunks[5])

def parseCodeUnit(context):
    line = context['line']
    chunks = context['chunks']

    if '|CODE_UNIT_STARTED|' in line:
        obj = setTimes(line,type='CODE_UNIT')
        obj['output'] = chunks[4] if len(chunks)>4 else chunks[3]
        append_and_increaseIdent(context,obj)

    if '|CODE_UNIT_FINISHED|' in line:
        decreaseIdent_pop_setFields(context,'CODE_UNIT',key='output',value=chunks[2])

def parseNamedCredentials(context):
    line = context['line']
    chunks = context['chunks']

    if '|NAMED_CREDENTIAL_REQUEST|' in line:
        obj = setTimes(line,field='output',value=chunks[2],type='NAMED_CRD')
        append_and_increaseIdent(context,obj)

    if "|NAMED_CREDENTIAL_RESPONSE|" in line:
        obj = decreaseIdent_pop_setFields(context,type='NAMED_CRD',key='type',value='NAMED_CRD')

#flowParserList = [] 
def parseFlow(context):
    line = context['line']
    chunks = context['chunks']
    debugList = context['debugList']

    if '|FLOW_START_INTERVIEWS_BEGINxx|' in line:
        obj = setTimes(line,type='FLOW_START_INTERVIEWS',field='output',value='FLOW_START_INTERVIEWS')
        append_and_increaseIdent(context,obj)

    if '|FLOW_START_INTERVIEWS_ENDxx|' in line:
        decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEWS',key='output',value='FLOW_START_INTERVIEWS')

    if '|FLOW_START_INTERVIEW_BEGIN|' in line:
        obj = setTimes(line,type='FLOW_START_INTERVIEW')
        obj['Id'] = chunks[2]
        obj['Name'] = chunks[3]
        obj['output'] = obj['Name']
        obj['key'] = obj['Id']
        append_and_increaseIdent(context,obj)

    if '|FLOW_START_INTERVIEW_END|' in line:
        decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEW',value=chunks[2])


    if '|FLOW_ELEMENT_ERROR|' in line:
        obj = setTimes(line,type='FLOW_ELEMENT_ERROR')
        obj['message'] = chunks[2]
        obj['elementType'] = chunks[3]
        obj['elementName'] = chunks[4]
        obj['output'] = utils.CRED+ f"{obj['message']} in {obj['elementType']}:{obj['elementName']}" + utils.CEND
        debugList.append(obj)
        _context['EXCEPTION'] = True

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def printDebugList(debugList,logId,toFile=False):
    if toFile == True:
        filename = f"{restClient.logFolder()}{logId}_ansi.txt"

        original_stdout = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f 
            _printDebugList(debugList,logId)
            sys.stdout = original_stdout 
        data = file.read(filename)
        html = ansi2html.Ansi2HTMLConverter().convert(data)
        filename = f"{restClient.logFolder()}{logId}.html"
        file.write(filename,html)
        print(f"Html file: {filename}")
        clean = escape_ansi(data)
        filename = f"{restClient.logFolder()}{logId}.txt"
        file.write(filename,clean)  
        print(f"Txt file: {filename}")
 
    else:
        colorama.just_fix_windows_console()
        _printDebugList(debugList,logId)

def _printDebugList(debugList,logId):
    print()
    if logId != None:
        print(f"Parsing log Id {logId}    file: {restClient.logFolder()}{logId}.log")

    firstLines = True
    for num,d in enumerate(debugList):
        if d['type'] == 'LOGDATA':
            print(d['output'])
            continue
        else:
            if firstLines == True:
                firstLines = False
                print()
                print()
        if num != len(debugList) -1:
            if '*** getCpuTime() ***' in d['output']:
                continue
            if '*** getQueries() ***' in d['output']:
                continue
        printParsedLog(d)    

def processRepetition(debugList):
    def isRep(repss,x,parsedLine):
      if parsedLine['type'] not in ['METHOD','WF_CRITERIA']:
        return False,None

      for reps in repss:
        delta = reps[1]-reps[0]
        if x>= reps[0] and x <= reps[0] + len(reps) * delta - 1:
          if x>= reps[0] and x <= reps[0] + delta-1:
            if 'output' not in parsedLine:
                print()
            parsedLine['output'] = f"{parsedLine['output']}  *** {len(reps)},  {x-reps[0]+1}"
            if len(parsedLine['timeStamp'])>1:
                parsedLine['timeStamp'][1] = debugList[x+(len(reps)-1)*delta]['timeStamp'][1]
            return True,parsedLine
          else:
            return True,None

      return False,None

    for deb in debugList:
        if 'output' not in deb:
            print()
    repss = utils.repeatingSequence(debugList,"output")

    parsedX = []
    for x,parsedLine in enumerate(debugList):
        isrepe, obj = isRep(repss,x,parsedLine)
        if isrepe == True and obj == None:
            continue
        parsedX.append(parsedLine)

    return parsedX   

def getMethod(line):
    chunks = line.split('|')
    if len(chunks) == 4:
        method = chunks[3]
    else:
        method = chunks[4]
    if '(' in method:
        method = method.split('(')[0]
    return method

def getTime(line):
    chunks = line.split('|')
    return chunks[0].split(' ')[0]

def getTimeStamp(line):
    chunks = line.split('|')
    return int ((chunks[0].split('(')[1]).split(')')[0])

def increaseIdent(context=None):
    if context == None:
        _context['ident'] = _context['ident'] + 1
    else:
        context['ident'] = context['ident'] + 1

def decreaseIdent(context=None):
    if context == None:
        _context['ident'] = _context['ident'] - 1
    else:
        context['ident'] = context['ident'] - 1

def emptyString(size,char=' ',ident=None):
    str = ''
    if ident is None:
        ident = _context['ident']
    length = ident * size
    for x in range(length):
        str = str + char  
    return str     

def rootString():
    str = ''
    length = _context['ident'] 
    if length == 0:
        return ''
    for x in range(length-1):
        str = str + '⎮'
    str = str + '⌈' 

    return str     

bufVal=''
buffer=''
previousEnd = False

prevTS = 0


def printParsedLog(d):

   # CEND    = '\33[0m'
   # CRED    = '\33[31m'
   # CGREEN  = '\33[32m'
   # CYELLOW = '\33[33m'
   # CBLUE   = '\33[34m'
   # CMAGENTA = '\033[35m'
   # CCYAN   = '\033[36m'
   # CWHITE  = '\33[37m'

    Cinit = utils.CEND

    _plimit=' '
 

    if d['type'] == 'LIMITS':
        _context['previousIsLimit'] = True
        return
    if _context['previousIsLimit'] == True:
        _plimit = '*' 
        _context['previousIsLimit'] = False

    if 'ident' not in d:
        print()
    level = d['ident']
    if _context['logLevel'] != None:
        if level > int(_context['logLevel']):
            return

    _type = d['type']
    if _type == 'DEBUG':
        _type = f"{d['type']}-{d['subType']}"
        Cinit = utils.CRED if d['subType'] == 'ERROR' else utils.CGREEN

    if d['type'] == 'EXCEPTION':
        Cinit = utils.CRED

    if _type == 'VAR_ASSIGN':
        if d['subType'] == 'EXCEPTION':
            Cinit = utils.CRED
        else:
            return

    if d['type'] == 'SOQL':
        Cinit = utils.CCYAN
    if d['type'] == 'DML':
        Cinit =  utils.CYELLOW
    if d['type'] == 'CODE_UNIT':
        Cinit =  utils.CPURPLE

    i = f"{emptyString(1,' ',level)}."
    i= level
    identation = f"{emptyString(3,' ',level)}"

    if 'output' not in d:
        print()
    val = d['output']

    if val == '':
        print()
    
    val = Cinit +f"{identation}{val}"

    _apexline = d['apexline'] if 'apexline' in d else ''

    _totalQueriesTrace = delta(d,'totalQueries') 
    spacer = '_' if d['type'] == 'SOQL' else '.'
    _totalQueriesTrace = f"{level:2}:{emptyString(1,spacer,level)}{_totalQueriesTrace}" if _totalQueriesTrace >0 else ' '

    _cpuTime0 = int(d['CPUTime'][0])
    _cpuTime1 = int(d['CPUTime'][1]) if len(d['CPUTime']) >1 else ''
    _timeStamp1 = d['timeStamp'][1] if len(d['timeStamp'])>1 else d['timeStamp'][0]

    _totalQueries0 = d['totalQueries'][0]
    _totalQueries1 = d['totalQueries'][1] if len(d['SOQLQueries']) >1 else _totalQueries0
    _totalQueriesD = _totalQueries1-_totalQueries0

    _cpuPrevD = _cpuTime0 - int(_context['previousCPUTime'])

    if level == _context['prevLevel']:
        _elapsedPrevD = d['timeStamp'][0] - _context['prevTimes'][level][1]

    if level > _context['prevLevel']:
        _elapsedPrevD = d['timeStamp'][0] - _context['prevTimes'][_context['prevLevel']][0]

    if level<_context['prevLevel']:
        _elapsedPrevD = d['timeStamp'][0] - _context['prevTimes'][level][1]

    if _elapsedPrevD <0:
        if '***' in d['output']:
            _elapsedPrevD = d['timeStamp'][0] - _context['prevTimes'][level][0]

    _context['prevTimes'][level] = [d['timeStamp'][0],_timeStamp1]

    _elapsedPrevD = ms(_elapsedPrevD)

    _context['prevLevel'] = level

    _exp = "!" if d['exception'] == True else ''

    _sql2 = d['SOQLQueries'][1] if len(d['SOQLQueries'])>1 else ''
    _sqlcmt2 = d['cmtSOQLQueries'][1] if len(d['cmtSOQLQueries'])>1 else d['cmtSOQLQueries'][0]

    _context['previousCPUTime'] = _cpuTime0
    _context['previousElapsedTime']  = d['elapsedTime']

    if d['type'] in ['SOQL','DML','VAR_ASSIGN'] and level == 0:
        _typeColor =utils. CYELLOW 
    else:
         _typeColor = ''

    if _cpuPrevD == 0:
        _cpuPrevD = ''
        _cpuTime0 = ''
        _cpuTime1 = ''
    if _cpuTime1 == '':
        _cpuTime1 = _cpuTime0
 #   if _cpuTime1!='' and int(_cpuTime1)>10000:
 #       _cpuTime1 = utils.CLIGHT_RED + f"{_cpuTime1:6}" + CEND
    if _totalQueriesD==0:
        _totalQueriesD = ''
    if _totalQueries1 ==0:
        _totalQueries1 = ''
    if _sql2 ==0:
        _sql2=''
    if _sqlcmt2==0:
        _sqlcmt2=''
    #_delta = ms(delta(d,'timeStamp'))
    _delta = f"{delta(d,'timeStamp')/1000000:.2f}"
    if _delta == "0.00":
        _delta =''
   # if _delta!='' and float(_delta)<10:
   #     _delta = utils.CDARK_GRAY + f"{_delta:>10}" + CEND


    if 1==2:
        if _context['firstLineOut'] == True:
            print(f"{' ':15}|{'time(ms)':10}|{'elapsed':10}|{'time1(ns)':12}|{'time2(ns)':12}|{'ExecTime':10}|{'QueriesStack':15}|{'Qd':4}|{'Qt':4}|{'L':1}|{'cpuD':6}|{'CPUin':6}|{'CPUout':6}|{'Q':3}|{'Qcm':3}|{'type':12}|{'E':1}|{'al':4}{'':50}")
            _context['firstLineOut'] = False

        print(f"{i:15} {ms(d['elapsedTime']):10}|{_elapsedPrevD:8}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_delta:10}|{_totalQueriesTrace:15}|{_totalQueriesD:4}|{_totalQueries1:4}|{_plimit:1}|{_cpuPrevD:6}|{_cpuTime0:6}|{_cpuTime1:6}|{_sql2:3}|{_sqlcmt2:3}|{_typeColor}{_type:12}{utils.CEND}|{_exp:1}|{_apexline:>4}|{val[:150]:50}"+utils.CEND)
    else:
        if _context['firstLineOut'] == True:
            print(f"{'time(ms)':10}|{'elapsed':10}|{'time1(ns)':12}|{'time2(ns)':12}|{'t2-t1':10}|{'Qd':4}|{'Qt':4}|{'cpuD':6}|{'CPUin':6}|{'Q':3}|{'Qcm':3}|{'type':21}|{'al':4}{'':50}")
            _context['firstLineOut'] = False

        print(f"{ms(d['elapsedTime']):10}|{_elapsedPrevD:8}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_delta:>10}|{_totalQueriesD:4}|{_totalQueries1:4}|{_cpuPrevD:6}|{_cpuTime1:6}|{_sql2:>3}|{_sqlcmt2:>3}|{_typeColor}{_type:21}{utils.CEND}|{_apexline:>4}| {val[:150]:50}"+utils.CEND)

logsList = []
def ms(val):
    return f"{val/1000000:10.2f}"
def printIdent(string,ident):
    str = ''
    for x in range(_context['ident'] * 3):
        str = str + ' '
    print(str + string)


def popFromList(context,type,value,key='key',endsWith=False):
    openItemsList = context['openItemsList']
    try:
        for i,obj in enumerate(openItemsList):
            if obj['type'] == type:
                if endsWith == True:
                    if key not in obj:
                        continue
                    if obj[key].endswith(value) or obj[key].startswith(value):
                        openItemsList.pop(i)
                        return obj    
                else:
                    if key not in obj:
                        continue
                    if obj[key] == value:
                        openItemsList.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None

def getFromList(theList,field,value,endsWith=False,delete=True):
    try:
        for i,obj in enumerate(theList):
            if field in obj:
                if endsWith == True:
                    if obj[field].endswith(value) or obj[field].startswith(value):
                        if delete == True:
                            theList.pop(i)
                        return obj    
                else:
                    if obj[field] == value:
                        if delete==True:
                            theList.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None

def getFromListX(theList,field,value):
    try:
        for i in range(len(theList)):
            obj = theList[len(theList)-i-1]

            if obj[field] == value:
                theList.pop(len(theList)-i-1)
                return obj

        for i in range(len(theList)):
            obj = theList[len(theList)-i-1]

            if value in obj[field]:
                theList.pop(len(theList)-i-1)
                return obj
    except Exception as e:
        print(e)
        return None
    return None    

