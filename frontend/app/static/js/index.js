function loadDataTable(id, data) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            data: data,
            "order": [[ 3, "desc" ]],
            "pageLength": 15,
            columns: [
                { title: "Spieler" },
                { title: "Follower" },
                { title: "Posts" },
                { title: "Fame" } ]
        } );
    } );
}

function onLoad(event) {
  console.info('Javascript has been loaded ...');
}

