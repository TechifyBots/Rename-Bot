from aiohttp import web
import asyncio
import time
import psutil
import shutil
import os
from config import Config
from plugins import __version__
from helper.utils import humanbytes
from helper.database import digital_botz
from helper.speedtest import network_speed_label

# Identity of the main bot client, injected from TechifyBots.start() after
# set_identity() has cached it; placeholders until startup completes.
bot_info = {"name": "Rename Bot", "username": ""}

# Status page counts are cosmetic; cache them so a page view doesn't hit Mongo
# twice. 60s staleness on a dashboard is invisible.
_COUNTS_TTL = 60
_counts_cache = (0.0, 0, "Disabled ✅")

async def _cached_counts():
    global _counts_cache
    ts, users, premium = _counts_cache
    if time.monotonic() - ts < _COUNTS_TTL:
        return users, premium
    users = await digital_botz.total_users_count()
    premium = (
        await digital_botz.total_premium_users_count()
        if Config.PREMIUM_MODE else "Disabled ✅"
    )
    _counts_cache = (time.monotonic(), users, premium)
    return users, premium

_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "welcome.html")
with open(_TEMPLATE_PATH, encoding="utf-8") as f:
    _WELCOME_TEMPLATE = f.read()

async def get_status():
    # Calculate your bot status metrics
    total_users, total_premium_users = await _cached_counts()
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    net = psutil.net_io_counters()
    sent = humanbytes(net.bytes_sent)
    recv = humanbytes(net.bytes_recv)
    cpu_usage = await asyncio.to_thread(psutil.cpu_percent, 0.5)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "status": "Operational",
        "version": __version__,
        "bot_name": bot_info["name"],
        "bot_username": f"@{bot_info['username']}" if bot_info["username"] else "—",
        "total_users": total_users,
        "total_premium_users": total_premium_users,
        "uptime": currentTime,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
        "total_disk": total,
        "used_disk": used,
        "free_disk": free,
        "sent": sent,
        "recv": recv,
    }
TechifyBots = web.RouteTableDef()

@TechifyBots.get("/", allow_head=True)
async def root_route_handler(request):
    status_data, speed_label = await asyncio.gather(get_status(), network_speed_label())
    data = {
        "{{bot_status}}": status_data["status"],
        "{{bot_version}}": str(status_data["version"]),
        "{{bot_name}}": str(status_data["bot_name"]),
        "{{bot_username}}": str(status_data["bot_username"]),
        "{{total_users}}": str(status_data["total_users"]),
        "{{premium_users}}": str(status_data["total_premium_users"]),
        "{{bot_uptime}}": status_data["uptime"],
        "{{system_uptime}}": status_data["uptime"],
        "{{system_sent}}": status_data["sent"],
        "{{system_recv}}": status_data["recv"],
        "{{cpu_usage}}": str(status_data["cpu_usage"]),
        "{{ram_usage}}": str(status_data["ram_usage"]),
        "{{disk_usage}}": str(status_data["disk_usage"]),
        "{{total_disk}}": status_data["total_disk"],
        "{{used_disk}}": status_data["used_disk"],
        "{{free_disk}}": status_data["free_disk"],
        "{{net_speed}}": speed_label,
    }
    html_content = _WELCOME_TEMPLATE
    for placeholder, value in data.items():
        html_content = html_content.replace(placeholder, value)
    return web.Response(text=html_content, content_type='text/html')

@TechifyBots.get("/favicon.ico", allow_head=True)
async def favicon_handler(request):
    return web.Response(status=204)

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(TechifyBots)
    return web_app
