from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.training.dataset_builder import FineTuningDatasetBuilder
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--path', default='data/runtime/sft.jsonl')
parser.add_argument('--mode', default='sft')
args = parser.parse_args()
print(json.dumps(FineTuningDatasetBuilder().export_jsonl(args.path, args.mode), indent=2))
