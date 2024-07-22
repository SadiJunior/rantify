/**
 * This file contains JavaScript functions for the Rantify application.
 */


// Runs after DOM is fully loaded.
$(document).ready(
    function() {
        onRateButtonClicked();
        onRoastButtonClicked();
        onRhymeButtonClicked();
    }
);


// Runs when Rate Button is clicked
function onRateButtonClicked() {
    onRantButtonClicked("#rate-button", "/rant/rate");
}


// Runs when Rate Button is clicked
function onRoastButtonClicked() {
    onRantButtonClicked("#roast-button", "/rant/roast");
}


// Runs when Rhyme Button is clicked
function onRhymeButtonClicked() {
    onRantButtonClicked("#rhyme-button", "/rant/rhyme");
}


// Runs when Rant Button is clicked
function onRantButtonClicked(buttonId, url) {
    $(buttonId).click(function(eventObject) {

        if (!$("#playlist-select").val()) {
            displayRantError("You must select a playlist.");
            return;
        }

        disableRantButtons();

        // Submits the rant data via jQuery AJAX.
        $.ajax({
            url: url,
            method: "POST",
            data: $("#rant-form").serialize(),
            beforeSend: function() {
                displayLoadingDots();
            },
            success: (data, textStatus, jqXHR) => {
                removeLoadingDots();
                displayRant(data);
                enableRantButtons();
            },
            error: (jqXHR, textStatus, errorThrown) => {
                removeLoadingDots();
                displayRantError("Failed to submit rant. Please try again.");
                enableRantButtons();
            },
            statusCode: {
                401: () => {
                    redirect("/auth/login");
                }
            }
        });
    });
}

// Displays the rant in index page via jQuery.
function displayRant(rantContent) {
    $("#rant-display").html(rantContent);
    removeRantError();
}


// Displays the rant errpr in index page via jQuery.
function displayRantError(errorMessage) {
    $("#rant-error").html(errorMessage);
    $("#rant-display").empty();
}


// Removes the rant errpr in index page via jQuery.
function removeRantError() {
    $("#rant-error").empty();
}


// Disables all rant buttons via jQuery.
function disableRantButtons() {
    $(".rant-button").prop("disabled", true);
}

// Enables all rant buttons via jQuery.
function enableRantButtons() {
    $(".rant-button").prop("disabled", false);
}


// Displays the loading dots in index page via jQuery.
function displayLoadingDots() {
    const loadingDotsHtml = `
        <div class="d-flex justify-content-center align-items-center h-100">
            <div class="loading-dots"></div>
        </div>
    `;

    $("#rant-display").html(loadingDotsHtml);
}


// Removes the loading dots in index page via jQuery.
function removeLoadingDots() {
    $(".loading-dots").remove();
}


// Redirects to the given URL.
function redirect(url) {
    window.location.href = url;
}
