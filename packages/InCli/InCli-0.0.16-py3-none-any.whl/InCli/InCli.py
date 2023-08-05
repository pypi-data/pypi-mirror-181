import json
from .SFAPI import Sobjects, query,restClient,jsonFile,utils,objectUtil,debugLogs,digitalCommerceUtil
import logging
import simplejson,sys
from operator import itemgetter
from inspect import getmembers, isfunction
import traceback


varsFile = 'confIcli.json'
vars = None


def readVars(field=None):
    global vars
    vars = jsonFile.read(varsFile)

    if field != None:
        return vars[field]
    return vars

def setVar(name,value):

    vars = jsonFile.read(varsFile)
    vars[name]=value
    jsonFile.write(varsFile,vars)
    print(simplejson.dumps(vars, indent=4))

def getParam(argv,key,i=1):
    if key not in argv:
        return None

    ind = argv.index(key)
    if (ind+i <= (len(argv)-1)):
        arg = argv[ind+i]
        if arg[0] == '-':
            return None
        return arg
    return None

def listEnvs():
    cons = restClient.getConfigOrgs()
    cons = sorted(cons,key=itemgetter('name'))
    utils.printFormated(cons,fieldsString='name:isSandBox:instance_url:login.username:login.password:login.bearer')
    env = readVars('environment')
    print(f"Current Environment is {env}")

def _queryAndPrint(q,fields=None,systemFields=True,nullFields=False):

    res = query.queryRecords(q)
    if fields != None:
        res = utils.deleteNulls(res,systemFields,nullFields)
        if fields=='all':
            utils.printFormated(res)
        else:
            utils.printFormated(res,fields)
    else:
        res = utils.deleteNulls(res,systemFields,nullFields)
        print(simplejson.dumps(res, indent=4))
    
    print()
    print(f"Null values printed-> {nullFields}  systemFields printed--> {systemFields}")

def option_q(args):
    if '-h' in args:
        help = f"""
        {utils.CGREEN}-q "select..."{utils.CEND} query to execute. System Fields, such as LastModifiedDate, and null fields are not returned. 
            {utils.CGREEN}-null{utils.CEND} - will print fields with null values
            {utils.CGREEN}-system{utils.CEND} - will print the system fields
            {utils.CGREEN}-all{utils.CEND} - will print both nulls and system fields
            {utils.CGREEN}-fields "a:b:c:..."{utils.CEND} --> print in table format the specified fields.
            {utils.CGREEN}-fields all{utils.CEND} --> print in table format"""
        return help

    #else:
    q = getParam(args,'-q')

    fields = getParam(args,'-fields') if '-fields' in args else None    
    nullFields = True if '-null' in args else False
    systemFields = True if '-system' in args else False
    all = True if '-all' in args else False
    if all == True:
        nullFields = True
        systemFields = True

    connectionInit(args)

    _queryAndPrint(q,fields=fields,systemFields=systemFields,nullFields=nullFields)

def option_checkCatalogs(args):
    if '-h' in args:
        help = f"""
        {utils.CGREEN}-checkCatalogs{utils.CEND} 
            Checks the catalogs. Gets all catalogs, does a getOffers, getOfferDetails, basketwithoutconfig and basket with config
            path: the path to a child product to configure. Path = ... ProductCode ... ProdcutCode
            quantity: the quantity for the object""" 
        return help

    connectionInit(args)

   # path = getParam(args,'-checkCatalogs')
   # quantity = getParam(args,'-checkCatalogs',2)

    digitalCommerceUtil.checkOffers()

    print()

def option_d(args):
    help = f"""
        {utils.CGREEN}-d objectName{utils.CEND} --> Describe an object
            {utils.CGREEN}-d objectName:fieldName{utils.CEND} --> describe a field in the objec"""
    if '-h' in args:
        return help    

    connectionInit(args)

    objectField = getParam(args,'-d')
    if objectField == None:
        print(help)
        return

    ofs = objectField.split(':')

    sObjectName = ofs[0]
    fieldName = ofs[1] if len(ofs) > 1 else None

    res = Sobjects.describe(sObjectName)
    if fieldName == None:
        print(simplejson.dumps(res['fields'], indent=4))
    else:
        sibbling = objectUtil.getSiblingWhere(res['fields'],'name',fieldName)['object']

        print(simplejson.dumps(sibbling, indent=4))

