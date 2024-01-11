function showDataLoading(){
    let tBody = document.getElementById("tableId");
    tBody.innerHTML = '<h1>Loading...................</h1>'
}

function showDataLoading2(){
    let tBody = document.getElementById("completedTableId");
    tBody.innerHTML = '<h1>Loading...................</h1>'
}

function showPreLoader(){
    let preloader = document.getElementById("preloader");
    preloader.style.display = 'block'
}


function hidePreLoader(){
    let preloader = document.getElementById("preloader");
    preloader.style.display = 'none'
}



// Getting the Todo by Id
function GetTodoById(event, todoId, type='edit'){
    event.preventDefault();

    
    $.ajax({
        type: 'GET',
        url: `/get/${todoId}/`,
        dataType: 'html',
        success: function (result) {
            $('#editTodoFormId').html(result);
            if(type === 'view'){
                document.getElementById("interactId").style.display = 'none' 
                $('#titleId').prop('readonly', true);
                $('#contentId').prop('readonly', true);
                document.getElementById('exampleModalLabelId').textContent = 'View Todo'
            }
            $('#editTodoModal').modal('show');
            

        },
        error: function(error){
            console.log(error)
        }
    })
}



// Getting the Completed Todo Details by Id
function GetCompletedTodoDetailsById(event, todoId){
    event.preventDefault();

    
    $.ajax({
        type: 'GET',
        url: `/get/${todoId}/`,
        dataType: 'html',
        success: function (result) {
            console.log(result)
            $('#viewCompletedTodoFormId').html(result);
            $('#titleId').prop('readonly', true);
            $('#contentId').prop('readonly', true);
            document.getElementById("interactId").style.display = 'none' 
            document.getElementById('exampleModalLabelId').textContent = 'View Todo'
            
            $('#editTodoModal').modal('show');
            

        },
        error: function(error){
            console.log(error)
        }
    })
}



