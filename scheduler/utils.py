import math

# round duration to the nearest multiplier of one block of time (30 mins)
def roundup(x):
    return int(math.ceil(x / 30.0)) * 30

# convert the time format from integer to string
def convert_time_from_int_to_str(x):
    h = x/60
    m = x - h*60
    return "%02d:%02d"%(h, m)

