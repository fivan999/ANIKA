from http.client import responses
from sys import prefix

import aiohttp
import asyncio


async def fetch_product_info(article):
    url = f"https://randewoo.ru/product/{article}/quickview"
    headers = {
        "authority": "randewoo.ru",
        "method": "GET",
        "path": "/product/491083/quickview",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "baggage": "sentry-environment=production,sentry-public_key=51f40e8cc71583795b67756ce944dd6f,sentry-trace_id=cfd731cd85d746ae86f295c88dbc335a,sentry-sample_rate=0.01,sentry-sampled=false",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://randewoo.ru/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    }
    headers = {
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    cookies = {
        "subscriber_status": "new",
        "_ga": "GA1.1.2029755882.1721668682",
        "_ym_uid": "1721573459247860409",
        "_ym_d": "1721668683",
        "popmechanic_sbjs_migrations": "popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1",
        "_userGUID": "0:lyx92y9j:N2rD7~x1bEiHxqdsO3Re8O6JSeJHHKpO",
        "_pin_unauth": "dWlkPU5XRTRNRGczTkdNdE9XSXdNQzAwWldNNUxXRTVNREl0WlRObE5ETTBPVGhtWW1Wag",
        "Fuuid": "674b3a90-7344-4602-805e-49a2232a47c6,1722162824",
        "deduplication_cookie": "direct",
        "digi_uc": "|v:172166:5715!172216:41720|s:172216:41720!172246:5715",
        "firstVisitTime": "1722789350027",
        "cartHash": "b05b87a1c86426f678f35b94af0d289e",
        "dSesn": "d602bf69-0114-5e52-ae61-4535ddc9a6d9",
        "_dvs": "0:lzfsasj9:pi7_3pzzYD7bEI_LTHlozJ7XSj7c1vn6",
        "_ym_isad": "2",
        "utm_params": "%5B%7B%22digiSearch%22%3A%22true%22%2C%22term%22%3A%22Cha%22%2C%22params%22%3A%22%7Csort%3DDEFAULT%22%2C%22created_at%22%3A%222024-07-29T22%3A52%3A28.409%2B03%3A00%22%7D%2C%7B%22digiSearch%22%3A%22true%22%2C%22term%22%3A%22Cha%22%2C%22params%22%3A%22%7Csort%3DDEFAULT%22%2C%22created_at%22%3A%222024-08-01T00%3A04%3A21.491%2B03%3A00%22%7D%2C%7B%22digiSearch%22%3A%22true%22%2C%22term%22%3A%22Cha%22%2C%22params%22%3A%22%7Csort%3DDEFAULT%22%2C%22created_at%22%3A%222024-08-01T00%3A07%3A45.968%2B03%3A00%22%7D%2C%7B%22digiSearch%22%3A%22true%22%2C%22term%22%3A%22Cha%22%2C%22params%22%3A%22%7Csort%3DDEFAULT%22%2C%22created_at%22%3A%222024-08-04T19%3A36%3A00.214%2B03%3A00%22%7D%2C%7B%22created_at%22%3A%222024-08-04T19%3A36%3A03.344%2B03%3A00%22%7D%5D",
        "last_request": "23789067-0971-44de-9617-22534091030d",
        "pageCount": "3",
        "_ga_RN3S387LJ5": "GS1.1.1722789354.8.1.1722789355.59.0.0",
        "_ga_LBDKL5SKRS": "GS1.1.1722789355.8.0.1722789355.60.0.0",
        "_derived_epik": "dj0yJnU9NXlsMHRPUjcwaTB5Wi1mSzRaODZ5c2piTXdXa3YzU3Ambj0tSXpiU0Nhbl8xdHI2ekNWRDBZSjVRJm09MSZ0PUFBQUFBR2F2cmZjJnJtPTEmcnQ9QUFBQUFHYXZyZmMmc3A9Mg",
        "mindboxDeviceUUID": "763e7233-8167-4712-a0dd-2b069fd8cd43",
        "directCrm-session": "%7B%22deviceGuid%22%3A%22763e7233-8167-4712-a0dd-2b069fd8cd43%22%7D",
        "_cd_randewoo_session_2": "LzFodEFrMHVhbVZHbG8xZTdFS20wMm9nN21uUnlpZ2l5dVBmdkVUeEVTN1FmZy9Fd1dvclBWRU9zQ0pUTGtrSUc0SkhINDZCNzJqTjhQazQ5OXBhcUhPdDVkUlVvYlZEckVXMEV0MURzL1o4KzRFSUUyeHFuRDJpYjY3N3dWMStqVGlWUTIzN2dFVncvZ3liZlJmNVc4TXB4QkwzMWtCNGV5aHlsR1hVNnlpRW9nVDhiU3pOajlOZ3VRUkdMV2VOM21HT3lDSHgwTDZMc2s3dER0UDlMbkF4VmZvdVY1WEFWM2cyTXlTeks0bjNBK2V5Q2JHV3BWZDdxeXRoZ2w4MjVqRGp4RjNMcnBnV2VFZGJwdUpDdUFXUmZLYmNnWlRQalY5K3Y4WTJ5azg9LS1SYUVObWMxbUhNZUhCVGlTWkJZNHB3PT0%3D--c68664ad8a7aec82fe6525f17c0ffe03785589c8",
        "Dsign": "y",
        "Duuid": "f3cf44e2-ae2e-4ce2-95ae-afa297b3b56e"
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://www.fragrantica.ru/news/Kollekcia-Zara-Amber-Amber-Fever-Amber-In-Bloom-Amber-Satin-i-Stellar-Amber-16109.html#cc205081'
        response = await session.get(url, headers=headers)
        print(await response.text())
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, headers=headers, cookies=cookies) as response:
    #         if response.status == 200:
    #             data = await response.text()
    #             print(data)  # Здесь можно обработать или вернуть данные
    #         else:
    #             print(f"Request failed with status: {response.status}")
    await asyncio.sleep(10)
