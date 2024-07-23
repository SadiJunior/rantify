/**
 * This file contains JavaScript functions for the Rantify application.
 */


// Runs after DOM is fully loaded.
$(document).ready(
    function() {
        addEventOnRateButtonClicked();
        addEventOnRoastButtonClicked();
        addEventOnRhymeButtonClicked();
        addEventOnSelectPlaylistChanged();
    }
);


// Adds an event listener to the click of Rant Button
function addEventOnRateButtonClicked() {
    addEventOnRantButtonClicked("#rate-button", "/rant/rate");
}


// Adds an event listener to the click of Roast Button
function addEventOnRoastButtonClicked() {
    addEventOnRantButtonClicked("#roast-button", "/rant/roast");
}


// Adds an event listener to the click of Rhyme Button
function addEventOnRhymeButtonClicked() {
    addEventOnRantButtonClicked("#rhyme-button", "/rant/rhyme");
}


// Adds an event listener to the change of Select Playlist dropdown
function addEventOnSelectPlaylistChanged() {
    const playlistSelect = $("#playlist-select");
    const playlistLink = $("#playlist-link");

    const baseSpotifyUrl = "https://open.spotify.com/";

    playlistSelect.change(function() {
        const selectedPlaylistId = playlistSelect.val();

        if (selectedPlaylistId) {
            const playlistUrl = baseSpotifyUrl + "playlist/" + selectedPlaylistId;

            playlistLink.attr("href", playlistUrl);
        }
        else {
            playlistLink.attr("href", baseSpotifyUrl);
        }
    });
}


// Adds an event listener to the click of a Rant Button
function addEventOnRantButtonClicked(buttonId, url) {
    $(buttonId).click(function() {

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
