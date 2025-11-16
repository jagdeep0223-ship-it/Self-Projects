function validation() {
  let userName = document.getElementById("user_name");
  let password = document.getElementById("user_pwd");
  let errorBox = document.getElementById("error_msg_container");
  let errors = [];

  // Username validation
  let usernameRegex = /^[A-Za-z]{3,50}$/;

  if (userName.value.trim() === "") {
    errors.push("User name is mandatory!");
    userName.style.border = "2px solid red";
  } else if (!usernameRegex.test(userName.value.trim())) {
    errors.push("Username must be 3-50 alphabetic characters only!");
    userName.style.border = "2px solid red";
  } else {
    userName.style.border = "1px solid #000";
  }

  // Password validation
  let passwordRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{6,30}$/;

  if (password.value.trim() === "") {
    errors.push("Password is mandatory!");
    password.style.border = "2px solid red";
  } else if (!passwordRegex.test(password.value.trim())) {
    errors.push(
      "Password must be 6-30 characters and include at least 1 letter, 1 digit, and 1 special character!"
    );
    password.style.border = "2px solid red";
  } else {
    password.style.border = "1px solid #000";
  }

  // Display errors
  if (errors.length > 0) {
    errorBox.innerHTML = errors.join("<br/>");
    errorBox.style.display = "block";
  } else {
    errorBox.style.display = "none";
  }
}
