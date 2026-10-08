# By MAHIR

import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os , asyncio
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
async def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()
    
async def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()
    
async def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  

async def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

async def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
    
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
    
async def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return await EnC_Vr(field_header) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr(field_header) + await EnC_Vr(len(encoded_value)) + encoded_value

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)  # لازم await
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet
    
async def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F ; return F
    else: return F

async def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = await Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

async def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = await Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
                      
def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 3] for i in range(0 , len(str(n)) , 3))
    
async def Ua():
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"
    
async def xBunnEr():
    """Returns working Avatar IDs as Integer to fix visual issues"""
    bN = [
        902000011, 902000013, 902047016, 902049015,
        902000154, 902000127, 902000207, 902000305,        
        902037031, 902042011, 902053016, 902053018
    ]
    return random.choice(bN)

# xC4.py তে শুধুমাত্র এই একটি ArA_CoLor ফাংশন রাখুন
def ArA_CoLor():
    colors = [
        "32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347", 
        "FF69B4", "FF8C00", "FFD700", "FFDAB9", "F0F0F0", "F0E68C", 
        "D3D3D3", "A9A9A9", "D2691E", "CD853F", "BC8F8F", "6A5ACD", 
        "483D8B", "4682B4", "9370DB", "C71585", "FFA07A"
    ]
    return random.choice(colors)

# Bright & Safe Colors List
SAFE_COLORS = [
    "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
    "[FFC0CB]", "[ADD8E6]", "[90EE90]", "[DC143C]", "[00CED1]", "[9400D3]", "[FF1493]",
    "[7CFC00]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[1E90FF]"
]

async def send_room_chat_enhanced(Msg, room_id, key, iv, region):
    """Send room chat message using leaked packet structure"""
    fields = {
        1: 1,
        2: {
            1: 9280892890,  # Sender UID (from leaked packet)
            2: int(room_id),
            3: 3,  # Chat type 3 = room chat
            4: f"[{await ArA_CoLor()}]{Msg}",  # Message with color
            5: int(datetime.now().timestamp()),  # Current timestamp
            
            9: {
                1: "RIJEXX",  # Your bot name
                2: int(await xBunnEr()),  # Avatar from your system
                4: 228,  # Rank/level from leaked packet
                7: 1,    # Unknown
            },
            10: "en",  # Changed from "ar" to "en"
            13: {2: 1, 3: 1},
        },
    }
    
    # Generate packet using your existing system
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    # Use 1215 packet type for chat messages (like your existing system)
    return await GeneRaTePk(packet, '1215', key, iv)

async def xSEndMsg(Msg , Tp , Tp2 , id , K , V):
    feilds = {1: id , 2: Tp2 , 3: Tp, 4: Msg, 5: 1735129800,  9: {1: "[FFFFFF]MAHIR", 2: int(await xBunnEr()), 3: 901048020, 4: 330, 5: 800000304, 8: "MAHIR - C4", 10: 1, 11: 1, 13: {1: 2}, 14: {1: 12484827014, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}, 12: 0}, 10: "en", 13: {3: 1}}    
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
    
