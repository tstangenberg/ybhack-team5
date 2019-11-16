function loadDataTable(id) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            //data: data,
            "stateSave": true,
	    "lengthChange": false,
            "order": [[ 2, "desc" ]],
            "pageLength": 15//,
            //columns: [
            //    { title: "Spieler" },
            //    { title: "Follower" },
            //    { title: "Posts" },
            //    { title: "Tweets" },
            //    { title: "Fame" } ]
        } );
    } );
}
