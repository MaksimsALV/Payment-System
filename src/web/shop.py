from flask import Blueprint, render_template_string

shop_ui = Blueprint('shop_ui', __name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Food Shop</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; }
    .card { border: 1px solid #e5e5e5; border-radius: 10px; padding: 16px; }
    h1 { margin: 0 0 12px; }
    label { display:block; margin-top: 12px; font-weight: 600; }
    input, select { width: 100%; padding: 10px; margin-top: 6px; box-sizing: border-box; }
    button { margin-top: 16px; padding: 10px 16px; cursor: pointer; width: 100%; }
    .row { display:flex; gap: 12px; }
    .col { flex: 1; }
    .muted { color: #666; font-size: 14px; }
    .summary { margin-top: 14px; padding: 12px; background: #f7f7f7; border-radius: 8px; }
    .summary div { display:flex; justify-content: space-between; margin: 6px 0; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Food Ordering</h1>
    <div class="muted">Pick an item, quantity, and pay with Stripe Checkout.</div>

    <div class="row">
      <div class="col">
        <label>Item</label>
        <select id="product"></select>
      </div>
      <div class="col">
        <label>Quantity</label>
        <input id="quantity" type="number" min="1" value="1" />
      </div>
    </div>

    <label>Customer email</label>
    <input id="customer_email" value="test@example.com" />

    <div class="summary">
      <div><span>Unit price</span><strong id="unitPrice">—</strong></div>
      <div><span>Total</span><strong id="totalPrice">—</strong></div>
    </div>

    <button id="btn">Proceed to checkout</button>
  </div>

  <script>
    // Predefined products: amount in smallest currency unit (e.g. cents)
    // Currency is tied to item directly.
    const PRODUCTS = [
      { id: "burger",  name: "Classic Burger",   amount: 700, currency: "eur" },
      { id: "fries",   name: "French Fries",     amount: 300, currency: "eur" },
      { id: "cola",    name: "Coca-Cola",        amount: 200, currency: "eur" },
      { id: "nuggets", name: "Chicken Nuggets",  amount: 400, currency: "eur" },
      { id: "salad",   name: "Caesar Salad",     amount: 500, currency: "eur" },
    ];

    const productSelect = document.getElementById("product");
    const qtyInput = document.getElementById("quantity");
    const unitPriceEl = document.getElementById("unitPrice");
    const totalPriceEl = document.getElementById("totalPrice");
    const btn = document.getElementById("btn");

    function formatMoney(cents, currency) {
      const value = (cents / 100);
      return `${value.toFixed(2)} ${currency.toUpperCase()}`;
    }

    function getSelectedProduct() {
      const id = productSelect.value;
      return PRODUCTS.find(p => p.id === id) || PRODUCTS[0];
    }

    function getQuantity() {
      const q = Number(qtyInput.value);
      return Number.isFinite(q) && q > 0 ? Math.floor(q) : 1;
    }

    function renderProducts() {
      productSelect.innerHTML = "";
      for (const p of PRODUCTS) {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${p.name} (${formatMoney(p.amount, p.currency)})`;
        productSelect.appendChild(opt);
      }
    }

    function updateSummary() {
      const p = getSelectedProduct();
      const q = getQuantity();
      unitPriceEl.textContent = formatMoney(p.amount, p.currency);
      totalPriceEl.textContent = formatMoney(p.amount * q, p.currency);
    }

    renderProducts();
    updateSummary();

    productSelect.addEventListener("change", updateSummary);
    qtyInput.addEventListener("input", updateSummary);

    btn.addEventListener("click", async () => {
      btn.disabled = true;
      btn.textContent = "Creating checkout session...";

      const p = getSelectedProduct();
      const q = getQuantity();
      const email = document.getElementById("customer_email").value.trim();

      // Your backend uses payload["amount"] as Stripe unit_amount (per item)
      const payload = {
        currency: p.currency,
        amount: p.amount,
        quantity: q,
        product_name: p.name,
        customer_email: email,
      };

      try {
        const res = await fetch("/checkout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          alert("Checkout failed: " + res.status);
          return;
        }

        const data = await res.json();

        // /checkout returns jsonify(url) => JSON string
        const url =
          (typeof data === "string" && data) ||
          (data && typeof data.url === "string" && data.url);

        if (!url) {
          alert("No redirect URL returned by /checkout");
          return;
        }

        window.location.assign(url);
      } catch (err) {
        alert("Error: " + err);
      } finally {
        // only relevant if we didn't navigate away
        btn.disabled = false;
        btn.textContent = "Pay";
      }
    });
  </script>
</body>
</html>
"""


@shop_ui.get("/")
def index():
    return render_template_string(HTML)
