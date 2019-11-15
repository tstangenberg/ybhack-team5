function loadDataTable(id, data) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            data: data,
            "pageLength": 15,
            columns: [
                { title: "Spiele" },
                { title: "Marktwert" },
                { title: "Follower" },
                { title: "Fame" } ]
        } );
    } );
}

function onLoad(event) {
  console.info('Javascript has been loaded ...');
}

