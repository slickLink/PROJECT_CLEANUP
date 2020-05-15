//variables
let selected_tracks = [];

let spotify_green = "rgba(29, 185, 84, 0.3)";
let spotify_black = "rgba(20, 20, 20, 0.3)";
let clear_color = "rgba(255, 255, 255, 0.3)";

//select important DOM elements
const back_btn = document.querySelector(".back_btn");
const main_playlist_btn = document.querySelector(".main_playlist_btn");
const other_playlist_btn = document.querySelector(".other_playlist_btn");

const btn_move = document.querySelector(".btn_move");
const btn_delete = document.querySelector(".btn_delete");
const btn_cancel = document.querySelector(".btn_cancel");
const counter = document.querySelector(".counter");

const tracks = document.querySelectorAll(".content_item");

// add EventListeners to DOM elements
back_btn.addEventListener("click", back);
main_playlist_btn.addEventListener("click", selectMain);
other_playlist_btn.addEventListener("click", selectOther);

btn_move.addEventListener("click", moveTracks);
btn_delete.addEventListener("click", deleteTracks);
btn_cancel.addEventListener("click", cancelSelection);


for (i = 0; i < tracks.length; i++) {
    tracks[i].addEventListener("click", selectTrack);
}

// functions
function back() {
    window.location.replace('http://127.0.0.1:5000/home')
}

function selectMain() {

}

function selectOther() {
    alert("Sorry, the feature to switch to this playlist is coming soon");
}

function moveTracks() {
    alert("Sorry, the feature to move the selected tracks is coming soon");
}

function deleteTracks() {
    if (selected_tracks.length > 0 && selected_tracks.length <= 100) {
        // send selected tracks to server for deletion
        let tracks = []
        for (let i = 0; i < selected_tracks.length; i++) {
            let id = selected_tracks[i].children[0].textContent;
            tracks.push(id);
        }
        let data = {
            mode: "delete-tracks"
        };
        data.tracks = tracks;
        console.log(data.tracks)
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://127.0.0.1:5000/dash", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send(JSON.stringify(data));

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
              if(this.responseText === 'True') {
                  window.location.reload(true);
              }
              else {
                  alert("There was an error requesting spotify to delete the selected tracks");
              }
            }
        };
    } else if (selected_tracks.length > 100) {
        alert("A maximum of 100 songs can be deleted at once.");
    }
    else {
        alert("Select tracks to delete from playlist");
    }
}

function cancelSelection() {
    // reset selection if needed
    if (selected_tracks.length > 0) {
        for (i = 0; i < selected_tracks.length; i++) {
            selected_tracks[i].style.backgroundColor = clear_color;
        }
        selected_tracks = []
        this.style.backgroundColor = clear_color;
        counter.textContent = 0;
    }
}

function selectTrack() {
    // check if track is not already selected
    index_of_track = selected_tracks.indexOf(this);

    if (index_of_track == -1) {
        //add track to selection
        selected_tracks.push(this);
        //change element styling
        this.style.backgroundColor = spotify_green;
    } else {
        // remove track from selection
        selected_tracks.splice(index_of_track, 1);
        //change element styling
        this.style.backgroundColor = clear_color;
    }

    // update counter
    counter.textContent = selected_tracks.length;
    if (selected_tracks.length > 0) {
        btn_cancel.style.backgroundColor = spotify_green;
    }
    else {
        btn_cancel.style.backgroundColor = spotify_black;
    }
}
