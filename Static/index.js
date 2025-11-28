let patternData = [];

const get = id => document.getElementById(id);

// ----------- SAVE PATTERN -----------
get("savePattern").addEventListener("click", () => {
    const name = get("patternName").value || "default";

    fetch("/save_pattern", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    })
    .then(r => r.json())
    .then(data => alert(`Pattern "${data.saved_pattern}" saved!`));
});

// ----------- LOAD PATTERN -----------
get("loadPattern").addEventListener("click", () => {
    const name = get("patternName").value || "default";

    fetch("/load_pattern", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status !== "success")
            return alert(data.message);

        patternData = data.pattern;
        renderPattern();
        alert(`Pattern "${name}" loaded!`);
    });
});

// ----------- INITIALIZE PAGE -----------
document.addEventListener("DOMContentLoaded", () => {
    fetch("/get_pattern")
        .then(r => r.json())
        .then(data => {
            patternData = data.pattern || [];
            renderPattern();
        });

    get("recoil_mode").addEventListener("change", updateModeVisibility);
    get("checkDefault").addEventListener("change", updateSettings);
    get("delay").addEventListener("blur", updateSettings);

    updateModeVisibility();
});

// ----------- UPDATE SETTINGS -----------
function updateSettings() {
    const enabled = get("checkDefault").checked;

    fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mode: get("recoil_mode").value,
            enabled,
            x: get("x_cont_val")?.value || 0,
            y: get("y_cont_val")?.value || 0,
            delay: get("delay").value || 0.01
        })
    })
    .then(r => r.json())
    .then(data => console.log("Settings updated:", data));
}

// ----------- MODE VISIBILITY -----------
function updateModeVisibility() {
    const mode = get("recoil_mode").value;

    get("simpleSection").style.display = mode === "Simple" ? "block" : "none";
    get("advancedSection").style.display = mode === "Advanced" ? "block" : "none";

    updateSettings();
}

// ----------- APPLY SIMPLE -----------
get("applySimple").addEventListener("click", () => {
    fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mode: "Simple",
            enabled: get("checkDefault").checked,
            x: get("x_cont_val").value,
            y: get("y_cont_val").value,
            delay: get("delay").value
        })
    })
    .then(r => r.json())
    .then(data => {
        console.log("Simple settings updated:", data);
        alert("Simple recoil settings applied!");
    });
});

// ----------- APPLY ADVANCED -----------
get("applyAdvanced").addEventListener("click", () => {
    const enabled = get("checkDefault").checked;

    fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mode: "Advanced",
            enabled,
            x: 0,
            y: 0,
            delay: get("delay").value
        })
    })
    .then(() => fetch("/update_pattern", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pattern_enabled: true, pattern: patternData })
    }))
    .then(r => r.json())
    .then(data => {
        console.log("Advanced pattern updated:", data);
        alert("Advanced pattern applied!");
    });
});

// ----------- ADD PATTERN STEP -----------
get("addPattern").addEventListener("click", () => {
    const x = get("newX").value;
    const y = get("newY").value;

    if (!x || !y) return;

    patternData.push({ x: parseFloat(x), y: parseFloat(y) });

    get("newX").value = "";
    get("newY").value = "";

    renderPattern();
});

// ----------- RENDER PATTERN LIST -----------
function renderPattern() {
    const list = get("patternList");
    list.innerHTML = "";

    patternData.forEach((item, i) => {
        const div = document.createElement("div");
        div.className = "pattern-item d-flex align-items-center mb-1";

        div.innerHTML = `
            <span class="me-2">Step ${i + 1}:</span>
            <input type="number" class="form-control form-control-sm mx-1 pattern-x custom-input" value="${item.x}" style="width: 70px;">
            <input type="number" class="form-control form-control-sm mx-1 pattern-y custom-input" value="${item.y}" style="width: 70px;">
            <button class="btn btn-sm btn-danger">×</button>
        `;

        const xInput = div.querySelector(".pattern-x");
        const yInput = div.querySelector(".pattern-y");
        const deleteBtn = div.querySelector("button");

        xInput.addEventListener("input", () => item.x = parseFloat(xInput.value) || 0);
        yInput.addEventListener("input", () => item.y = parseFloat(yInput.value) || 0);
        deleteBtn.addEventListener("click", () => removePattern(i));

        list.appendChild(div);
    });
}

// ----------- REMOVE PATTERN STEP -----------
function removePattern(i) {
    patternData.splice(i, 1);
    renderPattern();
}
