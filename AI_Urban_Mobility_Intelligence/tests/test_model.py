def test_model_files_exist():
    from config.config import MODEL_PATH, METADATA_PATH
    assert MODEL_PATH.exists(); assert METADATA_PATH.exists()