async def xSEndMsgsQ(Msg , id , K , V, region="BD"):
    """Send message with region 1 title included"""
    
    # Get random avatar
    avatar = await xBunnEr()
    
    fields = {
        1: id, 
        2: id, 
        4: Msg, 
        5: 1756580149, 
         
        8: 904990072, 
        9: {
            1: "[FFFFFF]MAHIR",
            2: avatar, 
            3: 2,
            4: 329, 
            5: 800000304, 
            6: 66,
            7: 66,
            8: "ONLY MAHIR", 
            9: 66,
            10: 66, 
            11: 1, 
            12: 66,
            13: {1: 68, 2:67}, 
            14: {
                1: 1158053040, 
                2: 8, 
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        }, 
        10: "en", 
        13: {66: 66, 66: 66},
        # ADD REGION 1 TITLE HERE (from second packet field 14)
        14: {
            11: {
                1: 3,          # Field 1
                2: 7,                              # Field 2  
                3: 170,         # Field 3
                4: 999,                              # Field 4
                5: 1, # Field 5
                6: region,              
                
                8: 2,
                9: 2
            }
        }
    }
    
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
    
async def xSEndMsgsQq(Msg , id , K , V, region="IND"):
    """Send message with region 1 title included"""
    
    # Get random avatar
    avatar = await xBunnEr()
    
    fields = {
        1: id, 
        2: id, 
        4: Msg, 
        5: 1756580149, 
         
        8: 904990072, 
        9: {
            1: "MAHIR", 
            2: avatar, 
            4: 330, 
            5: 800000304, 
            8: "ONLY MAHIR", 
            10: 1, 
            11: 1, 
            13: {1: 2}, 
            14: {
                1: 1158053040, 
                2: 8, 
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        }, 
        10: "en", 
        13: {2: 2, 3: 1},
        # ADD REGION 1 TITLE HERE (from second packet field 14)
        14: {
            1: {
                1: random.choice([1, 4]),          # Field 1
                2: 1,                              # Field 2  
                3: random.randint(1, 180),         # Field 3
                4: 1,                              # Field 4
                5: int(datetime.now().timestamp()), # Field 5
                6: region                          # Field 6 (region)
            }
        }
    }
    
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)

async def AutH_GlobAl(K, V):
    fields = {
    1: 3,
    2: {
        2: 5,
        3: "en"
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)

async def GeT_Status(PLayer_Uid , K , V):
    PLayer_Uid = await EnC_Uid(PLayer_Uid , Tp = 'Uid')
    if len(PLayer_Uid) == 8: Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10: Pk = f"080112090a05{PLayer_Uid}1005"
    return await GeneRaTePk(Pk , '0f15' , K , V)
           
async def SPam_Room(Uid , Rm , Nm , K , V):
    fields = {1: 78, 2: {1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}", 3: {2: 1, 3: 1}, 4: 330, 5: 1, 6: 201, 10: xBunnEr(), 11: int(Uid), 12: 1}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0e15' , K , V)        
    
# xC4.py এর GenJoinSquadsPacket ফাংশনটি এটি দিয়ে পরিবর্তন করুন
async def GenJoinSquadsPacket(T,key,iv):
    fields = {
  1: 4,
  2: {
    4: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000e\u0016\u0019\u001a \u001d'",
    5: str(T),
    6: 6,
    8: 1,
    9: {
      2: 3140,
      3: "vX\\Q\u0016\u0005\bN\u0006R\b\u0001U\u0002\rR[\u0003TU\u0006\b\u0007U\u0004P\\\u0000RRRT\t\u0007\fP\n\nS\u0000\u0013\u0000\u0001HpYHFN\u001e\u0000\u001d\u0001\u001d\u0016\u0005\nN[U\u0006\u0003cwewhaSdeF^Fr}Q|V\u000edRS\u0000\u0005\t\u001b\u0003K^s`c^\u0005\u001fw\u0003\u0005@Bz\u0006\u0006\\{\bVbSR~J{La\u0005\u0011\u0006\u0005L[UNAwHZ_\u0019s~_Rvdy\u001d_uq\u001aCNRpM{\n\u0015\bMaBR[JQezTvcELuu\u0005_tHdFS\u0006`OY\u0007\u000b\u0013\u0003LYA\u0000AAzPWdqDy~Uj\\\u0005GgovQzrU\r\u0012\tHq[@Dr[\u0000`zS|MIZR\u0005r\u0006g\u0005pM\nPTrS\f\u0013\u0005\rHIwVRhAgfl\u000e]R\u0019EZ\\A@\fLHYN\u001bXW\t\u0016\u0007DjydvuG\u0001]MUO\u0005^[tBcS\u0013J@\u0002\\ZJ\f\b\u0017\fNyNaV}F~\rT\u0006Y\u000fBzyag\u0007@{BxU^WNV\t\u001b\u0000\u0007J\\\u0003d\u0003vBBQ^^\u001bCd\u0005\\M`F@C\t\u0007^sUS\u000f\u0014\u0003LRX`lzm_\u0004ovtxDwPr@`^B_Y\\`Mks\n",
      4: "zW\\R",
      6: 11,
      7: "\u0014twqqq~\u0016\u0013",
      8: "1.120.19",
      9: 3,
      10: 2
    },
    13: "ar",
    16: "7OR\u0019",

  }
}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0501' , key , iv)
    
async def GLobaL(T, K, V):
    fields = {1: 3, 2: {2: 5, 3: f"{T}"}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', K, V)    
    
async def GenJoinGlobaL(owner , code , K, V):
    fields = {
    1: 4,
    2: {
        1: owner,
        6: 1,
        8: 1,
        13: "en",
        15: code,
        16: "OR",
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)

async def FS(key, iv, region="ind"):
    """Start match packet - converted from TCP version"""
    try:
        # Your original fields from TCP bot
        fields = {
            1: 9,  # Start match packet type
            2: {
                1: 12480598706,  # Your UID or specific value
            }
        }
        
        # Create protobuf packet
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        
        # Encrypt the packet
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        
        # Calculate header length
        header_length = len(encrypted_packet) // 2
        header_length_final = dec_to_hex(header_length)
        
        # Determine packet type based on region
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
        
        # Build final packet based on header length
        if len(header_length_final) == 2:
            final_packet_hex = packet_type + "000000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 3:
            final_packet_hex = packet_type + "00000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 4:
            final_packet_hex = packet_type + "0000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 5:
            final_packet_hex = packet_type + "000" + header_length_final + encrypted_packet
        elif len(header_length_final) == 6:
            final_packet_hex = packet_type + "00" + header_length_final + encrypted_packet
        else:
            final_packet_hex = packet_type + "000000" + header_length_final + encrypted_packet
        
        print(f"✅ Start match packet created: {len(final_packet_hex)//2} bytes")
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Error creating start packet: {e}")
        import traceback
        traceback.print_exc()
        return None

# xC4.py ফাইলে এই ফাংশনটি রিপ্লেস করুন
async def GeTSQDaTa(D):
    try:
        # ৫ নম্বর ফিল্ড চেক করা
        if '5' in D and 'data' in D['5']:
            s_data = D['5']['data']
            
            # সব ফিল্ড (১, ১৭, ৩১) আছে কিনা চেক করে ডাটা নেওয়া
            if '1' in s_data and '17' in s_data and '31' in s_data:
                uid = s_data['1']['data']
                chat_code = s_data['17']['data']
                squad_code = s_data['31']['data']
                return uid, chat_code, squad_code
        return None # যদি কোনো ফিল্ড মিসিং থাকে তবে None রিটার্ন করবে
    except Exception:
        return None

  
async def AuthClan(CLan_Uid, AuTh, K, V):
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1201' , K , V)

def join_room_chanel(room_id, key, iv):
    fields = {
        1: 3,
        2: {
            1: int(room_id),
            2: 3,
            3: "en",
        },
    }
    packet = create_protobuf_packet(fields)
    packet = packet.hex() + "7200"
    header_lenth = len(encrypt_packet(packet, key, iv)) // 2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) == 2:
        # print(header_lenth)
        # print('len of headr == 2')
        final_packet = "1215000000" + header_lenth + encrypt_packet(packet, key, iv)
        # print(final_packet)
        return bytes.fromhex(final_packet)

    if len(header_lenth) == 3:
        #  print(header_lenth)
        #  print('len of headr == 3')
        final_packet = "121500000" + header_lenth + encrypt_packet(packet, key, iv)
        # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 4:
        #  print('len of headr == 4')
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 5:
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)

async def AutH_Chat(T , uid, code , K, V):
    fields = {
  1: T,
  2: {
    1: uid,
    3: "en",
    4: str(code)
  }
}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)
    
async def Msg_Sq(msg, owner, bot, K, V):
    fields = {
    1: 1,
    2: 2,
    2: {
        1: bot,
        2: owner,
        4: msg,
        5: 1757799182,
        
        9: {
            1: "MAHIR",
            2: await xBunnEr(),
            3: 909000024,
            4: 330,
            5: 909000024,
            10: 1,
            11: 1,
            12: 0,
            13: {1: 2},
            14: {
                1: bot,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "ar",
        13: {3: 1},
        14: ""
    }
}
    proto_bytes = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_bytes.hex(), '1215', K, V)

# ================================================================
# 👻 GHOST PACKET FUNCTIONS (ADDED BY MAHIR)
# ================================================================

async def Join_Squad_Packet_TC(T,key,iv):
    fields = {
  1: 4,
  2: {
    4: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000e\u0016\u0019\u001a \u001d'",
    5: str(T),
    6: 6,
    8: 1,
    9: {
      2: 3140,
      3: "vX\\Q\u0016\u0005\bN\u0006R\b\u0001U\u0002\rR[\u0003TU\u0006\b\u0007U\u0004P\\\u0000RRRT\t\u0007\fP\n\nS\u0000\u0013\u0000\u0001HpYHFN\u001e\u0000\u001d\u0001\u001d\u0016\u0005\nN[U\u0006\u0003cwewhaSdeF^Fr}Q|V\u000edRS\u0000\u0005\t\u001b\u0003K^s`c^\u0005\u001fw\u0003\u0005@Bz\u0006\u0006\\{\bVbSR~J{La\u0005\u0011\u0006\u0005L[UNAwHZ_\u0019s~_Rvdy\u001d_uq\u001aCNRpM{\n\u0015\bMaBR[JQezTvcELuu\u0005_tHdFS\u0006`OY\u0007\u000b\u0013\u0003LYA\u0000AAzPWdqDy~Uj\\\u0005GgovQzrU\r\u0012\tHq[@Dr[\u0000`zS|MIZR\u0005r\u0006g\u0005pM\nPTrS\f\u0013\u0005\rHIwVRhAgfl\u000e]R\u0019EZ\\A@\fLHYN\u001bXW\t\u0016\u0007DjydvuG\u0001]MUO\u0005^[tBcS\u0013J@\u0002\\ZJ\f\b\u0017\fNyNaV}F~\rT\u0006Y\u000fBzyag\u0007@{BxU^WNV\t\u001b\u0000\u0007J\\\u0003d\u0003vBBQ^^\u001bCd\u0005\\M`F@C\t\u0007^sUS\u000f\u0014\u0003LRX`lzm_\u0004ovtxDwPr@`^B_Y\\`Mks\n",
      4: "zW\\R",
      6: 11,
      7: "\u0014twqqq~\u0016\u0013",
      8: "1.120.19",
      9: 3,
      10: 2
    },
    13: "ar",
    16: "7OR\u0019",

  }
}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0501' , key , iv)

# xC4.py তে শুধুমাত্র এই একটি ExiT ফাংশন রাখুন (পুরানো সব ExiT মুছে দিন)
async def ExiT(idT, K, V):
    try:
        fields = {
            1: 7,
            2: {
                1: int(idT) if idT else 11037044965,
            }
        }
        # অবশ্যই await করতে হবে
        proto_data = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(proto_data.hex(), '0515', K, V)
    except Exception as e:
        print(f"Error in ExiT packet: {e}")
        return b""

async def ghost_pakcet(player_id, nm, secret_code, key, iv): 
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id),
                2: 1159,
                3: f"[b][c][{ArA_CoLor()}]{nm}", 
                5: 12,
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,
        },
    }
    proto_data = await CrEaTe_ProTo(fields) 
    return await GeneRaTePk(proto_data.hex(), "0515", key, iv)

async def Ghost_Final_Packet(player_id, ghost_nm, secret_code, K, V):
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id),
                2: 1159,
                3: f"[b][c][{ArA_CoLor()}]{ghost_nm}", 
                5: 12,
                6: 9999999,
                7: 1,
                8: {2: 1, 3: 1},
                9: 3,
            },
            3: secret_code,
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), "0515", K, V)
    
