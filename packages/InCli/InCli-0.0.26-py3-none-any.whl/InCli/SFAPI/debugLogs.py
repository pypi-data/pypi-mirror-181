from . import restClient,query,digitalCommerceUtil,file,utils,objectUtil
import simplejson,logging

import colorama
import sys
import ansi2html,re

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
#    log = query.queryRecords(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog where Id ='{logId}' limit 1")

    if logRecords == None or len(logRecords)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLogwith Id {logId}")    
    logRecord = logRecords[0]
 #   logLine = f"""LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']}    Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}    lenght: {log['LogLength']}    duration: {log['DurationMilliseconds']}    startTime: {log['StartTime']} 
#LOGDATA:    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}
 #   """    

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
   # callbody = logLine + callbody
    return logRecord,logbody

def parseLog(logId=None,filepath=None,printLimits=True,userDebug=True,lastN=1,logUserId=None,level=None,whereClause=None,writeToFile=False):
    body = None

    if filepath != None:
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
        where = f" where {whereClause} " if whereClause is not None else ''
        where = f" where logUserId='{logUserId}' " if logUserId is not None else where

        q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
        logIds = query.queryFieldList(f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}")
        if logIds == None or len(logIds)==0:
            utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)
        for logId in logIds:
            print('___________________________________________________________________________________________________________________________________________________________________')
            parseLog(logId,filepath=filepath,printLimits=printLimits,writeToFile=writeToFile)
        return  

    if body == None :
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found. ')

    if len(body)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{logId}> is empty. ')

    if filepath == None:
        filename = f"{restClient.logFolder()}{logId}.log"
        file.write(filename,body)

    return parse(logId,body,printLimits=printLimits,userDebug=userDebug,level=level,writeTofile=writeToFile)

