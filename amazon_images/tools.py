import re


def url_is_scraped(connection, url):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * from urls where url = ?
        """, (url,))
        result = cursor.fetchone()
    finally:
        cursor.close()

    return result


def get_title(resp):
    title_xp = "//span[@id='productTitle']/text()"
    try:
        title = resp.xpath(title_xp).extract()[0]
        return title.strip()

    except IndexError:
        return None


def get_seller_rank(resp):
    rank_xp = "//b[contains(text(), 'Amazon Best Sellers Rank:')]\
/following-sibling::text()"
    try:
        rank = resp.xpath(rank_xp).extract()[0]
        rank = rank.split()[0]
        rank = re.sub(r'#|,', '', rank)
        return int(rank)

    except IndexError:
        return None
