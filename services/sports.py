import random

from telebot import types
from emoji import emojize

BICYCLE_RIDE = emojize("Time to go for a bicycle ride! :bicycle:")
JOGGING = emojize("Let's go for a run! :running_shoe:")

BURPEES = "Some burpees!"
WEIGHT_TRAINING = emojize(
    "It's time for some weight training then! :person_lifting_weights:"
)

OUTDOOR_SPORTS = [BICYCLE_RIDE, JOGGING]
INDOOR_SPORTS = [BURPEES, WEIGHT_TRAINING]


def gen_markup_weather():
    markup = types.InlineKeyboardMarkup()
    keys = [
        [emojize("Sunny :sun:"), "weather_sun"],
        [emojize("Cloudy :sun_behind_cloud:"), "weather_cloudy"],
        [emojize("Rainy :cloud_with_rain:"), "weather_rain"],
        [emojize("Pouring down :cloud_with_lightning_and_rain:"), "weather_pouring"],
    ]
    buttons = [
        types.InlineKeyboardButton(label, callback_data=key) for label, key in keys
    ]
    markup.add(*buttons, row_width=2)
    return markup


def get_random_sport(weather):
    if weather in ["sun", "cloudy"]:
        return random.choice(OUTDOOR_SPORTS)

    elif weather in ["rain", "pouring"]:
        return random.choice(INDOOR_SPORTS)

    else:
        return None
