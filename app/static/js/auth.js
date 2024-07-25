/**
 * This file contains JavaScript functions for the Rantify auth.
 */


// Runs after DOM is fully loaded.
$(document).ready(
    function() {
        onLoginButtonClicked();
    }
);


// Runs when Log in Button is clicked
function onLoginButtonClicked() {
    $("#login-button").click(function(eventObject) {
        displayLoadingDots();
    });}


// Displays the loading dots in index page via jQuery.
function displayLoadingDots() {
    const loadingDotsHtml = `
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;

    $("#loading").html(loadingDotsHtml);
}


// Removes the loading dots in index page via jQuery.
function removeLoadingDots() {
    $(".loading-dots").remove();
}
