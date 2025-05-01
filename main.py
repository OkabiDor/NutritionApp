from tracker import *

empty_eaten_foods()
load_eaten_foods()
while True:
    add_food()
    print_remaining_macros()
    suggest_foods()
    save_eaten_foods()
    
