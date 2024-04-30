$(document).ready(function() {
    //Script to upload an element
    $("#addForm").submit(function(event) {
        event.preventDefault() //Prevent the form from submitting normally
  
        $.post("/add_element_values.html", {
            'elementnumber': $('input[name=elementnumber]').val(),
            'elementcode': $('input[name=elementcode]').val(),
            'elementname': $('input[name=elementname]').val(),
            'colour1': $('input[name=colour1]').val(),
            'colour2': $('input[name=colour2]').val(),
            'colour3': $('input[name=colour3]').val(),
            'radius': $('input[name=radius]').val()
        },
        function(data) {
            alert(data)
        })

        $(this).get(0).reset() //Clear input fields
    })
  
    //Script to delete an element
    $("#deleteForm").submit(function(event) {
        event.preventDefault() //Prevent the form from submitting normally
        $.post("/delete_element_values.html", {
            'elementToDelete': $('input[name=elementToDelete]').val()
        },
        function(data) {
            alert(data)
        })

        $(this).get(0).reset() //Clear input fields
    })

    //Script to upload an SDF file
    $("#uploadForm").submit(function(event) {
        event.preventDefault() //Prevent the form from submitting normally
        // Create a new FormData object
        var formData = new FormData()

        // Add the file to the form data object
        formData.append('file', $('#file')[0].files[0])
        formData.append('moleculeName', $('input[name=moleculeName]').val())
   
        // Send the form data object using AJAX
        $.ajax({
            url: '/upload_sdf_file.html',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                alert(data)
            },
            error: function(xhr, status, error) {
                console.log(error)
            }
        })

        $(this).get(0).reset() //Clear input fields
    })
})