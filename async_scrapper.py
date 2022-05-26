from bs4 import BeautifulSoup
import csv
import time
import asyncio
import aiohttp
import datetime
import json

orders_data = []
start_time = time.time()


async def get_page_data(session, page):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
    }

    url = f'https://studwork.org/orders?discipline_group_ids=4&page={page + 1}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")
        all_orders_hrefs = soup.find_all(class_="sw-link order-item__link sw-link_styled")

        all_orders_dict = {}

        for item in all_orders_hrefs:
            item_text = item.text
            item_href = "https://studwork.org" + item.get("href")
            all_orders_dict[item_text] = item_href

        count = 0

        for order_name, order_href in all_orders_dict.items():

            async with session.get(url=order_href, headers=headers) as response:
                response_text = await response.text()

                soup = BeautifulSoup(response_text, "lxml")

                order_info = soup.find(class_="rich-editor-preview ql-editor order-text__text").find_all("p")
                start_date = soup.find_all("div", {"class": "chess-board-cell__value"})[8].text.strip()
                deadline_date = soup.find_all("div", {"class": "chess-board-cell__value"})[5].text.strip()
                user_name = soup.find(class_="user-info__right-top").text.strip()

                order_text = ''
                for item in order_info:
                    order_text += f"{item.text.strip()}"

                orders_data.append(
                    {
                        "order_name": order_name,
                        "order_text": order_text,
                        "start_date": start_date,
                        "deadline_date": deadline_date,
                        "user_name": user_name,
                        "order_href": order_href,
                    }
                )

                count += 1


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        pages_count = 5
        for page in range(1, pages_count):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)
pass
async def main():
    await gather_data()
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"order_{cur_time}_async.json", "w",encoding='utf-8') as file:
        json.dump(orders_data, file, indent=4, ensure_ascii=False)

    with open(f"order_{cur_time}_async.csv", "w",encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "order_name",
                "order_text",
                "start_date"   
                "deadline_date",
                "user_name",
                "order_href",
            )
        )

    for order in orders_data:

        with open(f"order_{cur_time}_async.csv", "a",encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    order["order_name"],
                    order["order_text"],
                    order["start_date"],
                    order["deadline_date"],
                    order["user_name"],
                    order["order_href"],
                )
            )
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")

    return f'order_{cur_time}_async.csv'

if __name__ == "__main__":
    asyncio.run(main())
