import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import sys
import asyncio
import httpx
import random
import json
import socket
import struct
import time
import uuid
import threading
import gc
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from google_play_scraper import app as play_scraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from protobuf_decoder.protobuf_decoder import Parser

import thunderFF_pb2
import MajoRLoGinrEq_pb2
from CDX import *

try:
    import MajorLoginRes_pb2 as _MajorLoginRes_orig
    MajorLoginRes = _MajorLoginRes_orig.MajorLoginRes
except Exception:
    MajorLoginRes = thunderFF_pb2.MajorLoginRes


# ==========================================
# টার্মিনাল কালার
# ==========================================
class Color:
    GREEN = "\033[1;92m"
    RED = "\033[1;91m"
    YELLOW = "\033[1;93m"
    BLUE = "\033[1;94m"
    CYAN = "\033[1;96m"
    MAGENTA = "\033[1;95m"
    WHITE = "\033[1;97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

def log_success(text: str): print(f"{Color.GREEN}[✓] {text}{Color.RESET}", flush=True)
def log_error(text: str):   print(f"{Color.RED}[✗] {text}{Color.RESET}", flush=True)
def log_warn(text: str):    print(f"{Color.YELLOW}[!] {text}{Color.RESET}", flush=True)
def log_info(text: str):    print(f"{Color.CYAN}[i] {text}{Color.RESET}", flush=True)
def log_squad(text: str):   print(f"{Color.MAGENTA}[👥] {text}{Color.RESET}", flush=True)
def log_leave(text: str):   print(f"{Color.YELLOW}[🚪] {text}{Color.RESET}", flush=True)
def log_recruit(text: str): print(f"{Color.BLUE}[📢] {text}{Color.RESET}", flush=True)

def log_progress(current: int, total: int, label: str = "Fetching", width: int = 30):
    filled = int(width * current / total) if total else 0
    bar = f"{Color.GREEN}{'█'*filled}{Color.RESET}{Color.YELLOW}{'░'*(width-filled)}{Color.RESET}"
    pct = (current / total * 100) if total else 0
    sys.stdout.write(f"\r  {bar}  {Color.BOLD}{pct:5.1f}%{Color.RESET}  {Color.CYAN}{label} {current}/{total}{Color.RESET}   ")
    sys.stdout.flush()

def log_progress_done():
    sys.stdout.write("\n")
    sys.stdout.flush()

def log_banner():
    banner = f"""
{Color.MAGENTA}╔════════════════════════════════════════════════════════════════╗
║    {Color.WHITE}FREE FIRE 24/7 AUTO ID GENERATOR + 700 ONLINE KEEPER{Color.MAGENTA}       ║
║  {Color.GREEN}API: {Color.YELLOW}ariyan-id.vercel.app{Color.GREEN} | TARGET: {Color.YELLOW}700 ONLINE{Color.GREEN} | LIVE: {Color.YELLOW}25s{Color.GREEN} | CYCLE: {Color.YELLOW}30s{Color.MAGENTA}  ║
╚════════════════════════════════════════════════════════════════╝{Color.RESET}
"""
    print(banner, flush=True)


# ==========================================
# কনফিগারেশন
# ==========================================
ACCOUNTS_TXT_FILE = "ariyan.txt"
TOKEN_CACHE_FILE = "token_cache.json"
DEVICES_FILE = "devices.json"
TOKEN_CACHE_TTL = 1200
MAX_LOGIN_THREADS = 20
MAX_LOGIN_ATTEMPTS = 2

GROUP_LIFETIMES = [25.0, 25.0, 25.0]
GROUP_CYCLE_SLEEP = 30.0
NUM_GROUPS = 3
FULL_REFRESH_INTERVAL = 5 * 60 * 60

INITIAL_ACCOUNT_COUNT = 400
TARGET_ACCOUNT_COUNT = 700
MIN_ACCOUNTS_TO_KEEP = 700

API_BASE_URL = "https://ariyan-id.vercel.app"
API_FETCH_TIMEOUT = 40.0
API_FETCH_RETRY = 5
API_CONCURRENT_FETCH = 20
REPLENISH_CHECK_INTERVAL = 20.0

VERSION_API = "https://version.ggwhitehawk.com/live/ver.php"
VERSION_API_TIMEOUT = 12.0
VERSION_API_RETRY = 5

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

headers = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.12f1',
    'X-GA-SV': '1789535859',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB55'
}

client = httpx.AsyncClient(
    verify=False,
    timeout=15.0,
    limits=httpx.Limits(max_connections=500, max_keepalive_connections=250)
)
_THREAD_SEMAPHORE = asyncio.Semaphore(MAX_LOGIN_THREADS)
_API_SEMAPHORE = asyncio.Semaphore(API_CONCURRENT_FETCH)

online_count = 0
squad_created_count = 0
total_accounts = 0
state_lock = threading.Lock()
_file_lock = threading.Lock()

current_release_ver = "OB55"
current_client_ver = "1.132.6"
current_server_url = None
_version_config_lock = asyncio.Lock()
_version_config_ready = False


