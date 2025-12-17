from flask import Flask, render_template, request
from apriori_builder import generate_rules, get_subcategory_sales

app = Flask(__name__)
CSV_PATH = "coffe_shop.xlsx"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    min_support = 0.01
    min_confidence = 0.1

    # 🔥 TOP 10 SUB-CATEGORY
    labels, values = get_subcategory_sales(CSV_PATH, top_n=10)

    rules_1to1, rules_2to1, items = generate_rules(
        CSV_PATH,
        min_support,
        min_confidence
    )

    if request.method == "POST":
        min_support = float(request.form.get("min_support"))
        min_confidence = float(request.form.get("min_confidence"))
        mode = int(request.form.get("mode"))

        rules_1to1, rules_2to1, items = generate_rules(
            CSV_PATH,
            min_support,
            min_confidence
        )

        if mode == 1:
            item1 = request.form.get("item1")
            result = rules_1to1.get(item1)

        elif mode == 2:
            item1 = request.form.get("item1")
            item2 = request.form.get("item2")
            key = tuple(sorted([item1, item2]))
            result = rules_2to1.get(key)

    return render_template(
        "index.html",
        result=result,
        items=items,
        labels=labels,
        values=values
    )

if __name__ == "__main__":
    app.run(debug=True)