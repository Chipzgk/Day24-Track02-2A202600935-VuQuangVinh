# src/pii/detector.py
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import SpacyRecognizer

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    TODO: Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\d{11,12}",          # Regex cho 11-12 chữ số (để xử lý lỗi pandas drop số 0)
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        supported_language="vi",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"]
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        supported_language="vi",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"0?[35789]\d{8}",      # Regex cho sdt (có thể mất số 0 do pandas)
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"]
    )

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": "vi_core_news_lg"}]   # Điền model name
    })
    nlp_engine = provider.create_engine()

    person_recognizer = PatternRecognizer(
        supported_entity="PERSON",
        supported_language="vi",
        patterns=[Pattern(name="vn_person", regex=r"([A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯẠ-Ỵ][a-zàáâãèéêìíòóôõùúăđĩũơưạ-ỵ]+\s?)+", score=0.6)]
    )

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["vi"])
    spacy_recognizer = SpacyRecognizer(supported_language="vi")
    analyzer.registry.add_recognizer(spacy_recognizer)
    analyzer.registry.add_recognizer(person_recognizer)
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    TODO: Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results