# ==========================================
# ভার্সন কনফিগ
# ==========================================
async def fetch_version_config_once() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    global current_release_ver, current_client_ver, current_server_url
    try:
        loop = asyncio.get_event_loop()
        app_version = await loop.run_in_executor(
            None, lambda: play_scraper('com.dts.freefireth', lang='hi', country='id')
        )
        app_version = app_version.get("version") or "1.132.6"
    except Exception:
        app_version = "1.132.6"

    api_url = (
        f"{VERSION_API}?version={app_version}"
        "&lang=hi&device=android&channel=android"
        "&appstore=googleplay&region=BD"
        "&whitelist_version=1.3.0&whitelist_sp_version=1.0.0"
    )

    for attempt in range(1, VERSION_API_RETRY + 1):
        try:
            log_info(f"Version API attempt {attempt}/{VERSION_API_RETRY}...")
            response = await client.get(api_url, timeout=VERSION_API_TIMEOUT)
            if response.status_code == 200:
                try:
                    data = response.json()
                except Exception:
                    try:
                        data = json.loads(response.text)
                    except Exception:
                        data = {}

                s_url = data.get("server_url")
                r_ver = data.get("remote_version") or data.get("client_version")
                l_rel = data.get("latest_release_version") or data.get("release_version")

                if l_rel: current_release_ver = str(l_rel)
                if r_ver: current_client_ver = str(r_ver)
                if s_url: current_server_url = str(s_url)

                if current_server_url:
                    return (current_release_ver, current_client_ver, current_server_url)
            elif response.status_code == 429:
                await asyncio.sleep(2.0 * attempt)
                continue
            else:
                await asyncio.sleep(1.0)
        except Exception as e:
            log_warn(f"Version API error: {type(e).__name__}")
            await asyncio.sleep(1.0)

    if current_server_url:
        return (current_release_ver, current_client_ver, current_server_url)
    return (None, None, None)


async def init_version_config():
    global _version_config_ready
    async with _version_config_lock:
        if _version_config_ready:
            return
        log_info("Fetching version config from real API...")
        l_rel, c_ver, s_url = await fetch_version_config_once()
        _version_config_ready = True

        if s_url:
            print(f"  {Color.GREEN}▶{Color.RESET} {Color.BOLD}Release Version{Color.RESET} : {Color.YELLOW}{l_rel}{Color.RESET}")
            print(f"  {Color.GREEN}▶{Color.RESET} {Color.BOLD}Client Version {Color.RESET} : {Color.YELLOW}{c_ver}{Color.RESET}")
            print(f"  {Color.GREEN}▶{Color.RESET} {Color.BOLD}Server URL     {Color.RESET} : {Color.CYAN}{s_url}{Color.RESET}")
            log_success("Version config cached.\n")
        else:
            log_error("Version API failed! Retrying in 5s...")
            _version_config_ready = False
            await asyncio.sleep(5)
            await init_version_config()


async def version_config() -> Tuple[str, str, str]:
    if not _version_config_ready or not current_server_url:
        await init_version_config()
    return (current_release_ver, current_client_ver, current_server_url)


# ==========================================
# API থেকে অ্যাকাউন্ট আনা
# ==========================================
async def fetch_one_account_from_api() -> Optional[Dict]:
    async with _API_SEMAPHORE:
        for attempt in range(1, API_FETCH_RETRY + 1):
            try:
                r = await client.get(API_BASE_URL, timeout=API_FETCH_TIMEOUT)
                if r.status_code == 429:
                    await asyncio.sleep(1.5 * attempt)
                    continue
                if r.status_code != 200:
                    await asyncio.sleep(0.8)
                    continue
                j = r.json()
                if j.get("status") != "SUCCESS":
                    await asyncio.sleep(0.6)
                    continue
                uid = str(j.get("uid", "")).strip()
                pw = str(j.get("password", "")).strip()
                if not uid or not pw:
                    await asyncio.sleep(0.6)
                    continue
                return {"uid": uid, "password": pw,
                        "name": j.get("name", ""),
                        "nickname": j.get("nickname", ""),
                        "region": j.get("region", "BD")}
            except Exception:
                await asyncio.sleep(0.6)
        return None


async def fetch_many_accounts(count: int, label: str = "Fetching") -> List[Dict]:
    if count <= 0: return []
    log_info(f"Fetching {Color.WHITE}{count}{Color.CYAN} accounts from API...")
    valid: List[Dict] = []
    done_count = 0
    CHUNK = max(1, API_CONCURRENT_FETCH)
    log_progress(0, count, label=label)
    for start in range(0, count, CHUNK):
        batch_size = min(CHUNK, count - start)
        tasks = [asyncio.create_task(fetch_one_account_from_api()) for _ in range(batch_size)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, dict) and res.get("uid"):
                valid.append(res)
        done_count += batch_size
        log_progress(min(done_count, count), count, label=label)
    log_progress_done()
    log_success(f"API returned {Color.WHITE}{len(valid)}{Color.GREEN}/{count} accounts.")
    return valid