def option_l(args):
    if '-h' in args:
        help = f"""
        {utils.CGREEN}-l{utils.CEND} --> current org limits consuptions. """
        return help
    connectionInit(args)
    action = '/services/data/v51.0/limits'
    res = restClient.callAPI(action)
    records = []
    for key in res.keys():
        record = {
            'Limit':key,
            'Max':res[key]['Max'],
            'Remaining':res[key]['Remaining'],
        }
        record['Percent Remaining'] =  100 *(res[key]['Remaining']/res[key]['Max']) if res[key]['Max']>0 else 0
        record['__color__'] = ''

        if record['Max'] != 0:
            if record['Percent Remaining']<50:
                record['__color__'] = utils.CYELLOW
            if record['Percent Remaining']<25:
                record['__color__'] = utils.CYELLOW
        records.append(record)

    utils.printFormated(records)

def option_o(args):
    if '-h' in args:
        help = f"""
        {utils.CGREEN}-o{utils.CEND} --> List all Objects
            {utils.CGREEN}objectName{utils.CEND}  --> get one row from the object
            {utils.CGREEN}objectName:Id{utils.CEND} --> get the row especified by the Id
            {utils.CGREEN}-like name{utils.CEND} --> where the Name contains the substring name"""

        return help
        
    connectionInit(args)

    if '-name' in args:
        obj = getParam(args,'-name')
        chunks = obj.split(':')

        if len(chunks) == 1:
            q = f"select fields(all) from {chunks[0]} limit 1"
        else:
            q = f"select fields(all) from {chunks[0]} where Id='{chunks[1]}'"

        print('pre q:'+q)
        _queryAndPrint(q,systemFields=True,nullFields=True)
        return
        
    like = getParam(args,'-like') if '-like' in args else None    
    count = True if '-count' in args else False   

    objs = Sobjects.listObjects()
    if like is not None:
        if ':' not in like:
            like = f"name:{like}"        
        ls = like.split(':')
        outs = []
        for obj in objs:
      #      print(f"{str(ls[1])} . {str(obj[ls[0]])}")
            if str(ls[1]).lower() in str(obj[ls[0]]).lower():
                outs.append(obj) 
    else:
        outs = objs

    if count==True:
        for out in outs:
            if out['queryable'] == True:
                print("Quering objects row count.")
                print("", end=".")          
                try:
                    if out['name'] == 'AccountUserTerritory2View':
                        print()
                    c = query.query(f" select count(Id) from {out['name']}",raiseEx=True)
                    out['count'] = c['records'][0]['expr0']
                except Exception as e:
                    out['count'] = 'E'
            else:
                out['count'] = '-'
    
    #print(simplejson.dumps(objs, indent=4))
    utils.printFormated(outs,'name:label:associateParentEntity:associateParentEntity:queryable:count')

def option_default(args):
    help = f"""
        {utils.CGREEN}-default:set key value{utils.CEND} --> defaults the specified key-value
        {utils.CGREEN}-default:del key  {utils.CEND}  --> deletes the default
        {utils.CGREEN}-default:get key  {utils.CEND}  --> displays the current value
        """

    if '-h' in args:
        return help   

    if "-default:del" in args:
        key = getParam(args,'-default:del',1)
        if key == None:
            restClient.glog().info(f'Key not found in the provided arguments. {args}')
            return 
        restClient.delConfigVar(key)
        return

    if "-default:set" in args: 
        key = getParam(args,'-default:set',1)
        value = getParam(args,'-default:set',2)
        if key == None or value==None:
            print(help)
            return

        restClient.setConfigVar(key,value)
        print(f"Default value for {key} is {value}")

    if "-default:get" in args: 
        key = getParam(args,'-default:get',1)
        value =restClient.getConfigVar(key)
        print(f"Default value for {key} is {value}")

