from typing import Literal, Union
from enum import Enum

import NaturalLanguage
from .CoreML import Model

from .utilities import _nsurl

class Language(Enum):
    AMHARIC = NaturalLanguage.NLLanguageAmharic
    ARABIC = NaturalLanguage.NLLanguageArabic
    ARMENIAN = NaturalLanguage.NLLanguageArmenian
    BENGALI = NaturalLanguage.NLLanguageBengali
    BULGARIAN = NaturalLanguage.NLLanguageBulgarian
    BURMESE = NaturalLanguage.NLLanguageBurmese
    CATALAN = NaturalLanguage.NLLanguageCatalan
    CHEROKEE = NaturalLanguage.NLLanguageCherokee
    CROATIAN = NaturalLanguage.NLLanguageCroatian
    CZECH = NaturalLanguage.NLLanguageCzech
    DANISH = NaturalLanguage.NLLanguageDanish
    DUTCH = NaturalLanguage.NLLanguageDutch
    ENGLISH = NaturalLanguage.NLLanguageEnglish
    FINNISH = NaturalLanguage.NLLanguageFinnish
    FRENCH = NaturalLanguage.NLLanguageFrench
    GEORGIAN = NaturalLanguage.NLLanguageGeorgian
    GERMAN = NaturalLanguage.NLLanguageGerman
    GREEK = NaturalLanguage.NLLanguageGreek
    GUJARATI = NaturalLanguage.NLLanguageGujarati
    HEBREW = NaturalLanguage.NLLanguageHebrew
    HINDI = NaturalLanguage.NLLanguageHindi
    HUNGARIAN = NaturalLanguage.NLLanguageHungarian
    ICELANDIC = NaturalLanguage.NLLanguageIcelandic
    INDONESIAN = NaturalLanguage.NLLanguageIndonesian
    ITALIAN = NaturalLanguage.NLLanguageItalian
    JAPANESE = NaturalLanguage.NLLanguageJapanese
    KANNADA = NaturalLanguage.NLLanguageKannada
    KAZAKH = NaturalLanguage.NLLanguageKazakh
    KHMER = NaturalLanguage.NLLanguageKhmer
    KOREAN = NaturalLanguage.NLLanguageKorean
    LAO = NaturalLanguage.NLLanguageLao
    MALAY = NaturalLanguage.NLLanguageMalay
    MALAYALAM = NaturalLanguage.NLLanguageMalayalam
    MARATHI = NaturalLanguage.NLLanguageMarathi
    MONGOLIAN = NaturalLanguage.NLLanguageMongolian
    NORWEGIAN = NaturalLanguage.NLLanguageNorwegian
    ORIYA = NaturalLanguage.NLLanguageOriya
    PERSIAN = NaturalLanguage.NLLanguagePersian
    POLISH = NaturalLanguage.NLLanguagePolish
    PORTUGESE = NaturalLanguage.NLLanguagePortuguese
    PUNJABI = NaturalLanguage.NLLanguagePunjabi
    ROMANIAN = NaturalLanguage.NLLanguageRomanian
    RUSSIAN = NaturalLanguage.NLLanguageRussian
    SIMPLIFIED_CHINESE = NaturalLanguage.NLLanguageSimplifiedChinese
    SINHALESE = NaturalLanguage.NLLanguageSinhalese
    SLOVAK = NaturalLanguage.NLLanguageSlovak
    SPANISH = NaturalLanguage.NLLanguageSpanish
    SWEDISH = NaturalLanguage.NLLanguageSwedish
    TAMIL = NaturalLanguage.NLLanguageTamil
    TELUGU = NaturalLanguage.NLLanguageTelugu
    THAI = NaturalLanguage.NLLanguageThai
    TIBETAN = NaturalLanguage.NLLanguageTibetan
    TRADITIONAL_CHINESE = NaturalLanguage.NLLanguageTraditionalChinese
    TURKISH = NaturalLanguage.NLLanguageTurkish
    UKRAINIAN = NaturalLanguage.NLLanguageUkrainian
    URDU = NaturalLanguage.NLLanguageUrdu
    VIETNAMESE = NaturalLanguage.NLLanguageVietnamese
    UNDETERMINED = NaturalLanguage.NLLanguageUndetermined

class TagScheme(Enum):
    TOKEN_TYPE = NaturalLanguage.NLTagSchemeTokenType
    LEXICAL_CLASS = NaturalLanguage.NLTagSchemeLexicalClass
    NAME_TYPE = NaturalLanguage.NLTagSchemeNameType
    NAME_TYPE_OR_LEXICAL_CLASS = NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass
    LEMMA = NaturalLanguage.NLTagSchemeLemma
    LANGUAGE = NaturalLanguage.NLTagSchemeLanguage
    SCRIPT = NaturalLanguage.NLTagSchemeScript
    SENTIMENT_SCORE = NaturalLanguage.NLTagSchemeSentimentScore

class TokenUnit(Enum):
    WORD = NaturalLanguage.NLTokenUnitWord
    SENTENCE = NaturalLanguage.NLTokenUnitSentence
    PARAGRAPH = NaturalLanguage.NLTokenUnitParagraph
    DOCUMENT = NaturalLanguage.NLTokenUnitDocument