// Getting the Updated Values
function CompleteTodo(event, todoId){
    event.preventDefault();
    showPreLoader()

    let obj = {
        id: todoId
    }
    
    $.ajax({
        type: 'POST',
        url: '/complete',
        dataType: 'html',
        data: JSON.stringify(obj),
        success: function (result) {
            $('#tableId').html(result);
            // $('#completedBtnId').tooltip({disabled: true})
            $("#completedBtnId").tooltip("disable");
            hidePreLoader()
            Swal.fire({
                position: "center",
                icon: "success",
                title: "Congratulations!!!",
                text: `"You Successfully Completed your Todo Task`,
                showConfirmButton: false,
                timer: 2500
              });


            $.ajax({
                type: 'GET',
                url: '/updated-values/',
                dataType: 'json',
                success: function (result) {
                    document.getElementById("completedTodosId").textContent = result.completedTodosAmount
                    document.getElementById("pendingTodosId").textContent = result.pendingTodosAmount
                    document.getElementById("totalTodosId").textContent = result.totalTodosAmount
                    document.getElementById("completionRateId").textContent = result.completionRate+'%'
                },
                error: function(error){
                    console.log(error)
                }
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}




// Data Intreactions Starts
function CreateTodo(event){
    event.preventDefault();
    showPreLoader()

    let title = $('#title').val()
    let content = $('#content').val()
    const token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 

    let obj = {
        title: title,
        content: content,        
    }
    
    $.ajax({
        type: 'POST',
        url: '/create',
        dataType: 'html',
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': token 
       },
        success: function (result) {
            document.getElementById('title').value = ''
            document.getElementById('content').value = ''
            $('#tableId').html(result);            
            $('#todoModal').modal('hide');
            $('.modal-backdrop').remove();
            hidePreLoader();
            Swal.fire({
                position: "center",
                icon: "success",
                title: "Congratulations!!!",
                text: `"You have Successfully Created a new Todo`,
                showConfirmButton: false,
                timer: 2500
              });

            $.ajax({
                type: 'GET',
                url: '/updated-values/',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': token 
               },
                success: function (result) {
                    document.getElementById("completedTodosId").textContent = result.completedTodosAmount
                    document.getElementById("pendingTodosId").textContent = result.pendingTodosAmount
                    document.getElementById("totalTodosId").textContent = result.totalTodosAmount
                    document.getElementById("completionRateId").textContent = result.completionRate+'%'
                },
                error: function(error){
                    console.log(error)
                }
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}




// Update The Todo in the Database
function UpdateTodo(event, id){
    event.preventDefault();
    showPreLoader()

    let title = $('#titleId').val()
    let content = $('#contentId').val()
    const token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 

    let obj = {
        title: title,
        content: content,        
    }
    
    $.ajax({
        type: 'PUT',
        url: `/edit/${id}`,
        dataType: 'html',
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': token
       },
        success: function (result) {
            document.getElementById('title').value = ''
            document.getElementById('content').value = ''
            $('#tableId').html(result);
            $('#editTodoModal').modal('hide');
            $('.modal-backdrop').remove();
            hidePreLoader();
            Swal.fire({
                position: "center",
                icon: "success",
                title: "Todo Updated Successfully!!!",
                text: `"You have Successfully Updated the Todo`,
                showConfirmButton: false,
                timer: 2500
              });

            $.ajax({
                type: 'GET',
                url: '/updated-values/',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': token
               },
                success: function (result) {
                    document.getElementById("completedTodosId").textContent = result.completedTodosAmount
                    document.getElementById("pendingTodosId").textContent = result.pendingTodosAmount
                    document.getElementById("totalTodosId").textContent = result.totalTodosAmount
                    document.getElementById("completionRateId").textContent = result.completionRate+'%'
                },
                error: function(error){
                    console.log(error)
                }
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}




function DeleteTodo(event, id){
    event.preventDefault();

    Swal.fire({
        title: "Are you sure you want to delete this todo?",
        text: "Note that You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
      }).then((result) => {
        if (result.isConfirmed) {  
            showPreLoader()      
            const token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 

            $.ajax({
                type: 'DELETE',
                url: `/delete/${id}`,
                dataType: 'html',
                headers: {
                    'X-CSRFToken': token 
               },
                success: function (result) {
                    $('#tableId').html(result);
                    $('#todoModal').modal('hide');
                    $('.modal-backdrop').remove();
                    hidePreLoader();

                    Swal.fire({
                        position: "center",
                        icon: "success",
                        title: "Todo Deleted Successfully!!!",
                        text: `"You have Successfully Delete a Todo`,
                        showConfirmButton: false,
                        timer: 2500
                      });
                      
                    $.ajax({
                        type: 'GET',
                        url: '/updated-values/',
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': token 
                       },
                        success: function (result) {
                            document.getElementById("completedTodosId").textContent = result.completedTodosAmount
                            document.getElementById("pendingTodosId").textContent = result.pendingTodosAmount
                            document.getElementById("totalTodosId").textContent = result.totalTodosAmount
                            document.getElementById("completionRateId").textContent = result.completionRate+'%'
                        },
                        error: function(error){
                            console.log(error)
                        }
                    })
                },
                error: function(error){
                    console.log(error)
                }
            })
        }
      });


    
   
}


function SearchTodo(event, condition){
    event.preventDefault();

    debugger
    let searchText = $('#searchId').val();
    let completionSearchId = $('#completionSearchId').val();
    if (completionSearchId){
        condition = 'completed'
    }

    // condition === 'pending' ? showDataLoading() : showDataLoading2()
       
    $.ajax({
        type: 'GET',
        url: `/get/search/${condition}/${searchText}/`,
        dataType: 'html',
        success: function (result) {
            debugger
            console.log(result)
            $('#tableId').html(result);
        },
        error: function(error){
            console.log(error)
        }
    })

}


function ResetData(){
    let searchText = $('#searchId').val();
    if(searchText.length == 0){
        $.ajax({
            type: 'GET',
            url: `/pending-todos/`,
            dataType: 'html',
            success: function (result) {
                $('#tableId').html(result);
            },
            error: function(error){
                console.log(error)
            }
        })
    }
}



