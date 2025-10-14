
def print_result(result: list, limit=4):
    if result is None:
        return
    
    for i in range(min(len(result), limit)):
        print(result[i])