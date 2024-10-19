

    $(document).ready(function() {
        $('#submitCategory').on('click', function() {
            // Get form data
            var categoryName = $('#name').val();

            // Make the POST request to add the category
            $.ajax({
                url: "{{ url_for('core.add_category') }}",
                method: 'POST',
                data: {
                    name: categoryName,
                    csrf_token: "{{ form.csrf_token._value() }}"
                },
                success: function(response) {
                    if (response.success) {
                        $('#successAlert').text(response.message).removeClass('d-none');
                        $('#errorAlert').addClass('d-none');
                        $('#name').val('');  // Clear form field

                        // Close the modal after a brief delay to show the success message
                        setTimeout(function() {
                            $('#categoryModal').modal('hide');
                        }, 1000);

                        // Refresh the page once the modal is fully hidden
                        $('#categoryModal').on('hidden.bs.modal', function () {
                            location.reload();
                        });
                    } else {
                        $('#errorAlert').text(response.message).removeClass('d-none');
                        $('#successAlert').addClass('d-none');
                    }
                },
                error: function() {
                    $('#errorAlert').text('An error occurred while adding the category.').removeClass('d-none');
                    $('#successAlert').addClass('d-none');
                }
            });
        });
    });
