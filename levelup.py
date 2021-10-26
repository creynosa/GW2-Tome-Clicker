#!/usr/bin/env python3.9

from pathlib import Path

import pyautogui
import pyscreeze
from elevate import elevate


def printInstructions() -> None:
    """Prints a set of basic instructions on how to use this program."""
    print('\n======================================================================')
    text = "To avoid any issues when using this program, do the following:\n\n" \
           "1. You'll need Guild Wars 2 to be on your main display.\n" \
           "2. Your tomes of knowledge must be visible somewhere on your screen at all times.\n" \
           "4. Please ensure that you have the exact tomes of knowledge required.\n" \
           "5. Avoid moving the mouse unless it is to exit this console window.\n" \
           "6. Feel free to move this window to any other monitor.\n" \
           "7. A message will appear once this program has finished running.\n\n" \
           "Press enter to continue: "
    input(text)


def askForStartingLevel() -> int:
    """Asks the user what level the user wishes to start at and returns it."""
    print('\n======================================================================')
    response = input('Please enter your starting level: ')
    validResponse = response.isdigit() and response in map(str, range(1, 80))
    while not validResponse:
        response = input('\nInvalid starting level. Please try again: ')

    response = int(response)
    return response


def askForEndingLevel() -> int:
    """Asks the user what level the user wishes to end at and returns it."""
    print('\n======================================================================')
    response = input('Please enter your desired end level: ')
    validResponse = response.isdigit() and response in map(str, range(2, 81))
    while not validResponse:
        response = input('\nInvalid end level. Please try again: ')

    response = int(response)
    return response


def calculateLoops(start: int, end: int) -> int:
    """Calculates the number of loops the program will execute."""
    loops = end - start
    return loops


def printTomesRequired(loops: int) -> None:
    """Prints a message with the number of tomes of knowledge that is required for a given number of loops."""
    if loops == 1:
        text = f"You will need a single tome of knowledge in your inventory."
    else:
        text = f"You will need {loops} tomes of knowledge in your inventory."

    print('\n======================================================================')
    print(text)
    print('\n')


def verifyUserHasTomes() -> None:
    """Asks the user to confirm they have the required candy corn before proceeding."""
    input('Press enter once you have verified you have the required amount of tomes of knowledge to commence: ')


def getTomeLocation() -> pyscreeze.Point:
    """Finds and returns the location of the tomes of knowledge on the main screen."""
    imagePath = str(Path(__file__).parent / 'resources' / 'tomes.png')

    print('\n======================================================================')
    location = None
    while location is None:
        print('Searching for tomes of knowledge...\n')
        location = pyautogui.locateCenterOnScreen(imagePath, grayscale=True, confidence=0.9)
    print('Tomes found!')
    return location


def getAcceptButtonLocation() -> pyscreeze.Point:
    """Finds and returns the location of the accept button on the main screen."""
    imagePath = str(Path(__file__).parent / 'resources' / 'accept.png')

    location = None
    while location is None:
        location = pyautogui.locateCenterOnScreen(imagePath, grayscale=True, confidence=0.9)
    return location


def clickTomes(loops: int) -> None:
    """Clicks on the tomes of knowledge for a determined amount of clicks."""
    print('\n======================================================================')
    print('To cancel, please close this window at anytime.\n\n')

    tomeLocation = getTomeLocation()
    acceptLocation = None

    loopsRemaining = loops
    loopsFinished = 0
    while loopsRemaining:
        pyautogui.doubleClick(tomeLocation)
        pyautogui.sleep(0.5)
        if acceptLocation is None:
            acceptLocation = getAcceptButtonLocation()
        pyautogui.click(acceptLocation)
        pyautogui.sleep(0.5)
        loopsRemaining -= 1
        loopsFinished += 1
        print("{:.1%} completed...".format(loopsFinished / loops), end='\r')

    print('')
    print('\n======================================================================')
    print('Finished! Enjoy!')


if __name__ == "__main__":
    launchBuddyResponse = input('Are you using launchbuddy and/or is your game running in administrative mode? y/n: ')
    if launchBuddyResponse.lower() in ['y', 'yes', 'yay']:
        elevate()

    printInstructions()

    startLevel = askForStartingLevel()
    endLevel = askForEndingLevel()

    tomeLoops = calculateLoops(startLevel, endLevel)

    printTomesRequired(tomeLoops)
    verifyUserHasTomes()

    clickTomes(tomeLoops)
