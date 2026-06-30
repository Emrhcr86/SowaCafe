const menuRoot = document.querySelector("#menu");

const fallbackMenu = {
  categories: [
    {
      name: "Kahveler",
      items: [
        { name: "Espresso", description: "", price: "₺70" },
        { name: "Double Espresso", description: "", price: "₺100" },
        { name: "Americano", description: "", price: "₺120" },
        { name: "Filtre Kahve", description: "", price: "₺120" },
        { name: "Cappuccino", description: "", price: "₺140" },
        { name: "Latte", description: "", price: "₺140" },
        { name: "Flat White", description: "", price: "₺150" },
        { name: "Mocha", description: "", price: "₺150" },
        { name: "White Mocha", description: "", price: "₺150" },
        { name: "Caramel Latte", description: "", price: "₺150" },
        { name: "Türk Kahvesi", description: "", price: "₺60" }
      ]
    },
    {
      name: "Çaylar",
      items: [
        { name: "Çay", description: "", price: "₺30" },
        { name: "Bitki Çayları", description: "", price: "" }
      ]
    },
    {
      name: "Soğuk İçecekler",
      items: [
        { name: "Ev Yapımı Limonata", description: "", price: "₺120" },
        { name: "Ice Americano", description: "", price: "₺130" },
        { name: "Ice Latte", description: "", price: "₺150" },
        { name: "Ice Cappuccino", description: "", price: "₺150" },
        { name: "Ice Mocha", description: "", price: "₺160" },
        { name: "Ice Caramel Latte", description: "", price: "₺160" },
        { name: "Frozen", description: "", price: "₺160" },
        { name: "Soda", description: "", price: "₺35-50" },
        { name: "Su", description: "", price: "₺15" }
      ]
    },
    {
      name: "Yiyecekler",
      items: [
        { name: "Brownie", description: "", price: "₺120" },
        { name: "Tiramisu", description: "", price: "₺140" },
        { name: "Tost", description: "", price: "₺120" }
      ]
    }
  ]
};

const categoryMarks = {
  Kahveler: "☕",
  Caylar: "♨",
  "Soguk Icecekler": "❄",
  Yiyecekler: "🥐"
};

const normalizeText = (value) =>
  value
    .replaceAll("Ç", "C")
    .replaceAll("ç", "c")
    .replaceAll("Ğ", "G")
    .replaceAll("ğ", "g")
    .replaceAll("İ", "I")
    .replaceAll("ı", "i")
    .replaceAll("Ö", "O")
    .replaceAll("ö", "o")
    .replaceAll("Ş", "S")
    .replaceAll("ş", "s")
    .replaceAll("Ü", "U")
    .replaceAll("ü", "u");

function createMenuItem(item) {
  const row = document.createElement("li");
  row.className = "item";

  const name = document.createElement("span");
  name.className = "item-name";
  name.textContent = item.name;

  row.append(name);

  if (item.price) {
    const price = document.createElement("span");
    price.className = "item-price";
    price.textContent = item.price;
    row.append(price);
  } else {
    row.classList.add("item--no-price");
  }

  return row;
}

function createCategoryCard(category) {
  const card = document.createElement("article");
  card.className = "category-card";
  card.dataset.mark = categoryMarks[normalizeText(category.name)] || "•";

  const title = document.createElement("h2");
  title.className = "category-title";
  title.textContent = category.name;

  const list = document.createElement("ul");
  list.className = "items";
  category.items.forEach((item) => list.append(createMenuItem(item)));

  card.append(title, list);
  return card;
}

function renderMenu(data) {
  const fragment = document.createDocumentFragment();

  menuRoot.innerHTML = "";
  data.categories.forEach((category) => fragment.append(createCategoryCard(category)));
  menuRoot.append(fragment);
}

async function loadMenu() {
  if (window.location.protocol === "file:") {
    renderMenu(fallbackMenu);
    return;
  }

  try {
    const response = await fetch("./menu.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error("Menü dosyası okunamadı.");
    }

    const data = await response.json();
    renderMenu(data);
  } catch (error) {
    renderMenu(fallbackMenu);
  }
}

loadMenu();
