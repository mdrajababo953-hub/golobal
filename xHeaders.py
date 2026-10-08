import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def ToK():
    while True:
        try:
            r = requests.get('https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?&type=ToKens')
            t = r.text
            i = t.find("ToKens : [")
            if i != -1:
                j = t.find("]", i)
                L = [x.strip(" '\"") for x in t[i+11:j].split(',') if x.strip()]
                if L:
                    with open("token.txt", "w") as f:
                        f.write(random.choice(L))
        except: pass
        time.sleep(5 * 60 * 60)

Thread(target=ToK , daemon = True).start()



def equie_emote(JWT,url):
    url = f"{url}/ChooseEmote"

    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {JWT}",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        #"Host": "clientbp.ggblueshark.com",
        "ReleaseVersion": "OB53",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }

    data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")

    requests.post(url, headers=headers, data=data)





def GeTToK():  
    with open("token.txt") as f: return f.read().strip()
    
def Likes(id):
    try:
        text = requests.get(f"https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=likes").text
        get = lambda p: re.search(p, text)
        name, lvl, exp, lb, la, lg = (get(r).group(1) if get(r) else None for r in 
            [r"PLayer NamE\s*:\s*(.+)", r"PLayer SerVer\s*:\s*(.+)", r"Exp\s*:\s*(\d+)", 
             r"LiKes BeFore\s*:\s*(\d+)", r"LiKes After\s*:\s*(\d+)", r"LiKes GiVen\s*:\s*(\d+)"])
        return name , f"{lvl}" if lvl else None, int(lb) if lb else None, int(la) if la else None, int(lg) if lg else None
    except: return None, None, None, None, None
    
def Requests_SPam(id):
    Api = requests.get(f'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=spam')        
    if Api.status_code in [200, 201] and '[SuccessFuLy] -> SenDinG Spam ReQuesTs !' in Api.text: return True
    else: return False

def GeT_Name(uid , Token):
    data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid , Tp = 'Uid')}1007"))
    url = "https://clientbp.common.ggpolarbear.com/GetPlayerPersonalShow"
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB53',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {GeTToK()}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    response = requests.post(url , headers=headers , data=data ,verify=False)
    if response.status_code == 200 or 201:
        packet = binascii.hexlify(response.content).decode('utf-8')
        BesTo_data = json.loads(DeCode_PackEt(packet))      
        try:
            a1 = BesTo_data["1"]["data"]["3"]["data"]
            return a1
        except: return ''  
    else: return ''
            	  	
