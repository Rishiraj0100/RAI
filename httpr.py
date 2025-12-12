"""
HTTP to HTTPS redirect server using Quart.
"""

from quart import Quart, redirect, request

app = Quart(__name__)


@app.route("/<path:path>")
@app.route("/")
async def redirect_to_https(path=""):
    return redirect(f"https://{request.host}{request.full_path}", code=301)

if __name__=="__main__":
    app.run("0.0.0.0", port=8080, debug=True)