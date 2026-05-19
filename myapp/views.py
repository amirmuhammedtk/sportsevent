import os
from datetime import datetime

import qrcode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group


# Create your views here.
from textblob import TextBlob

from eventManagment import settings
from myapp.models import Student, EventOrganaizer, SportsEvent, Register, Complaint, Review, refree, shedule, Poster, \
    EventCategory


def login_get_web(request):
    return render(request,'loginform.html')

@login_required(login_url='/myapp/login_get_web/')
def admin_home(request):
    return render(request,'admins/index.html')

@login_required(login_url='/myapp/login_get_web/')
def eventorgaiaser_home(request):
    return render(request,'EventOrganaizer/organaizerindex.html')

@login_required(login_url='/myapp/login_get_web/')
def student_home(request):
    return render(request,'Student/studentindex.html')

def web_login(request):
    email=request.POST['email']
    password=request.POST['password']
    if not email or not password:
        messages.warning(request,'email and password must be required')
        return redirect('/myapp/login_get_web/')
    check=authenticate(request,username=email,password=password)
    if check is not None:
        login(request,check)
        if check.groups.filter(name='admin').exists():
            # messages.success(request, 'login successfull')
            return redirect('/myapp/admin_view_events/#a/')
        elif check.groups.filter(name='Organaizer').exists():
            # messages.success(request, 'login successfull')
            return redirect('/myapp/organizer_profile/')
        elif check.groups.filter(name='Student').exists():
            # messages.success(request, 'login successfull')
            return redirect('/myapp/student_home/')
        else:
            messages.warning(request, 'not valid')
            return redirect('/myapp/login_get_web/')
    else:
        messages.error(request,'Invalid email or password')
        return redirect('/myapp/login_get_web/')


def Registering(request):
    return render(request,'Registering.html')


def student_signupGet(request):
    return render(request,'Student/studentSignup.html')


def studentSignup(request):
    name = request.POST['name']
    email = request.POST['email']
    gender = request.POST['gender']
    dob = request.POST['dob']
    college = request.POST['college']
    phone = request.POST['phone']
    place = request.POST['place']
    department=request.POST['department']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']
    password = request.POST['password']
    photo = request.FILES['photo']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    if User.objects.filter(username=email).exists():
        messages.error(request,'Email already exists! ')
        return redirect('/myapp/student_signupGet/')
    else:
        a=User.objects.create_user(username=email,password=password)
        a.groups.add(Group.objects.get(name='Student'))

        obj=Student()
        obj.name=name
        obj.dob=dob
        obj.college=college
        obj.gender=gender
        obj.department=department
        obj.email=email
        obj.place=place
        obj.city=city
        obj.pincode=pincode
        obj.state=state
        obj.phone=phone
        obj.photo=path
        obj.USER=a
        obj.save()
        messages.success(request,'signup successfull')
        return redirect('/myapp/login_get_web/')


def Organaizer_signupGet(request):
    return render(request,'EventOrganaizer/OrganaizerSignup.html')


