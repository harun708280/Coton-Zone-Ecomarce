function filterSelection(category) {
    var elements = document.getElementsByClassName("mix");
    if (category == "all") {
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        }
    } else {
        for (var i = 0; i < elements.length; i++) {
            if (elements[i].classList.contains(category)) {
                elements[i].style.display = "block";
            } else {
                elements[i].style.display = "none";
            }
        }
    }
}
// This JavaScript function will handle the filtering based on user clicks
function filterSelection(cetagory) {
    var elements = document.getElementsByClassName("filter__controls")[0].getElementsByTagName("li");
    // Loop through each filter control
    for (var i = 0; i < elements.length; i++) {
        // Remove the "active" class from all filter controls
        elements[i].classList.remove("active");
    }
    // Add the "active" class to the clicked filter control
    event.currentTarget.classList.add("active");
    // Call the filterSelection function with the selected category
    // Note: You may need to implement this function based on your specific requirements
    // For demonstration purposes, I've assumed you have a function named filterSelection
    // that handles the filtering logic
    filterSelection(cetagory);
}
