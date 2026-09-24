
from flask import Flask, request, render_template_string, jsonify
from ddgs import DDGS
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Gyugle</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: white;
    color: #202124;
}

body.dark {
    background: #202124;
    color: #eee;
}

header {
    height: 70px;
    padding: 0 25px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid #eee;
}

body.dark header {
    border-color: #444;
}

.logo {
    font-size: 28px;
    font-weight: bold;
}

.g { color:#4285f4; }
.y { color:#ea4335; }
.u { color:#fbbc05; }
.g2 { color:#4285f4; }
.l { color:#34a853; }
.e { color:#ea4335; }

.theme {
    border: 0;
    background: transparent;
    font-size: 22px;
    cursor: pointer;
}

.container {
    max-width: 950px;
    margin: 45px auto;
    padding: 20px;
}

.home-logo {
    text-align: center;
    font-size: 72px;
    font-weight: bold;
    margin-bottom: 30px;
}

.search-area {
    position: relative;
}

.search-box {
    display: flex;
    align-items: center;

    border: 1px solid #dfe1e5;
    border-radius: 30px;

    padding: 5px 7px 5px 20px;

    box-shadow: 0 2px 8px rgba(0,0,0,.08);
}

.search-box input {
    flex: 1;

    border: none;
    outline: none;

    background: transparent;
    color: inherit;

    font-size: 17px;
    padding: 12px 5px;
}

.search-button {
    border: none;

    border-radius: 25px;

    background: #4285f4;
    color: white;

    padding: 12px 20px;

    cursor: pointer;
}

.suggestions {
    position: absolute;

    left: 0;
    right: 0;

    top: 60px;

    background: white;

    border: 1px solid #ddd;

    border-radius: 12px;

    overflow: hidden;

    z-index: 100;

    box-shadow: 0 5px 20px rgba(0,0,0,.15);
}

body.dark .suggestions {
    background: #303134;
    border-color: #555;
}

.suggestion {
    padding: 12px 18px;
    cursor: pointer;
}

.suggestion:hover {
    background: #f1f3f4;
}

body.dark .suggestion:hover {
    background: #444;
}

.tabs {
    display: flex;
    gap: 25px;

    margin-top: 30px;

    border-bottom: 1px solid #ddd;

    padding-bottom: 12px;
}

.tabs a {
    color: #555;
    text-decoration: none;
}

body.dark .tabs a {
    color: #ddd;
}

.tabs .active {
    color: #4285f4;
    font-weight: bold;
}

.info {
    margin-top: 20px;
    color: #777;
    font-size: 14px;
}

.result {
    margin-top: 28px;
}

.url {
    color: #188038;
    font-size: 14px;
    overflow-wrap: anywhere;
}

.title {
    display: inline-block;

    margin-top: 5px;

    color: #1a0dab;

    font-size: 21px;

    text-decoration: none;
}

body.dark .title {
    color: #8ab4f8;
}

.title:hover {
    text-decoration: underline;
}

.description {
    margin-top: 7px;

    line-height: 1.5;

    color: #555;
}

body.dark .description {
    color: #ccc;
}

.pagination {
    display: flex;
    justify-content: center;

    gap: 8px;

    margin-top: 50px;
}

.pagination a {
    text-decoration: none;

    padding: 10px 15px;

    border: 1px solid #ddd;

    border-radius: 8px;

    color: inherit;
}

.pagination a:hover {
    background: #f1f3f4;
}

body.dark .pagination a:hover {
    background: #444;
}

.footer {
    text-align: center;

    margin-top: 80px;

    color: #777;
}

.error {
    margin-top: 25px;

    padding: 15px;

    background: #ffecec;

    color: #b00020;

    border-radius: 10px;
}

@media(max-width:600px) {

    .container {
        margin-top: 25px;
    }

    .home-logo {
        font-size: 50px;
    }

    .search-box input {
        font-size: 15px;
    }

    .search-button {
        padding: 10px 14px;
    }

}

</style>
</head>


<body>


<header>

<div class="logo">

<span class="g">G</span>
<span class="y">y</span>
<span class="u">u</span>
<span class="g2">g</span>
<span class="l">l</span>
<span class="e">e</span>

</div>


<button
class="theme"
onclick="toggleDark()"
>
🌙
</button>

</header>



<div class="container">


{% if not query %}

<div class="home-logo">

<span class="g">G</span>
<span class="y">y</span>
<span class="u">u</span>
<span class="g2">g</span>
<span class="l">l</span>
<span class="e">e</span>

</div>

{% endif %}



<div class="search-area">

<form
class="search-box"
method="GET"
>

<input
id="searchInput"
type="text"
name="q"
value="{{ query }}"
placeholder="무엇이든 검색하세요..."
autocomplete="off"
autofocus
>

<input
type="hidden"
name="page"
value="1"
>

<button
class="search-button"
type="submit"
>
🔎 검색
</button>

</form>


<div
id="suggestions"
class="suggestions"
style="display:none"
>
</div>

</div>



{% if query %}

<div class="tabs">

<a
class="active"
href="/?q={{ query }}&page=1"
>
🌐 웹
</a>

<a
href="https://duckduckgo.com/?q={{ query }}"
target="_blank"
>
🦆 DuckDuckGo
</a>

</div>

{% endif %}



{% if query %}

<div class="info">

검색 결과 {{ result_count }}개
· 약 {{ search_time }}초

</div>

{% endif %}



{% if error %}

<div class="error">
{{ error }}
</div>

{% endif %}



{% for result in results %}

<div class="result">

<div class="url">
{{ result.href }}
</div>

<a
class="title"
href="{{ result.href }}"
target="_blank"
rel="noopener noreferrer"
>
{{ result.title }}
</a>

{% if result.body %}

<div class="description">
{{ result.body }}
</div>

{% endif %}

</div>

{% endfor %}



{% if query and results %}

<div class="pagination">

{% if page > 1 %}

<a
href="/?q={{ query }}&page={{ page - 1 }}"
>
← 이전
</a>

{% endif %}


<a
href="/?q={{ query }}&page={{ page + 1 }}"
>
다음 →
</a>

</div>

{% endif %}



{% if query and not results and not error %}

<p>
검색 결과가 없습니다.
</p>

{% endif %}



<div class="footer">

Gyugle Search

<br>

Powered by DuckDuckGo

</div>


</div>



<script>

const input =
document.getElementById("searchInput");

const suggestions =
document.getElementById("suggestions");


input.addEventListener(
"input",
async function() {

    const q = input.value.trim();

    if (!q) {

        suggestions.style.display =
        "none";

        return;
    }

    try {

        const response =
        await fetch(
            "/suggest?q="
            + encodeURIComponent(q)
        );

        const data =
        await response.json();

        suggestions.innerHTML = "";

        if (
            !data.suggestions ||
            data.suggestions.length === 0
        ) {

            suggestions.style.display =
            "none";

            return;

        }


        data.suggestions.forEach(
        function(text) {

            const div =
            document.createElement("div");

            div.className =
            "suggestion";

            div.textContent =
            "🔎 " + text;

            div.onclick =
            function() {

                input.value = text;

                suggestions.style.display =
                "none";

                input.form.submit();

            };

            suggestions.appendChild(div);

        });


        suggestions.style.display =
        "block";

    } catch (error) {

        suggestions.style.display =
        "none";

    }

});


document.addEventListener(
"click",
function(event) {

    if (
        !event.target.closest(
            ".search-area"
        )
    ) {

        suggestions.style.display =
        "none";

    }

});


function toggleDark() {

    document.body.classList.toggle(
        "dark"
    );

    if (
        document.body.classList.contains(
            "dark"
        )
    ) {

        localStorage.setItem(
            "dark",
            "1"
        );

    } else {

        localStorage.removeItem(
            "dark"
        );

    }

}


if (
    localStorage.getItem("dark")
    === "1"
) {

    document.body.classList.add(
        "dark"
    );

}

</script>


</body>
</html>
"""


def search_web(query, page):

    offset = (page - 1) * 10

    with DDGS() as ddgs:

        return list(
            ddgs.text(
                query,
                max_results=10,
                safesearch="moderate"
            )
        )


def make_suggestions(query):

    suggestions = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=5
            )

            for result in results:

                title = result.get(
                    "title",
                    ""
                )

                if title:
                    suggestions.append(title)

    except Exception:
        pass

    return suggestions


@app.route("/")
def home():

    query = request.args.get(
        "q",
        ""
    ).strip()

    try:

        page = int(
            request.args.get(
                "page",
                1
            )
        )

    except ValueError:

        page = 1


    if page < 1:
        page = 1


    if not query:

        return render_template_string(
            HTML,

            query="",

            results=[],

            result_count=0,

            search_time="",

            page=1,

            error=""
        )


    start = time.time()

    error = ""

    results = []


    try:

        results = search_web(
            query,
            page
        )

    except Exception as e:

        print(
            "검색 오류:",
            e
        )

        error = (
            "검색에 실패했습니다. "
            "잠시 후 다시 시도해주세요."
        )


    elapsed = round(
        time.time() - start,
        2
    )


    return render_template_string(

        HTML,

        query=query,

        results=results,

        result_count=len(results),

        search_time=elapsed,

        page=page,

        error=error
    )


@app.route("/suggest")
def suggest():

    query = request.args.get(
        "q",
        ""
    ).strip()


    if not query:

        return jsonify({
            "suggestions": []
        })


    if len(query) > 100:

        return jsonify({
            "suggestions": []
        })


    suggestions =make_suggestions(query)


    return jsonify({
        "suggestions":
        suggestions
    })


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False
    )