# ==========================================
# ফাইল ম্যানেজমেন্ট
# ==========================================
def load_all_accounts_raw() -> List[Dict]:
    accounts = []
    if not os.path.exists(ACCOUNTS_TXT_FILE):
        return accounts
    try:
        with open(ACCOUNTS_TXT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith("#") or l.startswith("//"):
                    continue
                parts = None
                for delim in [":", "|", ",", " "]:
                    if delim in l:
                        p = [x.strip() for x in l.split(delim, 1)]
                        if len(p) == 2 and p[0] and p[1]:
                            parts = p
                            break
                if parts:
                    u, p = parts
                    accounts.append({"uid": u, "password": p})
    except Exception as e:
        log_error(f"load_all_accounts_raw: {e}")
    return accounts


def append_accounts_to_file(new_accounts: List[Dict]):
    if not new_accounts: return
    with _file_lock:
        try:
            existing = set()
            if os.path.exists(ACCOUNTS_TXT_FILE):
                with open(ACCOUNTS_TXT_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        u = line.strip().split(":")[0].strip()
                        if u: existing.add(u)
            with open(ACCOUNTS_TXT_FILE, "a", encoding="utf-8") as f:
                for acc in new_accounts:
                    uid = str(acc.get("uid", "")).strip()
                    pw = str(acc.get("password", "")).strip()
                    if not uid or not pw or uid in existing: continue
                    f.write(f"{uid}:{pw}\n")
                    existing.add(uid)
        except Exception as e:
            log_error(f"append_accounts_to_file: {e}")


def delete_accounts_from_file(uids_to_delete: set) -> int:
    if not uids_to_delete: return 0
    with _file_lock:
        try:
            if not os.path.exists(ACCOUNTS_TXT_FILE): return 0
            kept = []; removed = 0
            with open(ACCOUNTS_TXT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped: continue
                    uid = stripped.split(":")[0].strip()
                    if uid in uids_to_delete:
                        removed += 1; continue
                    kept.append(line if line.endswith("\n") else line + "\n")
            tmp = ACCOUNTS_TXT_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.writelines(kept)
            os.replace(tmp, ACCOUNTS_TXT_FILE)
            return removed
        except Exception as e:
            log_error(f"delete_accounts_from_file: {e}")
            return 0


# ==========================================
# ডিভাইস প্রোফাইল
# ==========================================
_MAX_DEVICES = 2000

def _generate_new_device() -> dict:
    device_list = [
        ("Xiaomi", "M2006C3LII", "PowerVR Rogue GE8320", "Android OS 10 / API-29 (QP1A.190711.020/V12.0.26.0.QCDINXM)"),
        ("Xiaomi", "22101316I", "Adreno (TM) 610", "Android OS 13 / API-33"),
        ("Samsung", "SM-G998B", "Adreno (TM) 660", "Android OS 12 / API-31"),
        ("Realme", "RMX3700", "Mali-G710", "Android OS 14 / API-34"),
        ("OnePlus", "CPH2451", "Adreno (TM) 740", "Android OS 13 / API-33"),
    ]
    brand, model, gpu, os_ver = random.choice(device_list)
    return {
        "unique_device_id": f"Google|{str(uuid.uuid4())}",
        "brand": brand, "model": model, "gpu_renderer": gpu,
        "system_software": os_ver,
        "screen_width": random.choice([1080, 1600, 720]),
        "screen_height": random.choice([2400, 720, 1600]),
        "screen_dpi": str(random.randint(300, 420)),
        "memory": random.randint(2800, 6500),
        "processor_details": f"ARM64 FP ASIMD AES VMH | {random.randint(2200, 3200)} | {random.randint(6, 12)}",
        "client_ip": f"{random.randint(103, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(10, 250)}"
    }

def get_device_for_account(account_identifier: str) -> dict:
    devices = {}
    if os.path.exists(DEVICES_FILE):
        try:
            with open(DEVICES_FILE, "r", encoding="utf-8") as f:
                devices = json.load(f)
                if not isinstance(devices, dict): devices = {}
        except Exception:
            devices = {}
    acc_key = str(account_identifier).strip()
    if acc_key in devices: return devices[acc_key]
    new_device = _generate_new_device()
    devices[acc_key] = new_device
    if len(devices) > _MAX_DEVICES:
        keys = list(devices.keys())
        for k in keys[:len(devices) - _MAX_DEVICES]:
            devices.pop(k, None)
    try:
        with open(DEVICES_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)
    except Exception:
        pass
    return new_device


# ==========================================
# DNS + Socket
# ==========================================
CLOUDFLARE_PRIMARY_DNS = "1.1.1.1"
CLOUDFLARE_SECONDARY_DNS = "1.0.0.1"
_DNS_CACHE: Dict[str, Tuple[str, float]] = {}
_DNS_CACHE_TTL = 300.0

async def resolve_host_cloudflare(hostname: str) -> str:
    if not hostname: return hostname
    parts = hostname.split('.')
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        return hostname
    now = time.time()
    if hostname in _DNS_CACHE:
        ip, exp = _DNS_CACHE[hostname]
        if now < exp: return ip

    def _query_cloudflare(server_ip: str) -> Optional[str]:
        s = None
        try:
            tx_id = random.randint(1000, 65535)
            header = struct.pack(">HHHHHH", tx_id, 0x0100, 1, 0, 0, 0)
            qname = b"".join(bytes([len(part)]) + part.encode('ascii') for part in hostname.split('.')) + b"\x00"
            query_pkt = header + qname + struct.pack(">HH", 1, 1)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.2)
            s.sendto(query_pkt, (server_ip, 53))
            resp, _ = s.recvfrom(1024)
            if len(resp) >= 12:
                ancount = struct.unpack(">H", resp[6:8])[0]
                if ancount > 0:
                    offset = 12 + len(qname) + 4
                    for _ in range(ancount):
                        if offset >= len(resp): break
                        if (resp[offset] & 0xC0) == 0xC0:
                            offset += 2
                        else:
                            while offset < len(resp) and resp[offset] != 0:
                                offset += 1 + resp[offset]
                            offset += 1
                        if offset + 10 > len(resp): break
                        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH", resp[offset:offset+10])
                        offset += 10
                        if rtype == 1 and rdlen == 4 and offset + 4 <= len(resp):
                            return socket.inet_ntoa(resp[offset:offset+4])
                        offset += rdlen
        except Exception:
            pass
        finally:
            if s:
                try: s.close()
                except Exception: pass
        return None

    loop = asyncio.get_running_loop()
    ip = await loop.run_in_executor(None, _query_cloudflare, CLOUDFLARE_PRIMARY_DNS)
    if not ip:
        ip = await loop.run_in_executor(None, _query_cloudflare, CLOUDFLARE_SECONDARY_DNS)
    if not ip:
        try:
            ip_info = await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
            if ip_info: ip = ip_info[0][4][0]
        except Exception:
            ip = hostname
    if ip:
        _DNS_CACHE[hostname] = (ip, now + _DNS_CACHE_TTL)
    return ip or hostname

def optimize_tcp_socket(sock: socket.socket):
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131072)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
    except Exception:
        pass

async def safe_close_writer(writer):
    if not writer: return
    try:
        if not writer.is_closing(): writer.close()
        await asyncio.wait_for(writer.wait_closed(), timeout=1.0)
    except Exception:
        pass


# ==========================================
# ক্যাশ
# ==========================================
def _json_serializer(obj):
    if isinstance(obj, (bytes, bytearray)):
        return {"__bytes_hex__": bytes(obj).hex()}
    raise TypeError(f"Type {type(obj)} not serializable")

def _json_deserializer(obj):
    if isinstance(obj, dict):
        if "__bytes_hex__" in obj and len(obj) == 1:
            try: return bytes.fromhex(obj["__bytes_hex__"])
            except Exception: return b""
        return {k: _json_deserializer(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_deserializer(x) for x in obj]
    return obj

def _load_token_cache() -> Dict[str, Any]:
    if not os.path.exists(TOKEN_CACHE_FILE): return {}
    try:
        with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content: return {}
        return _json_deserializer(json.loads(content))
    except Exception:
        return {}

def _save_token_cache(cache: Dict[str, Any]):
    try:
        tmp_file = TOKEN_CACHE_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, default=_json_serializer)
        os.replace(tmp_file, TOKEN_CACHE_FILE)
    except Exception:
        pass

def cache_get(uid: str) -> Optional[Dict]:
    cache = _load_token_cache()
    entry = cache.get(str(uid))
    if not entry: return None
    if time.time() - entry.get("cached_at", 0) > TOKEN_CACHE_TTL:
        cache_invalidate(uid); return None
    if str(entry.get("account_id", "")).isdigit():
        entry["account_id"] = int(entry["account_id"])
    if not isinstance(entry.get("login_payload_data"), (bytes, bytearray)):
        cache_invalidate(uid); return None
    return entry

def cache_set(uid: str, account_data: Dict):
    cache = _load_token_cache()
    entry = dict(account_data)
    entry["cached_at"] = time.time()
    cache[str(uid)] = entry
    _save_token_cache(cache)

def cache_invalidate(uid: str):
    cache = _load_token_cache()
    if str(uid) in cache:
        del cache[str(uid)]
        _save_token_cache(cache)

def clear_all_cache():
    try:
        if os.path.exists(TOKEN_CACHE_FILE): os.remove(TOKEN_CACHE_FILE)
    except Exception:
        pass
    _DNS_CACHE.clear()
    gc.collect()

async def aes_encrypt(payload, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(payload, AES.block_size))

def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict): return default
    if key in d:
        val = d[key].get('data')
        return val if val is not None else default
    if str(key) in d:
        val = d[str(key)].get('data')
        return val if val is not None else default
    return default

