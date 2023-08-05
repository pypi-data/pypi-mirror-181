from rivertils.lists import *

def get_language(test_message):
    """
    A crude quick test likely returns None
    """
    language = None
    if len(test_message) < 3:
        language = "en"
    else:
        # phrases like 'haha' are triggering bizarre language ids
        for x in indicates_english_message:
            if x.lower() in test_message.lower():
                language = "en"
    return language