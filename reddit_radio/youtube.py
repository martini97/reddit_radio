from urllib.parse import parse_qs, urlparse

from reddit_radio.logging import logger


def extract_video_id(url):
    if url.startswith(("youtu", "www")):
        url = "http://" + url

    query = urlparse(url)
    hostname = query.hostname or ""
    video_id = None

    if "youtu" not in hostname:
        return None

    if hostname == "youtu.be":
        return query.path[1:]

    if "youtube.com" in hostname:
        if query.path == "/watch":
            video_id = parse_qs(query.query)["v"][0]
        elif query.path[:7] == "/embed/":
            video_id = query.path.split("/")[2]
        elif query.path[:3] == "/v/":
            video_id = query.path.split("/")[2]
        elif query.path == "/attribution_link":
            video_id = parse_qs(parse_qs(query.query)["u"][0].split("?")[1])["v"][0]
        elif query.path == "/playlist":
            video_id = parse_qs(query.query)["list"][0]

    if not video_id:
        logger.warning(f"Failed to get youtube id from [{url}]")

    return video_id
