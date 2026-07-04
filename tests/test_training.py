from app.training.dataset_builder import FineTuningDatasetBuilder


def test_training_records_build():
    builder = FineTuningDatasetBuilder()
    records = builder.build_sft_records()
    assert isinstance(records, list)
