import functools


def powerml_filter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("\nRunning Filter: " + func.__name__)
        # Load Data to be filtered
        data_to_filter = kwargs['data']
        passing_data = []
        # pass data into filter function
        for datapoint in data_to_filter:
            result = func(datapoint["model_output"])
            if result:
                passing_data.append(datapoint)
        print("Cases: %d" %
              (len(data_to_filter)))
        print("Result: %d%%" %
              (100*len(passing_data)/len(data_to_filter)))
        return passing_data
    wrapper.is_filter_function = True
    return wrapper