async def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {"wire_type": result.wire_type}
        if result.wire_type in ("varint", "string", "bytes"):
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            if hasattr(result.data, "results"):
                field_data["data"] = await parse_results(result.data.results)
            elif isinstance(result.data, list):
                field_data["data"] = await parse_results(result.data)
            else:
                field_data["data"] = str(result.data)
        result_dict[str(result.field)] = field_data
    return result_dict


# ==========================================
# গেম অথেনটিকেশন
# ==========================================
async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 13;en;IN;)",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    payload = {
        "client_id": 100067,
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_type": 2,
        "password": str(password).strip(),
        "response_type": "token",
        "uid": int(str(uid).strip())
    }
    for attempt in range(2):
        try:
            response = await client.post(url, headers=hdrs, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                inner = res_data.get("data", res_data)
                open_id = inner.get("open_id")
                access_token = inner.get("access_token")
                platform = inner.get("platform", 4)
                if open_id and access_token:
                    return open_id, access_token, platform
            elif response.status_code == 429:
                await asyncio.sleep(1.0); continue
        except Exception:
            pass
        await asyncio.sleep(0.3)
    return None

async def build_majorlogin_payload(open_id, access_token, platform, client_version, device_info):
    try:
        major_login = MajoRLoGinrEq_pb2.MajorLogin()
        major_login.open_id = open_id
        major_login.access_token = access_token
        major_login.client_version = client_version
        major_login.event_time = str(datetime.now())[:-7]
        major_login.game_name = "free fire"
        major_login.platform_id = 1
        major_login.system_software = "Android OS 10 / API-29 (QP1A.190711.020/V12.0.26.0.QCDINXM)"
        major_login.system_hardware = "Handheld"
        major_login.telecom_operator = "Ncell"
        major_login.network_type = "WIFI"
        major_login.screen_width = 1600
        major_login.screen_height = 720
        major_login.screen_dpi = "320"
        major_login.processor_details = "ARMv7 VFPv3 NEON | 2001 | 8"
        major_login.memory = 3790
        major_login.gpu_renderer = "PowerVR Rogue GE8320"
        major_login.gpu_version = "OpenGL ES 3.2 build 1.11@5425693"
        major_login.unique_device_id = "Google|00000000-0000-0000-0000-000000000000"
        major_login.client_ip = "111.119.38.133"
        major_login.language = "en"
        major_login.open_id_type = "4"
        major_login.device_type = "Handheld"
        major_login.device_model = "Xiaomi M2006C3LII"
        major_login.country_code = "BD"
        major_login.platform_sdk_id = 1
        major_login.network_operator_a = "Ncell"
        major_login.network_type_a = "WIFI"
        major_login.client_using_version = "1ac4b80ecf0478a44203bf8fac6120f5"
        major_login.external_storage_total = 53041
        major_login.external_storage_available = 7291
        major_login.internal_storage_total = 2176
        major_login.game_disk_storage_available = 7395
        major_login.game_disk_storage_total = 53041
        major_login.external_sdcard_avail_storage = 7395
        major_login.external_sdcard_total_storage = 53041
        major_login.field_70 = 4
        major_login.login_by = 2
        major_login.library_path = "/data/app/com.dts.freefireth-yAPXAhp2RyIlrtNAM0VzKQ==/lib/arm"
        major_login.reg_avatar = 1
        major_login.library_token = "066a589fa3f5658377634fe7b1d88556|/data/app/com.dts.freefireth-yAPXAhp2RyIlrtNAM0VzKQ==/base.apk"
        major_login.channel_type = 6
        major_login.cpu_type = 1
        major_login.cpu_architecture = "32"
        major_login.client_version_code = "2019121227"
        major_login.field_85 = 3
        major_login.graphics_api = "OpenGLES2"
        major_login.supported_astc_bitset = 3071
        major_login.login_open_id_type = 4
        major_login.loading_time = 9329
        major_login.release_channel = "3rd_party"
        major_login.extra_info = "KqsHT3r+fXQIu/dyZrEa8fJBhbJ5uqDES7YsAUfu+Mck9A+Bly6lFfYk7Q7Nj68pqI8I3g4Oz3gLxWef6Eh/jKyzHug="
        major_login.android_engine_init_flag = 111207
        major_login.field_96 = json.dumps({"cur_rate": None, "support_etc2": False}, separators=(',', ':'))
        major_login.if_push = 1
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        major_login.field_102 = bytes.fromhex("42 54 4c 10 53 0e 5b 04 30")
        major_login.field_104 = 47591
        major_login.field_105 = 1
        major_login.field_106 = "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|1c2462939e53942fc995400436a3dc7b"
        major_login.field_107 = "c8e41b7a93f02d56e1a94c7b8203f5d1"
        string = major_login.SerializeToString()
        return await aes_encrypt(string, AES_KEY, AES_IV)
    except Exception:
        return None

async def send_majorlogin(data, release_version, server_url):
    try:
        if not server_url: return None
        url = f"{server_url.rstrip('/')}/MajorLogin"
        req_headers = headers.copy()
        req_headers["ReleaseVersion"] = release_version
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200: return None
        response_content = response.content
        if len(response_content) < 40: return None
        proto_payload = response_content[64:] if len(response_content) > 64 else response_content
        res_proto = MajorLoginRes()
        try:
            res_proto.ParseFromString(proto_payload)
            if res_proto.region and res_proto.token: return res_proto
        except Exception:
            pass
        for offset in range(min(128, len(proto_payload))):
            try:
                candidate = MajorLoginRes()
                candidate.ParseFromString(proto_payload[offset:])
                if candidate.region and candidate.token: return candidate
            except Exception:
                pass
        try:
            res_proto = MajorLoginRes()
            res_proto.ParseFromString(response_content)
            return res_proto
        except Exception:
            return None
    except Exception:
        return None

async def send_getlogin(data, base_url, token, release_version):
    try:
        if not base_url: return None
        url = f"{base_url.rstrip('/')}/GetLoginData"
        req_headers = headers.copy()
        req_headers["ReleaseVersion"] = release_version
        req_headers['Authorization'] = f"Bearer {token}"
        req_headers['Host'] = "clientbp.ppmainecoonghj.com"
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200: return None
        response_content = response.content
        res_proto = thunderFF_pb2.GetLoginDataRes()
        parsed_successfully = False
        try:
            res_proto.ParseFromString(response_content)
            if res_proto.functional_addrs or res_proto.informational_addrs:
                parsed_successfully = True
        except Exception:
            pass
        if not parsed_successfully:
            for offset in range(min(128, len(response_content))):
                try:
                    candidate = thunderFF_pb2.GetLoginDataRes()
                    candidate.ParseFromString(response_content[offset:])
                    if candidate.functional_addrs or candidate.informational_addrs:
                        res_proto = candidate; break
                except Exception:
                    pass
        dict_res = {}
        try:
            parsed = Parser().parse(response_content.hex())
            dict_res = await parse_results(parsed)
        except Exception:
            pass
        return res_proto, dict_res
    except Exception:
        return None

async def build_tcp_startup_packet(account_id, token, server_time, key, iv, region="BD", typ='OnLine'):
    uid_hex = f"{int(account_id):016x}"
    timestamp_hex = f"{int(server_time):08x}"
    encode_token = token.encode()
    encrypted_packet = (await aes_encrypt(encode_token, key, iv)).hex()
    encrypted_packet_length = f"{len(encrypted_packet) // 2:08x}"
    reg = str(region).upper() if region else "BD"
    if typ == 'OnLine':
        prefix = '7219' if reg == 'BD' else ('7214' if reg == 'IND' else '7215')
        return f"{prefix}{uid_hex}{timestamp_hex}00000000{encrypted_packet_length}{encrypted_packet}"
    else:
        prefix = '8119' if reg == 'BD' else ('8114' if reg == 'IND' else '8115')
        return f"{prefix}{uid_hex}{timestamp_hex}{encrypted_packet_length}{encrypted_packet}"

async def send_keep_alive(region="BD"):
    try:
        reg = str(region).upper() if region else "BD"
        ka_hex = "0219" if reg == "BD" else ("0214" if reg == "IND" else "0215")
        return bytes.fromhex(ka_hex)
    except Exception:
        return bytes.fromhex("0219")


# ==========================================
# অ্যাকাউন্ট প্রসেসর
# ==========================================
async def process_account_uid_pass(uid: str, password: str) -> Optional[Dict]:
    cached = cache_get(uid)
    if cached: return cached
    try:
        release_version, client_version, server_url = await version_config()
        if not server_url: return None
        tokengrant_res = await get_access_token(uid, password)
        if not tokengrant_res: return None
        open_id, access_token, platform = tokengrant_res
        device_info = get_device_for_account(uid)
        login_payload_data = await build_majorlogin_payload(open_id, access_token, platform, client_version, device_info)
        if not login_payload_data: return None
        majorlogin_res = await send_majorlogin(login_payload_data, release_version, server_url)
        if not majorlogin_res: return None
        getlogin_res = await send_getlogin(login_payload_data, majorlogin_res.url, majorlogin_res.token, release_version)
        if not getlogin_res: return None
        res_proto, dict_res = getlogin_res
        acc_id = str(majorlogin_res.account_id)
        level = int(get_proto_field(dict_res, 6, 1))
        exp = int(get_proto_field(dict_res, 7, 0))
        likes = int(get_proto_field(dict_res, 8, 0))
        nickname = res_proto.nickname or get_proto_field(dict_res, 4, f"Player_{acc_id}")
        region = majorlogin_res.region or get_proto_field(dict_res, 3, "BD")
        account_data = {
            'account_id': majorlogin_res.account_id,
            'nickname': nickname, 'region': region,
            'level': level, 'exp': exp, 'likes': likes,
            'open_id': open_id, 'access_token': access_token,
            'platform': str(platform),
            'token': majorlogin_res.token,
            'server_time': majorlogin_res.server_time,
            'aes_ak': majorlogin_res.aes_ak,
            'iv_i': majorlogin_res.iv_i,
            'functional_addrs': res_proto.functional_addrs or get_proto_field(dict_res, 14),
            'informational_addrs': res_proto.informational_addrs or get_proto_field(dict_res, 32),
            'release_version': release_version,
            'client_version': client_version,
            'server_url': majorlogin_res.url,
            'login_payload_data': login_payload_data,
            'auth_type': 'guest',
            'auth_uid': str(uid),
            'auth_password': str(password)
        }
        cache_set(uid, account_data)
        return account_data
    except Exception:
        return None


# ==========================================
# অনলাইন কিপার — সব ইভেন্ট টার্মিনালে দেখাবে
# ==========================================
async def run_account_online_worker(account_data: Dict, group_index: int, stop_event: asyncio.Event, failure_callback=None):
    global online_count, squad_created_count

    acc_id = str(account_data['account_id'])
    nickname = account_data.get('nickname', 'Player')
    level = account_data.get('level', 1)
    region = account_data.get('region', 'BD')
    func_addrs = account_data.get('functional_addrs')

    if not func_addrs:
        if failure_callback:
            await failure_callback(acc_id)
        return

    ip, port = func_addrs.split(":")
    key = account_data['aes_ak']
    iv = account_data['iv_i']

    cycle_lifetime = GROUP_LIFETIMES[group_index]
    reconnect_fail_count = 0
    short_name = f"{nickname[:14]}" if nickname else acc_id

    with state_lock:
        online_count += 1

    log_success(f"ONLINE → {Color.WHITE}{acc_id}{Color.GREEN} | {Color.YELLOW}{short_name}{Color.GREEN} | G{group_index+1}")

    try:
        while not stop_event.is_set():
            writer = None
            reader = None
            try:
                tcp_startup = await build_tcp_startup_packet(
                    account_data['account_id'], account_data['token'],
                    account_data['server_time'], key, iv,
                    region=region, typ='OnLine'
                )
                resolved_ip = await resolve_host_cloudflare(ip)
                reader, writer = await asyncio.open_connection(resolved_ip, int(port))
                raw_sock = writer.get_extra_info('socket')
                if raw_sock: optimize_tcp_socket(raw_sock)

                if writer.is_closing():
                    raise ConnectionError("Socket closed right after connect")
                writer.write(bytes.fromhex(tcp_startup))
                await writer.drain()

                init_ka = await send_keep_alive(region)
                if init_ka and not writer.is_closing():
                    writer.write(init_ka)
                    await writer.drain()

                ka_bytes = await send_keep_alive(region)
                reconnect_fail_count = 0

                while not stop_event.is_set():
                    # ═══════ SQUAD CREATE ═══════
                    try:
                        if writer.is_closing():
                            raise ConnectionError("Socket closed")
                        open_sq_pkt = OpEnSq(key, iv, region, current_client_ver)
                        if asyncio.iscoroutine(open_sq_pkt):
                            open_sq_pkt = await open_sq_pkt
                        if open_sq_pkt:
                            writer.write(open_sq_pkt)
                            await writer.drain()
                            log_squad(f"[G{group_index+1}] Squad Created → {Color.WHITE}{acc_id}{Color.MAGENTA} ({short_name})")
                            with state_lock:
                                squad_created_count += 1
                            await asyncio.sleep(0.3)
                    except (ConnectionError, OSError):
                        raise
                    except Exception:
                        pass

                    # ═══════ SQUAD SIZE ═══════
                    try:
                        if writer.is_closing():
                            raise ConnectionError("Socket closed")
                        sq_size_pkt = cHSq22(4, acc_id, key, iv, region)
                        if asyncio.iscoroutine(sq_size_pkt):
                            sq_size_pkt = await sq_size_pkt
                        if sq_size_pkt:
                            writer.write(sq_size_pkt)
                            await writer.drain()
                            await asyncio.sleep(0.3)
                    except (ConnectionError, OSError):
                        raise
                    except Exception:
                        pass

                    # ═══════ WORLD RECRUIT ═══════
                    try:
                        if writer.is_closing():
                            raise ConnectionError("Socket closed")
                        recruit_pkt = MAHIR_World_Recruit_Packet(acc_id, key, iv)
                        if asyncio.iscoroutine(recruit_pkt):
                            recruit_pkt = await recruit_pkt
                        if recruit_pkt:
                            writer.write(recruit_pkt)
                            await writer.drain()
                            log_recruit(f"[G{group_index+1}] World Recruit → {Color.WHITE}{acc_id}{Color.BLUE} ({short_name})")
                            await asyncio.sleep(0.3)
                    except (ConnectionError, OSError):
                        raise
                    except Exception:
                        pass

                    # ═══════ ২৫ সেকেন্ড LIVE ═══════
                    elapsed = 0.0
                    while elapsed < cycle_lifetime and not stop_event.is_set():
                        try:
                            await asyncio.wait_for(asyncio.sleep(5.0), timeout=5.0)
                        except asyncio.TimeoutError:
                            pass
                        except asyncio.CancelledError:
                            raise
                        elapsed += 5.0
                        if stop_event.is_set(): break
                        try:
                            if writer.is_closing():
                                raise ConnectionError("Socket closed")
                            writer.write(ka_bytes)
                            await writer.drain()
                        except (ConnectionError, OSError):
                            raise
                        except Exception:
                            pass

                    if stop_event.is_set(): break

                    # ═══════ LEAVE SQUAD ═══════
                    try:
                        if writer.is_closing():
                            raise ConnectionError("Socket closed")
                        chsq_pkt = cHSq(4, acc_id, key, iv, region)
                        if asyncio.iscoroutine(chsq_pkt):
                            chsq_pkt = await chsq_pkt
                        if chsq_pkt:
                            writer.write(chsq_pkt)
                            await writer.drain()
                            await asyncio.sleep(0.3)
                        leave_pkt = leave_squad_packet(key, iv, region, acc_id)
                        if asyncio.iscoroutine(leave_pkt):
                            leave_pkt = await leave_pkt
                        if leave_pkt:
                            writer.write(leave_pkt)
                            await writer.drain()
                            log_leave(f"[G{group_index+1}] Left Squad ← {Color.WHITE}{acc_id}{Color.YELLOW} ({short_name}) after {cycle_lifetime:.0f}s")
                    except (ConnectionError, OSError):
                        raise
                    except Exception:
                        pass

                    # ═══════ ৩০ সেকেন্ড cycle এর জন্য অপেক্ষা ═══════
                    rest_time = max(0.5, GROUP_CYCLE_SLEEP - cycle_lifetime)
                    try:
                        await asyncio.wait_for(asyncio.sleep(rest_time + random.uniform(0.5, 1.5)), timeout=rest_time + 3.0)
                    except asyncio.TimeoutError:
                        pass

            except asyncio.CancelledError:
                raise
            except Exception:
                reconnect_fail_count += 1
                if reconnect_fail_count >= 6:
                    log_warn(f"Account {acc_id} dead after 6 fails → deleting & replenishing")
                    if failure_callback:
                        await failure_callback(acc_id)
                    return
            finally:
                await safe_close_writer(writer)
                writer = None

            if stop_event.is_set(): break
            try:
                await asyncio.wait_for(asyncio.sleep(2.0), timeout=3.0)
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                raise

    finally:
        with state_lock:
            online_count = max(0, online_count - 1)


# ==========================================
# টোকেন তৈরি
# ==========================================
async def create_token_for_account(acc_info: dict, index: int, total: int) -> Optional[Dict]:
    account_data = None
    async with _THREAD_SEMAPHORE:
        for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
            try:
                if "uid" in acc_info and "password" in acc_info:
                    account_data = await process_account_uid_pass(str(acc_info["uid"]).strip(), str(acc_info["password"]).strip())
                if account_data:
                    break
                else:
                    if attempt < MAX_LOGIN_ATTEMPTS:
                        await asyncio.sleep(1.0)
            except Exception:
                if attempt < MAX_LOGIN_ATTEMPTS:
                    await asyncio.sleep(1.0)
    return account_data


async def create_all_tokens_with_progress(accounts: List[Dict]) -> Tuple[List[Dict], set]:
    total = len(accounts)
    valid_accounts: List[Dict] = []
    failed_uids: set = set()
    done_count = 0

    log_info(f"Creating tokens for {Color.WHITE}{total}{Color.CYAN} accounts ({MAX_LOGIN_THREADS} threads)...")
    log_progress(0, total, label="Tokens ")

    CHUNK = max(1, MAX_LOGIN_THREADS)
    for start in range(0, total, CHUNK):
        batch = accounts[start:start + CHUNK]
        tasks = []
        for i, acc in enumerate(batch):
            idx = start + i + 1
            tasks.append(asyncio.create_task(create_token_for_account(acc, idx, total)))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for acc, res in zip(batch, results):
            if isinstance(res, dict) and res.get('account_id'):
                valid_accounts.append(res)
            else:
                uid = acc.get("uid")
                if uid: failed_uids.add(str(uid))
        done_count += len(batch)
        log_progress(min(done_count, total), total, label="Tokens ")

    log_progress_done()
    log_success(f"Token creation: {Color.WHITE}{len(valid_accounts)}{Color.GREEN}/{total} OK | {Color.RED}{len(failed_uids)}{Color.GREEN} failed")
    return valid_accounts, failed_uids


# ==========================================
# ensure_accounts + Replenish
# ==========================================
async def ensure_accounts(target_count: int, label: str = "ensure"):
    current = len(load_all_accounts_raw())
    need = target_count - current
    if need <= 0:
        log_info(f"[{label}] Already have {current} accounts (target {target_count}).")
        return current
    log_warn(f"[{label}] Need {Color.WHITE}{need}{Color.YELLOW} more (have {current}, target {target_count}).")
    fetched = await fetch_many_accounts(need, label=label)
    if fetched:
        append_accounts_to_file(fetched)
    final = len(load_all_accounts_raw())
    log_success(f"[{label}] File now has {Color.WHITE}{final}{Color.GREEN} accounts.")
    return final


async def replenish_failed_account(uid: str):
    try:
        removed = delete_accounts_from_file({str(uid)})
        if removed:
            log_warn(f"Deleted dead account {uid}")
        new_acc = await fetch_one_account_from_api()
        if new_acc:
            append_accounts_to_file([new_acc])
            log_success(f"Replacement added: {Color.WHITE}{new_acc['uid']}{Color.GREEN}")
        else:
            log_error(f"Failed to fetch replacement for {uid}")
    except Exception as e:
        log_error(f"replenish_failed_account: {e}")


# ==========================================
# মেইন এক্সিকিউশন
# ==========================================
async def main():
    global total_accounts, squad_created_count
    log_banner()

    # ═══════ ধাপ ০: ভার্সন কনফিগ ═══════
    await init_version_config()

    # ═══════ ধাপ ১: ফাইলে থাকা অ্যাকাউন্ট চেক ═══════
    current_count = len(load_all_accounts_raw())
    if current_count > 0:
        log_info(f"Found {Color.WHITE}{current_count}{Color.CYAN} existing accounts in file.")
    else:
        log_info("No existing accounts. Starting fresh.")

    run_cycle = 0
    while True:
        run_cycle += 1
        log_info(f"{Color.MAGENTA}═══════ CYCLE #{run_cycle} ═══════{Color.CYAN}")

        # ═══════ ধাপ ২: টার্গেট নিশ্চিত করা ═══════
        # Cycle 1: INITIAL (৪০০), Cycle 2+: TARGET (৭০০)
        target = INITIAL_ACCOUNT_COUNT if run_cycle == 1 else TARGET_ACCOUNT_COUNT
        await ensure_accounts(target, label=f"cycle#{run_cycle}")

        # ═══════ ধাপ ৩: সব অ্যাকাউন্ট লোড ═══════
        accounts = load_all_accounts_raw()
        if not accounts:
            log_error("No accounts! Retrying in 10s...")
            await asyncio.sleep(10); continue

        total_accounts = len(accounts)
        log_info(f"File contains {Color.WHITE}{total_accounts}{Color.CYAN} accounts. Total target: {target}")

        # ═══════ ধাপ ৪: টোকেন তৈরি ═══════
        valid_accounts, failed_uids = await create_all_tokens_with_progress(accounts)

        # ═══════ ধাপ ৫: ফেইল ডিলিট + রিপ্লেস ═══════
        if failed_uids:
            log_warn(f"Deleting {len(failed_uids)} failed accounts...")
            delete_accounts_from_file(failed_uids)
            replacements = await fetch_many_accounts(len(failed_uids), label="Replacing")
            if replacements:
                append_accounts_to_file(replacements)
                log_success(f"Replaced {len(replacements)} accounts in file.")

        if not valid_accounts:
            log_error("No valid tokens! Retrying in 10s...")
            await asyncio.sleep(10); continue

        # ═══════ ধাপ ৬: গ্রুপ ভাগ ═══════
        groups: List[List[Tuple[int, Dict]]] = [[], [], []]
        for i, acc_data in enumerate(valid_accounts):
            group_idx = i % NUM_GROUPS
            groups[group_idx].append((group_idx, acc_data))

        print()
        log_info(f"{Color.BOLD}════ GROUP DISTRIBUTION ════{Color.CYAN}")
        for g in range(NUM_GROUPS):
            log_info(f"  Group {g+1}: {Color.WHITE}{len(groups[g])}{Color.CYAN} accounts | Live: {GROUP_LIFETIMES[g]:.0f}s | Cycle: {GROUP_CYCLE_SLEEP:.0f}s")
        log_info(f"{Color.BOLD}════ ALL {len(valid_accounts)} ACCOUNTS → ONLINE NOW ════{Color.CYAN}")
        print()

        # ═══════ ধাপ ৭: অনলাইন ═══════
        stop_event = asyncio.Event()
        online_tasks = []
        squad_created_count = 0

        async def on_failure(uid: str):
            try:
                await replenish_failed_account(uid)
            except Exception:
                pass

        for group_idx in range(NUM_GROUPS):
            for _, acc_data in groups[group_idx]:
                t = asyncio.create_task(
                    run_account_online_worker(acc_data, group_idx, stop_event, failure_callback=on_failure)
                )
                online_tasks.append(t)

        # ═══════ ধাপ ৮: ৫ ঘন্টা অপেক্ষা (লাইভ status) ═══════
        refresh_start = time.time()
        last_status = time.time()
        while True:
            elapsed = time.time() - refresh_start
            if elapsed >= FULL_REFRESH_INTERVAL:
                log_warn("5 Hours done! Full refresh...")
                break
            if time.time() - last_status >= 30.0:
                last_status = time.time()
                file_count = len(load_all_accounts_raw())
                online_now = online_count
                squads = squad_created_count
                remaining = FULL_REFRESH_INTERVAL - elapsed
                hrs = int(remaining // 3600); mins = int((remaining % 3600) // 60); secs = int(remaining % 60)
                log_info(
                    f"{Color.BOLD}STATUS{Color.RESET} | "
                    f"{Color.GREEN}Online: {online_now}{Color.RESET} | "
                    f"{Color.MAGENTA}Squads: {squads}{Color.RESET} | "
                    f"{Color.CYAN}File: {file_count}{Color.RESET} | "
                    f"{Color.YELLOW}Refresh in {hrs}h {mins}m {secs}s{Color.RESET}"
                )
                if file_count < MIN_ACCOUNTS_TO_KEEP:
                    try:
                        await ensure_accounts(MIN_ACCOUNTS_TO_KEEP, label="replenish-bg")
                    except Exception:
                        pass
            await asyncio.sleep(5)

        # ═══════ ধাপ ৯: সব বন্ধ ═══════
        log_warn("Stopping all sessions...")
        stop_event.set()
        for t in online_tasks:
            t.cancel()
        await asyncio.gather(*online_tasks, return_exceptions=True)
        await asyncio.sleep(random.uniform(2.0, 3.0))

        clear_all_cache()
        log_success("Cache cleared. Restarting cycle...")
        await asyncio.sleep(1.0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        log_warn("Shutting down...")
        log_success("All sessions closed.")