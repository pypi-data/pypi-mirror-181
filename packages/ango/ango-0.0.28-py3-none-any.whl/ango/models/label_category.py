import enum
import json
import uuid
import random
from typing import List


class Tool(enum.Enum):
    Segmentation = "segmentation"
    Polyline = "polyline"
    Polygon = "polygon"
    Rotated_bounding_box = "rotated-bounding-box"
    Ner = "ner"
    Point = "point"
    Pdf = "pdf"


class Classification(enum.Enum):
    Multi_dropdown = "multi-dropdown"
    Single_dropdown = "single-dropdown"
    Radio = "radio"
    Checkbox = "checkbox"
    Text = "text"
    Instance = "instance"


class Relation(enum.Enum):
    Single = "one-to-one"
    Group = "group"


def random_color():
    return "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])


class LabelOption:
    def __init__(self, value, schemaId=None):
        self.value = value,
        if schemaId:
            self.schemaId = schemaId
        else:
            self.schemaId = uuid.uuid4().hex

    def toDict(self):
        return self.__dict__


class Category:
    def __init__(self, tool: str, title: str = "", required: bool = False, schemaId: str = None,
                 columnField: bool = False, color: str = None, shortcutKey: str = "",
                 classifications: List = [], options: List[LabelOption] = []):
        self.tool = tool
        self.title = title
        self.required = required
        self.columnField = columnField
        self.color = color
        self.shortcutKey = shortcutKey
        self.classifications = classifications
        self.options = options
        if schemaId:
            self.schemaId = schemaId
        else:
            self.schemaId = uuid.uuid4().hex
        if color:
            self.color = random_color()
        else:
            self.color = random_color()

    def toDict(self):
        d = self.__dict__
        d['classifications'] = list(map(lambda t: t.toDict(), self.classifications))
        d['options'] = list(map(lambda t: t.toDict(), self.options))
        return d


class ClassificationCategory(Category):
    def __init__(self, classification: Classification, title: str = "", required: bool = False,
                 schemaId: str = None, columnField: bool = False, color: str = None, shortcutKey: str = "",
                 classifications: List = [], options: List[LabelOption] = [], parentOptionId=None, regex=None):
        super().__init__(classification.value, title, required, schemaId, columnField, color, shortcutKey,
                         classifications, options)
        self.regex = regex
        self.parentOptionId = parentOptionId

#        def toDict(self):
#            d = self.__dict__
#            return d

class RelationCategory(Category):
    def __init__(self, relation: Relation, title: str = "", required: bool = False, schemaId: str = None,
                 columnField: bool = False, color: str = None, shortcutKey: str = "",
                 classifications: List[ClassificationCategory] = [], options: List[LabelOption] = []):
        super().__init__(relation.value, title, required, schemaId, columnField, color, shortcutKey, classifications,
                         options)


class ToolCategory(Category):
    def __init__(self, tool: Tool, title: str = "", required: bool = False, schemaId: str = None,
                 columnField: bool = False, color: str = None, shortcutKey: str = "",
                 classifications: List[ClassificationCategory] = [], options: List[LabelOption] = []):
        super().__init__(tool.value, title, required, schemaId, columnField, color, shortcutKey, classifications,
                         options)
