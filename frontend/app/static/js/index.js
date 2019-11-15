function loadDataTable(id, data) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            data: data,
            "order": [[ 4, "desc" ]],
            "pageLength": 15,
            columns: [
                { title: "Spieler" },
                { title: "Follower" },
                { title: "Posts" },
                { title: "Tweets" },
                { title: "Fame" } ]
        } );
    } );
}

function onLoad(event) {
  console.info('Javascript has been loaded ...');
}

