# See if we can find the mismatch causing the error and fix it in normalise
import bisect
import json
import re
from collections import namedtuple
from difflib import SequenceMatcher
from math import floor
from time import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np


class Normalise:

    def __init__(self):
        self._app_data = None
        self._dataframe = None
        self._rules = None

    @property
    def app_data(self):
        return self._app_data

    @app_data.setter
    def app_data(self, value):
        self._app_data = json.dumps(value)

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    def obtain_keys(self) -> set:
        """Obtain all keys an app needs"""
        keys = {}
        json_data = self._app_data

        # Find uuid rename keys using negative lookahead regex; text between { and "type": "rename"
        rename_uuid_keys = re.findall(
            r'\{(?:(?!\{|' + re.escape('"type": "rename"') + r')[\s\S])*' + re.escape('"type": "rename"'), json_data)
        uuid_regex = re.compile(
            r'[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        uuidDollarRegex = re.compile(
            r'\$[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        rename_uuid_keys = list(
            set(re.findall(uuid_regex, str(rename_uuid_keys))))

        # Find all $uuid keys
        dollar_uuid_keys = re.findall(uuidDollarRegex, json_data)
        dollar_uuid_keys = [s.replace('$', '') for s in dollar_uuid_keys]

        # Remove styling parts
        json_data = re.sub(
            re.escape('config": [') + '.*?' + re.escape('"id"'), '', json_data)
        json_data = re.sub(
            re.escape('styling": {') + '.*?' + re.escape('}'), '', json_data)
        json_data = re.sub(
            re.escape('styling": [') + '.*?' + re.escape(']'), '', json_data)

        # Search normal and join keys
        normal_keys = re.findall(r'"key": "(.*?)"', json_data)
        join_keys = re.findall(r'"join_key": "(.*?)"', json_data)

        # Merge all key findings
        keys = set(normal_keys + join_keys +
                   rename_uuid_keys + dollar_uuid_keys)
        return keys

    def match_keys(self):
        """Pass a dataframe and appData to this function to find differences in keys"""
        keys = Normalise.obtain_keys(self)

        # Compare the two lists of keys to eachother
        additional_keys = list(self._dataframe.columns.difference(keys))
        missing_keys = list(keys.difference(self._dataframe.columns))

        values = namedtuple('keys', 'missing_keys additional_keys')
        return values(missing_keys, additional_keys)

    def fix_mismatch(self, strictness=0.8):
        """Pass a dataframe and appData to this function to fix the mismatch between the two"""
        keys = Normalise.match_keys(self)
        dataframe = self._dataframe

        if len(keys.missing_keys) < 1:
            return print("No missing keys")

        suggestions = []

        for i, missing_key in enumerate(keys.missing_keys):
            for additional_key in keys.additional_keys:
                similarity = SequenceMatcher(None, missing_key, additional_key)

                # Check if missing_key looks like additional_key
                if similarity.ratio() > strictness:
                    values = namedtuple('keys', 'missing_key additional_key')
                    suggestions.append(values(missing_key, additional_key))
                    keys.missing_keys.pop(i)

        print("\nWe did not find " + str(len(keys.missing_keys)) +
              " keys:\n" + str(sorted(keys.missing_keys, key=len)) + "\n")

        if len(suggestions) < 1:
            print("No matches, try lowering strictness")
            return dataframe

        # Propose suggestions
        for i, suggestion in enumerate(suggestions):
            print("Suggestion {}: missing '{}' might be additional: '{}'".format(
                i + 1, suggestion.missing_key, suggestion.additional_key))

        # Ask user which suggestions to fix and then rename dataframe columns
        suggestions_to_fix = list(map(int, input(
            "Which suggestion(s) do you want to fix? (example: 1 2 3): ").split()))
        for i in suggestions_to_fix:
            dataframe = dataframe.rename(
                columns={suggestions[i - 1].additional_key: suggestions[i - 1].missing_key})

        return dataframe

    def check_rules(self) -> pd.DataFrame:
        """Pass a dataframe and a JSON rules file to check if the rules are valid"""
        dataframe = self._dataframe
        rules = self._rules

        # Global settings
        reset_coverage = False
        global_check_coverage = False
        global_action = False
        global_verbose = "to_console"

        # Which rows to drop in one go
        drop_array = []
        
        # Which rows to np.nan in one go
        nan_array = []

        error_file = None

        # regex to match the string to_file in between quotes or double quotes
        regex = re.compile(r'\"(to_file)\"|\'(to_file)\'')
        if regex.search(str(rules)):
            error_file = open(str(floor(time())) + ".txt", "a")

        global_mapping = False

        # Contains "action" and "verbose"
        errors_found = False

        # Gets called when row doesn't match rule
        def handle_mismatch(i, value, rows):
            nonlocal errors_found
            errors_found = True

            action = global_action
            if "action" in rules[j]:
                action = rules[j]["action"]

            if action == "np.nan":
                # Which rows to np.nan later on in one go
                nan_array.append(i)

            if action == "drop":
                # Which rows to drop later onin one go
                drop_array.append(i)

            verbose = global_verbose
            if "verbose" in rules[j]:
                verbose = rules[j]["verbose"]

            if verbose == "to_file":
                error_file.write(
                    str(rules[j]["column"]) + " mismatch row " + str(i) + " - " + str(value) + "\n")

            if verbose == "to_console" or "verbose" in rules[j] == False:
                print(str(rules[j]["column"]) +
                      " mismatch row " + str(i) + " - " + str(value))

        def find_global_rules(j, rules):
            if not ("column" in rules[j]):
                nonlocal global_check_coverage
                nonlocal reset_coverage
                nonlocal global_action
                nonlocal global_verbose
                nonlocal global_mapping
                nonlocal dataframe

                if "check_coverage" in rules[j]:
                    global_check_coverage = rules[j]["check_coverage"]

                if ("reset_coverage" in rules[j]):
                    if (bool)(rules[j]["reset_coverage"]):
                        reset_coverage = bool(rules[j]["reset_coverage"])

                if ("action" in rules[j]):
                    global_action = rules[j]["action"]

                if ("verbose" in rules[j]):
                    global_verbose = rules[j]["verbose"]

                if ("column_mapping" in rules[j]):
                    dataframe = dataframe.rename(
                        columns=rules[j]["column_mapping"])

                if ("mapping" in rules[j]):
                    global_mapping = rules[j]["mapping"]

                # Continue with next rule
                return True

            # No global rules found
            return False

        # Loop through all rules
        j = -1
        while j < len(rules):
            # We're starting at -1 so j increment is at the top of the while loop
            j += 1
            if j >= len(rules):
                break

            if find_global_rules(j, rules) is True:
                continue

            # Column not found in dataset
            try:
                column_values = dataframe[rules[j]["column"]]
            except KeyError:
                print("Column " + rules[j]["column"] + " not found")
                continue

            if "mapping" in rules[j] or global_mapping != False:
                mapping = global_mapping
                if "mapping" in rules[j]:
                    mapping = rules[j]["mapping"]

                column_values = column_values.replace(mapping)

            if "reset_coverage" in rules[j]:
                if (bool)(rules[j]["reset_coverage"]):
                    reset_coverage = (bool(rules[j]["reset_coverage"]))

            if "check_coverage" in rules[j] or global_check_coverage != False:
                if errors_found and reset_coverage:
                    errors_found = False
                else:
                    check_coverage = global_check_coverage
                    if "check_coverage" in rules[j]:
                        check_coverage = (rules[j]["check_coverage"])
                    if re.match(r"^[1-9][0-9]?$|^100$", check_coverage):
                        column_values = column_values.sample(
                            frac=int(check_coverage) / 100)

            if "one_hot_encoding" in rules[j]:
                if len(rules[j]["one_hot_encoding"]) == 0:
                    dataframe = dataframe.join(pd.get_dummies(dataframe[rules[j]["column"]]))
                else:
                    dataframe = dataframe.join(pd.get_dummies(dataframe[rules[j]["column"]], prefix=rules[j]["one_hot_encoding"]))

            if "selection" in rules[j]:
                sorted_selection = sorted(rules[j]["selection"])
                for i, value in column_values.items():
                    index = bisect.bisect_left(sorted_selection, str(value))
                    if index >= len(sorted_selection) or sorted_selection[index] != value:
                        handle_mismatch(i, value, column_values)

            if "regex" in rules[j]:
                for i, value in column_values.items():
                    if not re.match(rules[j]["regex"], str(value)):
                        handle_mismatch(i, value, column_values)

            if "range" in rules[j]:
                for i, value in column_values.items():
                    try:
                        if not (float(rules[j]["range"][0]) <= float(value) <= float(rules[j]["range"][1])):
                            handle_mismatch(i, value, column_values)
                    except ValueError:
                        handle_mismatch(i, value, column_values)

            if "type" in rules[j]:

                if rules[j]["type"] == "percentage":
                    for i, value in column_values.items():
                        # Regex to match float between 0 and 100
                        if not re.match(r"^([0-9]|[1-9][0-9]|100)(\.[0-9]+)?$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "boolean":
                    for i, value in column_values.items():
                        if value != True and value != False:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "float":
                    if (column_values.dtype == float):
                        continue

                    for i, value in column_values.items():
                        try:
                            float(value)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "int":
                    if (column_values.dtype == int):
                        continue

                    for i, value in column_values.items():
                        try:
                            int(value)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "positive-int":
                    for i, value in column_values.items():
                        try:
                            if int(value) < 0:
                                handle_mismatch(i, value, column_values)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "negative-int":
                    for i, value in column_values.items():
                        try:
                            if int(value) >= 0:
                                handle_mismatch(i, value, column_values)
                        except ValueError:
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "letters":
                    for i, value in column_values.items():
                        if (value.isalpha() is False):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "postal_code":
                    column_values.astype(str).str.replace(
                        r"[^a-zA-Z0-9]+", "", regex=True).str.upper()

                    for i, value in column_values.items():
                        if not re.match(r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "longitude":
                    for i, value in column_values.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "latitude":
                    for i, value in column_values.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handle_mismatch(i, value, column_values)

                if rules[j]["type"] == "street":
                    for i, value in column_values.items():
                        value = list(value)  
                        for idx, character in enumerate(value):
                            if character not in ("'", "-", " ") and character.isalpha() is False:
                                handle_mismatch(i, value, column_values)
                                break

                            value[0] = value[0].upper()

                            if character in ("'", "-"):
                                try:
                                    # Make next character uppercase
                                    value[idx + 1] = value[idx + 1].upper()
                                except IndexError:
                                    continue

                            column_values[i] = "".join(value)
            # Loop again because error in sample
            if (reset_coverage and errors_found and len(column_values) < len(dataframe[rules[j]["column"]])):
                j -= 1
                continue

            # Bulk drop rows
            dataframe.drop(drop_array, inplace=True)

            # Make all the indexes inside the np.nan array nan values
            column_values.loc[nan_array] = np.nan

            # Update final dataframe with cached values
            dataframe[rules[j]["column"]].update(column_values)
    

            errors_found = False
        return dataframe
