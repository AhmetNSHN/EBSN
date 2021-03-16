def centeralize_screen(screen_width, screen_height, window_width, window_height): # always centralizing window according to screen size
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    return f"{window_width}x{window_height}+{x}+{y}"


# bellow functions are to generate values for spinboxes among application
def days():
    values = []
    for value in range(1, 10):
        values.append('{:0>2}'.format(value))
    for value in range(10, 32):
        values.append(value)
    return values

def months():
    values = []
    for value in range(1, 10):
        values.append('{:0>2}'.format(value))
    for value in range(10, 13):
        values.append(value)
    return values

def years():
    values = []
    for value in range(1950, 2020):
        values.append(value)
    return values

def future_years():
    values = []
    for value in range(2020, 2026):
        values.append(value)
    return values

def hour():
    values = []
    for value in range(1, 10):
        values.append('{:0>2}'.format(value))
    for value in range(10, 25):
        values.append(value)
    return values

def minute():
    values = []
    for value in range(1, 10):
        values.append('{:0>2}'.format(value))
    for value in range(10, 61):
        values.append(value)
    return values