class Tagger:
    def tag_parts_of_speech(string: str, unit: TokenUnit = TokenUnit.WORD) -> list[tuple[str, str]]:
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLexicalClass])
        tagger.setString_(string)
        
        tagged_pos = []
        def apply_tags(tag, token_range, error):
            word_phrase = string[token_range.location:token_range.location + token_range.length]
            tagged_pos.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(string)), unit.value, NaturalLanguage.NLTagSchemeLexicalClass, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_pos

    def tag_languages(string: str, unit: TokenUnit = TokenUnit.PARAGRAPH) -> list[tuple[str, str]]:
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLanguage])
        tagger.setString_(string)
        
        tagged_languages = []
        def apply_tags(tag, token_range, error):
            paragraph = string[token_range.location:token_range.location + token_range.length]
            if paragraph.strip() != "":
                tagged_languages.append((paragraph, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(string)), unit.value, NaturalLanguage.NLTagSchemeLanguage, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_languages

    def tag_entities(string: str, unit: TokenUnit = TokenUnit.WORD) -> list[tuple[str, str]]:
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass])
        tagger.setString_(string)
        
        tagged_languages = []
        def apply_tags(tag, token_range, error):
            word_phrase = string[token_range.location:token_range.location + token_range.length]
            if word_phrase.strip() != "":
                tagged_languages.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(string)), unit.value, NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace, apply_tags)
        return tagged_languages

    def tag_lemmas(string: str, unit: TokenUnit = TokenUnit.WORD) -> list[tuple[str, str]]:
        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeLemma])
        tagger.setString_(string)
        
        tagged_lemmas = []
        def apply_tags(tag, token_range, error):
            word_phrase = string[token_range.location:token_range.location + token_range.length]
            if word_phrase.strip() != "":
                tagged_lemmas.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(string)), unit.value, NaturalLanguage.NLTagSchemeLemma, NaturalLanguage.NLTaggerOmitPunctuation | NaturalLanguage.NLTaggerOmitWhitespace | NaturalLanguage.NLTaggerJoinContractions, apply_tags)
        return tagged_lemmas

    def tag_sentiments(string: str, sentiment_scale: list[str] = None, unit: TokenUnit = TokenUnit.PARAGRAPH) -> list[tuple[str, str]]:
        if sentiment_scale is None or len(sentiment_scale) == 0:
            sentiment_scale = ["Negative", "Neutral", "Positive"]

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_([NaturalLanguage.NLTagSchemeSentimentScore])
        tagger.setString_(string)
        
        tagged_sentiments = []
        def apply_tags(tag, token_range, error):
            paragraph = string[token_range.location:token_range.location + token_range.length]
            if paragraph.strip() != "":
                # Map raw tag value to range length
                raw_value = float(tag or 0)
                scaled = (raw_value + 1.0) / 2.0 * (len(sentiment_scale) - 1)

                label = sentiment_scale[int(scaled)]
                tagged_sentiments.append((paragraph, label))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_((0, len(string)), unit.value, NaturalLanguage.NLTagSchemeSentimentScore, 0, apply_tags)
        return tagged_sentiments

class _Embedding:
    def __init__(self):
        self._NLEmbedding = None
        self.language = None
    
    @property
    def vocab_size(self) -> int:
        return self._NLEmbedding.vocabularySize()

    @property
    def num_dimensions(self) -> int:
        return self._NLEmbedding.dimension()

    def write_dict(dictionary: dict[str, list[float]], language: Language, revision: int, file_path: str):
        file_url = _nsurl(file_path)
        NaturalLanguage.NLEmbedding.writeEmbeddingForDictionary_language_revision_toURL_error_(dictionary, language.value, revision, file_url, None)

    def neighbors(self, string: str, max_count: int = 100):
        neighbors = self._NLEmbedding.neighborsForString_maximumCount_distanceType_(string, max_count, NaturalLanguage.NLDistanceTypeCosine)
        return list(neighbors)

    def dist(self, string1: str, string2: str):
        return self._NLEmbedding.distanceBetweenString_andString_distanceType_(string1, string2, NaturalLanguage.NLDistanceTypeCosine)

    def contains(self, string: str):
        return self._NLEmbedding.containsString_(string)


class WordEmbedding(_Embedding):
    def __init__(self, language: Union[Language, None] = None, file_path: Union[str, None] = None):
        super().__init__()
        if file_path is not None:
            file_url = _nsurl(file_path)
            self._NLEmbedding = NaturalLanguage.NLEmbedding.embeddingWithContentsOfURL_error_(file_url, None)[0]
        elif language is not None:
            self.language = language
            self._NLEmbedding = NaturalLanguage.NLEmbedding.wordEmbeddingForLanguage_(language.value)

class SentenceEmbedding(_Embedding):
    def __init__(self, language: Language):
        super().__init__()
        self._NLEmbedding = NaturalLanguage.NLEmbedding.sentenceEmbeddingForLanguage_(language.value)
        self.language = language

class NLModel:
    def __init__(self, file_path: str, configuration=None):
        self.model = Model().load_from_file(file_path, configuration)
        self._NLModel = NaturalLanguage.NLModel.modelWithMLModel_error_(self.model._MLModel, None)[0]

        print(self._NLModel)

    def label_for_string(self, string: str):
        print(self._NLModel.predictedLabelsForTokens_([string]))
        return self._NLModel.predictedLabelForString_(string)

    # def labels_for_tokens(self, )