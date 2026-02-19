"""rotbot gateway — start all enabled channels."""

import asyncio
import logging

from rich.console import Console

from rotbot.core.bus import MessageBus
from rotbot.core.config import load_config, get_agent_defaults
from rotbot.core.loop import AgentLoop
from rotbot.core.memory import MemoryStore
from rotbot.core.session import SessionManager
from rotbot.channels.base import ChannelManager
from rotbot.providers.base import register_all_providers, ProviderRegistry
from rotbot.tools.base import ToolRegistry

console = Console()
logger = logging.getLogger(__name__)


async def run_gateway():
    """Start the gateway with all enabled channels."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    config = load_config()
    defaults = get_agent_defaults(config)

    # Initialize provider
    register_all_providers()
    provider_name = defaults.get("provider", "ollama")
    provider_config = config.get("providers", {}).get(provider_name, {})
    provider_config["provider_name"] = provider_name

    try:
        provider = ProviderRegistry.create(provider_name, provider_config)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return

    # Initialize core
    bus = MessageBus()
    sessions = SessionManager()
    memory = MemoryStore()
    tools = ToolRegistry()
    tools.register_builtins(config)

    # MCP tools
    mcp_config = config.get("tools", {}).get("mcpServers", {})
    mcp_manager = None
    if mcp_config:
        from rotbot.tools.mcp_client import MCPManager
        mcp_manager = MCPManager()
        mcp_tools = await mcp_manager.start_servers(mcp_config)
        for tool in mcp_tools:
            tools.register(tool)

    # Agent loop
    agent = AgentLoop(bus=bus, sessions=sessions, memory=memory,
                      provider=provider, tools=tools, config=config)

    # Channel manager
    channel_manager = ChannelManager(bus)
    channels_config = config.get("channels", {})

    # Register enabled channels
    enabled_count = 0

    if channels_config.get("discord", {}).get("enabled"):
        try:
            from rotbot.channels.discord_channel import DiscordChannel
            dc = DiscordChannel(bus=bus, config=channels_config["discord"])
            channel_manager.register(dc)
            enabled_count += 1
        except ImportError:
            console.print("[yellow]Discord: install discord.py (pip install rotbot-ai[discord])[/yellow]")

    if channels_config.get("telegram", {}).get("enabled"):
        try:
            from rotbot.channels.telegram_channel import TelegramChannel
            tc = TelegramChannel(bus=bus, config=channels_config["telegram"])
            channel_manager.register(tc)
            enabled_count += 1
        except ImportError:
            console.print("[yellow]Telegram: install pyTelegramBotAPI (pip install rotbot-ai[telegram])[/yellow]")

    if channels_config.get("signal", {}).get("enabled"):
        try:
            from rotbot.channels.signal_channel import SignalChannel
            sc = SignalChannel(bus=bus, config=channels_config["signal"])
            channel_manager.register(sc)
            enabled_count += 1
        except ImportError:
            console.print("[yellow]Signal channel not available[/yellow]")

    if enabled_count == 0:
        console.print("[red]No channels enabled. Edit ~/.rotbot/config.json or run 'rotbot onboard'.[/red]")
        return

    console.print(f"[green]Starting gateway with {enabled_count} channel(s)...[/green]")

    try:
        await asyncio.gather(
            agent.run(),
            channel_manager.start_all(),
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
    finally:
        agent.stop()
        await channel_manager.stop_all()
        await provider.close()
        if mcp_manager:
            await mcp_manager.stop_all()
