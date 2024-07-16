document.addEventListener("DOMContentLoaded", () => {
    const addProductBtn = document.getElementById("addProductBtn");
    const productFormPopup = document.getElementById("productFormPopup");
    const closeBtn = document.querySelector(".close-btn");
    const cancelBtn = document.getElementById("cancelBtn");
    const productForm = document.getElementById("productForm");
    const productTableBody = document.getElementById("productTableBody");

    let products = [];
    let currentProductIndex = null;

    const openPopup = () => {
      productFormPopup.style.display = "block";
    };

    const closePopup = () => {
      productFormPopup.style.display = "none";
      productForm.reset();
      currentProductIndex = null;
    };

    const renderProducts = () => {
      productTableBody.innerHTML = "";
      products.forEach((product, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
              <td>${index + 1}</td>
              <td>${product.name}</td>
              <td>${product.url}</td>
              <td>
                  <button onclick="editProduct(${index})">Edit</button>
                  <button onclick="deleteProduct(${index})">Delete</button>
              </td>
          `;
        productTableBody.appendChild(row);
      });
    };

    window.editProduct = (index) => {
      currentProductIndex = index;
      const product = products[index];
      document.getElementById("productId").value = product.id;
      document.getElementById("productName").value = product.name;
      document.getElementById("productURL").value = product.url;
      openPopup();
    };

    window.deleteProduct = (index) => {
      products.splice(index, 1);
      renderProducts();
    };

    addProductBtn.addEventListener("click", openPopup);
    closeBtn.addEventListener("click", closePopup);
    cancelBtn.addEventListener("click", closePopup);

    productForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const id = products.length + 1;
      const name = document.getElementById("productName").value;
      const url = document.getElementById("productURL").value;

      if (currentProductIndex !== null) {
        products[currentProductIndex] = { id, name, url };
      } else {
        products.push({ id, name, url });
      }

      renderProducts();
      closePopup();
    });
  });