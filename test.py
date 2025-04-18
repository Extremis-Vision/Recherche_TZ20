import json 

test = 'json{"function_call": [{"name": "weather","arguments": {"location": "current location"}},{"name": "agenda","arguments": {}}]}'


test = test.replace("'''", "")
test = test.replace("'''", "")
test = test.replace("json", "")

json_data = json.loads(test)
print(json_data['function_call'][0])