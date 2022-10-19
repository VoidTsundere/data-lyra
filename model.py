import json

intent = []
question = {
    "tag":"NULL",
    "type":"NULL",
    "text":[],
    "response":[],
    "requirement":[],
    "locked_response":[]
    }
requeriment_type = {
    "mission":{
        "type":"mission",
        "mission_id":[],
        "response":[]
        },
    "affection":{
        "type":"affection",
        "affection_lvl":0,
        "response":[],
    }
}


def add_to_requirement(question_index=None, index=None, value_index=None, value=None):
    if type(intent[question_index]["requirement"][index][value_index]) == str:  # type: ignore
        intent[question_index]["requirement"][index][value_index] = value       # type: ignore

    if type(intent[question_index]["requirement"][index][value_index]) == list:
        if type(value) == list:
            for i in value:
                intent[question_index]["requirement"][index][value_index].append(i)  # type: ignore        
        else:
            intent[question_index]["requirement"][index][value_index].append(value)  # type: ignore
    return

def add_requirement(rtype=None, question_index=None):
    intent[question_index]["requirement"].append(requeriment_type[rtype])  # type: ignore
    return

def add_value(question_index=None, index=None, value=None):
    if type(intent[question_index][index]) == str:  # type: ignore
        intent[question_index][index] = value # type: ignore

    if type(intent[question_index][index]) == list: # type: ignore
        if type(value) == list: # type: ignore
            for i in value:
                intent[question_index][index].append(i)
                print(i)
        else:
            intent[question_index][index].append(value) # type: ignore
    return

def add_question():
    intent.append(question)
    return len(intent)

add_question()
add_requirement("mission",0)
add_value(0,"tag","Boa noite")
add_to_requirement(0,0,"mission_id", 0)

add_value(0, "text", "bom dia")