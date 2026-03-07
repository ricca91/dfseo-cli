"""Banner and splash screen for dfseo CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box


def show_banner():
    """Display the dfseo-cli welcome banner."""
    console = Console()
    
    # ASCII art logo
    logo = """
╭─────────────────────────────────────────────────────────────╮
│                                                             │
│   ██████╗ ███████╗███████╗███████╗ ██████╗                 │
│   ██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗                │
│   ██║  ██║█████╗  █████╗  ███████╗██║   ██║                │
│   ██║  ██║██╔══╝  ██╔══╝  ╚════██║██║   ██║                │
│   ██████╔╝██║     ██║     ███████║╚██████╔╝                │
│   ╚═════╝ ╚═╝     ╚═╝     ╚══════╝ ╚═════╝                 │
│                                                             │
│              DataForSEO CLI for AI Agents                   │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
    """
    
    # Alternative minimal version
    minimal_logo = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                           ┃
┃   ██████╗ ███████╗███████╗███████╗ ██████╗               ┃
┃   ██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗              ┃
┃   ██║  ██║█████╗  █████╗  ███████╗██║   ██║              ┃
┃   ██║  ██║██╔══╝  ██╔══╝  ╚════██║██║   ██║              ┃
┃   ██████╔╝██║     ██║     ███████║╚██████╔╝              ┃
┃   ╚═════╝ ╚═╝     ╚═╝     ╚══════╝ ╚═════╝               ┃
┃                                                           ┃
┃   SEO data from your terminal                             ┃
┃   JSON-first for agents · Human-friendly for you          ┃
┃                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    
    # Rich-styled version
    title = Text("dfseo-cli", style="bold cyan")
    subtitle = Text("DataForSEO CLI for AI Agents", style="dim")
    
    # Create panel content
    content = Text()
    content.append("SEO data from your terminal\n", style="white")
    content.append("JSON-first for agents · Human-friendly for you", style="dim")
    
    # Build the banner
    console.print()
    console.print(minimal_logo, style="cyan")
    console.print()
    
    # Quick start hint
    hint = Panel(
        "[bold]Quick Start:[/bold]\n"
        "[dim]$[/dim] [cyan]dfseo auth setup[/cyan]          [dim]# Configure credentials[/dim]\n"
        "[dim]$[/dim] [cyan]dfseo serp google \"keyword\"[/cyan]  [dim]# Search Google SERP[/dim]\n"
        "[dim]$[/dim] [cyan]dfseo --help[/cyan]              [dim]# Show all commands[/dim]",
        box=box.ROUNDED,
        border_style="dim",
        title="Get Started",
        title_align="left"
    )
    console.print(hint)
    console.print()


def show_version_banner(version: str):
    """Show version with banner."""
    console = Console()
    
    text = Text()
    text.append("dfseo-cli ", style="bold cyan")
    text.append(f"v{version}", style="white")
    text.append(" — ", style="dim")
    text.append("SEO data from your terminal", style="dim")
    
    console.print(text)
