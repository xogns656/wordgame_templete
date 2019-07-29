from word_chain.consts import INITIAL_SOUND_SET


def check_match(agent_word: str, user_query: str):
    """
    :param agent_word: a word sent by the agent
    :type agent_word: basestring
    :param user_query: a word sent by the user
    :type user_query: basestring
    :return: whether the first syllable of a word sent by the user is
            the same as the last syllable of the word sent by the agent.
            This takes into account du-eum law - to avoid pronouncing a
            sound at the beginning of a word, read in a different pronunciation.
    """
    if agent_word[-1] in INITIAL_SOUND_SET:
        return INITIAL_SOUND_SET[agent_word[-1]] == user_query[0]
    else:
        return agent_word[-1] == user_query[0]

def check_reverse_match(agent_word: str, user_query: str):
    #reverse condition
    if agent_word[0] in INITIAL_SOUND_SET:
        return INITIAL_SOUND_SET[agent_word[0]] == user_query[-1]
    else:
        return agent_word[0] == user_query[-1]
