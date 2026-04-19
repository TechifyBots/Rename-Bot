from aiohttp import web
import json
import time
import psutil
import shutil
import os
import base64
from config import Config
from plugins import __version__
from helper.utils import humanbytes
from helper.database import digital_botz

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

async def get_status():
    # Calculate your bot status metrics
    total_users = await digital_botz.total_users_count()
    if Config.PREMIUM_MODE:
        total_premium_users = await digital_botz.total_premium_users_count()
    else:
        total_premium_users = "Disabled ✅"
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(psutil.net_io_counters().bytes_sent)
    recv = humanbytes(psutil.net_io_counters().bytes_recv)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "status": "Operational",
        "version": __version__,
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
        "recv": recv
    }
TechifyBots = web.RouteTableDef()

@TechifyBots.get("/", allow_head=True)
async def root_route_handler(request):
    # Get real-time status data - CORRECTED: use get_status() instead of get_bot_status() and get_live_status()
    status_data = await get_status()
    # Render template with actual data
    with open('templates/welcome.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    # Replace placeholders with actual data - CORRECTED: use status_data dictionary
    html_content = template_content
    html_content = html_content.replace('{{bot_status}}', status_data['status'])
    html_content = html_content.replace('{{bot_version}}', status_data['version'])
    html_content = html_content.replace('{{total_users}}', str(status_data['total_users']))
    html_content = html_content.replace('{{premium_users}}', str(status_data['total_premium_users']))
    html_content = html_content.replace('{{bot_uptime}}', status_data['uptime'])
    html_content = html_content.replace('{{data_sent}}', status_data['sent'])
    html_content = html_content.replace('{{data_recv}}', status_data['recv'])
    html_content = html_content.replace('{{system_uptime}}', status_data['uptime'])
    html_content = html_content.replace('{{cpu_usage}}', str(status_data['cpu_usage']))
    html_content = html_content.replace('{{ram_usage}}', str(status_data['ram_usage']))
    html_content = html_content.replace('{{disk_usage}}', str(status_data['disk_usage']))
    html_content = html_content.replace('{{total_disk}}', status_data['total_disk'])
    html_content = html_content.replace('{{used_disk}}', status_data['used_disk'])
    html_content = html_content.replace('{{free_disk}}', status_data['free_disk'])
    html_content = html_content.replace('{{system_sent}}', status_data['sent'])
    html_content = html_content.replace('{{system_recv}}', status_data['recv'])
    # Add current timestamp for cache busting
    html_content = html_content.replace('{{timestamp}}', str(int(time.time())))
    return web.Response(text=html_content, content_type='text/html')

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(TechifyBots)
    return web_app