async def GeneRaTePk(Pk , N , K , V):
    PkEnc = await EnC_PacKeT(Pk , K , V)
    _ = await DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    else: print('ErroR => GeneRatinG ThE PacKeT !! ')
    return bytes.fromhex(HeadEr + _ + PkEnc)
    
async def OpEnSq11(K, V, region, version):
    if region.lower() == "bd":
        packet_header = '0519'
        idc_name = "IDC3"
        reg_name = "BD"
    elif region.lower() == "ind":
        packet_header = '0514'
        idc_name = "IDC2"
        reg_name = "IND"
    else:
        packet_header = '0515'
        idc_name = "IDC1"
        reg_name = "ME"

    fields = {
        1: 1,
        2: {
            2: {},
            3: 1,
            4: 1,
            5: "en",
            8: {
                1: idc_name,
                2: 226,
                3: reg_name
            },
            9: 1,
            11: 1,
            13: 1,
            14: {
                6: 11,
                8: str(version),
                9: 3,
                10: 2
            }
        }
    }

    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), packet_header, K, V)

async def OpEnSq(K, V, region, version):
    fields = {
        1: 1,
        2: {
            2: "\u0001",
            3: 43,
            4: 1,
            5: "en",
            8: [
                {
                    1: "IDC2",
                    2: 171,
                    3: "BD"
                }
            ],
            9: 1,
            10: "rYUW\u0017\t\u0007NR\u000f\u0005\u0004\\W\u0002\u000fV\u0004TPQ\u0003\u000f\u0005\u0004]\u0005\u000b\u0000\u0002W\u0005\r\nVY\u0004\u0007\u0007\u0007\u0017\u0001\bNQ\fS\u0005\u000e\u0006\f\u0005\rT\u0002\r\u0000TS\u0007U\u0004X\u0006RY\u0005\u0003\u0003SW\u0000\u000eQ\u0000^\u0014\u0003\u0004JXS\u000f\u0000g{gqfePblEZJp{_xU\bmQW\f\u0007\u000f\u0015\u0007H\\U^CHXh@Ax`\u000f~\rPN~Nz\\\u001fr_ckPU\u000b\u0015\u0005\u0003Ekfp\u007fcY\u0001nWV\u0002\u0005azE~N\u0007HTg\u0007w}@\u0002{\t\u0013\u0001NeNP]DUf|]ugINs{\u0001\\rAgB_\u0004fA]\u0004\r\u001a\u0000HpOv\\\u0005|gS\u0019\\A\u007fWW\u0003\u007fTqFGi\u0004Qr\u0019dW\u0004\u0011\rD\u0002yeZ]A\u0016a\u0007Ungeg\u0007E\\P\u001b\u000b\u0004\u0005dd\ff\r\u000f\u0017\t\u000fNRyZd\u0012tZ\fe\u0007AGv\u007fw]{P\u001c\u007f\u000ff\u0005ZJK\u0004\u0005\u0014\u0001Jgq\u001frymsB\u0001\u000fd`\u001bj~[}\u0004SDZ|IxKB\u0000\n\u0011\u0002J^`tjYN\u0007WQdE[PQ\u0002_{VP`S\t\u007f\u001dP\n\u000f\u000f\u0015\u0004\u0004L{V\u0003@yP[rgJ{Hpk\u0001\u000bw\u0001Agt_\u0003HxPc\u000b\u0017\u0005E`y\ngWoy\u0006S{A\u001b``Y\u0002Xzw}dDWOKsg\t\u0013\u000eNf\u000e\\`\u0005AwJc\u0003BM\u0001^\u0000R\u0002Qoh]tbS~`G\r\u001a\u0004HibAQ\u000f^XNt~kDUWaeaNqcLQ]Py[G\u0004",
            11: 1,
            13: 1,
            14: {
                1: "08FAA33B035B3F16020859055555000200030001000000004AFA7572105C674946762514220104186fa2e8770e748c3f6a68ed75000000ff18470f0bcacfa16d",
                2: 681,
                3: {
                    14: {
                        11: "1106064f50055401030f03020403060155070d01540e060e020607540706030354530f041003064d715c46434b1f061f031e1205034a1c40677c5f554775755f504e677446185b584901534144685b67620f",
                        0: 72
                    }
                },
                4: "x\\\\R",
                6: 13,
                7: {2: 80},
                8: version,
                9: 2,
                10: 1,
                11: "03626253513677542b504e4635416456324b796f566c576a326567507844414c33507138513031762b66536c626a587648434e3348414e376c472b72474637794165676e72436b553671626b694538706f534e5a582b2f7a44675a547475465650542b384d69565a507151312b444b53576f786f6d592f7156394f76755254482b7154486a78486f664169734267564970454d454e6b4c326a4763445a4a5176416d687947356b7669564e544d71515745754b32324d4e384e4931424d437445395532415156694b667948314574412b32644536464b53773132554155596363372b7753652b66676c393742756544446a58496d6e35666d45444a51535948326644484c5650676755472f51794b776e77545151324a505265352f72314830616d374264424f556b712f523246734d635475516d47364c684a547a4379345774444245795268305754366f68532f785a48736a4c7a4366506378372f386a534133352b67787642657450397a4f6f463639344945386e6e77336b507344357a6e6337593649776b4142435761776f6d572b6948594f5939686d647632706975584168416d6d6a74496f5945444c6e506e5738616f7153304f74486b732f5a3953543252447345507a3343655438774e6874756d57634b4438585445376649386c305173726a772f4a57514f76394b50307257644538593375422f2b495836757675452b487a6a4853466c75726f33515432536567595758535854714674495a61454d476c51314b7639666c59525539465047366c30663045314f7a2b2b36324339644b664c4d39315a782f6f625938726a6e682b77524a3962636e544e41715466486f72354b714d3d"
            },
            19: 329,
            21: "374f5219",
            24: {1: 21},
            27: "a_6534489873065906362"
        }
    }
    
    # এখানে ফাংশনের নাম এবং await ঠিক করা হয়েছে
    proto_bytes = await CrEaTe_ProTo(fields)
    packet_type = '0515'
    packet = await GeneRaTePk(proto_bytes.hex(), packet_type, K, V)
    
    return packet