def Organaizer_signup(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    gender = request.POST['gender']
    city = request.POST['city']
    pincode = request.POST['pincode']
    state = request.POST['state']
    password = request.POST['password']
    photo = request.FILES['photo']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    if User.objects.filter(username=email).exists():
        messages.error(request,'Email already exists! ')
        return redirect('/myapp/Organaizer_signupGet/')
    else:

        a=User.objects.create_user(username=email,password=password)
        a.groups.add(Group.objects.get(name='Organaizer'))

        obj=EventOrganaizer()
        obj.name=name
        obj.email=email
        obj.phone=phone
        obj.place=place
        obj.gender=gender
        obj.city=city
        obj.pincode=pincode
        obj.state=state
        obj.photo=path
        obj.USER=a
        obj.save()
        messages.success(request, 'signup successfull')
        return redirect('/myapp/login_get_web/')

# addddd


def add_event_category_get(request):
    return render(request,'EventOrganaizer/Add_event_category.html')

def add_event_category_post(request):
    name = request.POST['name']

    obj = EventCategory()
    obj.name = name

    obj.save()
    messages.success(request, "Event category added successfully!")
    return redirect('/myapp/add_event_category_get/')


def view_event_categories(request):
    categories = EventCategory.objects.all()
    return render(request, 'EventOrganaizer/Viewevenetcategory.html', {'categories': categories})

def delete_event_category(request, id):
    EventCategory.objects.get(id=id).delete()
    messages.success(request, "Event category deleted successfully!")
    return redirect('/myapp/view_event_categories/')


def event_add_poster(request):
    return render(request, 'EventOrganaizer/Add_poster.html')

def event_add_poster_post(request):
    description = request.POST['description']
    poster = request.FILES['poster']

    fs = FileSystemStorage()
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs.save(filename, poster)
    path = fs.url(filename)

    p=Poster()
    p.photo = path
    p.title = description
    p.EVENTORGANIZER = EventOrganaizer.objects.get(USER=request.user)
    p.save()

    messages.success(request, "Poster added successfully!")
    return redirect('/myapp/event_add_poster/')

def event_view_posters(request):
    user = request.user.id
    posters = Poster.objects.filter(EVENTORGANIZER__USER_id=user)
    return render(request, 'EventOrganaizer/Viewposter.html', {'data': posters})

def deleteposter(request, id):
    Poster.objects.get(id=id).delete()
    messages.success(request, "Poster deleted successfully!")
    return redirect('/myapp/event_view_posters/')


# wdudey

@login_required(login_url='/myapp/login_get_web/')
def student_profile(request):
    obj = Student.objects.get(USER=request.user)
    return render(request, 'Student/studentProfile.html', {"student": obj})

@login_required(login_url='/myapp/login_get_web/')
def organizer_profile(request):
    obj = EventOrganaizer.objects.get(USER=request.user)
    return render(request, 'EventOrganaizer/organizerProfile.html', {"organizer": obj})

@login_required(login_url='/myapp/login_get_web/')
def addEvent(request):
    a=refree.objects.all()
    return render(request,'EventOrganaizer/Add_event.html',{'data':a})

@login_required(login_url='/myapp/login_get_web/')
def addEventPost(request):
    name = request.POST['name']
    refid=request.POST['refree']
    # shedule = request.POST['shedule']
    # description = request.POST['Description']
    eventtype = request.POST['eventtype']
    location = request.POST['location']
    photo = request.FILES['photo']
    date=datetime.now().today()
    fs = FileSystemStorage()
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs.save(filename, photo)
    path = fs.url(filename)



    organizer = EventOrganaizer.objects.get(USER=request.user)


    obj = SportsEvent()
    obj.name = name
    # obj.shedule = shedule
    # obj.description = description
    obj.eventtype = eventtype
    obj.date = date
    obj.status = 'pending'
    obj.location = location
    obj.photo = path
    obj.EVENTORGANAIZER = organizer
    obj.REFREE=refree.objects.get(id=refid)
    obj.save()
    messages.success(request, "Event added successfully!")
    return redirect('/myapp/organaizerViewEvent/#a')

@login_required(login_url='/myapp/login_get_web/')
def organaizerViewEvent(request):
    user=request.user.id
    a=SportsEvent.objects.filter(EVENTORGANAIZER__USER_id=user)
    return render(request, 'EventOrganaizer/ViewOrganaizerEvent.html',{'data':a})




@login_required(login_url='/myapp/login_get_web/')
def deleteEvent(request,id):
    SportsEvent.objects.get(id=id).delete()
    messages.success(request,'Event removed successfully!')
    return redirect('/myapp/organaizerViewEvent/')

@login_required(login_url='/myapp/login_get_web/')
# def eventViewEdit(request,id):
#     obj=SportsEvent.objects.get(id=id)
#     return render(request,'EventOrganaizer/EditEvent.html',{'data':obj})
def eventViewEdit(request, id):
    event = SportsEvent.objects.get(id=id)
    referees = refree.objects.all()
    return render(request, 'EventOrganaizer/editEvent.html', {
        'data': event,
        'referees': referees
    })
@login_required(login_url='/myapp/login_get_web/')
# def eventEditPost(request):
#     id = request.POST['id']
#     name = request.POST['name']
#     shedule = request.POST['shedule']
#     description = request.POST['Description']
#     eventtype = request.POST['eventtype']
#     location = request.POST['location']
#     date = datetime.now().today()
#     obj = SportsEvent.objects.get(id=id)
#
#     if 'photo' in request.FILES:
#         photo = request.FILES['photo']
#         fs = FileSystemStorage()
#         filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
#         fs.save(filename, photo)
#         path = fs.url(filename)
#         obj.photo = path
#
#
#     obj.name = name
#     obj.shedule = shedule
#     obj.description = description
#     obj.eventtype = eventtype
#     obj.date = date
#     obj.location = location
#     obj.save()
#     messages.success(request, 'Event edited successfully!')
#     return redirect('/myapp/organaizerViewEvent/#a')
def eventEditPost(request):
    id = request.POST['id']
    name = request.POST['name']
    # shedule = request.POST['shedule']  # string from datetime-local
    # description = request.POST['Description']
    eventtype = request.POST['eventtype']
    location = request.POST['location']
    refid = request.POST['refree']

    obj = SportsEvent.objects.get(id=id)

    # Convert string to datetime object
    # if shedule:
    #     shedule_dt = datetime.strptime(shedule, "%Y-%m-%dT%H:%M")
    #     obj.shedule = shedule_dt

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(filename, photo)
        path = fs.url(filename)
        obj.photo = path

    obj.name = name
    # obj.description = description
    obj.eventtype = eventtype
    obj.location = location
    obj.REFREE = refree.objects.get(id=refid)
    obj.save()
    messages.success(request, 'Event edited successfully!')
    return redirect('/myapp/organaizerViewEvent/#a')
@login_required(login_url='/myapp/login_get_web/')
def admin_view_events(request):
    events = SportsEvent.objects.all()
    return render(request, "admins/admin_view_events.html", {"events": events})

@login_required(login_url='/myapp/login_get_web/')
def approve_event(request, id):
    event = SportsEvent.objects.get(id=id)
    event.status = "approved"
    event.save()
    return redirect("/myapp/admin_view_events/")

@login_required(login_url='/myapp/login_get_web/')
def reject_event(request, id):
    SportsEvent.objects.filter(id=id).update(status="rejected")
    return redirect("/myapp/admin_view_events/")




# sheduleeee

def addShedule_get(request,id):
    data=SportsEvent.objects.get(id=id)
    return render(request,'EventOrganaizer/addShedule.html',{'data':data})

def addShedulePost(request):
    event_id = request.POST['event_id']
    description = request.POST['description']
    date = request.POST['date']
    fromTime = request.POST['fromTime']
    toTime = request.POST['toTime']

    event = SportsEvent.objects.get(id=event_id)
    organizer = EventOrganaizer.objects.get(USER=request.user)

    obj = shedule()
    obj.description = description
    obj.date = date
    obj.fromTime = fromTime
    obj.toTime = toTime
    obj.EVENT = event
    obj.ORGANAIZER=organizer
    obj.save()

    messages.success(request, "Schedule added successfully!")
    return redirect('/myapp/viewShedule_get/')

def viewShedule_get(request):
    organizer = EventOrganaizer.objects.get(USER=request.user)
    schedules = shedule.objects.filter(ORGANAIZER=organizer)

    return render(request, 'EventOrganaizer/viewShedule.html', {'data': schedules})


# def student_view_events(request):
#     a= Event.objects.filter(status="approved")
#     l=[]
#     for i in a:
#         g="no"
#         if Booking.objects.filter(EVENT=i.id,STUDENT__USER=request.user).exists():
#             g="yes"
#         l.append({'id':i.id,'g':g})
#     return render(request,'Student/student_view_events.html', {"events": l})
# def book_event(request, id):
#     id = Event.objects.get(id=id)
#
#     obj = Booking()
#     obj.date = datetime.now().date()
#     obj.status = "booked"
#     obj.STUDENT = request.user
#     obj.EVENT = id
#     obj.save()
#     return redirect('/myapp/student_view_events/')

@login_required(login_url='/myapp/login_get_web/')
def student_view_events(request):

    events = SportsEvent.objects.filter(status="approved")

    event_list = []
    for event in events:
        booked = Register.objects.filter(STUDENT__USER=request.user, EVENT=event).exists()

        event_list.append({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'eventtype': event.eventtype,
            'shedule': event.shedule,
            'photo': event.photo,
            'date': event.date,
            'location': event.location,
            'booked': booked,
        })

    return render(request, 'Student/student_view_events.html', {"events": event_list})

@login_required(login_url='/myapp/login_get_web/')
# def book_event(request, id):
#     event = SportsEvent.objects.get(id=id)
#     student = Student.objects.get(USER=request.user)
#
#     if not Register.objects.filter(STUDENT=student, EVENT=event).exists():
#         Register.objects.create(
#             STUDENT=student,
#             EVENT=event,
#             date=datetime.now().date(),
#             status='registered'
#         )
#     messages.success(request, 'booked successfully!')
#     return redirect('/myapp/student_booked_events/#a')




def book_event(request, id):
    event = SportsEvent.objects.get(id=id)
    student = Student.objects.get(USER=request.user)

    if not Register.objects.filter(STUDENT=student, EVENT=event).exists():
        register = Register.objects.create(
            STUDENT=student,
            EVENT=event,
            date=datetime.now().date(),
            status='registered',
            winner='pending'
        )

        # 🔹 Data inside QR (unique info)
        qr_data = f"BookingID:{register.id}, Student:{student.name}, Event:{event.name}, Date:{register.date}"

        # 🔹 Create QR
        qr = qrcode.make(qr_data)

        # 🔹 Save path
        qr_dir = os.path.join(settings.MEDIA_ROOT, "qrcodes")
        os.makedirs(qr_dir, exist_ok=True)
        qr_path = os.path.join(qr_dir, f"booking_{register.id}.png")
        qr.save(qr_path)

        # 🔹 Save path to model
        register.qr_code = f"qrcodes/booking_{register.id}.png"
        register.save()

    messages.success(request, 'Booked successfully! QR code generated.')
    return redirect('/myapp/student_booked_events/#a')



# @login_required(login_url='/myapp/login_get_web/')
# def student_booked_events(request):
#     bookings = Register.objects.filter(STUDENT__USER=request.user)
#
#     l = []
#     for b in bookings:
#         l.append({
#             'id': b.EVENT.id,
#             'name': b.EVENT.name,
#             'description': b.EVENT.description,
#             'eventtype': b.EVENT.eventtype,
#             'shedule': b.EVENT.shedule,
#             'photo': b.EVENT.photo,
#             'date': b.EVENT.date,
#             'location': b.EVENT.location,
#             'status': b.status
#         })
#
#     return render(request, 'Student/student_booked_events.html', {"events": l})

@login_required(login_url='/myapp/login_get_web/')
def student_booked_events(request):
    bookings = Register.objects.filter(STUDENT__USER=request.user).select_related("EVENT")
    return render(request, 'Student/student_booked_events.html', {"bookings": bookings})


@login_required(login_url='/myapp/login_get_web/')
def organizer_bookings(request):
    organizer = request.user
    events = SportsEvent.objects.filter(EVENTORGANAIZER__USER=organizer)
    l = []
    for event in events:
        bookings = Register.objects.filter(EVENT=event)
        for b in bookings:
            l.append({
                'id': b.id,
                'event_name': event.name,
                # 'student_name': b.STUDENT.name,
                # 'student_email': b.STUDENT.email,
                # 'student_phone': b.STUDENT.phone,
                'date': b.date,
                'status': b.status
            })

    return render(request, 'EventOrganaizer/organizer_bookings.html', {"bookings": l})

#
def organaizerviewParticpents(request,id):
    reg = Register.objects.get(id=id)
    event = reg.EVENT
    a = Register.objects.filter(EVENT=event)
    print(a,'dfbhvh')

    return render(request, 'EventOrganaizer/event_participants.html', {'data':a})

def SetAsWinner(request,id):
    Register.objects.filter(id=id).update(winner='Winner')
    return redirect('/myapp/organaizerViewEvent/')


@login_required(login_url='/myapp/login_get_web/')
def admin_view_bookings(request):
    a = Register.objects.all()
    return render(request, 'admins/admin_bookings.html', {"data": a})

@login_required(login_url='/myapp/login_get_web/')
def student_send_complaintGet(request):
    return render(request,'Student/send_complaint.html')

@login_required(login_url='/myapp/login_get_web/')
def student_send_complaint(request):
    complaint = request.POST['complaint']
    user=request.user
    obj = Complaint()
    obj.date = datetime.now().today()
    obj.complaint = complaint
    obj.replay = ""
    obj.status = "Pending"
    obj.STUDENT = Student.objects.get(USER=user)
    obj.save()
    messages.success(request, 'send complaint  successfully!')
    return redirect('/myapp/student_view_complaints/#a')

@login_required(login_url='/myapp/login_get_web/')
def admin_view_complaints(request):
    a = Complaint.objects.all()
    return render(request, 'admins/viewComplaint.html', {"data": a})

@login_required(login_url='/myapp/login_get_web/')
def adminSendReplayGet(request, id):
    obj = Complaint.objects.get(id=id)
    return render(request, 'admins/sendReplay.html', {"data": obj})

@login_required(login_url='/myapp/login_get_web/')
def adminSendReplay(request):
    id=request.POST['id']
    replay= request.POST['replay']
    obj = Complaint.objects.get(id=id)
    obj.replay = replay
    obj.status = "Replied"
    obj.save()
    messages.success(request, 'send replay successfully!')
    return redirect("/myapp/admin_view_complaints/#a")

@login_required(login_url='/myapp/login_get_web/')
def student_view_complaints(request):
    a = Student.objects.get(USER=request.user)
    data = Complaint.objects.filter(STUDENT=a)
    return render(request, 'Student/viewComplaints.html', {"data": data})

@login_required(login_url='/myapp/login_get_web/')
def admin_view_students(request):
    a = Student.objects.all()
    return render(request, 'admins/viewStudents.html', {"data": a})

@login_required(login_url='/myapp/login_get_web/')
def admin_view_organizers(request):
    a = EventOrganaizer.objects.all()
    return render(request, 'admins/viewOrganizers.html', {"data": a})

@login_required(login_url='/myapp/login_get_web/')
def student_edit_profile_get(request):
    a = Student.objects.get(USER=request.user)

    return render(request, 'Student/studentEditProfile.html', {"student": a})

@login_required(login_url='/myapp/login_get_web/')
def student_edit_profile(request):
    id = request.POST['id']
    name = request.POST['name']
    dob = request.POST['dob']
    college = request.POST['college']
    gender = request.POST['gender']
    department = request.POST['department']
    email = request.POST['email']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']
    phone = request.POST['phone']

    student = Student.objects.get(id=id)

    student.name = name
    student.dob = dob
    student.college = college
    student.gender = gender
    student.department = department
    student.email = email
    student.place = place
    student.city = city
    student.state = state
    student.pincode = pincode
    student.phone = phone

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(filename, photo)
        student.photo = fs.url(filename)


    user = student.USER
    user.username = email
    user.email = email
    user.save()
    student.save()
    messages.success(request, 'edited successfully!')
    return redirect('/myapp/student_profile/#a')

@login_required(login_url='/myapp/login_get_web/')
def organizer_edit_profile_get(request):
    a = EventOrganaizer.objects.get(USER=request.user)
    return render(request, 'EventOrganaizer/organizerEditProfile.html', {"organizer": a})

@login_required(login_url='/myapp/login_get_web/')
def organizer_edit_profile(request):
    id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    gender = request.POST['gender']
    city = request.POST['city']
    pincode = request.POST['pincode']
    state = request.POST['state']

    organizer = EventOrganaizer.objects.get(id=id)

    organizer.name = name
    organizer.email = email
    organizer.phone = phone
    organizer.place = place
    organizer.gender = gender
    organizer.city = city
    organizer.pincode = pincode
    organizer.state = state

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(filename, photo)
        organizer.photo = fs.url(filename)

    user = organizer.USER
    user.username = email
    user.email = email
    user.save()

    organizer.save()
    return redirect('/myapp/organizer_profile/#a')


def adminChangePasswordGet(request):
    return render(request,'admins/admin_changePassword.html')


def adminchangepasswordpost(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)

            return redirect('/myapp/login_get_web/')
        else:
            messages.success(request, "Password changed successfully. Please login again.")
            return redirect('/myapp/adminChangePasswordGet/')
    else:
        messages.error(request, "Current password is incorrect.")
        return redirect('/myapp/adminChangePasswordGet/')


@login_required(login_url='/myapp/login_get_web/')
def OrganaizerChangePasswordGet(request):
    return render(request,'EventOrganaizer/eventOrganaizer_changePassword.html')

@login_required(login_url='/myapp/login_get_web/')
def organaizerchangepasswordpost(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            messages.success(request, "Password changed successfully. Please login again.")
            return redirect('/myapp/login_get_web/')
        else:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('/myapp/OrganaizerChangePasswordGet/')
    else:
        messages.error(request, "Current password is incorrect.")

        return redirect('/myapp/OrganaizerChangePasswordGet/')

@login_required(login_url='/myapp/login_get_web/')
def StudentChangePasswordGet(request):
    return render(request,'Student/Student_changePassword.html')

@login_required(login_url='/myapp/login_get_web/')
def Studentchangepasswordpost(request):
    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']

    user = request.user

    if check_password(currentpassword, user.password):
        if newpassword == confirmpassword:
            user.set_password(newpassword)
            user.save()
            logout(request)
            messages.success(request, "Password changed successfully. Please login again.")
            return redirect('/myapp/login_get_web/')
        else:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('/myapp/StudentChangePasswordGet/')
    else:
        messages.error(request, "Current password is incorrect.")
        return redirect('/myapp/StudentChangePasswordGet/')

@login_required(login_url='/myapp/login_get_web/')
def logout_get(request):
    logout(request)
    return redirect('/myapp/login_get_web/')


def studentSendReviewGet(request):
    event_id = request.GET.get("event_id")
    event = SportsEvent.objects.get(id=event_id)
    return render(request, 'Student/student_add_review.html', {"event": event})


def studentSendReviewPost(request, id):
    if request.method == "POST":
        review_text = request.POST['review']
        student = Student.objects.get(USER=request.user)
        event = SportsEvent.objects.get(id=id)

        blob = TextBlob(review_text)
        polarity = blob.sentiment.polarity

        pos, neg, neu = 0, 0, 0
        if polarity > 0:
            pos = 1
        elif polarity < 0:
            neg = 1
        else:
            neu = 1

        Review.objects.create(
            date=datetime.now().today(),
            review=review_text,
            positive=pos,
            negative=neg,
            nutrel=neu,
            STUDENT=student,
            EVENT=event
        )

        messages.success(request,'send review successfull ')
        return redirect('/myapp/student_booked_events/#a')

def admin_view_reviews(request):
    a = Review.objects.all()
    return render(request, "admins/admin_view_reviews.html", {"reviews": a})
def addRefree_get(request):
    return render(request,'admins/addrefree.html')

def admin_addRefree(request):
    name=request.POST['name']
    gender=request.POST['gender']
    email=request.POST['email']
    mobile=request.POST['mobile']

    obj=refree()
    obj.name=name
    obj.gender=gender
    obj.email=email
    obj.mobile=mobile
    obj.save()
    return redirect('/myapp/adminViewRefree/')
def adminViewRefree(request):
    a=refree.objects.all()
    return render(request,'admins/viewRefree.html',{'data':a})
def refree_viewEdit(request,id):
    a=refree.objects.get(id=id)
    return render(request,'admins/editrefree.html',{'data':a})
def editRefree(request):
    id=request.POST['id']
    name = request.POST['name']
    gender = request.POST['gender']
    email = request.POST['email']
    mobile = request.POST['mobile']

    obj = refree.objects.get(id=id)
    obj.name = name
    obj.gender = gender
    obj.email = email
    obj.mobile = mobile
    obj.save()
    return redirect('/myapp/adminViewRefree/')
def deleteRefree(request,id):
    refree.objects.get(id=id).delete()
    return redirect('/myapp/adminViewRefree/')
def admin_viewWinners(request,id):
    a=Register.objects.filter(winner='Winner',EVENT_id=id)
    return render(request,'admins/viewwinners.html',{'data':a})



