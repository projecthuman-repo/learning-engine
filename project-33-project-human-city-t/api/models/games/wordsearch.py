# Generate a wordsearch puzzle from a list of words and their definitions
import random
import string
import itertools

def prepare_word(word):
    word = word.upper()
    word = "".join([char for char in word if char in string.ascii_letters])
    return word

def generate_wordsearch(word_definitions, grid_size):
    # Returns a grid and a list of hints
    
    # Prepare words
    word_definitions = {prepare_word(item["Word"]): item["Definition"] for item in word_definitions}
    words = [word for word in word_definitions if len(word) <= grid_size]
    sorted_words = sorted(words, key=len, reverse=True)

    # Create a grid of size grid_size
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    grid_positions = list(itertools.product(range(grid_size), range(grid_size)))
    direction_options = ['horizontal', 'vertical', 'diagonal_lr', 'diagonal_rl']
    reverse_options = [True, False]

    hints = []

    if sorted_words:
        # Place the words randomly in the grid
        word_placed = True
        while word_placed:
            word_placed = False
            for word in sorted_words:
                random.shuffle(grid_positions)
                for x, y in grid_positions:
                    if word_placed := try_to_place_word(grid, direction_options, reverse_options, word, x, y):
                        sorted_words.remove(word)
                        hints.append(word_definitions[word])
                        break

                if word_placed:
                    break
    
    fill_empty_cells(grid)

    return grid, hints


def fill_empty_cells(grid):
    for i, j in itertools.product(range(len(grid)), range(len(grid))):
        if grid[i][j] == '':
            grid[i][j] = random.choice(string.ascii_uppercase)

def try_to_place_word(grid, direction_options, reverse_options, word, x, y):
    random.shuffle(direction_options)
    random.shuffle(reverse_options)
    for placement, reverse in itertools.product(direction_options, reverse_options):
        if placement == "horizontal" and check_horizontal(grid, word, x, y):
            place_horizontal(grid, word, reverse, x, y)
            return True
        elif placement == "vertical" and check_vertical(grid, word, x, y):
            place_vertical(grid, word, reverse, x, y)
            return True
        elif placement == "diagonal_lr" and check_diagonal_lr(grid, word, x, y):
            place_diagonal_lr(grid, word, reverse, x, y)
            return True
        elif placement == "diagonal_rl" and check_diagonal_rl(grid, word, x, y):
            place_diagonal_rl(grid, word, reverse, x, y)
            return True
    return False


def check_horizontal(grid, word, x, y):
    # Checks: doesn't overlap with another word
    return x + len(word) <= len(grid) and all(a in [b, ''] for a, b in zip(grid[y][x : x + len(word)], word))


def check_vertical(grid, word, x, y):
    # Checks: doesn't overlap with another word
    return y + len(word) <= len(grid) and all(a in [b, ''] for a, b in zip([grid[y + i][x] for i in range(len(word))], word))


def check_diagonal_lr(grid, word, x, y):
    # Checks: doesn't overlap with another word
    return x + len(word) <= len(grid) and y + len(word) <= len(grid) and all(a in [b, ''] for a, b in zip([grid[y + i][x + i] for i in range(len(word))], word))


def check_diagonal_rl(grid, word, x, y):
    # Checks: doesn't overlap with another word
    return x - len(word) >= -1 and y + len(word) <= len(grid) and all(a in [b, ''] for a, b in zip([grid[y + i][x - i] for i in range(len(word))], word))


def place_horizontal(grid, word, reverse, x, y):
    for i, char in enumerate(reversed(word)) if reverse else enumerate(word):
        grid[y][x + i] = char


def place_vertical(grid, word, reverse, x, y):
    for i, char in enumerate(reversed(word)) if reverse else enumerate(word):
        grid[y + i][x] = char


def place_diagonal_lr(grid, word, reverse, x, y):
    for i, char in enumerate(reversed(word)) if reverse else enumerate(word):
        grid[y + i][x + i] = char


def place_diagonal_rl(grid, word, reverse, x, y):
    for i, char in enumerate(reversed(word)) if reverse else enumerate(word):
        grid[y + i][x - i] = char



if __name__ == '__main__':
    topic, definitions = 'java', {'JVM': 'A virtual machine that executes Java bytecode, allowing Java programs to run on various platforms without modification.', 'Java Standard Library': 'A collection of pre-written Java classes and libraries that provide a wide range of functionality for common programming tasks.', 'Object': 'An instance of a class in Java. Objects represent real-world entities and encapsulate both data (attributes) and behaviors (methods).', 'Thread': 'A lightweight process that runs within a Java program, allowing concurrent execution of tasks. Java supports multi-threading.', 'Garbage Collection': 'The automatic process in Java that reclaims memory occupied by objects that are no longer in use, preventing memory leaks.', 'Abstraction': 'A fundamental concept in Java that involves hiding the complex implementation details and showing only the essential features of an object.', 'Package': 'A namespace that organizes a set of related classes and interfaces in Java. Packages help in organizing and managing code.', 'Java': 'A popular, platform-independent, object-oriented programming language known for its write-once, run-anywhere capability.', 'Java EE': 'A set of specifications that extend the Java SE (Standard Edition) for building enterprise-level applications, often used for web and server-side development.', 'Exception Handling': 'The process of managing and responding to unexpected runtime errors in Java using try, catch, and finally blocks.'}
    wordsearch = generate_wordsearch(definitions, 3)
    print(wordsearch)