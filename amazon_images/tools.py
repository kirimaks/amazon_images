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