#def option_history(args):
#    return
#    if '-h' in args:
        help = """
        -history"""
        return help
#    print()
#    print('HISTORY:')
#    vars = jsonFile.read(varsFile)
#    for line in vars['history']:
        print(line)

def option_logs(args):
    help = f"""
        {utils.CGREEN}-logs{utils.CEND} --> list logs in the org. 
            {utils.CGREEN}-limit X{utils.CEND}, where X specifies the number of logs to list. Default 50 max 50K
            {utils.CGREEN}-loguser field:value{utils.CEND}, filter the logs for the specified user. The user can be specified by any field in the User Object. 
                Examples:
                    "Id:XXXXXXXX"
                    "name:Onboarding Site Guest User"
                    "Alias:John.Doe"
                    "FirstName:Onboarding"
                    "ProfileId:00e3O000000IHneQAG"
                {utils.CPURPLE}Defaultable loguser{utils.CEND}: Can be set to default. -default:set loguser "Alias:John.Doe"
        {utils.CGREEN}-logs Id{utils.CEND} --> parse the logs with the provided Id
        {utils.CGREEN}-logs -last X {utils.CEND}--> parses the last X logs. 
        """

    if '-h' in args:
        return help

    logId = getParam(args,'-logs')    
    last = getParam(args,'-last')  
    limit = getParam(args,'-limit')    
    level = getParam(args,'-level') 
    loguser = getParam(args,'-loguser') 

    if loguser == None:
        loguser = restClient.getConfigVar('loguser')

    if logId == None and last== None:
        connectionInit(args)
        lim = 50 if limit == None else limit
        id = None
        if loguser != None:
            chunks = loguser.split(":")
            key = chunks[0] if len(chunks)>1 else 'Id'
            value = chunks[1] if len(chunks)>1 else chunks[0]
            id = query.queryField(f"Select Id from User where {key}='{value}'") if key.lower()!='id' else value
            if id == None:
                utils.raiseException('QUERY',f"User with field {key} = {value} does not exist in the User Object.")
        if id != None:
            print(f"Logs for user {loguser}, id:{id}")
        debugLogs.printLogs(logUserId=id,limit=lim)
        return

    connectionInit(args)
    debugLogs.parseLog(logId,lastN=last,level=level)

    return

def option_h(args):
    module = __import__('InCli')

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    for f in functions:
        if f == 'option_h':
            continue

        print(eval(f'{f}(args)'))      

def connectionInit(argsIn):

    userName_or_ofgAlias = getParam(argsIn,'-u') 
    restClient.init(userName_or_ofgAlias)

def _main(argsIn):
    restClient.setLoggingLevel(logging.INFO)

    if '-h' in argsIn:
        help = f"""
    {utils.CGREEN}-u{utils.CEND} --> username or org alias to be used to log into the org. 
            {utils.CPURPLE}Defaultable u{utils.CEND}: Can be set to a default value --> -default:set u "xx@adas.com"
    """
        print(help)

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    args = []
    for argv in argsIn:
        if argv == '|':
            break
        args.append(argv)

    for arg in args:
        ar = arg.split(':')[0][1:]
        ar = f"option_{ar}"
        if ar in functions:
        #       module = __import__('InCli')
            eval(f'{ar}(args)')
        #      func = getattr(module, ar)
        #      func(args)

    if '-h' in argsIn:
        print()
        print(utils.CBOLD+"SFDX Commands:"+utils.CEND)
        print(f" - {utils.CGREEN}sfdx force:org:list --verbose --all {utils.CEND}--> to list all authorized Orgs and Connection Status")
        print(f" - {utils.CGREEN}sfdx auth:web:login -r 'Instance Url' -a 'Alias' {utils.CEND}--> to re-authorize")
        print(f" - {utils.CGREEN}sfdx auth:web:login -u 'userName'  -a 'alias' {utils.CEND}--> to authorize and Org")
        print()

def main():
    argsIn = sys.argv
    try:
        _main(argsIn)

    except Exception as e:
        utils.printException(e)
        traceback.format_exc()

if __name__ == '__main__':
    main()

