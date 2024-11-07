// Ensure compatibility with HTML elements and initiate requests for comparison animations.

function loadComparisonAnimation() {
    // Fetch user inputs
    const initialization1 = document.getElementById("initialization_1").value;
    const initialization2 = document.getElementById("initialization_2").value;
    const feature = document.getElementById("feature").value;
    const block = document.getElementById("block").value;
    const mode = document.getElementById("mode").value;
    const epochOrBatch = document.getElementById("epoch_or_batch").value;
    const layer = document.getElementById("transformer_layer").value;
    // Validate user input
    if (!initialization1 || !initialization2 || !feature || !block || !mode || (!epochOrBatch && mode === "single_epoch") || !layer) {
        alert("Please select all required options.");
        return;
    }
    
    // Prepare query parameters
    const queryParams = new URLSearchParams({
        initialization1: initialization1,
        initialization2: initialization2,
        feature: feature,
        block: block,
        mode: mode,
        epoch_or_batch: epochOrBatch,
        layer: layer 
    });
    console.log(queryParams)
    
    // Construct the URL for the API call
    const url = `/get_comparison_animation?${queryParams.toString()}`;
    
    // Make an asynchronous request to fetch the comparison animations
    fetch(url)
    .then(response => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then(data => {
        // Display animations in designated elements

            document.getElementById("animation_1").src = data.animation_url_1;
            document.getElementById("animation_2").src = data.animation_url_2;
        })
        .catch(error => {
            console.error("Error loading comparison animations:", error);
            alert("There was an error loading the comparison animations. Please try again.");
        });
}