async def cHSq(Nu, bot_uid, K, V, region):
    """Sets the team size for the squad"""
    fields = {
        1: 17,
        2: {
            1: int(bot_uid),
            2: 1,
            3: int(Nu),  
            4: 46,
            5: "\x1a", 
            8: 12,    
            13: 330
        }
    }

    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"

    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), packet_type, K, V)

async def cHSq22(Nu, bot_uid, K, V, region):
    """Sets the team size for the squad"""
    fields = {
        1: 17,
        2: {
            1: int(bot_uid),
            2: 1,
            3: 3,
            4: 1,
            5: "\x1a", 
            8: 1
        }
    }

    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"

    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), packet_type, K, V)

async def SEnd_InV(Nu , Uid , K , V,region):
    
    fields = {1: 2 , 2: {1: int(Uid) , 2: region , 4: int(Nu)}}

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet , K , V)

# xC4.py এর একদম নিচে এই দুটি ফাংশন আপডেট করুন

async def openroom(K, V):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 1,
            4: "MAHIR",
            5: "11",
            6: 4,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: {1: "IDC3", 2: 126, 3: "BD"},
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 3030901002000,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {1: 2},
        }
    }
    proto_data = await CrEaTe_ProTo(fields) # await যোগ করা হয়েছে
    return await GeneRaTePk(proto_data.hex(), '0E15', K, V) # await যোগ করা হয়েছে

