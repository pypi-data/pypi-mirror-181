import functools
import csv
import os


def powerml_data(func):
    @functools.wraps(func)
    def wrapper():
        print("\nGenerating_data: " + func.__name__)
        result = func()
        print(result)
        return result
    wrapper.is_generator_function = True
    return wrapper


def powerml_data_local(func):
    @functools.wraps(func)
    def wrapper():
        print("\nGenerating data and saving to file: " + func.__name__)
        generated_data = func()
        print(generated_data)
        # save generated data to a csv file
        cwd = os.getcwd()
        data_cwd = cwd + "/data"
        with open(data_cwd + '/data.csv', 'w', newline='') as csvfile:
            fieldnames = ['model_input', 'model_output']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in generated_data:
                writer.writerow(data)
        return generated_data
    wrapper.is_generator_function = True
    return wrapper
