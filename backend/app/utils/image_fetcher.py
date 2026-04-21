import requests


def fetch_wikipedia_image(query: str):
    print("\n===== IMAGE FETCH DEBUG =====")
    print("Query:", query)

    try:
        url = "https://en.wikipedia.org/w/api.php"

        # STEP 1: SEARCH PAGE
        search_params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srsearch": query
        }

        search_res = requests.get(url, params=search_params)
        search_data = search_res.json()

        results = search_data.get("query", {}).get("search", [])

        if not results:
            print("❌ No search results")
            return None

        page_title = results[0]["title"]
        print("Page title:", page_title)

        # STEP 2: GET IMAGE USING pageimages
        image_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 500
        }

        image_res = requests.get(url, params=image_params)
        image_data = image_res.json()

        pages = image_data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "thumbnail" in page:
                image_url = page["thumbnail"]["source"]
                print("✅ Image found:", image_url)
                return image_url

        print("⚠️ No thumbnail found, trying fallback...")

        # STEP 3: FALLBACK → use pageimages with original image
        fallback_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "pageimages",
            "piprop": "original"
        }

        fallback_res = requests.get(url, params=fallback_params)
        fallback_data = fallback_res.json()

        pages = fallback_data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "original" in page:
                image_url = page["original"]["source"]
                print("✅ Fallback image:", image_url)
                return image_url

        print("❌ No image found even in fallback")

    except Exception as e:
        print("❌ Error:", e)

    return None