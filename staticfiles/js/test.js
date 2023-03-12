$(document).ready(function() {
    $('#id_marque').change(function() {
        var marque_id = $(this).val();
        $.ajax({
            url: '/models/' +  marque_id,
            success: function(data) {
                var options = '<option value="">---------</option>';
                $.each(data, function(index, models) {
                    options += '<option value="' + models.id + '">' + models.name + '</option>';
                });
                $('#id_models').html(options);
            }
        });
    });
});
