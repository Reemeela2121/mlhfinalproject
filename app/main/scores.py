def age_score(own_age, other_age):
    diff = abs(own_age - other_age)
    if diff == 0:
        diff = 1
    return 5 / diff


def gender_score(own_gender, other_gender):
    if own_gender == other_gender:
        return 3
    else:
        return 1


def personality_score(own_personality, other_personality):
    if own_personality == other_personality:
        return 3
    elif own_personality == "ambivert" or other_personality == "ambivert":
        return 1.5
    else:
        return 0


def horoscope_score(
    own_horoscope, other_horoscope
):  # i dont believe in horoscopes but this is kinda fun
    if (own_horoscope == "cancer" or other_horoscope == "cancer") and (
        own_horoscope == "saggitarius" or other_horoscope == "saggitarius"
    ):
        return 3
    elif (own_horoscope == "taurus" or other_horoscope == "taurus") and (
        own_horoscope == "pisces" or other_horoscope == "pisces"
    ):
        return 3
    elif (own_horoscope == "gemini" or other_horoscope == "gemini") and (
        own_horoscope == "capricorn" or other_horoscope == "capricorn"
    ):
        return 3
    elif (own_horoscope == "libra" or other_horoscope == "libra") and (
        own_horoscope == "leo" or other_horoscope == "leo"
    ):
        return 3
    elif (own_horoscope == "scorpio" or other_horoscope == "scorpio") and (
        own_horoscope == "aries" or other_horoscope == "aries"
    ):
        return 3
    elif (own_horoscope == "virgo" or other_horoscope == "virgo") and (
        own_horoscope == "aquarius" or other_horoscope == "aquarius"
    ):
        return 3
    else:
        return 0


def hobby_score(own_hobbies, other_hobbies):
    own_hobbies_arr = own_hobbies.split(", ")
    other_hobbies_arr = other_hobbies.split(", ")
    common = list(set(own_hobbies_arr).intersection(other_hobbies_arr))
    return len(common)


def term_score(own_term, other_term):
    if own_term == other_term:
        return 4
    else:
        return 0


def profession_score(own_profession, other_profession):
    if own_profession == other_profession:
        return 3
    else:
        return 0


def music_score(own_music, other_music):
    own_music_arr = own_music.split(", ")
    other_music_arr = other_music.split(", ")
    common = list(set(own_music_arr).intersection(other_music_arr))
    return len(common)


def age_score(own_age, other_age):
    diff = abs(own_age - other_age)
    if diff == 0:
        diff = 1
    return 5 / diff


def gender_score(own_gender, other_gender):
    if own_gender == other_gender:
        return 3
    else:
        return 1


def personality_score(own_personality, other_personality):
    if own_personality == other_personality:
        return 3
    elif own_personality == "ambivert" or other_personality == "ambivert":
        return 1.5
    else:
        return 0


def horoscope_score(
    own_horoscope, other_horoscope
):  # i dont believe in horoscopes but this is kinda fun
    if (own_horoscope == "cancer" or other_horoscope == "cancer") and (
        own_horoscope == "saggitarius" or other_horoscope == "saggitarius"
    ):
        return 3
    elif (own_horoscope == "taurus" or other_horoscope == "taurus") and (
        own_horoscope == "pisces" or other_horoscope == "pisces"
    ):
        return 3
    elif (own_horoscope == "gemini" or other_horoscope == "gemini") and (
        own_horoscope == "capricorn" or other_horoscope == "capricorn"
    ):
        return 3
    elif (own_horoscope == "libra" or other_horoscope == "libra") and (
        own_horoscope == "leo" or other_horoscope == "leo"
    ):
        return 3
    elif (own_horoscope == "scorpio" or other_horoscope == "scorpio") and (
        own_horoscope == "aries" or other_horoscope == "aries"
    ):
        return 3
    elif (own_horoscope == "virgo" or other_horoscope == "virgo") and (
        own_horoscope == "aquarius" or other_horoscope == "aquarius"
    ):
        return 3
    else:
        return 0


def hobby_score(own_hobbies, other_hobbies):
    own_hobbies_arr = own_hobbies.split(", ")
    other_hobbies_arr = other_hobbies.split(", ")
    common = list(set(own_hobbies_arr).intersection(other_hobbies_arr))
    return len(common)


def term_score(own_term, other_term):
    if own_term == other_term:
        return 4
    else:
        return 0


def profession_score(own_profession, other_profession):
    if own_profession == other_profession:
        return 3
    else:
        return 0


def music_score(own_music, other_music):
    own_music_arr = own_music.split(", ")
    other_music_arr = other_music.split(", ")
    common = list(set(own_music_arr).intersection(other_music_arr))
    return len(common)
