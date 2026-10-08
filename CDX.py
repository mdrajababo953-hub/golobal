import time
import requests, json, binascii, time, urllib3, base64, datetime, re, socket, threading, random, os, sys
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_OWN_ID = 0

def random_badge():
    badge_list = [
        "902000306",
        "1200000004",
        "901000194",
        "827001005",
        "827001006",
        "203000543",
        "203000348",
        "827001008",
        "902000308"
    ]
    return random.choice(badge_list)


def EnC_AEs(HeX):
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()


def ArA_CoLor():
    Tp = ["32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347", "FF69B4", "FF8C00", "FF6347",
          "FFD700", "FFDAB9", "F0F0F0", "F0E68C", "D3D3D3", "A9A9A9", "D2691E", "CD853F", "BC8F8F",
          "6A5ACD", "483D8B", "4682B4", "9370DB", "C71585", "FF8C00", "FFA07A"]
    return random.choice(Tp)


def DEc_AEs(HeX):
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()


def xBunnEr():
    avatar_list = [
        '902000016', '902000306', '902000305', '902000065',
        '902000306', '902000192', '902000334', '902000179',
        '902000308', '902045009', '902038023', '902048018',
        '902039014', '902000306', '902000306', '902000305'
    ]
    return int(random.choice(avatar_list))


# ━━━━━━━━━━━━━━━━━━━
def EnC_PacKeT(HeX, K, V):
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()


# ━━━━━━━━━━━━━━━━━━━
def DEc_PacKeT(HeX, K, V):
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()


# ━━━━━━━━━━━━━━━━━━━
def EnC_Uid(H, Tp):
    e, H = [], int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0))
        H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None


# ━━━━━━━━━━━━━━━━━━━
def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)


def EnC_Vr(N):
    if N < 0:
        return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N:
            BesTo |= 0x80
        H.append(BesTo)
        if not N:
            break
    return bytes(H)


# ━━━━━━━━━━━━━━━━━━━
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n


# ━━━━━━━━━━━━━━━━━━━
def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value


# ━━━━━━━━━━━━━━━━━━━
def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))
    return packet


# ━━━━━━━━━━━━━━━━━━━
def DecodE_HeX(H):
    R = hex(H)
    F = str(R)[2:]
    if len(F) == 1:
        F = "0" + F
        return F
    else:
        return F

# ============================================================
#  ASYNC WRAPPERS (if base functions are sync)
# ============================================================
async def CrEaTe_ProTo_Async(fields):
    """Async wrapper for CrEaTe_ProTo"""
    return CrEaTe_ProTo(fields)


async def GeneRaTePk_Async(Pk, N, K, V):
    """Async wrapper for GeneRaTePk"""
    return GeneRaTePk(Pk, N, K, V)

