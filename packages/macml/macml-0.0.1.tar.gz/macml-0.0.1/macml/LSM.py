from typing import Union

import Foundation
import LatentSemanticMapping

from .utilities import _nsurl

class LSM:
    def __init__(self, dataset: dict[str, list[str]], from_file: bool = False):
        self.active_dataset = {}
        self.__categories = {}

        if not from_file:
            # No data provided, data might be loaded from file
            self.map = LatentSemanticMapping.LSMMapCreate(None, 0)
            LatentSemanticMapping.LSMMapStartTraining(self.map)
            LatentSemanticMapping.LSMMapSetProperties(self.map, {
                LatentSemanticMapping.kLSMSweepCutoffKey: 0,
                LatentSemanticMapping.kLSMAlgorithmKey: LatentSemanticMapping.kLSMAlgorithmSparse,
            })

            for category in dataset:
                self.new_category(category, dataset[category])
        else:
            self.active_dataset = dataset

        self.__categories = {category: index + 1 for index, category in enumerate(self.active_dataset.keys())}

        print(self.active_dataset)

    def load(file_path: str, categories: list[str]) -> 'LSM':
        file_url = _nsurl(file_path)

        new_lsm = LSM({category: [] for category in categories}, True)
        new_lsm.map = LatentSemanticMapping.LSMMapCreateFromURL(None, file_url, LatentSemanticMapping.kLSMMapLoadMutable)
        LatentSemanticMapping.LSMMapCompile(new_lsm.map)
        return new_lsm

    def save(self, file_path: str) -> bool:
        file_url = _nsurl(file_path)
        status = LatentSemanticMapping.LSMMapWriteToURL(self.map, file_url, 0)
        return status == 0

    def new_category(self, name: str, initial_data: Union[list[str], None] = None) -> int:
        loc = Foundation.CFLocaleGetSystem()
        category_ref = LatentSemanticMapping.LSMMapAddCategory(self.map)
        self.active_dataset[name] = initial_data
        self.__categories[name] = category_ref
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        if initial_data is not None:
            LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(initial_data), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
        LatentSemanticMapping.LSMMapAddText(self.map, text_ref, category_ref)
        return category_ref

    def add_data(self, data: dict[str, list[str]]) -> list[int]:
        category_refs = []
        LatentSemanticMapping.LSMMapStartTraining(self.map)
        for category in data:
            if category not in self.active_dataset:
                category_refs.append(self.new_category(category, data[category]))
            else:
                loc = Foundation.CFLocaleGetSystem()
                text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
                LatentSemanticMapping.LSMTextAddWords(text_ref, " ".join(data[category]), loc, LatentSemanticMapping.kLSMTextPreserveAcronyms)
                LatentSemanticMapping.LSMMapAddText(self.map, text_ref, self.__categories[category])
        return category_refs

    def categorize(self, query: str, num_results=1) -> list[tuple[str, float]]:
        LatentSemanticMapping.LSMMapCompile(self.map)
        loc = Foundation.CFLocaleGetSystem()
        text_ref = LatentSemanticMapping.LSMTextCreate(None, self.map)
        LatentSemanticMapping.LSMTextAddWords(text_ref, query, loc, 0)
        rows = LatentSemanticMapping.LSMResultCreate(None, self.map, text_ref, 10, LatentSemanticMapping.kLSMTextPreserveAcronyms)

        categorization = []
        num_results = min(num_results, LatentSemanticMapping.LSMResultGetCount(rows))
        for i in range(0, num_results):
            category_num = LatentSemanticMapping.LSMResultGetCategory(rows, i)
            category_name = list(self.__categories.keys())[category_num - 1]
            score = LatentSemanticMapping.LSMResultGetScore(rows, i)
            categorization.append((category_name, score))
        return categorization