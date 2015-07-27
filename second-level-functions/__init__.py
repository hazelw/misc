from second_level import Runner

def print_hay():
    print('hay')

runner = Runner()
runner.set_function(print_hay)
runner.run_function()
