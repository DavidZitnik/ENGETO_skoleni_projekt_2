"""
bulls_and_cows.py: druhý projekt do Engeto Online Python Akademie
author: David Zitnik
email: zitnik.david@seznam.cz
discord: DavidŽ#0653
"""

import random, time

line = "-" * 46
line2 = "+-" * 23
new_game = True
game_statistic = {"rounds": [], "time": []}


def introduction():
    """Invitation to the game."""
    text = "I've generated a random 4 digit number for you.\nLet's play a bulls and cows game."
    print(line, text, line, sep="\n")


def create_number():
    """Selection of unique numbers by program. All numbers must be different
    and the first number cannot be 0."""
    numbers = [random.randint(1, 9)]
    while len(numbers) < 4:
        random_number = random.randint(0, 9)
        if random_number not in numbers:
            numbers.append(random_number)
    return numbers


def enter_number():
    """The player must enter 4 numbers,
    numbers must be different and must not, start with 0."""
    return list(input(f'Enter a number\n{line}\n'))


def check_format_number(numbers):
    """Checking the correct format of the number entered by the player,
    numbers must be different and must not start with 0."""
    if not "".join(numbers).isnumeric() \
            or len(set(numbers)) != 4 \
            or int(numbers[0]) == 0:
        output = f"{line}\nYou entered a number in the wrong format.\n" \
                 f"All 4 numbers must be different\n" \
                 f"and not start with 0. Try it again.\n{line}"
    else:
        output = [int(number) for number in numbers]
    return output


def numbers_checking(num_pc, num_player):
    """Checking the entered numbers and evaluating the round."""
    bulls, cows = 0, 0
    for index, value in enumerate(num_pc):
        if value == num_player[index]:
            bulls += 1
        elif value in num_player:
            cows += 1
    return bulls, cows


def write_rating(animals):
    """Text statement of round evaluation."""
    text_buuls = "bull" if animals[0] == 1 else "bulls"
    text_cows = "cow" if animals[1] == 1 else "cows"
    return f"{animals[0]} {text_buuls}, {animals[1]} {text_cows}"


def round_stamp(good_limit, bad_limit, actual_value):
    """Verbal assessment of the game according to the good/bad limits"""
    if good_limit >= actual_value:
        stamp = "amazing"
    elif good_limit < actual_value <= bad_limit:
        stamp = "average"
    else:
        stamp = "not so good"
    return stamp


def statistics(game_round_num, start_time, verbal_stamp):
    """Statistic of the last 10 games. The best/worst time and rounds
     and verbal evaluation of the last game."""
    # doba hry
    game_time = time.time() - start_time
    # pokud hra trva dele nez 60s, prepocet doby na minuty a sekundy
    if game_time > 60:
        gametime_minute, gametime_second = divmod(game_time, 60)
        text_minute = "minutes" if gametime_minute > 1 else "minute"
        text_time = f"{gametime_minute} {text_minute} and {round(gametime_second, 1)}"
    else:
        text_time = f"{round(game_time, 1)}"

    # zapis hodnot (doba a pocet kol) do statistiky - max 10 poslednich her
    if len(game_statistic["rounds"]) >= 10:
        game_statistic["rounds"].pop(0)
        game_statistic["time"].pop(0)
    game_statistic["rounds"].append(game_round_num)
    game_statistic["time"].append(round(game_time, 1))

    # nejlepsi/nejhorsi casy a kola
    best_round = min(game_statistic["rounds"])
    best_time = min(game_statistic["time"])
    worst_round = max(game_statistic["rounds"])
    worst_time = max(game_statistic["time"])
    # vypocet hranic DOBRE/PRUMERNE a PRUMERNE/SPATNE podle poctu kol a casu
    round_good_limit = best_round + ((worst_round - best_round) / 3)
    round_bad_limit = worst_round - ((worst_round - best_round) / 3)
    time_good_limit = best_time + ((worst_time - best_time) / 3)
    time_bad_limit = worst_time - ((worst_time - best_time) / 3)
    # slovni vyhodnoceni posledni hry (AMAZING/AVERAGE/NOT SO GOOD)
    stamp_round = verbal_stamp(round_good_limit, round_bad_limit, game_round_num)
    stamp_time = verbal_stamp(time_good_limit, time_bad_limit, game_time)

    # vypsani info textu: "min 3 hry pro slovni hodnoceni" nebo "slovni hodnoceni hry"
    if len(game_statistic['rounds']) < 3:
        text_evaluation = "Play at least 3 games for verbal assessment."
    else:
        text_evaluation = f"That's {stamp_round} score in {stamp_time} time."

    # vypis textu statistiky her
    return f"{line}\nCorrect, you've guessed the right number\n" \
           f"in {game_round_num} {'guesses' if game_round_num > 1 else 'guess'} in {text_time} seconds!\n" \
           f"{'+-' * 3}  Statistic of the last{len(game_statistic['rounds']):>2} games  {'+-' * 3}\n" \
           f"{text_evaluation}\n" \
           f"{line2}\n" \
           f"The best round: {best_round:>3}  |  The best time:  {best_time:>4}s\n" \
           f"The worst round: {worst_round:>2}  |  The worst time: {worst_time:>4}s\n" \
           f"{line2}"


def ask_new_game():
    """Choosing to start a new game or exit the program"""
    game = input("\nDo you want to play again? [y/N] ")
    return game.lower() == "y"


# -------------------------------   hra   ----------------------------------------------
print("!!! Hi there !!!")
while new_game:
    # inicializace promennych: pocet kol, cas hry
    num_rounds = 0
    time_start = time.time()
    # uvod hry
    introduction()
    # vyber nahodneho cisla
    number_PC = create_number()
    print(number_PC)  # pro kontrolu vypsani hledaneho cisla
    # hra trva, dokud hrac neuhodne spravne vsechny cisla
    while True:
        # hrac zadava cislo, dokud nebude ve spravnem formatu
        while True:
            number_player = check_format_number(enter_number())
            num_rounds += 1
            if not isinstance(number_player, list):
                print(number_player)
            else:
                break
        # kontrola cisel hrace s s cisly vybranymi programem
        result = numbers_checking(number_PC, number_player)
        # vypis hodnoceni kola (bulls and cows)
        print(write_rating(result))
        if result[0] == 4:
            # vypis statistiky ukoncene hry
            print(statistics(num_rounds, time_start, round_stamp))
            break
    # start dalsi hry nebo konec
    new_game = ask_new_game()
print(f"{line}\nEND")
