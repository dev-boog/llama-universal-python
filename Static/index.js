document.querySelector(".btn-success").addEventListener("click", function () {
    const enabled = document.getElementById("checkDefault").checked;
    const x = document.getElementById("x_cont_val").value;
    const y = document.getElementById("y_cont_val").value;
    const delay = document.getElementById("delay").value;

    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            enabled: enabled,
            x: x,
            y: y,
            delay: delay
        })
    })
    .then(response => response.json())
});