# ============================================================
#  cHSq - Change Squad Settings (before leave)
# ============================================================
async def cHSq(Nu, bot_uid, K, V, region):
    """Sets the team size for the squad"""
    fields = {
        1: 17,
        2: {
            1: int(bot_uid),
            2: 1,
            3: 4,
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

    proto_data = CrEaTe_ProTo(fields)
    return GeneRaTePk(proto_data.hex(), packet_type, K, V)

# ============================================================
#  HELP MESSAGE PACKET (for group chat reply)
# ============================================================
def yasser_HelpMsg(target_uid, bot_uid, key, iv):
    """
    Group এ সুন্দর Help message পাঠানোর packet।
    """
    help_text = (
        "[B][C][FF0000]╔══════════════════════╗\n"
        "[C][B][FFD700]        🤖 MAHIR BOT HELP 🤖\n"
        "[C][B][FF0000]╚══════════════════════╝\n\n"
        
        "[C][B][00FFFF]╔━━━──[FF0000] • [00FFFF]──━━━╗\n"
        "[C][B][FFFFFF]     📋 AVAILABLE COMMANDS\n"
        "[C][B][00FFFF]╚━━━──[FF0000] • [00FFFF]──━━━╝\n\n"

        "[C][B][FF0000]╔━━━──[FFD700] • [FF0000]──━━━╗\n"
        "[C][B][FFFF00]     ⚡ BOT FEATURES ⚡\n"
        "[C][B][FF0000]╚━━━──[FFD700] • [FF0000]──━━━╝\n\n"
        
        "[C][B][FFFFFF]🎯 Status    : [00FF00]ONLINE 24/7\n"
        "[C][B][FFFFFF]🤖 Speed     : [00FF00]ULTRA FAST\n"
        "[C][B][FFFFFF]🔒 Security  : [00FF00]PROTECTED\n"
        "[C][B][FFFFFF]🌐 Servers   : [00FF00]ALL REGIONS\n"
        "[C][B][FFFFFF]💎 Version   : [00FF00]PREMIUM\n\n"
        
        "[C][B][FF0000]╔━━━──[FFD700] • [FF0000]──━━━╗\n"
        "[C][B][FFFF00]     👑 OWNER INFO 👑\n"
        "[C][B][FF0000]╚━━━──[FFD700] • [FF0000]──━━━╝\n\n"
        
        "[C][B][FFFFFF]👑 Owner     : [00FFFF]MAHIR\n"
        "[C][B][FFFFFF]📱 Contact   : [FFFF00]@MAHIR0208\n"
        "[C][B][FFFFFF]💬 Telegram  : [FFFF00]@MAHIR_BOT\n"
        "[C][B][FFFFFF]🎵 TikTok    : [FFFF00]MAHIR__222\n\n"
        
        "[C][B][00FFFF]╔━━━──[FF0000] • [00FFFF]──━━━╗\n"
        "[C][B][FFFFFF]  💚 TYPE [FF0000]APP [FFFFFF]TO DOWNLOAD 💚\n"
        "[C][B][FF0000]  🔥 ENJOY THE EXPERIENCE 🔥\n"
        "[C][B][00FFFF]╚━━━──[FF0000] • [00FFFF]──━━━╝\n\n"
        
        "[C][B][FFD700]━━━━━━━━━━━━━━━━━━━━━━\n"
        "[C][B][00FF00]✨ Powered By [FF0000]MAHIR BOT [00FF00]✨\n"
        "[C][B][FFD700]━━━━━━━━━━━━━━━━━━━━━━"
    )

    fields = {
        1: 1,
        2: 2,
        2: {
            1: int(bot_uid),
            2: int(target_uid),
            4: help_text,
            5: str(time.time()).split('.')[0],
            9: {
                1: "Fun1w5a2",
                2: xBunnEr(),
                3: int(random_badge()),
                4: 330,
                5: int(random_badge()),
                10: 1,
                11: 1,
                7: 2,
                13: {1: 2},
                14: {
                    1: int(bot_uid),
                    2: 8,
                    3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                }
            },
            10: "fr",
            13: {
                2: 1,
                3: 1
            },
            14: {}
        }
    }
    yasser_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(yasser_fields), '1215', key, iv)

# ============================================================
#  OPEnSq - Opens Squad (Auto Create)
# ============================================================
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

    proto_bytes = CrEaTe_ProTo(fields)
    packet_type = '0515'
    packet = GeneRaTePk(proto_bytes.hex(), packet_type, K, V)
    return packet


# ============================================================
#  cHSq22 - Change Squad Size (Team Size)
# ============================================================
async def cHSq22(Nu, bot_uid, K, V, region):
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

    proto_data = CrEaTe_ProTo(fields)
    return GeneRaTePk(proto_data.hex(), packet_type, K, V)


# ============================================================
#  MAHIR_World_Recruit_Packet
# ============================================================
async def MAHIR_World_Recruit_Packet(target_id, key, iv):
    try:
        fields = {
            1: 66,
            2: {
                1: int(target_id),
                5: {},
                9: "",
                10: 1
            }
        }
        proto_data = CrEaTe_ProTo(fields)
        packet_type = '0515'
        final_packet = GeneRaTePk(proto_data.hex(), packet_type, key, iv)
        return final_packet
    except Exception as e:
        print(f"❌ World Promo Packet Error: {e}")
        return None


# ============================================================
#  leave_squad_packet
# ============================================================
async def leave_squad_packet(key, iv, region, bot_own_id):
    fields = {1: 7, 2: {1: int(bot_own_id)}}
    p_type = '0514' if region.lower() == "ind" else ("0519" if region.lower() == "bd" else "0515")
    proto_data = CrEaTe_ProTo(fields)
    return GeneRaTePk(proto_data.hex(), p_type, key, iv)

# ━━━━━━━━━━━━━━━━━━━
def Fix_PackEt(parsed_results):
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
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


# ━━━━━━━━━━━━━━━━━━━
def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        return None


# ━━━━━━━━━━━━━━━━━━━
Key, Iv = (
    bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]),
    bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
)


