from collections import defaultdict

CATEGORY_KEYWORDS = {
    "Food": ["food", "restaurant", "cafe", "lunch", "dinner", "breakfast", "pizza", "burger",
             "grocery", "groceries", "snack", "coffee", "tea", "meal", "eat", "swiggy", "zomato"],
    "Travel": ["travel", "uber", "ola", "taxi", "bus", "train", "flight", "fuel", "petrol",
               "diesel", "metro", "cab", "transport", "trip", "ticket"],
    "Shopping": ["shopping", "amazon", "flipkart", "clothes", "shirt", "shoes", "mall",
                 "store", "purchase", "buy", "order", "fashion"],
    "Bills": ["bill", "electricity", "water", "internet", "wifi", "phone", "mobile",
              "recharge", "subscription", "netflix", "rent", "emi"],
    "Health": ["medicine", "doctor", "hospital", "pharmacy", "health", "gym", "fitness",
               "medical", "clinic", "dental"],
    "Education": ["book", "course", "school", "college", "tuition", "fee", "education",
                  "study", "class", "training"],
}

def categorize_expense(title: str) -> str:
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            return category
    return "General"

def get_tips(expenses: list) -> dict:
    if not expenses:
        return {"tips": ["Start adding expenses to get personalized financial tips."], "total": 0}

    total = sum(e["amount"] for e in expenses)
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e.get("category", "General")] += e["amount"]

    tips = []

    # High spending categories
    for cat, amt in category_totals.items():
        pct = (amt / total * 100) if total > 0 else 0
        if pct > 40:
            tips.append(f"You're spending {pct:.0f}% on {cat}. Consider setting a budget cap for this category.")
        elif pct > 25:
            tips.append(f"{cat} accounts for {pct:.0f}% of your expenses. Look for ways to reduce it.")

    # General tips based on total
    if total > 50000:
        tips.append("Your total spending is quite high. Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings.")
    elif total > 20000:
        tips.append("Consider tracking daily expenses to identify unnecessary spending.")
    else:
        tips.append("Good job keeping expenses in check. Keep saving consistently.")

    # Category-specific tips
    if category_totals.get("Food", 0) > 5000:
        tips.append("Cooking at home more often can significantly reduce food expenses.")
    if category_totals.get("Shopping", 0) > 10000:
        tips.append("Try a 30-day rule: wait 30 days before making non-essential purchases.")
    if category_totals.get("Travel", 0) > 8000:
        tips.append("Consider carpooling or public transport to cut travel costs.")
    if category_totals.get("Bills", 0) > 5000:
        tips.append("Review your subscriptions — cancel ones you rarely use.")

    if not tips:
        tips.append("Your spending looks balanced. Keep an emergency fund of 3-6 months of expenses.")

    return {
        "tips": tips,
        "total": round(total, 2),
        "by_category": {k: round(v, 2) for k, v in category_totals.items()}
    }
