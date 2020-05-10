
//variables
let btn_1_bool = true;
let btn_2_bool = false;

let spotify_green = "rgba(29, 185, 84, 0.3)";
let spotify_black = "rgba(20, 20, 20, 0.3)";
let clear_color = "rgba(255, 255, 255, 0.3)";

let main_playlist = null;
let bin_playlist = null;

// get important document elements
const title = document.querySelector("#Header");
title.textContent = "Select a main playlist";

const playlist_items = document.querySelectorAll(".grid_item");

const btn_1 = document.querySelector(".btn_1");
const btn_2 = document.querySelector(".btn_2");
const next_btn = document.querySelector(".btn_next");

//add Eventlisteners
for (let i = 0; i < playlist_items.length; i++) {
    playlist_items[i].addEventListener("click", selectItem);
}
btn_1.addEventListener("click", toggleBtn_knob_1);
btn_2.addEventListener("click", toggleBtn_knob_2);
next_btn.addEventListener("click", nextPage);

//functions

function selectItem() {
    if (btn_1_bool) {
        // set clicked item to green and previous green item to clear
        if(main_playlist === null){
            // if main playlist is empty
            main_playlist = this;
            this.children[0].style.backgroundColor = spotify_green;
        }
        else if (main_playlist !== this) {
            // if switching main playlist
            this.children[0].style.backgroundColor = spotify_green;
            main_playlist.children[0].style.backgroundColor = clear_color;
            main_playlist = this;
        }
        // if newly selected item was already the bin playlist
        if (main_playlist === bin_playlist){
            // clear the bin playlist
            bin_playlist = null;
        }
    }
    else if (btn_2_bool) {
        // set clicked item to black and previous item to clear
        if(bin_playlist === null){
            // if main playlist is empty
            bin_playlist = this;
            this.children[0].style.backgroundColor = spotify_black;
        }
        else if (bin_playlist !== this) {
            // if switching main playlist
            this.children[0].style.backgroundColor = spotify_black;
            bin_playlist.children[0].style.backgroundColor = clear_color;
            bin_playlist = this;
        }
        // if newly selected item was already the main playlist
        if (main_playlist === bin_playlist){
            // clear the main playlist
            main_playlist = null;
        }
    }
}

function toggleBtn_knob_1() {
    title.textContent = "Select a main playlist";
    if(!btn_1_bool){
        // if main playlist is not toggled, toggle it
        btn_1_bool = true;
        btn_2_bool = false;

        btn_1.style.border = "solid 3px";
        btn_2.style.border = "none";
    }
}

function toggleBtn_knob_2(){
    title.textContent = "Select a other playlist";
    if(!btn_2_bool) {
        // if bin playlist is not toggled, toggle it
        btn_2_bool = true;
        btn_1_bool = false;

        btn_2.style.border = "solid 3px";
        btn_1.style.border = "none";
    }
}

function nextPage() {
    // check to see if user selected both playlists
    if(main_playlist === null || bin_playlist === null) {
        alert("Please select both main and bin playlists to continue!");
    }
    
    // code to send info back to server
}