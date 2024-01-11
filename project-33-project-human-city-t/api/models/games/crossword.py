# Generate a crossword puzzle from a list of words and their definitions
import random
import string
import itertools
from copy import deepcopy

def prepare_word(word):
    word = word.upper()
    word = "".join([char for char in word if char in string.ascii_letters])
    return word

def generate_crossword(word_definitions, grid_size):
    # Returns a tuple of (grid, hints)
    
    # Prepare words
    word_definitions = {prepare_word(item["Word"]): item["Definition"] for item in word_definitions}
    words = [word for word in word_definitions if len(word) <= grid_size]
    sorted_words = sorted(words, key=len, reverse=True)

    # Create a grid of size grid_size
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    grid_positions = list(itertools.product(range(grid_size), range(grid_size)))
    direction_options = ['horizontal', 'vertical']

    # bools to keep track of which cells can't be used by 
    taken = {
        "horizontal": [[False for _ in range(-1, grid_size + 1)] for _ in range(-1, grid_size + 1)], 
        "vertical": [[False for _ in range(-1, grid_size + 1)] for _ in range(-1, grid_size + 1)]
    }

    hints = {"horizontal": {}, "vertical": {}}

    if sorted_words:
        # Place the first word randomly in the grid
        word = sorted_words.pop(0)
        if random.choice(direction_options) == "horizontal":
            x, y = random.randint(0, grid_size - len(word)), random.randint(0, grid_size - 1)
            place_horizontal(grid, taken, word, x, y)
            hints["horizontal"][(x, y)] = word_definitions[word]
        else:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - len(word))
            place_vertical(grid, taken, word, x, y)
            hints["vertical"][(x, y)] = word_definitions[word]


        # Place the remaining words in the grid
        word_placed = True
        while word_placed:
            word_placed = False
            for word in sorted_words:
                random.shuffle(grid_positions)
                for x, y in grid_positions:
                    if word_placed := try_to_place_word(grid, direction_options, taken, hints, word, word_definitions, x, y):
                        sorted_words.remove(word)
                        break

                if word_placed:
                    break

    empty_grid, number_hints = generate_empty_crossword(hints, grid)

    return empty_grid, number_hints


def generate_empty_crossword(hints, grid):
    # Number the hint positions
    starting_points = list(hints["horizontal"].keys()) + list(hints["vertical"].keys())
    sorted_starting_points = sorted(starting_points, key=lambda x: (x[1], x[0]))

    # Create an empty grid with only the hint positions filled
    empty_grid = deepcopy(grid)
    for x, y in itertools.product(range(len(empty_grid)), range(len(empty_grid))):
        if (x, y) in sorted_starting_points:
            empty_grid[y][x] = sorted_starting_points.index((x, y)) + 1
        elif grid[y][x] != '':
            empty_grid[y][x] = ' '
    
    number_hints = {
        "horizontal": [{"number": sorted_starting_points.index(position) + 1, "hint": hint} for position, hint in hints["horizontal"].items()],
        "vertical": [{"number": sorted_starting_points.index(position) + 1, "hint": hint} for position, hint in hints["vertical"].items()]
    }
    
    return empty_grid, number_hints


def try_to_place_word(grid, direction_options, taken, hints, word, word_definitions, x, y):
    random.shuffle(direction_options)
    for placement in direction_options:
        if placement == "horizontal" and check_horizontal(grid, taken, word, x, y):
            place_horizontal(grid, taken, word, x, y)
            hints["horizontal"][(x, y)] = word_definitions[word]
            return True
        elif placement == "vertical" and check_vertical(grid, taken, word, x, y):
            place_vertical(grid, taken, word, x, y)
            hints["vertical"][(x, y)] = word_definitions[word]
            return True
    return False


def check_horizontal(grid, taken, word, x, y):
    # Checks:
    # 1. word fits in the grid
    # 2. intersects with another word
    # 3. doesn't overlap with another word
    # 4. near another word
    # 5. starts/ends on the side of another word in the oposite direction
    return (
        x + len(word) <= len(grid)
        and any(a == b for a, b in zip(grid[y][x : x + len(word)], word))
        and all(a in [b, ''] for a, b in zip(grid[y][x : x + len(word)], word))
        and not any(taken["horizontal"][y][x + i] for i in range(len(word)))
        and (
            not taken["vertical"][y][x - 1]
            and not taken["vertical"][y][x + len(word)]
        )
    )


def check_vertical(grid, taken, word, x, y):
    # Checks:
    # 1. word fits in the grid
    # 2. intersects with another word
    # 3. doesn't overlap with another word
    # 4. near another word
    # 5. starts/ends on the side of another word in the oposite direction
    return (
        y + len(word) <= len(grid)
        and any(a == b for a, b in zip([grid[y + i][x] for i in range(len(word))], word))
        and all(a in [b, ''] for a, b in zip([grid[y + i][x] for i in range(len(word))], word))
        and not any(taken["vertical"][y + i][x] for i in range(len(word)))
        and (not taken["horizontal"][y - 1][x] and not taken["horizontal"][y + len(word)][x])
    )


def place_horizontal(grid, taken, word, x, y):
    taken["vertical"][y][x - 1] = True
    taken["vertical"][y][x + len(word)] = True
    for i, char in enumerate(word):
        taken["horizontal"][y][x + i] = True
        taken["horizontal"][y - 1][x + i] = True
        taken["horizontal"][y + 1][x + i] = True
        grid[y][x + i] = char


def place_vertical(grid, taken, word, x, y):
    taken["horizontal"][y - 1][x] = True
    taken["horizontal"][y + len(word)][x] = True
    for i, char in enumerate(word):
        taken["vertical"][y + i][x] = True
        taken["vertical"][y + i][x - 1] = True
        taken["vertical"][y + i][x + 1] = True
        grid[y + i][x] = char



if __name__ == '__main__':
    topic, definitions = 'java', {'JVM': 'A virtual machine that executes Java bytecode, allowing Java programs to run on various platforms without modification.', 'Java Standard Library': 'A collection of pre-written Java classes and libraries that provide a wide range of functionality for common programming tasks.', 'Object': 'An instance of a class in Java. Objects represent real-world entities and encapsulate both data (attributes) and behaviors (methods).', 'Thread': 'A lightweight process that runs within a Java program, allowing concurrent execution of tasks. Java supports multi-threading.', 'Garbage Collection': 'The automatic process in Java that reclaims memory occupied by objects that are no longer in use, preventing memory leaks.', 'Abstraction': 'A fundamental concept in Java that involves hiding the complex implementation details and showing only the essential features of an object.', 'Package': 'A namespace that organizes a set of related classes and interfaces in Java. Packages help in organizing and managing code.', 'Java': 'A popular, platform-independent, object-oriented programming language known for its write-once, run-anywhere capability.', 'Java EE': 'A set of specifications that extend the Java SE (Standard Edition) for building enterprise-level applications, often used for web and server-side development.', 'Exception Handling': 'The process of managing and responding to unexpected runtime errors in Java using try, catch, and finally blocks.'}
    crossword = generate_crossword(definitions, 30)
    print(crossword)