import json

def build_response(fragment, parameters):
    print('fragment type: ' + str(type(fragment)))
    try:
        assert 'Object' in fragment, "Object key does not exist"
        print('keys list len = ' + str(len(fragment.keys())))
        assert len(fragment.keys()) == 1, "Input object has more than 1 key"
        for item in fragment.items():
            print('item ' + ' = ' + json.dumps(item))
            print('stringified fragment: ' + json.dumps(fragment))
            stringified_fragment = json.dumps(fragment)
            assert stringified_fragment.find(parameters['iteratorplaceholder']) != -1, "no placeholder found"
            iterated_list = []
            for item in parameters['iteratorlist']:
                stringified_output_fragment = stringified_fragment.replace(parameters['iteratorplaceholder'], item)
                deserialized_output = json.loads(stringified_output_fragment) 
                iterated_list.append(deserialized_output['Object'])
            output_fragment = iterated_list
            status = 'success'
    except AssertionError as asserterr:
        print('exception assertion not matched: ' + str(asserterr.args))
        output_fragment = {}
        status = 'failed'
    except:
        print('unknown exception building response')
        output_fragment = {}
        status = 'failed'
    return status, output_fragment

def lambda_handler(event, context):
    print('event received:\n' + str(event))
    try:
        status, output_fragment = build_response(event['fragment'], event['params'])
    except:
        print('unknown exception')
        output_fragment = {}
        status = 'failed'
    print('response status: ' + str(status))
    print('response fragment: ' + str(output_fragment))
    response = {
        'requestId': event['requestId'],
        'status': status,
        'fragment': output_fragment
    }
    print('response: ' + str(response))
    return response

if __name__ == '__main__':
    event={}
    context={}
    lambda_handler(event, context)