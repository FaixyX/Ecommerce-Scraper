document
.getElementById("hamburger-menu")
.addEventListener("click", function () {
  document.getElementById("slide-menu").classList.add("show");
  document.getElementById("hamburger-menu").style.display = "none";
});

document.getElementById("close-btn").addEventListener("click", function () {
document.getElementById("slide-menu").classList.remove("show");
document.getElementById("hamburger-menu").style.display = "block";
});

// ------------------Filter-----------
// -----------------------------------

document.addEventListener("DOMContentLoaded", () => {
const filterBtn = document.querySelector(".filter-btn");
const filterPanel = document.querySelector(".filter-panel");
const closeBtn = document.querySelector(".close-btn1");
const overlay = document.querySelector(".overlay");
const priceRangeButtons = document.querySelectorAll(
  ".price-range button"
);
const productCards = document.querySelectorAll(".product-cart");

filterBtn.addEventListener("click", () => {
  filterPanel.classList.add("open");
  overlay.classList.add("visible");
});

closeBtn.addEventListener("click", () => {
  filterPanel.classList.remove("open");
  overlay.classList.remove("visible");
});

overlay.addEventListener("click", () => {
  filterPanel.classList.remove("open");
  overlay.classList.remove("visible");
});

priceRangeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const range = button.getAttribute("data-range").split("-");
    let minPrice, maxPrice;
    
    minPrice = parseInt(range[0], 10);
    
    if (range[1] == "all") {
      maxPrice = Infinity;
    } else {
      maxPrice = parseInt(range[1], 10);
    }

    productCards.forEach((card) => {
      const productPrice = parseInt(card.getAttribute("data-price"), 10);
      if (productPrice >= minPrice && productPrice <= maxPrice) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });

    filterPanel.classList.remove("open");
    overlay.classList.remove("visible");
  });
});
});
// ----------------------------------
// ----------Sort-------------------
document.addEventListener("DOMContentLoaded", () => {
const sortBtn = document.querySelector("#sort-btn");
const sortPanel = document.querySelector(".sort-panel");
const sortCloseBtn = document.querySelector(".sort-close-btn");
const sortOverlay = document.querySelector(".sort-overlay");
const sortOptions = document.querySelectorAll('input[name="sort"]');
const productGrid = document.querySelector(".product-container");
const productCards = Array.from(
  document.querySelectorAll(".product-cart")
);

sortBtn.addEventListener("click", () => {
  sortPanel.classList.add("open");
  sortOverlay.classList.add("visible");
});

sortCloseBtn.addEventListener("click", () => {
  sortPanel.classList.remove("open");
  sortOverlay.classList.remove("visible");
});

sortOverlay.addEventListener("click", () => {
  sortPanel.classList.remove("open");
  sortOverlay.classList.remove("visible");
});

sortOptions.forEach((option) => {
  option.addEventListener("change", () => {
    const sortValue = option.value;
    const sortedCards = [...productCards].sort((a, b) => {
      const priceA = parseInt(a.getAttribute("data-price"), 10);
      const priceB = parseInt(b.getAttribute("data-price"), 10);
      return sortValue === "low-to-high"
        ? priceA - priceB
        : priceB - priceA;
    });

    productGrid.innerHTML = "";
    sortedCards.forEach((card) => {
      productGrid.appendChild(card);
    });

    sortPanel.classList.remove("open");
    sortOverlay.classList.remove("visible");
  });
});
});
//  ----------------------------------------
//  ----------------Pagination-------------

document.addEventListener("DOMContentLoaded", function () {
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
const pageNumbers = document.querySelectorAll(".page-number");

function updateActivePage(newIndex) {
  pageNumbers.forEach((page) => page.classList.remove("active"));
  pageNumbers[newIndex].classList.add("active");
}

prevButton.addEventListener("click", function (event) {
  event.preventDefault();
  const currentIndex = Array.from(pageNumbers).findIndex((page) =>
    page.classList.contains("active")
  );
  if (currentIndex > 0) {
    updateActivePage(currentIndex - 1);
  }
});

nextButton.addEventListener("click", function (event) {
  event.preventDefault();
  const currentIndex = Array.from(pageNumbers).findIndex((page) =>
    page.classList.contains("active")
  );
  if (currentIndex < pageNumbers.length - 1) {
    updateActivePage(currentIndex + 1);
  }
});

pageNumbers.forEach((page, index) => {
  page.addEventListener("click", function (event) {
    event.preventDefault();
    updateActivePage(index);
  });
});
});