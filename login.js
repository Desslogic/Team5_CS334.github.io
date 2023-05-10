document.addEventListener("DOMContentLoaded", () => {
  let isAuthenticated = false;

  const loginForm = document.getElementById("login-form");
  const editProductsButton = document.getElementById("edit_products");
  const logOutButton = document.getElementById("logout");
  const reportsButton = document.getElementById("sales_reports");

  // Add a "Forgot Password" link after the password input
  const forgotPasswordLink = document.createElement("a");
  forgotPasswordLink.href = "#";
  forgotPasswordLink.textContent = "Forgot Password?";
  document.querySelector(".overlap-group4").appendChild(forgotPasswordLink);

  const submitButton = document.querySelector("#submit");

  submitButton.addEventListener("click", (event) => {
    event.preventDefault();
    loginForm.dispatchEvent(new Event("submit"));
  });

  function validateEmail(email) {
    const re = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    return re.test(email);
  }

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const managerId = event.target["manager-id"].value;
    const password = event.target["password"].value;

    if (!validateEmail(managerId)) {
      isAuthenticated = false;
      alert("Invalid email address.");
      return;
    }

    // Dummy user for demonstration purposes
    const user = {
      email: "skyler.landess@gmail.com",
      password: "password123",
    };

    if (managerId === user.email && password === user.password) {
      isAuthenticated = true;
      alert("Access granted. Select the Edit Products or Reports.");
    } else {
      isAuthenticated = false;
      alert("Access denied. Incorrect email or password.");
    }
  });

  function redirectTo(url) {
    if (isAuthenticated) {
      window.location.href = url;
    } else {
      alert("Please log in to access this feature.");
    }
  }

  editProductsButton.addEventListener("click", (event) => {
    event.preventDefault();
    redirectTo("editProducts.html");
  });
  reportsButton.addEventListener("click", (event) => {
    event.preventDefault();
    redirectTo("salesReports.html");
  });

  logOutButton.addEventListener("click", () => {
    isAuthenticated = false;
    alert("You have been logged out.");
  });

  // Add event listener for forgotPasswordLink
  forgotPasswordLink.addEventListener("click", (event) => {
    event.preventDefault();
    alert("We are sending an email to the provided address assisting you with a password change.");
  });
});