import fire


func_list = [
]
func_dict = {}
for func in func_list:
    func_dict[func.__name__] = func


def main():
    fire.Fire(func_dict)
