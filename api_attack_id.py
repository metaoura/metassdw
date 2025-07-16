import httpx
import time
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from flask import Flask, request, jsonify
from datetime import datetime
from threading import Thread
from flask import Flask, jsonify, request
import asyncio

app = Flask(__name__)

# Encryption configuration
key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

############ ENCRYPT-UID ##############
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

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

###### ENCRYPT & DECRYPT ID EMOTES ########
def Encrypt_id_emote(uid):
    result = []
    while uid > 0:
        byte = uid & 0x7F
        uid >>= 7
        if uid > 0:
            byte |= 0x80
        result.append(byte)
    return bytes(result).hex()

def Decrypt_id_emote(uidd):
    bytes_value = bytes.fromhex(uidd)
    r, _ = 0, 0
    for byte in bytes_value:
        r |= (byte & 0x7F) << _
        if not (byte & 0x80):
            break
        _ += 7
    return r

# Account credentials
tokens = {
    "3926914727": "1FA1752173731CC4BD541C20EAB4904C0C8366A68DC8C8012620C4D8B3457D64",
    "3926919103": "38D2C169750CBF96150D41A52017EEBB98F2A0B32D6EC6D9DB401D8887D0F9F5",
    "3926921041": "64E792645C000A900B5B57D6FD2BD11C19FE1157DF245E11F0C84F95C01CF98B",
    "3926922704": "2F86C96304D97C12D22E773BA94A87D08CE0B6D242B3F00E6E513B9F51AEBB4E",
    "3926925415": "AA3E57EEB6D0B7635DF323678642E454A4073301713B930482F5DF129F530D88",
    "3926928553": "7EE0EBEF5E81D747A57D4E4B7694E1125BCD3DA4474FCA83B8112E56EA31590E",
    "3926931190": "21AE58FDA73A4C0E4BE07857408D2F41A3904A1DFED871F09FF63B9F9A4F244C",
    "3926933016": "18F9EFC96E575E46DBA04C1FA54844BA16D215227CE9A666278854430FC1DE85",
    "3926934852": "A817063950F0042C7FD75DD568E03EFC04F418AF6075EDF73D7126B062B6C04A",
}

# JWT tokens storage
jwt_tokens = {}

async def get_jwttoken(uid, password, max_retries=3):
    url = f"https://projects-fox-x-get-jwt.vercel.app/get?uid={uid}&password={password}"
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'success':
                    jwt_tokens[uid] = data['token']
                    jwt_tokens[f"{uid}_timestamp"] = time.time()
                    print(f"JWT Token updated for UID {uid}")
                    return True
                else:
                    print(f"Attempt {attempt + 1} failed for UID {uid}: {data.get('message', 'No error message')}")
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error for UID {uid} (attempt {attempt + 1}): {e.response.status_code}")
        except httpx.RequestError as e:
            print(f"Request error for UID {uid} (attempt {attempt + 1}): {str(e)}")
        except Exception as e:
            print(f"Unexpected error for UID {uid} (attempt {attempt + 1}): {str(e)}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    print(f"Failed to get JWT token for UID {uid} after {max_retries} attempts")
    return False

async def update_all_jwt_tokens():
    tasks = [get_jwttoken(uid, password) for uid, password in tokens.items()]
    results = await asyncio.gather(*tasks)
    
    successful = sum(results)
    print(f"Token update completed. Success: {successful}/{len(tokens)}")
    
    if successful < len(tokens):
        print("Warning: Some tokens failed to update")

async def token_updater():
    while True:
        print("\nStarting scheduled token update...")
        await update_all_jwt_tokens()
        await asyncio.sleep(8 * 3600)  # Update every 8 hours

async def send_request(player_id, uid):
    if uid not in jwt_tokens:
        return f"JWT Token missing for UID {uid}"

    try:
        encrypted_id = Encrypt_ID(player_id)
        encrypted_api = encrypt_api(f"08{encrypted_id}1007")
        target = bytes.fromhex(encrypted_api)
        
        url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
        headers = {
            "Authorization": f"Bearer {jwt_tokens.get(uid)}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "ob49",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Host": "clientbp.common.ggbluefox.com",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate, br",
        }

        async with httpx.AsyncClient(verify=False ,timeout=30.0) as client:
            response = await client.post(url, headers=headers, data=target)
            
            if response.status_code == 200:
                return f"Success: {player_id} with UID {uid}"
            else:
                return f"Failed: {player_id} with UID {uid} (HTTP {response.status_code})"
    
    except Exception as e:
        return f"Error: {player_id} with UID {uid} - {str(e)}"

@app.route('/attack', methods=['GET'])
async def attack_handler():
    player_id = request.args.get('uid')
    if not player_id:
        return jsonify({"status": "error", "message": "uid parameter is required"}), 400

    try:
        # Validate player_id is numeric
        int(player_id)
    except ValueError:
        return jsonify({"status": "error", "message": "uid must be a numeric value"}), 400

    tasks = [send_request(player_id, uid) for uid in tokens.keys()]
    results = await asyncio.gather(*tasks)

    return jsonify({
        "status": "completed",
        "target": player_id,
        "attempts": len(tasks),
        "results": results
    })

async def startup():
    print("Initializing token update...")
    await update_all_jwt_tokens()
    asyncio.create_task(token_updater())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
    app.run(host='0.0.0.0', port=8399, debug=False)