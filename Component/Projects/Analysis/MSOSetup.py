import copy
from Connector.Equipment import ReturnEquip
from Connector.Cable import ReturnCable

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class MSOSetup:
    def __init__(self, db_name, areas_selected, logic_selected):
        self.__return_cable__ = ReturnCable(db_name)
        self.__return_equip__ = ReturnEquip(db_name)
        self.db_name = db_name
        self.logic_origin = logic_selected.split(' ')
        self.areas_seleted = areas_selected
        self.__setup__()

    def __setup__(self):
        self.__variables__()
        self.__adjust__()

    def __variables__(self):
        self.equipments = self.__return_equip__.Equipments()

    def __adjust__(self):
        logic_split = copy.deepcopy(self.logic_origin)
        for idx, logic in enumerate(logic_split):
            if '(' in logic:
                logic_split[idx] = logic.replace('(', '')
            elif ')' in logic:
                logic_split[idx] = logic.replace(')', '')
            elif 'and' in logic:
                logic_split[idx] = logic.replace('and', ' and ')
            elif 'or' in logic:
                logic_split[idx] = logic.replace('or', ' or ')

        self.logic_dicts = []
        self.logic_dict = {}
        for logic in logic_split:
            if logic in self.equipments:
                self.logic_dict[logic] = ''
            elif logic not in self.equipments and logic != ' and ' and logic != ' or ':
                self.logic_dict[logic] = 'N/A'

        for area in self.areas_seleted:
            logic_dict = copy.deepcopy(self.logic_dict)
            for key in self.logic_dict.keys():
                route = list(set(self.__return_cable__.Route(key)))
                if '' in route:
                    route.remove('')
                if area in route and key in self.equipments:
                    logic_dict[key] = 'True'
                elif area not in route and key in self.equipments:
                    logic_dict[key] = 'False'
            self.logic_dicts.append(logic_dict)

        self.logic_final = []
        for dic in self.logic_dicts:
            self.logic_split = copy.deepcopy(self.logic_origin)
            for idx, logic in enumerate(self.logic_split):
                if 'and' in logic:
                    self.logic_split[idx] = logic.replace('and', ' and ')
                elif 'or' in logic:
                    self.logic_split[idx] = logic.replace('or', ' or ')
            for key in dic:
                for idx, logic in enumerate(self.logic_split):
                    if key in logic:
                        self.logic_split[idx] = logic.replace(key, dic[key])
            self.logic_final.append(''.join(self.logic_split))

        self.boolean = []
        for logic in self.logic_final:
            if 'N/A' not in logic:
                boolean = eval(logic)
                self.boolean.append(str(boolean))
            else:
                self.boolean.append(logic)

        self.mso = []
        for boolean in self.boolean:
            if boolean == 'True':
                self.mso.append('불만족')
            elif boolean == 'False':
                self.mso.append('만족')
            else:
                self.mso.append(boolean)