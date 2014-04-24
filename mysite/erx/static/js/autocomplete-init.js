
function makeAutocomplete(sel) {
    sel.autocomplete('/erx/autocomplete-drug/', {
        delay: 200,
        formatItem: function(row) {
            return row[1];
        }
    });
}

$(function() {
    makeAutocomplete($('.autocomplete-me'));
})
