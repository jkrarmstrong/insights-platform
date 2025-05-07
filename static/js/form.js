document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the selected analysis type from localStorage
    var analysisType = localStorage.getItem('selectedAnalysisType');
    
    // If a value exists in localStorage, set the dropdown value to the stored selection
    if (analysisType) {
        document.getElementById('analysis-dropdown').value = analysisType;
    }
});

// When the user changes the selection in the dropdown, save the selected value in localStorage
document.getElementById('analysis-dropdown').addEventListener('change', function() {
    // Get the selected value from the dropdown
    var selectedType = this.value;
    
    // Store the selected value in localStorage so it can be remembered later
    localStorage.setItem('selectedAnalysisType', selectedType);
});
