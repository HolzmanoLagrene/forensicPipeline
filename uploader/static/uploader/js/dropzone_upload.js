var Upload = function (files) {
    this.files = files;
};

Upload.prototype.doUpload = function () {
    var that = this;
    var formData = new FormData();

    // add assoc key values, this will be posts values
    for (i = 0; i < that.files.length; i++) {
        formData.append(i, that.files[i]);
    }

    $.ajax({
        type: "POST",
        url: "upload",
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', that.progressHandling, false);
            }
            return myXhr;
        },
        success: function (data) {
            $.ajaxSetup({cache: false}); // This part addresses an IE bug.  without it, IE will only load the first number and will never refresh
            $('#file_list').load(' #file_list', function () {
                $(this).children().unwrap()
            })
        },
        error: function (error) {
            // handle error
        },
        async: true,
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 300000
    });
};
Upload.prototype.progressHandling = function (event) {
    var percent = 0;
    var position = event.loaded || event.position;
    var total = event.total;
    var progress_bar_id = "#progress-wrp";
    if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    // update progressbars classes so it fits your code
    $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
    $(progress_bar_id + " .status").text(percent + "%");
};

Upload.prototype.incrementalHash = function (event) {

    if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    // update progressbars classes so it fits your code
    $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
    $(progress_bar_id + " .status").text(percent + "%");
};

var dropZone = document.getElementById('drop-zone');
dropZone.ondrop = function (e) {
    e.preventDefault();
    this.className = 'upload-drop-zone';


    var upload = new Upload(e.dataTransfer.files);
    upload.doUpload();
}
dropZone.ondragover = function () {
    this.className = 'upload-drop-zone drop';
    return false;
}
dropZone.ondragleave = function () {
    this.className = 'upload-drop-zone';
    return false;
}