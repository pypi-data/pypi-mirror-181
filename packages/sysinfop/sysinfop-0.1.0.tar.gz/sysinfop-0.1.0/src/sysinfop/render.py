from rich.panel import Panel
from rich import box
from .sysinfo import getSystemInfo

data = getSystemInfo()
box = box.MINIMAL

# System info section
h = data["hostname"]
i = data["ip-address"]
p = data["platform"]
P = data["processor"]
r = data["ram"]

layout = Panel(f"[bold]{h}[/bold]\n* IP: {i}\n* OS: {p}\n* CPU: {P}\n* RAM: {r}",
               expand=False,
               height=7,
               box=box)
