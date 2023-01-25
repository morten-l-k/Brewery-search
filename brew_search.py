import requests
import json

#BASE_URL angiver basen for api-kaldet
BASE_URL = 'https://api.openbrewerydb.org/breweries'

def check_status(url:str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except Exception as ex:
        print('An exception was thrown:',ex)

def to_python_list(response:bytes) -> list:
    try:
        py_obj = json.loads(response)
        return py_obj ##
    except Exception as ex:
        try:
            py_obj = json.loads(response.content)
            return py_obj
        except Exception as ex:
            print('An exception was thrown:',ex)

def get_breweries_by_search(search:str,py_list:list) -> list :
    tmp_lst = []
    for elm in py_list:
        if (search == elm.get('name')
            or search == elm.get('state')
            or search == elm.get('city')):
            tmp_lst.append(elm)
    return tmp_lst

def clean_str(key_input:str) -> str:
    split = key_input.split(' ')
    for elm in split:
        index = split.index(elm)
        elm = elm.title()
        split[index] = elm
    return " ".join(split)

def get_search_query() -> list :
    return clean_str(input('Type your search query: '))

def make_api_argument(search:str) -> str:
    split = search.split()
    for elm in split:
        index = split.index(elm)
        elm = elm.lower()
        split[index] = elm
    return "_".join(split)

def make_api_call() :
    api_arg = make_api_argument(get_search_query())
    search_parameters = ['?by_state=','?by_name=','?by_city=']
    tmp_result = []
    for param in search_parameters:
        url_call = BASE_URL + param + api_arg
        tmp_result.append(to_python_list(check_status(url_call)))
    result = []
    for lst in tmp_result:
        for dictionary in lst:
            result.append(dictionary)
    return result

def showed_results(results):
    if len(results) == 0:
        print('Search query gave no result')
    else:
        tmp = results[0:5]
        print(f'THE SEARCH GAVE THE FOLLOWING RESULT:\n',tmp)
        return tmp

results = make_api_call()
showed_results(results)