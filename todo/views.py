from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db.models import Q
import json

from utilities.EmailNotification import EmailNotify
from utilities.EncryptData import Encrypt
from .models import List
from django.views.decorators.csrf import csrf_exempt


base_url = 'http://127.0.0.1:8000/'



# Create your views here.
def registration(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            email = body['email']
            password = body['password']
            username = email.split('@')[0]
            
            user = User(email = email, username=username)
            user.set_password(password)
            user.save()
            
            return JsonResponse({"Message": "Success", "Status": "200"})
        except Exception as ex:
            print(ex)
            
            


def sendMail(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            receiver = body['receiver']
            checkReceiver = User.objects.filter(email=receiver).first()
            # checkReceiver.set_password("00000")
            # checkReceiver.save()
            
            if not checkReceiver:
                return JsonResponse({"Message": "Account with this Email does not exist", "Status": "404"})
            
            subject = 'Reset Password!!!'            
            encMessage = Encrypt(receiver)
            url = base_url+"reset-password/"+str(encMessage)
            body = 'Reset the Password of your Acount by clicking on this link; \n'+url
            
            result = EmailNotify(receiver, subject, body)
            if result:
                return JsonResponse({"Message": "Email sent Successlly", "Status": "200"})
            
        except Exception as ex:
            print(ex)
        
        
        
        
        
def reset(request, url):
    if request.method == 'GET':
        return render(request, 'resetPassword.html')
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            email = body['email']
            password = body['password']
            username = email.split('@')[0]
            
            user = User.objects.filter(email = email).first()
            user.set_password(password)
            user.save()
            
            return JsonResponse({"Message": "Password Reset Successul", "Status": "200"})
        except Exception as ex:
            print(ex)
        return redirect('authentication')
            




def authentication(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            email = body['email']
            password = body['password']
            
            user = User.objects.filter(email=email).first()
            if user is not None:
                isAuthenticated = user.check_password(password)
                if isAuthenticated: 
                    login(request, user)
                    return JsonResponse({"message": "Success", "status":"200"})  
                
                return JsonResponse({"message": "Invalid Credentials", "status":"404"})             
            else:
                return JsonResponse({"message": "User not Found", "status":"404"})
        except Exception as ex:
            print(ex)
         
    return render(request, 'authentication.html')




@login_required()
def home(request):
    if request.method == 'GET':
        try:
            userId = request.user.id
            todoLists = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).order_by('-dateCreated')[:5]
            pendingTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).count()
            completedTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=True).count()
            totalTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False).count()
            
            if totalTodosAmount == 0:
                completionRate = 0
            else:
                completionRate = (completedTodosAmount / totalTodosAmount) * 100
            
            context = {
                "todos": todoLists,
                "pendingTodosAmount": pendingTodosAmount,
                "completedTodosAmount": completedTodosAmount,
                "totalTodosAmount": totalTodosAmount,
                "completionRate": round(completionRate, 2)

                }
            
            return render(request, 'pendingTodos.html', context)
        
        except Exception as ex:
            print(ex)
            
    


@login_required
def getTodos(request):
    if request.method == 'GET':
        try: 
            userId = request.user.id
            todoLists = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False)[:5]
            return render(request, "_tableDetailsListPartial.html", {"todos": todoLists})
        
        except Exception as ex:
            print(ex)
            
            
            
            
@login_required
def getTodoBySearchValue(request, condition, value):
    try:
        if request.method == "GET" and value is not None:
            
                userId = request.user.id
                if condition == 'pending':
                    todoLists = List.objects.filter(Q(content__icontains=value, createdBy_id=userId, isDeleted=False,isCompleted=False) |
                                                    Q(title__icontains=value, createdBy_id=userId, isDeleted=False,isCompleted=False))[:5]
                    return render(request, "_tableDetailsListPartial.html", {"todos": todoLists})
                elif condition == 'completed':
                    todoLists = List.objects.filter(content__icontains=value, createdBy_id=userId, isDeleted=False,isCompleted=True)[:5]
                    return render(request, "_tableDetailsListPartial.html", {"todos": todoLists})
    except Exception as ex:
        print(ex)
        



