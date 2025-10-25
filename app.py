from flask import Flask, request, jsonify
import instaloader
import time

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/getBulkPosts', methods=['POST'])
def get_bulk_posts():
    urls = request.json.get('urls', [])
    results = []
    
    for url in urls[:15]:
        try:
            shortcode = url.strip('/').split('/')[-1]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            post_data = {
                "url": url,
                "caption": post.caption,
                "media": []
            }

            if post.typename == 'GraphSidecar':
                for node in post.get_sidecar_nodes():
                    media_url = node.video_url if node.is_video else node.display_url
                    post_data["media"].append(media_url)
            else:
                media_url = post.video_url if post.is_video else post.url
                post_data["media"].append(media_url)

            results.append(post_data)
            time.sleep(1)

        except Exception as e:
            results.append({"url": url, "error": str(e)})

    return jsonify(results)

@app.route('/')
def home():
    return jsonify({"message": "Instagram Bulk Downloader API Running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
