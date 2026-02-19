"""CLI entry point for rotbot."""

import argparse
import asyncio
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="rotbot",
        description="rotbot - the open agent framework for every platform",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # rotbot onboard
    subparsers.add_parser("onboard", help="Initialize config and workspace")

    # rotbot agent
    agent_parser = subparsers.add_parser("agent", help="Interactive chat mode")
    agent_parser.add_argument("-m", "--message", help="Send a single message")
    agent_parser.add_argument("--no-markdown", action="store_true", help="Plain text output")
    agent_parser.add_argument("--logs", action="store_true", help="Show runtime logs")

    # rotbot gateway
    subparsers.add_parser("gateway", help="Start all enabled channels")

    # rotbot provider
    provider_parser = subparsers.add_parser("provider", help="Manage LLM providers")
    provider_sub = provider_parser.add_subparsers(dest="provider_action")
    provider_sub.add_parser("add", help="Add a new provider interactively")
    provider_sub.add_parser("list", help="List configured providers")
    provider_sub.add_parser("login", help="OAuth login for a provider")

    # rotbot status
    subparsers.add_parser("status", help="Show system status")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "onboard":
        from rotbot.cli.onboard import run_onboard
        asyncio.run(run_onboard())

    elif args.command == "agent":
        from rotbot.cli.agent import run_agent
        asyncio.run(run_agent(
            message=args.message,
            no_markdown=args.no_markdown,
            show_logs=args.logs,
        ))

    elif args.command == "gateway":
        from rotbot.cli.gateway import run_gateway
        asyncio.run(run_gateway())

    elif args.command == "provider":
        from rotbot.cli.provider_cmd import run_provider
        asyncio.run(run_provider(args.provider_action))

    elif args.command == "status":
        from rotbot.cli.status import run_status
        asyncio.run(run_status())


if __name__ == "__main__":
    main()
