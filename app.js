const menu = [
  {
    id: "chiri-uchu",
    name: "Chiri Uchu",
    description: "El plato bandera de Cusco, ideal para compartir.",
    price: 28,
    icon: "🌽",
  },
  {
    id: "kapchi",
    name: "Kapchi de habas",
    description: "Habas, papa y queso en una receta casera y reconfortante.",
    price: 18,
    icon: "🥔",
  },
  {
    id: "picarones",
    name: "Picarones andinos",
    description: "Porción de seis picarones con miel de chancaca.",
    price: 12,
    icon: "🍯",
  },
];

const order = new Map();
const menuList = document.querySelector("#menu-list");
const orderItems = document.querySelector("#order-items");
const orderTotal = document.querySelector("#order-total");
const cartCount = document.querySelector("#cart-count");
const orderFeedback = document.querySelector("#order-feedback");

const formatPrice = (price) => `S/ ${price.toFixed(2)}`;

function renderMenu() {
  menuList.innerHTML = menu
    .map(
      (item) => `
        <article class="menu-item">
          <div>
            <div class="menu-item-icon" aria-hidden="true">${item.icon}</div>
            <h3>${item.name}</h3>
            <p>${item.description}</p>
          </div>
          <div class="menu-item-footer">
            <span class="menu-price">${formatPrice(item.price)}</span>
            <button class="add-button" type="button" data-add-item="${item.id}">
              Agregar
            </button>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderOrder() {
  const items = [...order.values()];
  const itemCount = items.reduce((total, item) => total + item.quantity, 0);
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  cartCount.textContent = itemCount;
  orderTotal.textContent = formatPrice(total);

  if (items.length === 0) {
    orderItems.innerHTML = '<p class="empty-state">Todavía no agregaste productos.</p>';
    return;
  }

  orderItems.innerHTML = items
    .map(
      (item) => `
        <div class="order-item">
          <div>
            <div class="order-item-name">${item.name}</div>
            <div class="order-item-detail">${item.quantity} × ${formatPrice(item.price)}</div>
          </div>
          <strong>${formatPrice(item.price * item.quantity)}</strong>
        </div>
      `,
    )
    .join("");
}

menuList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-add-item]");
  if (!button) return;

  const item = menu.find((menuItem) => menuItem.id === button.dataset.addItem);
  const current = order.get(item.id);
  order.set(item.id, { ...item, quantity: (current?.quantity ?? 0) + 1 });
  orderFeedback.textContent = `${item.name} se agregó al pedido.`;
  renderOrder();
});

document.querySelector("#clear-order").addEventListener("click", () => {
  order.clear();
  orderFeedback.textContent = "";
  renderOrder();
});

document.querySelector("#submit-order").addEventListener("click", () => {
  if (order.size === 0) {
    orderFeedback.textContent = "Agregá al menos un producto para confirmar.";
    return;
  }

  orderFeedback.textContent = "¡Pedido recibido! Te contactaremos para coordinar la entrega.";
});

renderMenu();
renderOrder();

