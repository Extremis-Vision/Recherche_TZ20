import wolframalpha

def maths(query):
    api_key = '6TEW3G-R3L4W38GWG'
    client = wolframalpha.Client(api_key)
    res = client.query(query)
    responses = []

    for pod in res.pods:
        if pod.title is not None and pod.text is not None:
            responses.append({pod.title: pod.text})

    return responses

