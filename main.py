from bs4 import BeautifulSoup
import requests
import json
import csv
import time

start_time = time.time()
start_time =start_time
print('Работа началасьdfdffd')

def get_data():
    with open(f"output_orders.csv", "w",encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow(
            (
                "order_name",
                "description",
                "start_date",
                "deadline_date",
                "user_name",
                "order_href",
            )
        )

    orders_data = []
    pages_count = 5
    for page in range(1,pages_count):

        url = f'https://studwork.org/orders?discipline_group_ids=4&page={page + 1}'

        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
        }

        req = requests.get(url, headers=headers)
        src = req.text

        with open("index.html", "w", encoding='utf-8') as file:
            file.write(src)

        with open("index.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_orders_hrefs = soup.find_all(class_="sw-link order-item__link sw-link_styled")

        all_orders_dict = {}

        for item in all_orders_hrefs:
            item_text = item.text
            item_href = "https://studwork.org" + item.get("href")
            all_orders_dict[item_text] = item_href

        count = 0

        for order_name, order_href in all_orders_dict.items():

            req = requests.get(url=order_href, headers=headers)
            src = req.text

            '''with open(f'data/{count}.html', "w", encoding='utf-8') as file:
                file.write(src)

            with open(f"data/{count}.html", encoding='utf-8') as file:
                src = file.read()'''

            soup = BeautifulSoup(src, "lxml")

            order_info = soup.find(class_="rich-editor-preview ql-editor order-text__text").find_all("p")
            start_date = soup.find_all("div", {"class": "chess-board-cell__value"})[8].text.strip()
            deadline_date = soup.find_all("div", {"class": "chess-board-cell__value"})[5].text.strip()
            user_name = soup.find(class_="user-info__right-top").text.strip()

            order_text = ''
            for item in order_info:
                order_text += f"{item.text.strip()}"

            count += 1

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

            with open(f"output_orders.csv", "a",encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        order_name,
                        order_text,
                        start_date,
                        deadline_date,
                        user_name,
                        order_href
                    )
                )
        print(f"Обработана {page}/{pages_count}")
        time.sleep(1)

    with open(f"order_{count}.json", "w",encoding='utf-8') as file:
        json.dump(orders_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")
    print(' ЫЫ')

if __name__ == "__main__":
    main()