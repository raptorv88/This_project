import math
import random

print("❤️ Welcome to the Love Probability Calculator ❤️\n")

def get_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 10:
                return value
            else:
                print("Please enter a number from 1 to 10.")
        except ValueError:
            print("Please enter a valid number.")


# Get inputs
social = get_input("How social are you? (1-10): ")
communication = get_input("How confident are you talking to new people? (1-10): ")
attractiveness = get_input("How attractive do you feel you are? (1-10): ")
eye_contacts = get_input("How often do you make eye contact? (1-10): ")


# -----------------------------
# 1. Non-linear base score
# -----------------------------
base_score = (
    0.40 * (social ** 1.30) +
    0.30 * (communication ** 1.35) +
    0.20 * (attractiveness ** 1.20) +
    0.10 * (eye_contacts ** 1.25)
)


# -----------------------------
# 2. Interaction Effects
# -----------------------------
# social × communication synergy
interaction1 = (social * communication) * 0.25

# attractiveness × eye contact synergy
interaction2 = (attractiveness * eye_contacts) * 0.20

interaction_boost = (interaction1 + interaction2) / 2


# -----------------------------
# 3. Romantic Luck Factor
# -----------------------------
# Luck varies from -10 to +10, but influenced by social presence
luck = random.randint(-10, 10) + (social // 3)

# Reduce extreme luck
luck = max(-12, min(luck, 12))  


# -----------------------------
# Final Score
# -----------------------------
raw_score = (base_score * 2.8) + interaction_boost + luck
love_score = max(0, min(raw_score, 100))

print("\n💖 Your Advanced Love Score:", round(love_score, 2), "/ 100")


# Luck Explanation
if luck > 5:
    print(f"🍀 Luck Boost: +{luck} — The universe is definitely on your side today!")
elif luck > 0:
    print(f"🍀 Luck Boost: +{luck} — You have a small romantic push today.")
elif luck == 0:
    print("🍀 Luck: Neutral — Your actions matter more than luck right now.")
else:
    print(f"🍂 Luck Penalty: {luck} — Might be a slow day, but don't worry!")


# Interpretation
if love_score < 30:
    print("🔮 Love Energy: Low — You're still developing your charm aura.")
elif love_score < 60:
    print("🔮 Love Energy: Moderate — Good potential, keep growing!")
elif love_score < 85:
    print("🔮 Love Energy: High — You naturally attract attention.")
else:
    print("🔮 Love Energy: Very High — Your romantic aura is powerful right now!")