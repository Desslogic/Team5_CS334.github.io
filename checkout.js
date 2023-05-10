// Get the cart data from local storage
const storedCartData = localStorage.getItem('cartData');
const cart = storedCartData ? JSON.parse(storedCartData) : [];

// Populate the cart table
const cartTable = document.getElementById('cartTable');
let subtotal = 0;

cart.forEach(item => {
    const row = cartTable.insertRow();

    row.insertCell().textContent = item.title;
    row.insertCell().textContent = item.price;
    row.insertCell().textContent = item.quantity;
    row.insertCell().textContent = item.total;

    subtotal += item.total;
});

// Update the subtotal cell
document.getElementById('subtotal').textContent = subtotal.toFixed(2);

// Calculate and update the sales tax cell
const salesTaxRate = 0.07875;
const salesTax = subtotal * salesTaxRate;
document.getElementById('salesTax').textContent = salesTax.toFixed(2);

// Calculate and update the total cell
const total = subtotal + salesTax;
document.getElementById('total').textContent = total.toFixed(2);

// Handle checkout form submission
document.getElementById('checkoutForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = this.name.value;
    const email = this.email.value;
    const address = this.address.value;
    const cardNumber = this.cardNumber.value;
    const expDate = this.expDate.value;
    const cvv = this.cvv.value;

    // Perform validation and submit the form data
    // Replace this with actual form submission and validation logic
    alert(`Name: ${name}\nEmail: ${email}\nAddress: ${address}\nCard Number: ${cardNumber}\nExpiration Date: ${expDate}\nCVV: ${cvv}`); 

    // Clear the form
    this.reset();
});