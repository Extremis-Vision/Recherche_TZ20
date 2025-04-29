import json

response = """{'querys':[
                        'CNNLLMscomparison',
                        'ConvolutionalNeuralNetworksLanguageModels',
                        'LLMarchitecturelimitations',
                        'WhynotCNNforLLMs',
                        'AlternativearchitecturestoTransformers'
                    ],
                    'categories':'AIResearch'
                }"""



try:
    response_final = json.loads(response)

except Exception as e:
    print("Erreur : " + str(e))

while " " in response:
    response = response.replace(" ", "")

print(response)