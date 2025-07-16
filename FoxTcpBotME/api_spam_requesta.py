from flask import Flask, request, Response
import asyncio
import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import threading

app = Flask(__name__)

# توكنات الحسابات
SPAM_TOKENS = {
     "3024323714": "4p5r2t2qmtwrzi",
    "3024323708": "7o4ef44z4ehq23",
    "3024323350": "0aahuth4yqpd54",
    "3024323717": "nnnwppxex8hsin",
    "3024323718": "568d17dw3bisgl",
    "3024323737": "60hqraifovbp37",
    "3024323738": "vqenhsmmbgne6b",
    "3024323746": "vszykj2gvpmqjp",
    "3024323748": "2s7sqqb3f3vthu",
    "3024323751": "er1oieq4srdk0g",
    "3024323755": "itkxefm65mpgrs",
    "3024323758": "vh184l3u8822zr",
    "3024323757": "pkbvwth92nhuq7",
    "3024323759": "7m2y3musz2gzcp",
    "3024323767": "nnz05aa6xztgcd",
    "3024323781": "aeu3yavotgumtv",
    "3024323780": "61h8zblprpv7fc",
    "3024323790": "nlzxrdyfotyz00",
    "3024323794": "yptmmydr1ke2o9",
    "3024323792": "d6bftelbye28se",
    "3024323793": "izrwy51gfbl7db",
    "3024323789": "ndomiu2ukyosvc",
    "3024323796": "vu2vp2s2ilcc9m",
    "3024323805": "93j0wgostntcab",
    "3024323816": "syogfcteb79xj8",
    "3024323822": "i6z6zfsqegufcw",
    "3024323832": "n9sv46jfk755j4",
    "3024323835": "wh8sq1jic8kueh",
    "3024323831": "as2fibke2biz8x",
    "3024323838": "lgsepblq0k71x4",
    "3024323837": "il497rsylaelef",
    "3024323843": "qcgclrjo2zhsgr",
    "3024323845": "jn1zv9twbcgivq",
    "3024323849": "ey0lzpu9d5rnrc",
    "3024323848": "quoasvjznjudzv",
    "3024323856": "g8rjim8fbia56v",
    "3024323862": "yr552jjhaxzhs8",
    "3024323867": "emq1n6ww9oltyh",
    "3024323866": "dukalipk4v99zc",
    "3024323870": "ipe8gagls0l3u3",
    "3024323878": "gdakp0pv56uslf",
    "3024323879": "zkm5r8c6pfntri",
    "3024323877": "k0sdqnq98kb9gd",
    "3024323876": "pxc350zyvxj59m",
    "3024323875": "3b89x6wzj9u07p",
    "3024323891": "d7y78m40o5253u",
    "3024323897": "r1m4gt4gfd7nhp",
    "3024323901": "zp787rg6tcnd6p",
    "3024323906": "qw4qnggotmqcib",
    "3024323905": "p0jpwymx08p0jt",
    "3024323922": "0iwej2is9ureqa",
    "3024323930": "2ll22vshotxc88",
    "3024323929": "dbt0oes86spmrb",
    "3024323938": "7t6fnc8xdngyp3",
    "3024323941": "qljt3km4hf7de9",
    "3024323946": "tfj2f8fec12nbt",
    "3024323945": "m3eyxb59ilnkyy",
    "3024323953": "hayoieyu76ynpo",
    "3024323964": "520la6qh5z164f",
    "3024323972": "47ocdt8y8prxto",
    "3024323957": "txbf3b809jbwvn",
    "3024323985": "tqswdjid2j6b6h",
    "3024323987": "8ad0c4shw3q9fr",
    "3024323995": "w2hxhib1hz2pw7",
    "3024323996": "aat3p7a7re1bpz",
    "3024324006": "k8qc0yejosmris",
    "3024324005": "z29411ol1b98fo",
    "3024324004": "6yntivfbgex4yx",
    "3024324023": "1tym3sfqd0gu2v",
    "3024324033": "ry7f607frayr59",
    "3024324037": "zxiy3jwed9zro8",
    "3024324047": "u8l6rhfskrm6d3",
    "3024324063": "vnsvnuyiu33enp",
    "3024324084": "crffkqwva6f6v5",
    "3024324096": "lqpfgb44db7q5q",
    "3024324098": "fulgz6jfjaiafw",
    "3024324108": "wrxgd07ojk0az3",
    "3024324131": "f87t8qwjjf23fl",
    "3024324137": "ttidwfe5orgeik",
    "3024324138": "motmo45zm2i4wd",
    "3024324140": "oklu9hxlugmrt5",
    "3024324147": "if11myhxj14n9h",
    "3024324150": "lvcp86mh58uu2x",
    "3024324167": "778zvwu0ghqlg2",
    "3024324159": "660noauxybcxtz",
    "3024324172": "dxef1w25zz8sk5",
    "3024324173": "zcc6rrgz28om4l",
    "3024324175": "0haptrszyk7p6u",
    "3024324179": "5pj3wtj2gfxuhb",
    "3024324184": "coorgnmsbhdmnq",
    "3024324188": "qdayoeu9mn3fhq",
    "3024324191": "13197nja8wny5e",
    "3024324192": "ywsmfk7q2bp62a",
    "3024324197": "ou1qxjpnjgkqfo",
    "3024324203": "6o6oxwlnypo461",
    "3024324201": "a9e70eh3ygv6uc",
    "3024324208": "7nqyze21zo33i9",
    "3024324202": "i4vnbydrj2hxfg",
    "3024324210": "9sdw21j7nl91vl",
    "3024324211": "ksfc28olz61c2k",
    "3024324207": "nofum7429np1ca",
    "3024324214": "l0pyqj1fuljqhm",
    "3024324218": "osd5rxabqnvyh1",
    "3024324220": "l0yoss7cj9pwaq",
    "3024324223": "rd9t31h8k6113l",
    "3024324243": "hu5j0nkltwnb2r",
    "3024324251": "9xxa5yupxr7w8t",
    "3024324280": "obsefh8yl4i587",
    "3024324284": "047ehew7uw91k4",
    "3024324283": "sbx8xqh3l04xd5",
    "3024324292": "ex9o9h2w783kmn",
    "3024324293": "b0tanaw0lc81lt",
    "3024324296": "6q9iiscjdyqk6s",
    "3024324298": "62lvk9l2xa1opq",
    "3024324305": "6gpoty7ah4o3af",
    "3024324311": "7nnw5vw9pfm99s",
    "3024324312": "ca1v32x42x1wcr",
    "3024324323": "idk87v1ny7tcaz",
    "3024324329": "7jwhevaz720os2",
    "3024324333": "fct8kt8weljfuf",
    "3024324341": "tz021yumvczw6r",
    "3024324342": "2fjbn5f4mw3msc",
    "3024324346": "ifjlz1wvc84ei1",
    "3024324362": "fio3hd2czk9dmk",
    "3024324361": "3qfiti3wt44crs",
    "3024324359": "f3j6bb3izc9am2",
    "3024324368": "sg8hkhb6wso7ny",
    "3024324365": "j26wrlv16evoz0",
    "3024324369": "vrbfh0si2br6eo",
    "3024324376": "ivg0wap5ptss0k",
    "3024324384": "8eweshgg1asit3",
    "3024324398": "bzv6z9z49rqfpq",
    "3024324437": "g05wx0edwc0gbv",
    "3024324447": "30g1w2vfuf7oqn",
    "3024324453": "pw7f2rfbi863y4",
    "3024324487": "eloii3605x3wk3",
    "3024324497": "ceurrdqu50c84f",
    "3024324430": "rr4w65925jz02d",
    "3024324520": "7r7rlzohcwztz9",
    "3024324534": "c81e0ijwrysedk",
    "3024324542": "t8k1xlxp9amyua",
    "3024324546": "p310ka2gz4j06v",
    "3024324556": "ed2dztkbohlmrk"
}