def Ua():
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


# ━━━━━━━━━━━━━━━━━━━
def random_channel():
    channel = random.choice(['en', 'ar', 'fr', 'br'])
    return channel


# ━━━━━━━━━━━━━━━━━━━
def GLobaL(T, K, V):
    """✅ FIX: header '1215' → '0515'"""
    fields = {1: 3, 2: {2: 5, 3: f"{T}"}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def ChaT_sQ(T, N, U, sQ, K, V):
    fields = {1: N, 2: {1: int(U), 3: f"{T}", 4: str(sQ)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '1215', K, V)


# ━━━━━━━━━━━━━━━━━━━
def ReFLeSH_Yr():
    fields = {4: 264304360}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', Key, Iv)


# ━━━━━━━━━━━━━━━━━━━
def Join_Sq(K, V):
    fields = {
        1: 69,
        2: {
            2: random.choice(['tr']),
            7: 330,
            8: 330,
            9: "",
            10: "\u0001\t\n\u000b\u0012\u0019 '",
            11: 1,
            12: {
                1: "088B823A900F2FEF020101000000000200140001001100020E682E6B13949B6B46762514110000010594e97dca3ca4f96a3ba7bd0000004f00000100cacfa16d",
                2: 31,
                3: "tY_S\u0013\b\u0001MV\u0003\u0007\u0005\u0004W\u0005]\u0007\t\u0002\u0007\u0001\u0000\u0003\u0000T\fS\u0006\u0000W\u0004\u0003\u0002\u0000\b\r\u0000\u0001U\u0005\u0011\u0001\u0002JuTAEN\u001e\u0002\u001c\u0002\u001f\u0013\b\u0003M\u001cDbz_Q@}p_QOgsC\u001dYVI\u0004UAAj_ga\u0004\u0012\u0000K\u001d\u0007_t\u0019b\bCx\u0002UeGat\u001fTTCBLER\u0006\u0001\r\f\u0012\u0006\u0005NYaeA~ha\u000fZzr\u0006IZw|F}qf\u007f\u0001l\u0007t\n\u0015\nL\\Nh\u0000~G\u000et\u0000eb]VQ\u0006t^F[ZIGxCdZD\u000b\u0011\u0002OA\u0000\u000fgTtbgJcfq\u0001euAYAQKQtTsHD{\u000f\u0013\nJx^k^EO[c\u0005aTRw\u0002\u007fw@\u007f\u0002BX\ntY@@]\r\u0010\u0007\bES~N[kxUE\u0002o\u001eZ\\C@A{F[tvhN\u0003Qr\u000b\u0013\nMr\u0018zTzK}\u007fqE]vnvwROuheYvwduvQ\r\u001a\u0005M\u0006z\u001dfXfzvHFc~dXUz}O\u001aB\u0005t\u0002i\u001co_\u0004\u0012\u0003\u0007J\u0006b\u0003\u000eqlfvbEstgu~wB\u0001v@yI\u0002ZPx\f\u0014\u0003NR\u0002yBZvuD_cd\u0004q]lH]\u0007bD}pCe\t\u0004t\n",
                4: "w^_R",
                6: 11,
                7: "\u0016xx`wc\u0015\u0013",
                8: "1.128.15",
                9: 3,
                10: 2,
                11: "0003626253513637456372725663416456324b796f566c586c6449716f4662743755656f5a4c633547475052557472782f7646515a4c54753272754d7432676d6875504f4d6c5a74444371496c4c5944447961546572366864394e6774365462364e754549774959395243614f3348793873666b47696c6444656b36394846426e3657442b31415430695566336e42714b41724b38315945743231393671617a4e61434144514f6772466c6e614358306f646849436b35625347476963687a6e61764850757264562b5a4365576d4a6470736f556961504d544c3039587662345530674b6453486d4a396b2b56476767432f6d525972613965476c52444d4a4d45566b36434a4458786e6a6263327a7a4c536e32576a5a4977646f7a305750796368415a4970636f61366c6d35794474636c734c3953514c74615055617370626549314f6b5a5a3265517062786837774152464e617a4642795661354a79546e675558425a796246566565464f656a6b6d53585a714e5764567a65314443583858737a414364795246636332624e6a7438476e4866396d61744d492b766a33577a6446526c537073655350582f364945714157546c45306a6958785674656144586a2f6878716b49312b6339695534736f52666578526e757548486d4f33583839476277475678695475774278764772746532616732582f4f4f51497a44314d644177475177386e364b584c646c4f44547274654f7448306170324174674e6d4634694d6a654c484e4c70504c366964694e5850594633413d3d"
            },
            16: 1,
            17: "\u0001\u0002\u0003\u0004",
            18: "\u0001\u0002\u0003\u0004\u0005",
            21: "\b\u0015",
            28: "\bH\u0010\u0003",
            29: 5
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def LeVe_C(cid, K, V):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][1] = int(cid)
    fields[2][2] = 5
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '1201', K, V)


# ━━━━━━━━━━━━━━━━━━━
def send_craftland_share_sync(sock, bot_uid, target_id, chat_type, map_code, key, iv):
    try:
        # ✅ FIX: bot_uid int conversion safety
        try:
            bot_uid_int = int(bot_uid)
        except (ValueError, TypeError):
            print(f"❌ Invalid bot_uid: {bot_uid}")
            return False

        craftland_data = {
            "WorkshopCode": map_code,
            "type": "UGCMapShare"
        }
        craftland_json = json.dumps(craftland_data)

        fields = {
            1: 1,
            2: {
                1: bot_uid_int,
                2: int(target_id),
                3: 5,
                5: int(time.time()),
                7: 1,
                8: craftland_json,
                9: {
                    1: "MAHIR BOT",
                    2: xBunnEr(),
                    4: 330,
                    5: 801046518,
                    8: "MAHIR TEAM",
                    10: 1,
                    11: 1,
                    13: {1: 2},
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: "\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {2: 2, 3: 1}
            }
        }

        proto_bytes = CrEaTe_ProTo(fields)
        packet = GeneRaTePk(proto_bytes.hex(), '1215', key, iv)

        sock.send(packet)
        print(f"✅ CRAFTLAND MAP ({map_code}) SENT Successfully!")
        return True

    except Exception as e:
        print(f"❌ Craftland Error: {e}")
        return False


# ━━━━━━━━━━━━━━━━━━━
def Send_GhosTs(Uid, Nm, sQ, K, V):
    fields = {1: 61, 2: {1: int(Uid), 2: {1: int(Uid), 2: 1159, 3: f'{Nm}', 5: 12, 6: 9999999, 7: 1, 8: {2: 1, 3: 1}, 9: 3}, 3: sQ}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def Send_InV(N, U, K, V):
    fields = {1: 2, 2: {1: int(U), 2: "ME", 4: N}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def RefLeSh(K, V):
    fields = {
        1: 67,
        2: {
            1: "ar",
            6: 315,
            7: 322,
            10: 1,
            12: 1,
            13: {},
            14: {}
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def Join_Sq1(T, U, rQ, K, V):
    fields = {
        1: 4,
        2: {
            1: U,
            4: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u0019\u001a ",
            6: 1,
            8: 1,
            9: {
                4: "y[WW",
                6: 11,
                7: "\u001d`at\u0005d\u001d\u0016",
                8: "1.118.3",
                9: 3,
                10: 2
            },
            13: "ar",
            15: rQ,
            16: "OR",
            20: {1: 21}
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def trydecyasser(pack):
    try:
        r = pack['5']['data']['3']['data']['31']['data']
    except KeyError:
        r = pack['5']['data']['31']['data']
    except:
        return None
    return r


# ━━━━━━━━━━━━━━━━━━━
def yasser_Chat(uid, code, K, I):
    fields = {
        1: 3,
        2: {
            1: uid,
            3: "fr",
            4: str(code)
        }
    }
    yasser_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(yasser_fields), '1215', K, I)


# ━━━━━━━━━━━━━━━━━━━
def yasser_quitcaht(uid, K, I):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: "fr"
        }
    }
    yasser_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(yasser_fields), '1215', K, I)


# ━━━━━━━━━━━━━━━━━━━
def yasser_SendInv(bot_uid, uid, K, V):
    fields = {1: 33, 2: {1: int(uid), 2: "ME", 3: 1, 4: 1, 6: "yyt", 7: 330, 8: 1000, 9: 100, 10: "DZ", 12: 1, 13: int(uid), 16: 1, 17: {2: 159, 4: "y[WW", 6: 11, 8: "1.118.1", 9: 3, 10: 1}, 18: 306, 19: 18, 24: 902000306, 26: {}, 27: {1: 11, 2: int(bot_uid), 3: 999}, 28: {}, 31: {1: 1, 2: 32768}, 32: 32768, 34: {1: bot_uid, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def yasser_Msg(msg, owner, bot, K, I):
    fields = {
        1: 1,
        2: 2,
        2: {
            1: bot,
            2: owner,
            4: msg,
            5: str(time.time()).split('.')[0],
            9: {
                1: "Fun1w5a2",
                2: xBunnEr(),
                3: int(random_badge()),
                4: 330,
                5: int(random_badge()),
                10: 1,
                11: 1,
                7: 2,
                13: {1: 2},
                14: {
                    1: bot,
                    2: 8,
                    3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                }
            },
            10: "fr",
            13: {
                2: 1,
                3: 1
            },
            14: {}
        }
    }
    yasser_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(yasser_fields), '1215', K, I)


# ━━━━━━━━━━━━━━━━━━━
def ExiT(bot_uid, K, V):
    """✅ FIX: ekhon bot UID pathai, 0 noy"""
    try:
        uid_int = int(bot_uid) if str(bot_uid).isdigit() else 0
    except (ValueError, TypeError):
        uid_int = 0
    fields = {1: 7, 2: {1: uid_int}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def reflesh(uid, K, V):
    fields = {
        1: 1,
        2: {
            1: {
                1: uid,
                2: 14,
                4: 84
            },
            2: {
                6: 9
            },
            3: {
                1: uid,
                2: 5,
                4: 68
            },
            4: {
                2: 1596891
            }
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


# ━━━━━━━━━━━━━━━━━━━
def GeT_Time(timestamp):
    last_login = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last_login
    h, rem = divmod(diff.seconds, 3600)
    m, s = divmod(rem, 60)
    return h, m, s


# ━━━━━━━━━━━━━━━━━━━
def ResTarTinG():
    print('\n  ResTartinG BoT ... !')
    try:
        p = psutil.Process(os.getpid())
        for f in p.open_files():
            try:
                os.close(f.fd)
            except:
                pass
        for conn in p.net_connections(kind='inet'):
            try:
                if conn.fd != -1:
                    os.close(conn.fd)
            except:
                pass
    except:
        pass
    time.sleep(0.5)
    python = sys.executable
    os.execl(python, python, *sys.argv)


# ━━━━━━━━━━━━━━━━━━━
def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 1] for i in range(0, len(str(n)), 1))


def LogOuT(A):
    R = requests.Session().get(f'https://100067.connect.garena.com/oauth/logout?access_token={A}&refresh_token=')
    print('LoGOuT =>', R.text)
    if R.status_code == 200 and '0' in R.text:
        return True
    else:
        return False


# ━━━━━━━━━━━━━━━━━━━
def GeneRaTePk(Pk, N, K, V):
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2:
        HeadEr = N + "000000"
    elif len(_) == 3:
        HeadEr = N + "00000"
    elif len(_) == 4:
        HeadEr = N + "0000"
    elif len(_) == 5:
        HeadEr = N + "000"
    else:
        HeadEr = N + "0000"
    return bytes.fromhex(HeadEr + _ + PkEnc)


# ━━━━━━━━━━━━━━━━━━━
def AuTo_ResTartinG():
    time.sleep(6 * 60 * 60)
    print('\n  AuTo ResTartinG The BoT ... !')
    try:
        p = psutil.Process(os.getpid())
        for f in p.open_files():
            try:
                os.close(f.fd)
            except Exception:
                pass
        for conn in p.net_connections(kind='inet'):
            try:
                if conn.fd != -1:
                    os.close(conn.fd)
            except Exception:
                pass
    except Exception:
        pass

    python = sys.executable
    os.execl(python, python, *sys.argv)