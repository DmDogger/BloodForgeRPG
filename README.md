# BloodForge

BloodForge is a console-based, turn-based RPG. Players fight against enemies, manage resources like health and power, and gain experience to level up.

## Core Features

*   **Turn-Based Combat:** The battle unfolds in rounds, with the player and enemy taking turns to attack.
*   **Resource Management:** Characters have Health and Power. Power is spent to perform attacks. Running out of power penalizes the character.
*   **Attack States:**
    *   **Normal Attack:** A standard, reliable attack.
    *   **Rage Attack:** A high-risk, high-reward move. It has a chance to deal massive damage, but if it fails, the character takes damage.
*   **Weapons:** Choose from a variety of weapons, including swords, axes, and spears, each with a specific damage value.
*   **Stats Tracking:** The game keeps a record of your wins, losses, and total fights.
*   **XP and Leveling:** Gain experience points from winning battles to level up your character (Note: leveling up logic is not yet implemented).

## How to Run

To start the game, execute the main game file:

```bash
python game.py
```
