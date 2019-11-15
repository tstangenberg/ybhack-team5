function loadDataTable(id, data) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            data: data,
            "pageLength": 15,
            columns: [
                { title: "Namespace" },
                { title: "Creation" },
                { title: "Admin" },
                { title: "AD group" },
                { title: "Size" },
                { title: "State" },
                { title: "PullSecret" } ]
        } );
    } );
}

function onLoad(event) {
  console.info('Javascript has been loaded ...');
}

