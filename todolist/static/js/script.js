$(document).ready(function () {

    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    // $(document).ajaxError(function (event, request) {
    //     var message = null;
    //
    //     if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
    //         message = request.responseJSON.message;
    //     } else if (request.responseText) {
    //         var IS_JSON = true;
    //         try {
    //             var data = JSON.parse(request.responseText);
    //         } catch (err) {
    //             IS_JSON = false;
    //         }
    //
    //         if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
    //             message = JSON.parse(request.responseText).message;
    //         } else {
    //             message = default_error_message;
    //         }
    //     } else {
    //         message = default_error_message;
    //     }
    // });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    $(document).on('keyup', '#category-input', function (e) {
        var $input = $('#category-input');
        var $this = $(this);
        var value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }

        $.ajax({
            type: 'POST',
            url: $this.data('href'),
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('.categories').append(data.html);
            }
        })
    })

    $(document).on('keyup', '.comment-input', function (e) {
        // var $input = $('.comment-input');
        var $this = $(this);
        var $input = $this
        var value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $.ajax({
            type: 'POST',
            cache: false,
            url: $this.data('href'),
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $this.parent().parent().parent().parent().prev().prev().find('div').append(data.html);
            }
        })
    })


    $(document).on('click', '.finished-btn', function () {
        var $task = $(this).parent().parent().parent().parent();
        var $this = $(this);

        if ($task.data('is_finished')) {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    var $that = $this.parent().next().find('a');
                    $this.parent().prev().find('p').addClass('unfinished-task');
                    $this.parent().prev().find('p').removeClass('finished-task');
                    $task.data('is_finished', false);
                    $this.text("Unfinished");

                }
            })
        } else {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    // $this.next().removeClass('active-task');
                    // $this.next().addClass('inactive-task');
                    // $this.find('a').text('Unfinished');
                    $this.parent().prev().find('p').addClass('finished-task');
                    $this.parent().prev().find('p').removeClass('unfinished-task');
                    $task.data('is_finished', true);
                    $this.text("Finished");
                }
            })

        }
    });

    $(document).on('click', '.delete-btn', function () {
        var $task = $(this).parent().parent();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function (data) {
                $task.remove();
            }
        });
    });


    $(document).on('click', '#unfinished-task', function () {
        // var $this=$(this);
        // $this.addClass('active');
        var $tasks = $('.task');
        $tasks.show();
        $tasks.filter(function () {
            return $(this).data('is_finished');
        }).hide();
    });

    $(document).on('click', '#finished-task', function () {
        var $tasks = $('.task');

        $tasks.show();
        $tasks.filter(function () {
            return !$(this).data('is_finished');
        }).hide();
    });

    $(document).on('click', '#all-task', function () {
        var $tasks = $('.task');
        $tasks.show();
    })


});