let patternData = [];

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_pattern')
        .then(response => response.json())
        .then(data => {
            patternData = data.pattern || [];
            renderPattern();
        });
    
    document.getElementById('recoil_mode').addEventListener('change', updateModeVisibility);
    
    document.getElementById('checkDefault').addEventListener('change', function() {
        updateSettings();
    });
    
    document.getElementById('delay').addEventListener('blur', function() {
        updateSettings();
    });
    
    updateModeVisibility();
});

function updateSettings() {
    const enabled = document.getElementById("checkDefault").checked;
    const mode = document.getElementById("recoil_mode").value;
    const delay = document.getElementById("delay").value;
    const x = document.getElementById("x_cont_val") ? document.getElementById("x_cont_val").value : 0;
    const y = document.getElementById("y_cont_val") ? document.getElementById("y_cont_val").value : 0;

    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mode: mode,
            enabled: enabled,
            x: x || 0,
            y: y || 0,
            delay: delay || 0.01
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Settings updated:", data);
    });
}

function updateModeVisibility() {
    const mode = document.getElementById('recoil_mode').value;
    const simpleSection = document.getElementById('simpleSection');
    const advancedSection = document.getElementById('advancedSection');
    
    if (mode === "Simple") {
        simpleSection.style.display = 'block';
        advancedSection.style.display = 'none';
    } else if (mode === "Advanced") {
        simpleSection.style.display = 'none';
        advancedSection.style.display = 'block';
    }
    
    updateSettings();
}

document.getElementById("applySimple").addEventListener("click", function () {
    const enabled = document.getElementById("checkDefault").checked;
    const delay = document.getElementById("delay").value;
    const x = document.getElementById("x_cont_val").value;
    const y = document.getElementById("y_cont_val").value;

    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mode: "Simple",
            enabled: enabled,
            x: x,
            y: y,
            delay: delay
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Simple settings updated:", data);
        alert("Simple recoil settings applied!");
    });
});

document.getElementById("applyAdvanced").addEventListener("click", function() {
    const enabled = document.getElementById("checkDefault").checked;
    const delay = document.getElementById("delay").value;

    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mode: "Advanced",
            enabled: enabled,
            x: 0,
            y: 0,
            delay: delay
        })
    })
    .then(response => response.json())
    .then(() => {
        return fetch("/update_pattern", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pattern_enabled: true,
                pattern: patternData
            })
        });
    })
    .then(response => response.json())
    .then(data => {
        console.log("Advanced pattern updated:", data);
        alert("Advanced pattern applied!");
    });
});

document.getElementById("addPattern").addEventListener("click", function() {
    const x = document.getElementById("newX").value;
    const y = document.getElementById("newY").value;

    if (x !== "" && y !== "") {
        patternData.push({ x: parseFloat(x), y: parseFloat(y) });
        document.getElementById("newX").value = "";
        document.getElementById("newY").value = "";
        renderPattern();
    }
});

function renderPattern() {
    const patternList = document.getElementById("patternList");
    patternList.innerHTML = "";

    if (patternData.length === 0) {
        return;
    }

    patternData.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "pattern-item";
        div.innerHTML = `
            <span class="pattern-item-text">Step ${index + 1}: X=${item.x}, Y=${item.y}</span>
            <button class="pattern-item-remove" onclick="removePattern(${index})">×</button>
        `;
        patternList.appendChild(div);
    });
}

function removePattern(index) {
    patternData.splice(index, 1);
    renderPattern();
}