import functools


def powerml_unit_test_suite(func):
    @functools.wraps(func)
    def wrapper():
        print("\nTest Name: " + func.__name__)
        metric_result, num_tests = func()
        print("Result: " + str(round(metric_result*100)) +
              '%' + " over "+str(num_tests)+" test cases.")
    return wrapper


def powerml_unit_test(func):
    @functools.wraps(func)
    def wrapper():
        print("\nTest Name: " + func.__name__)
        test_result = func()
        if test_result:
            print("Test " + func.__name__ + " passed!")
        else:
            print("Test " + func.__name__ + " failed!")
    return wrapper


def powerml_metric(func):
    @functools.wraps(func)
    def wrapper():
        print("\nMetric Name: " + func.__name__)
        metric_result = func()
        # Expect information about the metric to be non-boolean.
        print("Result: " + str(round(metric_result*100)) + '%' + " passed!")
    return wrapper
