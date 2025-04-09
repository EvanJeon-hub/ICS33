# Set 1 Problem1
# Evan-Soobin Jeon
# 3537131
# ejeon2@uci.edu

def only_truthy(**kwargs):
    return {f"_{keyword}": value for keyword, value in kwargs.items() if value}