async def GeT_PLayer_InFo(uid, Token):
    try:
        # ১. ইউআইডি এবং প্যাকেট এনক্রিপ্ট করা
        enc_uid = await EnC_Uid(uid, Tp='Uid')
        payload_hex = f"08{enc_uid}1007"
        enc_aes = await EnC_AEs(payload_hex)
        data = bytes.fromhex(enc_aes)
        
        # ২. সার্ভার ইউআরএল (প্রয়োজনে ggwhitehawk.com ট্রাই করতে পারেন যদি polarbear কাজ না করে)
        url = "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow"
        
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB53', # এটি বর্তমান OB ভার্সন অনুযায়ী হতে হবে
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {Token}',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
            
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
        
        if response.status_code == 200 or response.status_code == 201:
            packet = binascii.hexlify(response.content).decode('utf-8')
            decoded_packet = await DeCode_PackEt(packet)
            
            if not decoded_packet:
                return "[b][c][FF0000]❌ প্যাকেট ডিকোড করা সম্ভব হয়নি!"
                
            BesTo_data = json.loads(decoded_packet)
            NoCLan = False   
            
            try:
                # তথ্যগুলো ফিল্ড আইডি অনুযায়ী সংগ্রহ (Protobuf fields)
                # নোট: ফিল্ড আইডি মাঝে মাঝে গেম আপডেটের সাথে পরিবর্তন হয়
                base = BesTo_data.get("1", {}).get("data", {})
                
                a1 = str(base.get("1", {}).get("data", uid)) # Account UID
                a2 = base.get("21", {}).get("data", "0")    # Likes
                a3 = base.get("3", {}).get("data", "Unknown") # Nickname
                player_server = base.get("5", {}).get("data", "N/A")
                player_level = base.get("6", {}).get("data", "0")
                
                # বায়ো সংগ্রহ (সাধারণত ফিল্ড ৯ এ থাকে)
                player_bio = BesTo_data.get("9", {}).get("data", {}).get("9", {}).get("data", "No Bio")
                
                # টাইমস্ট্যাম্প কনভার্ট
                acc_create_ts = base.get("44", {}).get("data", 0)
                last_log_ts = base.get("24", {}).get("data", 0)
                
                account_date = datetime.fromtimestamp(acc_create_ts).strftime("%d/%m/%y") if acc_create_ts else "N/A"
                last_login = datetime.fromtimestamp(last_log_ts).strftime("%d/%m/%y %I:%M %p") if last_log_ts else "N/A"
                
                # গিল্ড ইনফো
                clan_data = BesTo_data.get("6", {}).get("data", {})
                if clan_data:
                    clan_id = clan_data.get("1", {}).get("data", "N/A")
                    clan_name = clan_data.get("2", {}).get("data", "N/A")
                    clan_leader = clan_data.get("3", {}).get("data", "N/A")
                    clan_level = clan_data.get("4", {}).get("data", "0")
                    clan_members_num = clan_data.get("6", {}).get("data", "0")
                else:
                    NoCLan = True

                if NoCLan:
                    a = f'''
[b][c][00FF00]✅ PLAYER INFO FOUND!

[FFFF00]👤 Profile Info :
[ffffff] Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Created : {account_date}
 Last Login : {last_login}
 Bio : {player_bio}
 
[00FFFF]Dev : MAHIR BOT'''            
                    return a
                                                            
                else:                                                       
                    a = f'''
[b][c][00FF00]✅ PLAYER INFO FOUND!

[FFFF00]👤 Profile Info :
[ffffff] Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Created : {account_date}
 Last Login : {last_login}
 Bio : {player_bio}

[FFFF00]🛡️ Guild Info :
[ffffff] Guild Name : {clan_name}
 Guild Uid : {xMsGFixinG(clan_id)}
 Guild LeveL : {clan_level}
 Members : {clan_members_num}

[00FFFF]Dev : MAHIR BOT'''	
                    return a
                                           
            except Exception as e:
               print(f"Parsing Error: {e}")
               return f'\n[b][c][FFD700]❌ তথ্য পার্স করতে সমস্যা হয়েছে!\n'
        else:
            print(f"Server Response Code: {response.status_code}")
            return f'\n[b][c][FFD700]❌ সার্ভার এরর! কোড: {response.status_code}\n'
            
    except Exception as e:
        print(f"Global Error: {e}")
        return f'\n[b][c][FFD700]❌ এরর: {str(e)[:50]}\n'
    
def DeLet_Uid(id , Tok):
    print(f' Done FuckinG > {id} ')
    url = 'https://clientbp.ggpolarbear.com/RemoveFriend'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB53',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {Tok}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'}
    data = bytes.fromhex(EnC_AEs(f"08a7c4839f1e10{EnC_Uid(id , Tp = 'Uid')}"))
    ResPonse = requests.post(url , headers=headers , data=data , verify=False)    
    if ResPonse.status_code == 400 and 'BR_FRIEND_NOT_SAME_REGION' in ResPonse.text:
        return f'[b][c]Id : {xMsGFixinG(id)} Not In Same Region !'
    elif ResPonse.status_code == 200:
        return f'[b][c]Good Response Done Delete Id : {xMsGFixinG(id)} !'
    else:
        return f'[b][c]Erorr !'
                                                        
def ChEck_The_Uid(id):
    Api = requests.get("https://panel-g2ccathtf6gdcmdw.polandcentral-01.azurewebsites.net/Uids")
    if Api.status_code not in [200, 201]: 
        return False    
    lines = Api.text.splitlines()    
    for i, line in enumerate(lines):
        if f' - Uid : {id}' in line:
            expire, status = None, None
            for sub_line in lines[i:]:
                if "Expire In" in sub_line: 
                    expire = re.search(r"Expire In\s*:\s*(.*)", sub_line).group(1).strip()
                if "Status" in sub_line: 
                    status = re.search(r"Status\s*:\s*(\w+)", sub_line).group(1)
                if expire and status: return status, expire
            return False
    return False