# تعريف دالة Encrypt_ID المفقودة
def Encrypt_ID(x):
    x = int(x)
    dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
    xxx = ['1', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
    x = x / 128
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]

# وظيفة التشفير
def encrypt_api(plain_text):
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(plain_text), AES.block_size)).hex()

# بقية الكود يبقى كما هو...

# وظيفة التشفير
def encrypt_api(plain_text):
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(plain_text), AES.block_size)).hex()

# جلب التوكن
async def get_jwt_async(uid, password):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://projects-fox-x-get-jwt.vercel.app/get?uid={uid}&password={password}",
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("token")
    except:
        return None

# إرسال طلب الصداقة
async def send_friend_request(id, token):
    url = 'https://clientbp.common.ggbluefox.com/RequestAddingFriend'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB49',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {token}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    encrypted_data = encrypt_api(f'08a7c4839f1e10{Encrypt_ID(id)}1801')
    data = bytes.fromhex(encrypted_data)
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=60) as client:
            response = await client.post(url, headers=headers, data=data)
            if response.status_code == 200:
                return f"تم الإرسال لـ {id}"
            return f"خطأ: {response.text}"
    except Exception as e:
        return f"فشل: {str(e)}"

# العملية الرئيسية
async def process_account(uid, pw, id):
    token = await get_jwt_async(uid, pw)
    if token:
        return await send_friend_request(id, token)
    return f"فشل جلب التوكن لـ {uid}"

async def process_all_accounts(id):
    tasks = []
    for uid, pw in SPAM_TOKENS.items():
        task = asyncio.create_task(process_account(uid, pw, id))
        tasks.append(task)
    return await asyncio.gather(*tasks)

def run_async(id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(process_all_accounts(id))
    loop.close()
    print("النتائج:", results)

@app.route('/spam')
def spam():
    id = request.args.get('id')
    if id:
        thread = threading.Thread(target=run_async, args=(id,))
        thread.start()
        return "جاري إرسال طلبات الصداقة..."
    return "يجب إدخال ID صحيح"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8398)