async def spmroom(K, V, uid):
    fields = {1: 22, 2: {1: int(uid)}}
    proto_data = await CrEaTe_ProTo(fields) # await যোগ করা হয়েছে
    return await GeneRaTePk(proto_data.hex(), '0E15', K, V) # await যোগ করা হয়েছে

def load_emotes_from_file(filename="emotes.json"):
    """
    ফাইল থেকে সব ইমোট লোড করবে। 
    all_aliases এ সব থাকবে (যাতে নাম্বার দিয়ে কমান্ড কাজ করে), 
    কিন্তু categorized_emotes এ শুধু নামগুলো থাকবে (মেনুর জন্য)।
    """
    all_aliases = {}
    categorized_emotes = {}
    current_category = "Uncategorized"
    
    print(f"📦 '{filename}' LOADING EMOTES FROM DATABASE...")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # ক্যাটাগরি ডিটেকশন (যেমন: # Evo Guns)
            if line.startswith("#"):
                current_category = line.replace("#", "").strip()
                if current_category not in categorized_emotes:
                    categorized_emotes[current_category] = []
                continue
            
            # নাম ও আইডি খুঁজে বের করা
            match = re.search(r"'([^']+)':\s*(\d+)", line)
            if match:
                alias = match.group(1).strip().lower()
                emote_id = int(match.group(2))
                
                # সব এলিয়াস সেভ রাখা হচ্ছে মেইন ফাংশনের জন্য
                all_aliases[alias] = emote_id
                
                # ফিল্টার: যদি নামটা নাম্বার না হয়, তবেই মেনুতে দেখাবে
                if not alias.isdigit():
                    if current_category not in categorized_emotes:
                        categorized_emotes[current_category] = []
                    
                    if alias not in categorized_emotes[current_category]:
                        categorized_emotes[current_category].append(alias)

    except FileNotFoundError:
        print(f"❌ Error: {filename} Not Found")
    except Exception as e:
        print(f"❌ Error loading emotes: {e}")
        
    print(f"✅ Total Loaded: {len(all_aliases)} emotes (Numbers Filtered for Menu).")
    return all_aliases, categorized_emotes

