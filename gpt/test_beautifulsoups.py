import requests
from bs4 import BeautifulSoup

# 简易版联网搜索
def online_search(query):
    # 联网搜索URL
    url = 'http://www.bing.com/s'
    # 查询参数
    params = {'wd': query}
    # 发送GET请求
    response = requests.get(url, params=params)
    # 确保请求成功
    response.raise_for_status()
    # 使用BeautifulSoup解析HTML内容

    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找所有搜索结果
    results = soup.find_all('h3', class_='t')

    for result in results:
        # 获取每个结果的标题和链接
        title = result.get_text()
        link = result.find('a').get('href')
        print(f"标题: {title}")
        print(f"链接: {link}")
        print("------")


# ------------------------------------
# 不可用  code: 521
def query_cve(cve_id):
    # url = f"https://www.cvedetails.com/cve/{cve_id}/"
    url = f"https://www.cnvd.org.cn/flaw/show/{cve_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    with requests.Session() as session:
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 查找并提取CVE详情
            cve_details = {}
            cve_details['cve_id'] = cve_id

            # 示例：提取CVE描述
            description_tag = soup.find('div', attrs={'class': 'cvedetailssummary'})
            if description_tag:
                cve_details['description'] = description_tag.text.strip()

            # 示例：提取其他信息（例如：得分、发布日期等）
            score_tag = soup.find('div', attrs={'class': 'cvssbox'})
            if score_tag:
                cve_details['cvss_score'] = score_tag.text.strip()

            publish_date_tag = soup.find('span', attrs={'data-cve-id': cve_id})
            if publish_date_tag:
                cve_details['publish_date'] = publish_date_tag.text.strip()

            return cve_details
        else:
            print(f"Failed to retrieve data for {cve_id}. Status code: {response.status_code}")
            return None

# # 示例：查询特定CVE编号
# # cve_id = "CVE-2021-44228"
# # cve_id = "CNVD-2024-31091"
# cve_id = "CNVD-2024-31085"

# cve_details = query_cve(cve_id)

# if cve_details:
#     print("CVE Details:")
#     for key, value in cve_details.items():
#         print(f"{key}: {value}")
# else:
#     print("No details found for the given CVE.")