def printLogs(logUserId=None,limit=50,whereClause=None):
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

    if _context['exception'] == True and obj['exception'] == False:
        obj['exception'] = True
        _context['exception'] = False

    if obj['type'] is None:
        print()

    if field is not None:
        obj[field] = chunks[chunkNum] if value is None else value

    if _context['timeZero'] == 0:
        _context['timeZero'] = obj['timeStamp'][0]

    obj['elapsedTime'] = obj[f'timeStamp'][0] - _context['timeZero']

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

    for num,line in enumerate(lines):

        chunks = line.split('|')

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

        if '|USER_INFO|' in line:
            obj = setTimes(line,field='string',value=chunks[4],type='USER_INFO')
            debugList.append(obj)
            obj['output'] = obj['string'] 


        if '|' in line:   #This is a new line always. 
            multiLine = None
        
        if exceptionDict is not None:
            if multiLine != 'EXCEPTION':   #This is a new line without the exeption
                exceptionDict['output'] = ""
                debugList.append(exceptionDict.copy())
                exceptionDict = None
                multiLine = None
            else:
                if line != '':
                    exceptionDict['line'] = exceptionDict['line'] + line
        if '|EXCEPTION_THROWN|' in line or 'FATAL_ERROR' in line:
            exceptionDict = {
                'line': line,
                'type': 'EXCEPTION'
            }
            _context['exception'] = True
            multiLine = 'EXCEPTION'


        if 'EXP_VAR' in _context and _context['EXP_VAR'] == True:
            if chunks[1] == 'VARIABLE_ASSIGNMENT' and chunks[2] == '[EXTERNAL]':
                obj = setTimes(line,type='VAR_ASSIGN')
                obj['type'] = 'VAR_ASSIGN'
                obj['subType'] = 'EXCEPTION'
                obj['string'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

                debugList.append(obj)         
                obj['output'] = obj['string'] 
   
            else:
                _context['EXP_VAR'] = False
        if '|VARIABLE_ASSIGNMENT|' in line:
            if len(chunks) >= 5:
                if 'ExecutionException' in chunks[4]:
                    obj = setTimes(line,type='VAR_ASSIGN')
                    obj['type'] = 'VAR_ASSIGN'
                    obj['subType'] = 'EXCEPTION'
                    obj['string'] = chunks[4]
                    obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

                    debugList.append(obj)
                    obj['output'] = obj['string'] 

                    _context['EXP_VAR'] = True
 
        if '|LIMIT_USAGE|' in line:
            if '|SOQL|' in line:
                _context[f'DEF:SOQL queries'] = chunks[4]

        if '|LIMIT_USAGE_FOR_NS|' in line:
            limits = chunks[2]
            if limits == '(default)':
                limits = 'DEF:'
            elif limits == 'vlocity_cmt':
                limits = 'CMT:'
            else:
                limits = f"{limits}:"

            limitsDict = setTimes(line,type='LIMITS')
            limitsDict['limitType'] = limits
            limitsDict['output'] = limitsDict['limitType']

        if limits is not None and line == ' ':
            limits = None
        
        if limits is not None:
            chunks = line.split(' ')
            if 'SOQL queries' in line:
                _context[f'{limits}SOQL queries'] = chunks[6]
            if 'CPU time' in line:
                _context[f'{limits}CPU time'] = chunks[5]

        if limits is not None and line =='':
            setTimes(limitsDict['lines'][0],limitsDict)
            s = f"limits-{limits.lower()} {limitsDict['time'][0]}"
            if _context['printLimits'] == True:
                debugList.append(limitsDict)
            limits = None   


        if '*** getCpuTime() ***' in line:
            chs = chunks[4].split(' ')
            _context[f'DEF:CPU time'] = chs[4]
        if '*** getQueries() ***' in line:
            chs = chunks[4].split(' ')
            _context[f'DEF:SOQL queries'] = chs[4]

        if '|USER_DEBUG|' in line:
            multiLine = 'DEBUG'
        if multiLine == 'DEBUG':
            if '|' in line:
                obj = setTimes(line,type='DEBUG')
                obj['type'] = 'DEBUG'
                obj['subType'] = chunks[3]
                obj['string'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1]

            else:
                obj = debugList[-1].copy()
                obj['string'] = line
        #    if _context['userDebug'] == True:
            debugList.append(obj)
            obj['output'] = obj['string'] 


        if 'NAMED_CREDENTIAL_' in line:
            if "REQUEST" in chunks[1]:
                obj = setTimes(line,field='string',value=chunks[2],type='NAMED_CRD')
                onGoingCalls.append(obj)
                increaseIdent()    
                debugList.append(obj)
                obj['output'] = obj['string'] 

            if "NAMED_CREDENTIAL_RESPONSE" == chunks[1]:
                decreaseIdent()
                obj = delFromList(onGoingCalls,'type','NAMED_CRD')
                setTimes(line,obj) 

        if 'CALLOUT_RESPONSE' in line:
            obj = setTimes(line,type='CALLOUT')
          #  obj['type'] = 'DEBUG'
          #  obj['subType'] = chunks[3]
            obj['string'] = chunks[3]
            obj['apexline'] = chunks[2][1:-1]

            debugList.append(obj)  
            obj['output'] = obj['string'] 
 

        if '|WF_RULE_EVAL' in line:
            if 'BEGIN' in chunks[1]:
                workflow = setTimes(line,field='method',value=chunks[2],type='RULE_EVAL')

            if 'END' in chunks[1]:
                setTimes(line,workflow)
        if '|WF_ACTION|' in line:
            workflow['action'] = chunks[2]

        if '|CONSTRUCTOR_' in line:
            if 'ENTRY' in chunks[1]:      
                obj = setTimes(line,field='method',value=chunks[5],type='CONSTRUCTOR')
                constructorList.append(obj)
                increaseIdent()    
                debugList.append(obj)

            if 'EXIT' in chunks[1]:    
                decreaseIdent()
                obj = delFromList(constructorList,'method',chunks[5])
                setTimes(line,obj)   
                obj['output'] = obj['method'] 

         
        if '|CODE_UNIT_' in line:
            if 'STARTED' in chunks[1]:
                obj = setTimes(line,type='CODE_UNIT')
                obj['trigger'] = chunks[3]  if len(chunks)>4 else ''
                obj['method'] = chunks[4] if len(chunks)>4 else chunks[3]
                codeUnitsList.append(obj)
                increaseIdent()
                debugList.append(obj)

            if 'FINISHED' in chunks[1]:
                decreaseIdent()
                obj = delFromList(codeUnitsList,'method',chunks[2])
                setTimes(line,obj)
                obj['output'] = obj['method']


        if '|DML_' in line:
            if 'BEGIN' in chunks[1]:
                obj = setTimes(line,type="DML")
                obj['OP'] = chunks[3]
                obj['Type'] = chunks[4]
                obj['Id'] = chunks[2]
                obj['apexline'] = chunks[2][1:-1]
                dmlList.append(obj)
                increaseIdent()
                debugList.append(obj)

            if 'END' in chunks[1]:
                obj = delFromList(dmlList,'Id',chunks[2])
                setTimes(line,obj)
                decreaseIdent()
                obj['output'] = f"{obj['OP']} {obj['Type']}" 


        if 'SOQL_EXECUTE_' in line:
            if 'BEGIN' in chunks[1]:
                SOQL = setTimes(line,field='query',value=chunks[4],type="SOQL")
                SOQL['object'] = chunks[4].lower().split(' from ')[1].strip().split(' ')[0]
                SOQL['apexline'] = chunks[2][1:-1]

                a= 1
                debugList.append(SOQL)

            if 'END' in chunks[1]:
                _context['totalQueries'] = _context['totalQueries'] + 1
                setTimes(line,SOQL)
                SOQL['rows'] = chunks[3].split(':')[1]

                soql = SOQL['query'].lower()

                _from = soql.split(' from ')[-1].strip()
                _from = _from.split(' ')[0]

                SOQL['output'] = f"Select: {_from} --> {SOQL['rows']} rows"

             #   if len(SOQL['query']) > 180:
             #       if 'from' in SOQL['query'].lower():
             #           SOQL['query'] = SOQL['query'].replace('from',"FROM")
             #           SOQL['query'] = SOQL['query'].replace('From',"FROM")

            #        SOQL['query'] = f"{SOQL['query'].split(' ')[0]} ... FROM {SOQL['query'].split('FROM')[1]}"

        if '|METHOD_' in line:
            if len(chunks)<4:
                print(line)
                continue

            operation = chunks[1]
            method = getMethod(line)

            if 'ENTRY' in operation:
                obj = setTimes(line,type='METHOD')
                obj['method'] = method
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
                obj['output'] = obj['method']
                debugList.append(obj)

                if '.getInstance' in method:
                    pass
                else:
                    methodsList.append(obj)
                    increaseIdent()
            else:
                obj = delFromList(methodsList,'method',method)
                if obj == None:
                    obj = delFromList(methodsList,'method',f"{method}",endsWith=True)

                if obj is not None:
                    decreaseIdent()
                    setTimes(line,obj)

                else:
                    obj = setTimes(line,type='NO_ENTRY')
                    debugList.append(obj)

                if 'method' in obj:
                    obj['output']=obj['method']
                else:
                    obj['output']=obj['Id']

    repDebugList = processRepetition(debugList)
    printDebugList(repDebugList,logId,writeTofile)

    print()

    return debugList

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
    print(f"Parsing log Id {logId}    file: {restClient.logFolder()}{logId}.log")

    firstLines = True
    for d in debugList:
        if d['type'] == 'LOGDATA':
            print(d['output'])
            continue
        else:
            if firstLines == True:
                firstLines = False
                print()
                print()
        if '*** getCpuTime() ***' in d['output']:
            continue
        printParsedLog(d)    

def processRepetition(debugList):
    def isRep(repss,x,parsedLine):
      if parsedLine['type'] != 'METHOD':
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

def increaseIdent():
    _context['ident'] = _context['ident'] + 1

def decreaseIdent():
    _context['ident'] = _context['ident'] - 1

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

    CEND    = '\33[0m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CMAGENTA = '\033[35m'
    CCYAN   = '\033[36m'
    CWHITE  = '\33[37m'

    Cinit = CEND

    _plimit=' '
    if d['type'] == 'EXCEPTION':
        print(CRED + d['line'] + CEND)
        return

    if d['type'] == 'LIMITS':
        _context['previousIsLimit'] = True
        return
    if _context['previousIsLimit'] == True:
        _plimit = '*' 
        _context['previousIsLimit'] = False

    level = d['ident']
    if _context['logLevel'] != None:
        if level > int(_context['logLevel']):
            return

    _type = d['type']
    if _type == 'DEBUG':
        _type = f"{d['type']}-{d['subType']}"
        Cinit = CRED if d['subType'] == 'ERROR' else CGREEN

    if _type == 'VAR_ASSIGN':
        if d['subType'] == 'EXCEPTION':
            Cinit = CRED
        else:
            return

        
    if d['type'] == 'SOQL':
        Cinit = CCYAN
    if d['type'] == 'DML':
        Cinit =  CYELLOW
    if d['type'] == 'CODE_UNIT':
        Cinit =  CMAGENTA

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
        _typeColor = CYELLOW 
    else:
         _typeColor = ''

    if _cpuPrevD == 0:
        _cpuPrevD = ''
        _cpuTime0 = ''
        _cpuTime1 = ''
    if _cpuTime1!='' and int(_cpuTime1)>10000:
        _cpuTime1 = utils.CLIGHT_RED + f"{_cpuTime1:6}" + CEND
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

        print(f"{i:15} {ms(d['elapsedTime']):10}|{_elapsedPrevD:8}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_delta:10}|{_totalQueriesTrace:15}|{_totalQueriesD:4}|{_totalQueries1:4}|{_plimit:1}|{_cpuPrevD:6}|{_cpuTime0:6}|{_cpuTime1:6}|{_sql2:3}|{_sqlcmt2:3}|{_typeColor}{_type:12}{CEND}|{_exp:1}|{_apexline:>4}|{val[:150]:50}"+CEND)
    else:
        if _context['firstLineOut'] == True:
            print(f"{'time(ms)':10}|{'elapsed':10}|{'time1(ns)':12}|{'time2(ns)':12}|{'t2-t1':10}|{'Qd':4}|{'Qt':4}|{'cpuD':6}|{'CPUin':6}|{'Q':3}|{'Qcm':3}|{'type':12}|{'E':1}|{'al':4}{'':50}")
            _context['firstLineOut'] = False

        print(f"{ms(d['elapsedTime']):10}|{_elapsedPrevD:8}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_delta:>10}|{_totalQueriesD:4}|{_totalQueries1:4}|{_cpuPrevD:6}|{_cpuTime1:6}|{_sql2:>3}|{_sqlcmt2:>3}|{_typeColor}{_type:12}{CEND}|{_exp:1}|{_apexline:>4}| {val[:150]:50}"+CEND)

logsList = []
def ms(val):
    return f"{val/1000000:10.2f}"
def printIdent(string,ident):
    str = ''
    for x in range(_context['ident'] * 3):
        str = str + ' '
    print(str + string)


def delFromList(theList,field,value,endsWith=False):
    try:
        for i,obj in enumerate(theList):
            if field in obj:
                if endsWith == True:
                    if obj[field].endswith(value) or obj[field].startswith(value):
                        theList.pop(i)
                        return obj    
                else:
                    if obj[field] == value:
                        theList.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None

def delFromListX(theList,field,value):
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

