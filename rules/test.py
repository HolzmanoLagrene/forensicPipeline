import glob

import plyara
import yara
from yarabuilder import YaraBuilder
from yaramanager.models.meta import Meta
from yaramanager.models.rule import Rule
from yaramanager.models.ruleset import Ruleset
from yaramanager.models.string import String
from yaramanager.models.tag import Tag
from yaramanager.utils.utils import parse_rule_file


def plyara_obj_to_rule(obj):
    r = Rule()
    r.name = obj.get("rule_name", "Unnamed rule")
    r.meta = plyara_object_to_meta(obj)
    r.strings = plyara_object_to_strings(obj)
    r.imports = plyara_object_to_imports(obj)
    r.tags = plyara_object_to_tags(obj)
    r.condition = plyara_object_to_condition(obj)
    ruleset = plyara_object_to_ruleset(obj)
    r.ruleset = ruleset
    return r


def plyara_object_to_meta(obj):
    """Returns a list of initialized Meta objects based on a plyara object."""
    meta = []
    for idx, m_dict in enumerate(obj.get("metadata", [])):
        for k, v in m_dict.items():
            if k.lower() == "ruleset":
                continue
            m = Meta(
                key=k,
                value=v,
                order=idx
            )
            meta.append(m)
    return meta


def plyara_object_to_strings(obj):
    """Returns a list of initialized String objects from a plyara object."""
    strings = []
    for idx, ply_string in enumerate(obj.get("strings", [])):
        s = String(
            name=ply_string["name"],
            value=ply_string["value"],
            order=idx,
            type=ply_string["type"]
        )
        s.modifiers = 0
        for mod in ply_string.get("modifiers", []):
            if mod == "ascii":
                s.modifiers = s.modifiers | 0x1
            elif mod == "wide":
                s.modifiers = s.modifiers | 0x2
            elif mod == "xor":
                s.modifiers = s.modifiers | 0x4
            elif mod == "base64":
                s.modifiers = s.modifiers | 0x8
        strings.append(s)
    return strings


def plyara_object_to_imports(obj):
    """Returns an integer representing imported yara modules."""
    imports = 0
    conditions = plyara_object_to_condition(obj)
    for imp in obj.get("imports", []):
        if imp == "pe" and "pe." in conditions:
            imports = imports | 0x1
        elif imp == "elf" and "elf." in conditions:
            imports = imports | 0x2
        elif imp == "math" and "math." in conditions:
            imports = imports | 0x4
        elif imp == "hash" and "hash." in conditions:
            imports = imports | 0x8
        elif imp == "vt" and "vt." in conditions:
            imports = imports | 0x10
    return imports


def plyara_object_to_tags(obj):
    """Returns a list of initialized Tag objects based on a plyara dict"""
    tags = []

    for tag in obj.get("tags", []):
        t = Tag(
            name=tag
        )
        tags.append(t)
    return tags


def plyara_object_to_condition(obj) -> str:
    """Returns condition string from plyara object"""
    return obj["raw_condition"].split(":", 1)[1].strip()


def plyara_object_to_ruleset(obj):
    """Returns ruleset object, if ruleset is given as meta tag, or None"""
    for m_dict in obj.get("metadata", []):
        for k, v in m_dict.items():
            return Ruleset(name=v)
    return None


def consolidate_rules(dir_):
    yb = YaraBuilder()

    for file in glob.glob(f"{dir_}/**/*"):
        if file.endswith(".yar"):
            try:
                yara.compile(filepath=file)
            except:
                continue
            d = parse_rule_file(file)
            for a in d:
                r = plyara_obj_to_rule(a)
                try:
                    r.add_to_yarabuilder(yb)
                except KeyError:
                    temp_yb = YaraBuilder()
                    r.add_to_yarabuilder(temp_yb)
                    if temp_yb.build_rule(r.name)==yb.build_rule(r.name):
                        continue
                    else:
                        r.name = r.name+"_1"
                        r.add_to_yarabuilder(yb)
    with open("all.yar", "w") as fh:
        fh.write(yb.build_rules())

consolidate_rules(".")
rules = yara.compile(filepath='/Users/holzmano/Documents/Projects/forensicPipeline/rules/all.yar', includes=True)
