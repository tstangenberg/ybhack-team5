function loadDataTable(id, data) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            data: data,
	    "pageLength": 15,
	    "lengthChange": false,
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

window.onload = function(event) {
  onLoad(event);
  console.info('Javascript has been loaded ...');
}
