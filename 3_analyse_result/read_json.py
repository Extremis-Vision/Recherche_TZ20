import json 

with open('/home/ghost/Documents/function_calling/3_analyse_result/becnhmark_structured_output.json') as f:
    data = json.load(f)


print(data["results"][0]["result"])