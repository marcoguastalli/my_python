from colorama import Fore, Style


def calculate_variation_amount(amount_from, amount_to):
    try:
        variation = ((amount_to - amount_from) / amount_from) * 100
    except ZeroDivisionError:
        return None
    return variation


def print_variation_with_colorama(created, instrument, variation):
    if variation >= 2:
        print(Fore.LIGHTGREEN_EX + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation >= 1.5:
        print(Fore.GREEN + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation >= 1:
        print(Style.RESET_ALL + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation <= -1:
        print(Style.RESET_ALL + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation <= -2:
        print(Fore.LIGHTRED_EX + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
