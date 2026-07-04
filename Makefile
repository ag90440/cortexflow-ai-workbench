install:
	pip install -r requirements.txt

api:
	uvicorn app.main:app --reload

ui:
	streamlit run ui/streamlit_app.py

test:
	pytest -q

smoke:
	python scripts/smoke_demo.py

export-sft:
	python scripts/export_sft_dataset.py --path data/runtime/sft.jsonl --mode sft
