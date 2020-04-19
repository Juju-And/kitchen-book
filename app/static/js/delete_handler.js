function delete_handler(el) {
    var url = $('#delete-button').attr("data-url")
    return fetch(url, {
        method: 'delete'
    })
    .then(() => window.location.replace("/products"));

}