def get_menu_pages(categorized_emotes):
    """
    ইমোট মেনু জেনারেট করবে। 
    শুধুমাত্র নামগুলো রঙিন লিস্ট আকারে সাজাবে।
    """
    pages = []
    # সুন্দর হেডার
    current_msg = "[B][C][FF0000]🔥 ᎷAH!Ꮢ ᏋᎷOᎿᏋ ᎷᏋᏁᏌ 🔥\n"
    current_msg += "[B][C][FFFFFF]━━━━━━━━━━━━━━━━━━\n"
    
    for category, emotes in categorized_emotes.items():
        if not emotes: continue
            
        header = f"\n[B][C][00FFFF]◈ {category.upper()} ◈\n"
        
        # মেসেজ সাইজ চেক (ফ্রি ফায়ার চ্যাট লিমিট ~৫০০ ক্যারেক্টার)
        if len(current_msg) + len(header) > 420:
            pages.append(current_msg + "\n[B][C][00FF00]>>> Next Page...")
            current_msg = f"[B][C][00FFFF]◈ {category.upper()} (Cont) ◈\n"
        else:
            current_msg += header

        for name in emotes:
            color = random.choice(SAFE_COLORS)
            # ফরম্যাট: ➥ ak (কালারফুল)
            line_item = f"{color}➥ {name}\n"
            
            if len(current_msg) + len(line_item) > 450:
                pages.append(current_msg + "\n[B][C][00FF00]>>> Next Page...")
                current_msg = f"[B][C][00FFFF]◈ {category.upper()} (Cont) ◈\n" + line_item
            else:
                current_msg += line_item
        
    current_msg += "[B][C][FFFFFF]━━━━━━━━━━━━━━━━━━\n"
    current_msg += "[B][C][FF0000]💡 Type name to play!"
    pages.append(current_msg)
    
    return pages
    
