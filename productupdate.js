const container = document.querySelector('.product-container');

fetch('products.json')
.then(response => response.json())
.then(data => {
  const container = document.getElementById('product-container');
  data.products.forEach(product => {
    const box = document.createElement('div');
    box.classList.add('box');
    box.innerHTML = `
      <img src="${product.image}" alt="" class="product-img">
      <h3 class="product-title">${product.name}</h3>
      <span class="price">${product.price}</span>
      <i class="add-cart">add to cart</i>
    `;
    container.appendChild(box);
  });
});

fetch('products.json')
.then(response => response.json())
.then(data => {
  const container = document.getElementById('bestsellers');
  data.bestsellers.forEach(product => {
    const box = document.createElement('div');
    box.classList.add('box');
    box.innerHTML = `
      <img src="${product.image}" alt="" class="product-img">
      <h3 class="product-title">${product.name}</h3>
      <span class="price">${product.price}</span>
      <i class="add-cart">add to cart</i>
    `;
    container.appendChild(box);
  });
});