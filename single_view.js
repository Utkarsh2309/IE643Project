function loadSingleAnimation() {
    const data = {
        initialization: document.getElementById("initialization").value,
        feature: document.getElementById("feature").value,
        block: document.getElementById("block").value,
        epoch_or_batch: document.getElementById("epoch_or_batch").value,
        mode: document.getElementById("mode").value,
        layer: document.getElementById("transformer_layer").value


    };

    fetch("/get_single_animation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("singleAnimation").src = data.animation_url;
    });
}
