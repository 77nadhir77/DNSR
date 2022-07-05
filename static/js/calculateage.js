$('#birthDate').change(function(){
    let yearOfBirth = new Date($(this).val()).getYear();
    let today = new Date().getYear()
    

    $('#calculateAge').val(today - yearOfBirth);
});