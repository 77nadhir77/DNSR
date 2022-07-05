$("#hamburger").click(function(){
    $("#sidebar").toggleClass("opensidebar sidebar");
    $('#hamburger').toggleClass("hamburger nothamburger");
    });
    
    
    $('li').click(function(){
    $(this).find('ul').stop().slideToggle(500);
    $(this).find('#sahm').toggleClass("sahm sahm1");
    });