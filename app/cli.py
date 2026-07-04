from app.agents.multi_agent import MultiAgentCoordinator
from app.core.schemas import AgentRequest, MultiAgentRequest
from app.dependencies import agent_runner, eval_runner, rag
from app.training.dataset_builder import FineTuningDatasetBuilder
import argparse
import json


def main():
    parser = argparse.ArgumentParser(prog='cortexflow')
    sub = parser.add_subparsers(dest='command', required=True)
    ask = sub.add_parser('ask')
    ask.add_argument('question')
    ask.add_argument('--strategy', default='hybrid')
    agent = sub.add_parser('agent')
    agent.add_argument('goal')
    multi = sub.add_parser('multiagent')
    multi.add_argument('objective')
    ingest = sub.add_parser('ingest')
    ingest.add_argument('source')
    ingest.add_argument('file')
    ev = sub.add_parser('eval')
    ev.add_argument('--name', default='rag_eval.json')
    train = sub.add_parser('export-training')
    train.add_argument('--path', default='data/runtime/sft.jsonl')
    train.add_argument('--mode', default='sft')
    args = parser.parse_args()
    if args.command == 'ask':
        print(json.dumps(rag.answer(args.question, strategy=args.strategy).model_dump(), indent=2))
    if args.command == 'agent':
        print(json.dumps(agent_runner.run(AgentRequest(goal=args.goal)).model_dump(), indent=2))
    if args.command == 'multiagent':
        print(json.dumps(MultiAgentCoordinator(rag).run(MultiAgentRequest(objective=args.objective)), indent=2))
    if args.command == 'ingest':
        text = open(args.file, encoding='utf-8').read()
        print(json.dumps({'chunks': rag.ingest_text(args.source, text)}, indent=2))
    if args.command == 'eval':
        print(json.dumps(eval_runner.run_file(args.name).model_dump(), indent=2))
    if args.command == 'export-training':
        print(json.dumps(FineTuningDatasetBuilder().export_jsonl(args.path, args.mode), indent=2))

if __name__ == '__main__':
    main()
