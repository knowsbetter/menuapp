from .save_as_excel import convert_to_excel


def convert_menu(res: list):
    temp = []
    menus_list = []
    submenus_list = []
    dishes_list = []
    result = []

    for i in res:
        if i[0:3] not in temp:
            temp.append(i[0:3])
    for i in temp:
        dict = {}
        dict["title"] = i[0]
        dict["description"] = i[1]
        dict["dishes_count"] = i[2]
        menus_list.append(dict)

    result.append(menus_list)
    temp = []

    for i in res:
        if i[3:6] not in temp:
            temp.append(i[3:6])
    for i in temp:
        dict = {}
        dict["title"] = i[0]
        dict["description"] = i[1]
        dict["dishes_count"] = i[2]
        submenus_list.append(dict)

    result.append(submenus_list)
    temp = []

    for i in res:
        if i[6:] not in temp:
            temp.append(i[6:])
    for i in temp:
        dict = {}
        dict["title"] = i[0]
        dict["description"] = i[1]
        dict["price"] = i[2]
        dishes_list.append(dict)

    result.append(dishes_list)

    convert_to_excel(result)
