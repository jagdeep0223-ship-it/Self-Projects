function calculate(operation) {
    let a = parseFloat(document.getElementById("first_num").value);
    let b = parseFloat(document.getElementById("second_num").value);

    if (isNaN(a) || isNaN(b)) {
        document.getElementById("result").innerHTML = "Please enter valid numbers";
        return;
    }

    let result;

    switch (operation) {
        case "add":
            result = a + b;
            break;
        case "sub":
            result = a - b;
            break;
        case "mul":
            result = a * b;
            break;
        case "div":
            result = b === 0 ? "Cannot divide by zero!" : a / b;
            break;
        default:
            result = "Invalid operation";
    }

    document.getElementById("result").innerHTML = result;
}

// Existing hover color functions
function changeBgColor() {
    document.getElementById("box1").style.backgroundColor = "#F9F188";
}

function undoBgColor() {
    document.getElementById("box1").style.backgroundColor = "#69D147";
}

// Just your test function
let secondFunc = function() {
    console.log("This is my second function");
};
console.log("data type of second function is:", typeof secondFunc);
