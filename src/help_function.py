from loguru import logger


def dict_diff(old_dict: dict, new_dict: dict):
    """old_dict = {
        "a": 10,
        "b": 10,
        "c": None
    }

    new_dict = {
        "a": 10,
        "b": 20,
        "d": 30
    }

    print(dict_diff(old_dict, new_dict))

    :param old_dict: [description]
    :type old_dict: dict
    :param new_dict: [description]
    :type new_dict: dict
    :return: [description]
    :rtype: [type]
    """
    logger.trace("Running dict diff function")
    diff = {
        "new": list(),
        "remove": list(),
        "same": list(),
        "change": list()
    }

    for dict_a_value in old_dict.keys():
        if dict_a_value in new_dict.keys():
            if old_dict[dict_a_value] == new_dict.get(dict_a_value):
                diff["same"].append(dict_a_value)
            else:
                diff["change"].append(dict_a_value)
        else:
            diff["remove"].append(dict_a_value)

    diff["new"] = list(new_dict.keys() - old_dict.keys())
    logger.trace("Resolut of diff dict is : {}".format(diff))
    return diff