@login_required
def getCompletedTodos(request):
    if request.method == 'GET':
        try:
            userId = request.user.id
            completedTodoLists = List.objects.filter(createdBy_id=userId,isDeleted=False,isCompleted=True).order_by('-dateCompleted')
            pendingTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).count()
            completedTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=True).count()
            totalTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False).count()
            
            if completedTodosAmount > 0:
                completionRate = (completedTodosAmount / totalTodosAmount) * 100
            else:
                completionRate = 0
            
            context = {
                "todos": completedTodoLists,
                "pendingTodosAmount": pendingTodosAmount,
                "completedTodosAmount": completedTodosAmount,
                "totalTodosAmount": totalTodosAmount,
                "completionRate": round(completionRate, 2)
                }
            
            return render(request, 'completedTodos.html', context)
        
        except Exception as ex:
            print(ex)




@login_required
def createTodo(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
                    
            title = body['title']
            content = body['content']
            createdBy = request.user
            
            list = List(
                title=title,
                content = content,
                createdBy = createdBy
            )
            list.save()
            
            return redirect('pendingTodosPartial')
    except Exception as ex:
        print(ex)
        
        
        
        
@login_required
def getPendingTodosPartial(request):
    try:
        userId = request.user.id
        todoLists = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).order_by('-dateCreated')[:5]
        UpdateTodoValuesToSession(request)
        
        context = {
            "todos": todoLists,
            }
        
        return render(request, '_tableDetailsListPartial.html', context)
    
    except Exception as ex:
        print(ex)
    
        
        
        
@login_required
def getTodoByIdPartial(request, id):
    if request.method == 'GET':
        try:
            userId = request.user.id
            todoList = List.objects.filter(createdBy_id=userId, id=id, isDeleted=False).first()
            
            context = {
                "todo": todoList,
                }
            
            return render(request, '_editTodoFormPartial.html', context)
        
        except Exception as ex:
            print(ex)
        
        
            
       
    
@login_required
def getUpdatedTodoValues(request):
    try:
        tvalues = request.session['tvalues']
        return JsonResponse(tvalues)
    
    except Exception as ex:
            print(ex)




@login_required
@csrf_exempt
def completeTodo(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            userId = request.user.id
                    
            id = body['id']
            
            todo = List.objects.filter(createdBy_id=userId, id=id, isDeleted=False).first()
            todo.isCompleted = True
            todo.dateCompleted = datetime.now()
            todo.save()
            
            UpdateTodoValuesToSession(request)
            
            return redirect('pendingTodosPartial')
    except Exception as ex:
        print(ex)
        
        
        
        
def UpdateTodoValuesToSession(request):
    try:
        userId = request.user.id
        pendingTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).count()
        completedTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=True).count()
        totalTodosAmount = List.objects.filter(createdBy_id=userId, isDeleted=False).count()
        completionRate = (completedTodosAmount / totalTodosAmount) * 100
        
        
        tvalues = {
            "pendingTodosAmount": pendingTodosAmount,
            "completedTodosAmount": completedTodosAmount,
            "totalTodosAmount": totalTodosAmount,
            "completionRate": round(completionRate, 2)
        }
        
        request.session['tvalues'] = tvalues
        return "Success"
    
    except Exception as ex:
            print(ex)
        
        
        
        
@login_required
def editTodoById(request, id):
    try:
        if request.method == 'PUT':
            body = json.loads(request.body)
                    
            title = body['title']
            content = body['content']
            createdBy = request.user
            
            todo = List.objects.filter(id=id, isDeleted=False, createdBy=createdBy.id).first()
            todo.title = title
            todo.content = content
            todo.save()
            
            return redirect('pendingTodosPartial')
    except Exception as ex:
        print(ex)
 
        
        


@login_required
def deleteTodoById(request, id):
    if request.method == 'DELETE':
        try:
            userId = request.user.id
            todo = List.objects.filter(createdBy_id=userId, id=id, isDeleted=False).first()
            todo.isDeleted = True
            todo.save()       
            
            todoLists = List.objects.filter(createdBy_id=userId, isDeleted=False,isCompleted=False).order_by('-dateCreated')[:5]
            UpdateTodoValuesToSession(request)
            
            context = {
                "todos": todoLists,
                }
            
            return render(request, '_tableDetailsListPartial.html', context)
        
        except Exception as ex:
            print(ex)
    
         

        
        

@login_required
def logoutAuth(request):
    try:
        logout(request)
        return redirect('authentication')
    
    except Exception as ex:
            print(ex)