"""
SmartLab - Django views.py (reference copy)

Extracted from the code appendix of the final project report (the original
project folder is no longer accessible). PDF text extraction does not
preserve exact indentation, so the block structure below needs to be
reviewed and reformatted before this will actually run - treat it as a
logic reference, not a working file.

Kept here as an honest record of the backend logic rather than a runnable
checkout. models.py, urls.py, settings.py, templates, and static assets
were not part of the report appendix and are not recovered.
"""

import os
  from datetime import datetime

  from django.contrib.auth import logout, authenticate, login
  from django.contrib.auth.decorators import login_required
  from django.contrib.auth.hashers import make_password
  from django.contrib.auth.models import Group,User
  from django.core.files.storage import FileSystemStorage
  from django.http import JsonResponse, HttpResponse
  from django.shortcuts import render, redirect

  # Create your views here.
  from myapp.models import *
  from smartlab import settings


  def login_get(request):
        return render(request,'loginindex.html')

  def login_post(request):
        username=request.POST['username']
        password=request.POST['password']

     user=authenticate(request,username=username,password=password)
        if user is not None:
      if user.groups.filter(name="Admin").exists():
        login(request,user)
        return redirect("/myapp/admin_home/")
      elif user.groups.filter(name="Lab Assistant").exists():
        login(request,user)
        return redirect("/myapp/labassistant_home/")
      elif user.groups.filter(name="Staff").exists():
        login(request,user)
        return redirect("/myapp/staff_home/")
      else:
        return render(request, 'loginindex.html')
        return redirect("/myapp/login_get/")

  def logout_get(request):
        logout(request)
        return render(request,'loginindex.html')

  def view_course(request):
        ab=course_table.objects.all()
         return render(request,'admin_module/view_course.html',{'data':ab})

    def Add_course(request):
         a=department_table.objects.all()


         return render(request,'admin_module/Add_course.html',{"data":a})

    def add_course_post(request):
          dept=request.POST['dept']

      coursename=request.POST['course_name']
         details=request.POST['details']

         ab=course_table()

         ab.coursename=coursename
         ab.details=details
         ab.DEPARTMENT_id=dept
         ab.save()
         return redirect(f'/myapp/view_course/')


    def department_add(request):
          return render(request,'admin_module/department_add.html')

    def department_add_post(request):
          department = request.POST['department']
          details = request.POST['details']

         ab=department_table()
         ab.dept_name=department
         ab.details=details
         ab.save()
         return redirect('/myapp/view_department/')

    def view_department(request):

         ab=department_table.objects.all()
         return render(request,'admin_module/view_department.html',{'data':ab})

    def edit_course(request,id):
          request.session['id']=id
          ab=course_table.objects.get(id=id)
          dept=department_table.objects.all()
          return render(request,'admin_module/edit_course.html',{'data':ab,'dept':dept})
    def edit_course_post(request):
          coursename = request.POST['course']
          details = request.POST['details']
          dept = request.POST['dept']
          ab=course_table.objects.get(id= request.session['id'])
          ab.coursename=coursename
          dept=request.session['id']
          ab.details=details
          ab.DEPARTMENT_id=dept
          ab.save()
          return redirect('/myapp/view_course/')

    def delete_course(request,id):
      course_table.objects.get(id=id).delete()
          return redirect('/myapp/view_course/')

    def add_lab(request):
          a=department_table.objects.all()
          return render(request,'admin_module/add_lab.html',{"data":a})

    def add_lab_post(request):
          labno=request.POST['labno']
          dept=request.POST['dept']
          details = request.POST['details']

          a=Lab_table()
          a.DEPARTMENT_id=dept
          # a = Lab_table.objects.get(id=request.session['id'])
          a.lab_no=labno
          a.lab_details=details
          a.save()
          return redirect('/myapp/view_lab/')



    def admin_view_lab(request):
      ab = Lab_table.objects.all()
         return render(request,'admin_module/view_lab.html', {'data':ab})

    def edit_lab(request,id):
          request.session['id'] = id
          ab = Lab_table.objects.get(id=id)
          ob=department_table.objects.all()
          return render(request, 'admin_module/edit_lab.html', {'data': ab,'a':ob})

    def edit_lab_post(request):
          labno = request.POST['labno']
           dept = request.POST['dept']
           details = request.POST['details']

           a = Lab_table.objects.get(id=request.session['id'])
           a.DEPARTMENT_id = dept
           a.lab_no = labno
           a.lab_details = details
           a.save()
           return redirect('/myapp/view_lab/')


    def delete_lab(request,id):
          Lab_table.objects.get(id=id).delete()
          return redirect('/myapp/view_lab/')

    def add_labsubject(request):
          c=course_table.objects.all()
          return render(request,'admin_module/add_labsubject.html',{'course':c})

    def add_labsubject_post(request):
          subject=request.POST['subject']
          syllabus=request.FILES['syllabus']
          course = request.POST['course']

           ab=labsubject_table()
           ab.COURSE_id=course
           ab.subject = subject
           ab.syllabus = syllabus
           ab.save()
           return redirect('/myapp/view_labsubject/')

    def edit_labsubject(request,id):
          request.session['id']=id
      ab=labsubject_table.objects.get(id=id)
          ob=course_table.objects.all()
          return render(request,'admin_module/edit_labsubject.html',{"data":ab,"course":ob})

    def edit_labsubject_post(request):
          subject = request.POST['subject']
          course = request.POST['course']

           ab = labsubject_table.objects.get(id=request.session['id'])

           if 'syllabus' in request.FILES:
           syllabus = request.FILES['syllabus']
           ab.syllabus = syllabus
           ab.save()
          ab.COURSE_id = course
          ab.subject = subject
          ab.save()
          return redirect('/myapp/view_labsubject/')


    def view_labsubject(request):
          res=labsubject_table.objects.all()
          return render(request,'admin_module/view_labsubject.html',{'data':res})


    def delete_labsubject(request,id):
          labsubject_table.objects.get(id=id).delete()
          return redirect('/myapp/view_labsubject/')


    def allocatelabtolabassistant(request):
          return render(request,'admin_module/allocatelabtolabassistant.html')
    def view_allocation(request):
          ab = Lab_table.objects.all()
          return render(request,'admin_module/view_allocation.html', {'data'})
    def add_examschedule(request):
          a=labsubject_table.objects.all()
          return render(request,'admin_module/add_examschedule.html',{'subject':a})
    def add_examschedule_post(request):
          exam_name=request.POST['exam']
          subject = request.POST['subject']
          date = request.POST['date']
          from_time = request.POST['fromtime']
          to_time = request.POST['totime']
          duration = request.POST['duration']
          total_mark = request.POST['mark']
          obj=exam_table()
          obj.SUBJECT_id=subject
          obj.exam_name=exam_name
          obj.date=date
          obj.fromtime=from_time
          obj.totime=to_time
          obj.duration=duration
          obj.totalmark=total_mark
          obj.save()
          return redirect('/myapp/view_examschedule_get/')

    def delete_examschedule(request,id):
      exam_table.objects.get(id=id).delete()
          return redirect('/myapp/view_examschedule_get/')
    def view_examschedule_get(request):
          res = exam_table.objects.all()
          return render(request, 'admin_module/view_examschedule.html', {'data': res})

    def edit_examschedule(request,id):
          request.session['eid'] = id
          ab = exam_table.objects.get(id=id)

         a=labsubject_table.objects.all()

         return render(request,'admin_module/edit_examschedule.html',{'data':ab,'a':a})

    def edit_examschedule_post(request):
          exam_name = request.POST['exam']
          subject = request.POST['subject']
          date = request.POST['date']
          from_time = request.POST['fromtime']
          to_time = request.POST['totime']
          duration = request.POST['duration']
          total_mark = request.POST['mark']
          obj = exam_table.objects.get(id=request.session['eid'])
          obj.SUBJECT_id = subject
          obj.exam_name = exam_name
          obj.date = date
          obj.fromtime = from_time
          obj.totime = to_time
          obj.duration = duration
          obj.totalmark = total_mark
          obj.save()
          return redirect('/myapp/view_examschedule_get/')

    def add_student(request):
          c=course_table.objects.all()
          return render(request,'admin_module/add_student.html',{'course':c})


    def add_student_post(request):
          name=request.POST['name']
          lname=request.POST['lname']
          dob=request.POST['dob']
          Gender=request.POST['Gender']
          email=request.POST['email']
          phone=request.POST['phone']
          place=request.POST['place']
          pincode=request.POST['pincode']
          district=request.POST['district']
       photo=request.FILES['photo']
       course=request.POST['course']
       username=request.POST['username']
       password=request.POST['password']


        user = User.objects.create(username=username,
password=make_password(password),email=email,first_name=password)
        user.save()
    user.groups.add(Group.objects.get(name="Student"))

        ab=student_table()
        ab.fname=name
        ab.lname=lname
        ab.COURSE_id=course
        ab.dob=dob
        ab.gender=Gender
        ab.email=email
        ab.phone=phone
        ab.place=place
        ab.pin=pincode
        ab.district=district
        ab.photo=photo
        ab.COURSE_id=course
        ab.LOGIN=user
        ab.save()
        return redirect('/myapp/view_student/')

  def delete_student(request,id):
    student_table.objects.get(LOGIN=id).delete()
        User.objects.get(id=id).delete()
        return redirect('/myapp/view_student/')

  def view_student(request):
        res = student_table.objects.all()
        return render(request,'admin_module/view_student.html', {'data':res})

  def Edit_student(request,id):
        c=course_table.objects.all()
        request.session['sid']=id
        data=student_table.objects.get(id=id)
        return render(request,'admin_module/Edit_student.html',{'data':data,'course':c})

  def Edit_student_post(request):
        name = request.POST['name']
        lname = request.POST['lname']
        dob = request.POST['dob']
           Gender = request.POST['Gender']
           email = request.POST['email']
           phone = request.POST['phone']
           place = request.POST['place']
           pincode = request.POST['pincode']
           # district = request.POST['district']
           photo = request.FILES.get('photo')
           course = request.POST['course']



        ab=student_table.objects.get(id=request.session['sid'])
           ab.fname=name
           ab.lname=lname
           ab.COURSE_id=course
           ab.dob=dob
           ab.gender=Gender
           ab.email=email
           ab.phone=phone
           ab.place=place
           ab.pin=pincode
           if photo:
         ab.photo=photo
           ab.COURSE_id=course
           ab.save()
           return redirect('/myapp/view_student/')



    def View_feedback(request):
          res=feedback_table.objects.all()
          return render(request,'admin_module/View_feedback.html',{'data':res})


    def add_videos(request):
          res=labsubject_table.objects.all()
          return render(request,'admin_module/add_videos.html',{'data':res})

    def add_videos_post(request):
          title = request.POST['title']
          details = request.POST['details']
          sub = request.POST['subject']
          video = request.FILES['video']

           ab = notes_table()
           ab.title = title
           ab.details = details
           ab.video = video
           ab.SUBJECT_id=sub
           ab.LOGIN = User.objects.get(id=request.user.id) # lid must already exist
           ab.save()

           return redirect('/myapp/view_videos/')

    def edit_videos(request,id):
          request.session['vid']=id
          v=notes_table.objects.get(id=id)
          s=labsubject_table.objects.all()
          return render(request,'admin_module/edit_videos.html',{'data':v,'data2':s})

    def edit_videos_post(request):
          title = request.POST['title']
          details = request.POST['details']
          sub = request.POST['subject']

           ab = notes_table.objects.get(id=request.session['vid'])
           ab.title = title
           ab.details = details
           ab.SUBJECT_id=sub

              ✅

           #      condition for video
           if 'video' in request.FILES:
           ab.video = request.FILES['video'] # update only if new video selected

          ab.save()
          return redirect('/myapp/view_videos/')
    def delete_videos(request,id):
      notes_table.objects.filter(id=id).delete()
          return redirect('/myapp/view_videos/')

    def view_videos(request):
          res = notes_table.objects.all()
          return render(request,'admin_module/view_videos.html',{'data':res})


    def View_lab_submissions(request):
          return render(request,'admin_module/View_lab_submissions.html')


    def admin_home(request):
         return render(request,'admin_module/index.html')


    def add_labassistant(request):
          l=Lab_table.objects.all()
          return render(request,'admin_module/add_labassistant.html',{'data':l})


    def add_labssitant_post(request):
          name=request.POST['name']
          gender = request.POST['gender']
          dob = request.POST['dob']
          place = request.POST['place']
          pin = request.POST['pin']
          post = request.POST['post']
          phone = request.POST['phone']
          photo = request.FILES['photo']
          email = request.POST['email']
          qualification = request.POST['qualification']
          lab_id= request.POST['labid']
          username= request.POST['username']
          password= request.POST['password']



user=User.objects.create(username=username,password=make_password(password),email=ema
il,first_name=password)
        user.save()
    user.groups.add(Group.objects.get(name="Lab Assistant"))

        ab=labassistant_table()
        ab.name=name
        ab.gender = gender
        ab.dob = dob
        ab.place = place
        ab.pin = pin
        ab.phone = phone
        ab.LOGIN = user
        ab.post = post
        ab.email = email
        ab.qualification = qualification
        ab.photo = photo
        ab.LAB_id = lab_id

        ab.save()

        return redirect('/myapp/view_labassistant/')

  def view_labassistant(request):
        ab = labassistant_table.objects.all()
        return render(request,'admin_module/view_labassistant.html',{"data":ab})
    def delete_labassistant(request,id):
      labassistant_table.objects.get(LOGIN=id).delete()
          User.objects.get(id=id).delete()
          return redirect('/myapp/view_labassistant/')

    def delete_department(request,id):
      department_table.objects.get(id=id).delete()
          return redirect('/myapp/view_department/')


    def edit_labassistant(request,id):
          l=Lab_table.objects.all()
      res=labassistant_table.objects.get(id=id)
          request.session['labassit_id']=id
          return render(request,'admin_module/edit_labassistant.html',{'data2':l,'data':res})


    def edit_labassitant_post(request):
          name=request.POST['name']
          gender = request.POST['gender']
          dob = request.POST['dob']
          place = request.POST['place']
          pin = request.POST['pin']
          post = request.POST['post']
          phone = request.POST['phone']
          photo = request.FILES['photo']
          email = request.POST['email']
          qualification = request.POST['qualification']
          lab_id= request.POST['labid']
          # username= request.POST['username']
          # password= request.POST['password']
          #
          #
          # user=User.objects.create(username=username,password=make_password(password))
          # user.save()
          # user.groups.add(Group.objects.get(name="Lab Assistant"))
          #
      ab=labassistant_table.objects.get(id=request.session['labassit_id'])
          ab.name=name
          ab.gender = gender
          ab.dob = dob
          ab.place = place
          ab.pin = pin
          ab.phone = phone
          ab.post = post
          ab.email = email
         ab.qualification = qualification
         ab.photo = photo
         ab.LAB_id = lab_id

         ab.save()

         return redirect('/myapp/view_labassistant/')




    def add_staff_get(request):
          l=department_table.objects.all()
          return render(request,'admin_module/add_staff.html',{'data':l})


    def add_staff_post(request):
          name=request.POST['name']
          gender = request.POST['gender']
          place = request.POST['place']
          pin = request.POST['pin']
          post = request.POST['post']
          phone = request.POST['phone']
          photo = request.FILES['photo']
          email = request.POST['email']
          program_language = request.POST['program_language']
          qualification = request.POST['qualification']
          dept= request.POST['dept']
          username= request.POST['username']
          password= request.POST['password']



user=User.objects.create(username=username,password=make_password(password),email=ema
il,first_name=password)
        user.save()
    user.groups.add(Group.objects.get(name="Staff"))

        ab=staff_table()
        ab.name=name
        ab.gender = gender
        ab.place = place
        ab.pin = pin
        ab.phone = phone
        ab.LOGIN = user
        ab.post = post
        ab.email = email
           ab.qualification = qualification
           ab.program_language=program_language
           ab.photo = photo
           ab.DEPARTMENT_id = dept

           ab.save()

           return redirect('/myapp/view_staff_get/')

    def view_staff_get(request):
          ab = staff_table.objects.all()
          return render(request,'admin_module/view_staff.html',{"data":ab})

    def delete_staff(request,id):
          staff_table.objects.get(LOGIN=id).delete()
          User.objects.get(id=id).delete()
          return redirect('/myapp/view_staff_get/')

    def edit_staff(request,id):
          request.session['stfid'] = id
          ab = staff_table.objects.get(id=id)
          ob=department_table.objects.all()
          return render(request, 'admin_module/edit_staff.html', {'val': ab,'data':ob})

    def edit_staff_post(request):
          name=request.POST['name']
          gender = request.POST['gender']
          place = request.POST['place']
          pin = request.POST['pin']
          post = request.POST['post']
          phone = request.POST['phone']
          email = request.POST['email']
          program_language = request.POST['program_language']
          qualification = request.POST['qualification']
          dept= request.POST['dept']
          # username= request.POST['username']
          # password= request.POST['password']
          #
          #
          # user=User.objects.create(username=username,password=make_password(password))
          # user.save()
          # user.groups.add(Group.objects.get(name="Staff"))

        ab=staff_table.objects.get(id=request.session['stfid'])

           if 'photo' in request.FILES:
           photo = request.FILES['photo']
           ab.photo = photo
           ab.save()

           ab.name=name
           ab.gender = gender
           ab.place = place
           ab.pin = pin
           ab.phone = phone
           ab.post = post
           ab.email = email
           ab.qualification = qualification
           ab.program_language=program_language
           ab.DEPARTMENT_id = dept

           ab.save()

           return redirect('/myapp/view_staff_get/')


  def assign_subjectTo_lab_assistant(request):
        sub=labsubject_table.objects.all()
        laba=labassistant_table.objects.all()
        return
render(request,'admin_module/assign_sub_to_assistant.html',{'assistant':laba,'subject':sub})


  def add_assign_post(request):
        sub=request.POST['subject']
        assistant=request.POST['assistant']
        day=request.POST['day']
        hour=request.POST['hour']
        obj=subjectTo_lab_table()
        obj.LABASSISTANT_id=assistant
        obj.LABSUBJECT_id=sub
        obj.day=day
        obj.hour=hour
        obj.save()
        return redirect('/myapp/view_assign/')

  def view_assign(request):
        res=subjectTo_lab_table.objects.all()
        return render(request,'admin_module/view assign.html',{'data':res})

  def delete_assign(request,id):
    subjectTo_lab_table.objects.get(id=id).delete()
        return redirect('/myapp/view_assign/')
    ####


  def assign_subjectTo_staff(request):
        sub=labsubject_table.objects.all()
        laba=staff_table.objects.all()
        return
render(request,'admin_module/assign_sub_to_staff.html',{'staff':laba,'subject':sub})


  def add_staff_assign_post(request):
        sub=request.POST['subject']
        assistant=request.POST['staff']

        obj=labsubTo_staff_table()
        obj.STAFF_id=assistant
        obj.LABSUBJECT_id=sub
        obj.date=datetime.now().today()
        obj.save()
        return redirect('/myapp/view_staff_assign/')

  def view_staff_assign(request):
    res=labsubTo_staff_table.objects.all()
        return render(request,'admin_module/view staff assign.html',{'data':res})

  def delete_staff_assign(request,id):
    labsubTo_staff_table.objects.get(id=id).delete()
        return redirect('/myapp/view_staff_assign/')



  # ========================= staff ==========================

  def staff_home(request):
        return render(request,'staff_module/staff_home.html')

  def add_video(request,id):
        request.session['sub_id']=id
        return render(request,'staff_module/add_video.html')

  def add_video_post(request):
        title=request.POST['title']
        details=request.POST['details']
        video=request.FILES['video']
        obj=notes_table()
      obj.LOGIN=User.objects.get(id=request.user.id)
         obj.title=title
         obj.details=details
         obj.video=video
      obj.SUBJECT_id=request.session['sub_id']
         obj.save()
         k=request.session['vid']
         return redirect(f'/myapp/view_video/{k}')


  #
  #
  # def view_allocated_exam(request):
  #
obj=labsubTo_staff_table.objects.get(STAFF__LOGIN_id=request.user.id).LABSUBJECT.id
  # a=exam_table.objects.filter(SUBJECT_id=obj)
  #      return render(request,'staff_module/view_allocated_exam.html',{'data':a})

  def view_allocated_exam(request):
         lab_staff_qs = labsubTo_staff_table.objects.filter(
      STAFF__LOGIN_id=request.user.id
         )

         if not lab_staff_qs.exists():
      return render(
        request,
           'staff_module/view_allocated_exam.html',
        {
                  'data': [],
                  'error': 'No subject allocated to this staff'
        }
      )

         subject_ids = lab_staff_qs.values_list(
      'LABSUBJECT_id', flat=True
         )

         exams = exam_table.objects.filter(
      SUBJECT_id__in=subject_ids
         )

         return render(
      request,
       'staff_module/view_allocated_exam.html',
      {'data': exams}
         )
    def view_allocated_subject(request):
      obj=labsubTo_staff_table.objects.filter(STAFF__LOGIN_id=request.user.id)
          return render(request,'staff_module/view_allocated_subject.html',{'data':obj})


    def view_timetable(request):
          return render(request,'staff_module/view_timetable.html')

    def view_video(request,id):
      res=notes_table.objects.filter(SUBJECT_id=id)
          request.session['vid']=id
          return render(request,'staff_module/view_video.html',{'data':res})

    def edit_video(request,id):
          request.session['subid']=id
          res=notes_table.objects.get(id=id)
          return render(request,'staff_module/edit_video.html',{'data':res})


    def edit_video_post(request):
          title=request.POST['title']
          details=request.POST['details']
      obj=notes_table.objects.get(id=request.session['subid'])
          if 'video' in request.FILES:
       video = request.FILES['video']
       obj.video = video
       obj.save()
      obj.LOGIN=User.objects.get(id=request.user.id)
          obj.title=title
          obj.details=details
      obj.SUBJECT_id=request.session['sub_id']
          obj.save()
          k=request.session['vid']
          return redirect(f'/myapp/view_video/{k}')

    def delete_video(request,id):
      notes_table.objects.get(id=id).delete()
          k = request.session['vid']
          return redirect(f'/myapp/view_video/{k}')



    def view_complaint(request):
      res=complaint_table.objects.filter(STAFF__LOGIN_id=request.user.id)
          return render(request,'staff_module/view_complaint.html',{'data':res})

    def send_reply(request,id):
           request.session['sid']=id
           return render(request,'staff_module/send reply.html')

    def send_reply_post(request):
          reply=request.POST['reply']
      obj=complaint_table.objects.get(id=request.session['sid'])
          obj.reply=reply
          obj.save()
          return redirect('/myapp/view_complaint/')

    #
    # def staff_view_student(request):
    #     # lab_staff_qs = labsubTo_staff_table.objects.filter(
    #     #      STAFF__LOGIN_id=request.user.id
    #     # )
    #
    #     # lab_staff_qs=staff_table.objects.filter(LOGIN_id=request.user.id)
    #
    #     # print(lab_staff_qs,'aaaaaaa')
    #     #
    #     course_ids = staff_table.objects.filter(
    #  'DEPARTMENT__COURSE_id', flat=True
    #     )
    #
    #     res = student_table.objects.filter(COURSE_id__in=course_ids)
    #
    #     return render(
    #  request,
    #      'staff_module/staff_view_student.html',
    #  {'data': res}
    #     )

    def staff_view_student(request):

           # Get logged-in staff
           staff = staff_table.objects.get(LOGIN=request.user)

           # Get courses under same department
           course_ids = course_table.objects.filter(
           DEPARTMENT=staff.DEPARTMENT
           ).values_list('id', flat=True)

           # Get students of those courses
           res = student_table.objects.filter(
           COURSE_id__in=course_ids
           )
          return render(
          request,
        'staff_module/staff_view_student.html',
       {'data': res}
          )

    def view_allocated_std_to_system(request):

           lab_staff_qs = labsubTo_staff_table.objects.filter(
           STAFF__LOGIN_id=request.user.id
           )

           course_ids = lab_staff_qs.values_list(
           'LABSUBJECT__COURSE_id', flat=True
           )

           res = student_table.objects.filter(COURSE_id__in=course_ids)

              ✅

           #     FIX HERE
           stf = systemTo_student_table.objects.filter(STUDENT__in=res)

          return render(
       request,
        'staff_module/viewstudent_assignsystem.html',
       {'data': stf}
          )






    def add_labwork(request,id):
          request.session['subject_id']=id
          return render(request,'staff_module/add_work.html')

    def add_labwork_post(request):
          title=request.POST['title']
          details=request.POST['details']
          deadline=request.POST['deadline']
          obj=Assign_lab_work()
      obj.LABSTAFF_id=request.session['subject_id']
          obj.worktitle=title
          obj.details=details
          obj.deadline=deadline
          obj.enterdate=datetime.now().date()
          obj.status='pending'
         obj.save()
         return redirect('/myapp/view_allocated_subject/')


    def view_labwork(request,id):
          res=Assign_lab_work.objects.filter(LABSTAFF_id=id)
          request.session['labid']=id
          return render(request,'staff_module/view_labwork.html',{'data':res})

    def delete_labwork(request,id):
      Assign_lab_work.objects.get(id=id).delete()
          k = request.session['labid']
          return redirect(f'/myapp/view_labwork/{k}')


    def view_student_work(request,id):
      res=Upload_lab_work.objects.filter(ASSIGNLABWORK_id=id)
          request.session['k']=id
          return render(request,'staff_module/view upload work.html',{'data':res})


    def verified_status(request,id):
          request.session['sid'] = id
          return render(request,'staff_module/send_status.html')

    def verified_status_post(request):
          status=request.POST['status']
      Upload_lab_work.objects.filter(id=request.session['sid']).update(status=status)
          k=request.session['k']
          return redirect(f'/myapp/view_student_work/{k}')


    def chat(request,id):
          request.session["userid"] = id
          cid = str(request.session["userid"])
          request.session["new"] = cid
          qry = student_table.objects.get(LOGIN=cid)
      photo=request.build_absolute_uri(qry.photo.url)if qry.photo else ""

        return render(request, "staff_module/Chat.html", {'photo': photo, 'name': qry.fname,
'toid': cid})

  def chat_view(request):
        fromid = request.user.id
        toid = request.session["userid"]
        qry = student_table.objects.get(LOGIN=request.session["userid"])
        from django.db.models import Q
        res = chat_table.objects.filter(Q(FROM_id=fromid,TO_id=toid) | Q(FROM_id=toid,
TO_id=fromid)).order_by('id')
        l = []

    photo=request.build_absolute_uri(qry.photo.url)if qry.photo else ""

        for i in res:
     l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from":
i.FROM_id})

        return JsonResponse({'photo': photo, "data": l, 'name': qry.fname, 'toid':
request.session["userid"]})

  def chat_send(request, msg):
        lid = request.user.id
        toid = request.session["userid"]
        message = msg

        import datetime
        d = datetime.datetime.now().date()
        chatobt = chat_table()
        chatobt.message = message
        chatobt.TO_id = toid
        chatobt.FROM_id = lid
        chatobt.date = d
        chatobt.save()

        return JsonResponse({"status": "ok"})

  # ========================= lab assistant ==========================



  def labassistant_home(request):
        return render(request,'labassistant_module/labassistant_home.html')

  def add_systemdetails(request):
        return render(request,'labassistant_module/add_systemdetails.html')

  def add_systemdetails_post(request):
        RAM=request.POST['RAM']
        HDD=request.POST['HDD']
        processor=request.POST['processor']
        SSD = request.POST['SSD']
        system = request.POST['system']
         ab=system_table()
         ab.RAM=RAM
         ab.HDD=HDD
         ab.SystemNumber=system
         ab.processor=processor
         ab.SSD=SSD
         ab.date=datetime.now().today()
      ab.LAB_ASSISTANT=labassistant_table.objects.get(LOGIN_id=request.user.id)
         ab.save()
         return redirect('/myapp/view_systemdetails/')

    def view_systemdetails(request):
      res=system_table.objects.filter(LAB_ASSISTANT__LOGIN_id=request.user.id)
          return render(request, 'labassistant_module/view_systemdetails.html', {"data": res})

    def delete_system(request,id):
      system_table.objects.get(id=id).delete()
          return redirect('/myapp/view_systemdetails/')


  def assign_system(request):
        sys=system_table.objects.all()
        lab_staff_qs = subjectTo_lab_table.objects.filter(
       LABASSISTANT__LOGIN_id=request.user.id)
        print(lab_staff_qs,'lllllllllll')
        course_ids = lab_staff_qs.values_list(
     'LABSUBJECT__COURSE_id', flat=True)
        print(course_ids,'ccccccccccccc')
        res = student_table.objects.filter(COURSE_id__in=course_ids)
        print(res,'sssssssss')
        return
render(request,'labassistant_module/assign_system.html',{'system':sys,'student':res})

  def assign_system_post(request):
        system=request.POST['system']
        student=request.POST['student']
        obj=systemTo_student_table()
        obj.date=datetime.now().today()
        obj.STUDENT_id=student
        obj.SYSTEM_id=system
        obj.save()
        return redirect('/myapp/viewstudent_assignsystem/')
    def manage_system(request):
      res=system_table.objects.filter(LAB_ASSISTANT__LOGIN_id=request.user.id)
         return render(request,'labassistant_module/manage_system.html',{'data':res})

    def view_assigned_subject(request):
      res=subjectTo_lab_table.objects.filter(LABASSISTANT__LOGIN_id=request.user.id)
          return render(request,'labassistant_module/view_assigned_subject.html',{'data':res})

    def view_exam(request):

res=subjectTo_lab_table.objects.get(LABASSISTANT__LOGIN_id=request.user.id).LABSUB
JECT.id
    ex=exam_table.objects.filter(SUBJECT_id=res)
        return render(request,'labassistant_module/view_exam.html',{'data':ex})

  def lab_view_timetable(request):
        return render(request,'labassistant_module/view_timetable.html')

  def viewstudent_assignssystem(request):

obj=systemTo_student_table.objects.filter(SYSTEM__LAB_ASSISTANT__LOGIN_id=reques
t.user.id)
        return render(request,'labassistant_module/viewstudent_assignsystem.html',{'data':obj})
  def delete_assign_system(request,id):
    systemTo_student_table.objects.get(id=id).delete()
        return redirect('/myapp/viewstudent_assignsystem/')






  ########################3student



  def android_login(request):
        username=request.POST['username']
        password=request.POST['password']
    user=authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
       print("==================")
     if user.groups.filter(name="Student").exists():
        print(user,"]]]]]]]]]]]]]]")
        return JsonResponse({'status':'ok','lid':str(user.id),'type':'Student'})
         else:
           print("............")
         return JsonResponse({'status':'Not ok'})
         else:
       return JsonResponse({'status': 'Not ok'})

    def view_lab_subject(request):
          l=[]
          lid=request.POST['lid']
      obst=student_table.objects.get(LOGIN__id=lid)
      var=labsubject_table.objects.filter(COURSE__id= obst.COURSE.id)
          for i in var:
       l.append({
          'id':i.id,
          'course':str(i.COURSE.details),
          'Subject':str(i.subject),
          'Syllabus': request.build_absolute_uri(i.syllabus.url)if i.syllabus else""


           })
           return JsonResponse({'status':'ok','data':l})



    def view_notes_student(request):
          l=[]
          sid=request.POST['sid']
      var=notes_table.objects.filter(SUBJECT_id= sid)
          for i in var:
       l.append({
          'id':i.id,
          'title':str(i.title),
          'details':str(i.details),
          'video': request.build_absolute_uri(i.video.url)if i.video else""


           })
           return JsonResponse({'status':'ok','data':l})


    def view_allocated_system(request):
          l=[]
          lid=request.POST['lid']
      var=systemTo_student_table.objects.filter(STUDENT__LOGIN_id=lid)
          for i in var:
       l.append({
             'id': i.id,
             'SystemNumber': str(i.SYSTEM.SystemNumber),
             'Processor': str(i.SYSTEM.processor),
             'Ram': str(i.SYSTEM.RAM),
             'HDD': str(i.SYSTEM.HDD),
             'SSD': str(i.SYSTEM.SSD),
             'lab': str(i.SYSTEM.LAB_ASSISTANT.LAB.lab_no),
             'Date':str( i.date),

            })
            return JsonResponse({'status': 'ok', 'data': l})


    def view_reply(request):
          lid=request.POST['lid']
          l = []
          var = complaint_table.objects.filter(STUDENT__LOGIN_id=lid)
          for i in var:
       l.append({
          'Staff': i.STAFF.name,
          'complaint': i.complaint,
          'Date': str(i.date),
          'Reply': str(i.reply),
          'id': str(i.id),
       })
          return JsonResponse({'status': 'ok', 'data': l})



    def user_view_exam(request):
          lid = request.POST['lid']
          l = []
          obst = student_table.objects.get(LOGIN__id=lid)
          var = exam_table.objects.filter(
       SUBJECT__COURSE=obst.COURSE
          )
          for i in var:
       l.append({
          'Subject': i.SUBJECT.subject,
          'Exam_name': i.exam_name,
          'Date': i.date,
          'From_time': i.fromtime,
          'To_time': i.totime,
          'Duration': i.duration,
          'Total_mark': i.totalmark,
       })
           return JsonResponse({'status': 'ok', 'data': l})

    def user_view_staff(request):
          lid = request.POST['lid']
          obst = student_table.objects.get(LOGIN__id=lid)
          var = staff_table.objects.filter(
       DEPARTMENT=obst.COURSE.DEPARTMENT
          )

           l = []
           for i in var:
         l.append({
           'id': i.id,
           'LOGIN': str(i.LOGIN.id),
           'Name': i.name,
           'Gender': i.gender,
           'Place': i.place,
           'Pin': i.pin,
           'Post': i.post,
           'Phone': i.phone,
           'Email': i.email,
           'Qualification': i.qualification,
           'Program_language': i.program_language,
           'Photo': request.build_absolute_uri(i.photo.url) if i.photo else "",
           'Course': i.DEPARTMENT.dept_name,
         })

           return JsonResponse({'status': 'ok', 'data': l})



    def user_sent_complaint(request):
          lid=request.POST['lid']
          sid=request.POST['sid']
          complaint=request.POST['complaint']
          var=complaint_table()
      var.STAFF=staff_table.objects.get(id=sid)
      var.STUDENT=student_table.objects.get(LOGIN_id=lid)
          var.complaint=complaint
      var.date=datetime.now().today().date()
          var.reply='pending'
          var.save()
          return JsonResponse({'status': 'ok', })



    def user_send_feedback(request):
            lid=request.POST['lid']
            sid=request.POST['sid']
            feedback=request.POST['feedback']
            rating=request.POST['rating']
            var=feedback_table()
            var.STUDENT=student_table.objects.get(LOGIN_id=lid)
        var.STAFF=staff_table.objects.get(id=sid)
        var.date=datetime.now().today().date()
            var.feedback=feedback
            var.rating=rating
            var.save()
            return JsonResponse({'task': 'ok'})

    from django.db.models import Q

  def user_viewchat(request):
        fromid = request.POST["from_id"]
        toid = request.POST["to_id"]
        # lmid = request.POST["lastmsgid"] from django.db.models import Q
        res = chat_table.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid,
TO_id=fromid)).order_by("id")
        l = []
        for i in res:
     l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to":
i.TO_id})
        return JsonResponse({"status":"ok",'data':l})


  def user_sendchat(request):
        FROM_id=request.POST['from_id']
        TOID_id=request.POST['to_id']
        print(FROM_id)
        print(TOID_id)
        msg=request.POST['message']
        from datetime import datetime
        c=chat_table()
        c.FROM_id=FROM_id
        c.TO_id=TOID_id
        c.message=msg
        c.date=datetime.now()
        c.save()
        return JsonResponse({'status':"ok"})
    def user_view_lab_work(request):
          lid = request.POST['lid']
          l = []
          obst = student_table.objects.get(LOGIN__id=lid)
          var = Assign_lab_work.objects.filter(
         LABSTAFF__LABSUBJECT__COURSE=obst.COURSE
          )
          for i in var:
       l.append({
          'Subject': i.LABSTAFF.LABSUBJECT.subject,
          'enterdate': i.enterdate,
          'deadline': i.deadline,
          'worktitle': i.worktitle,
          'details': i.details,
          'workstatus': i.status,
          'id': i.id,
       })

         return JsonResponse({'status': 'ok', 'data': l})


    def upload_work_result(request):
          file=request.FILES['file']
          aid=request.POST['aid']
          lid=request.POST['lid']
          obj=Upload_lab_work()
          obj.enterdate=datetime.now().date()
          obj.status="Completed"
          obj.upload=file
      obj.STUDENT=student_table.objects.get(LOGIN=lid)
          obj.ASSIGNLABWORK_id=aid
          obj.save()
          return JsonResponse({'status':'ok'})



    def user_view_lab_work_status(request):
          lid = request.POST['lid']
          l = []
          obst = Upload_lab_work.objects.filter(STUDENT__LOGIN__id=lid)
          for i in obst:
         upload=request.build_absolute_uri(i.upload.url)if i.upload else ""
       l.append({
          'Subject': i.ASSIGNLABWORK.LABSTAFF.LABSUBJECT.subject,
          'enterdate': i.enterdate,
          'deadline': i.ASSIGNLABWORK.deadline,
          'worktitle': i.ASSIGNLABWORK.worktitle,
           'details': i.ASSIGNLABWORK.details,
           'workstatus': i.status,
           'upload': upload,
           'id': i.id,
         })

          return JsonResponse({'status': 'ok', 'data': l})









    #############################################MAIN Function




    def monitor_function(request,id):
         request.session['sid']=id
         return render(request,"Staff_module/monitor.html")

    def shutdown(request):
          id=request.session['sid']
          ob=command_table()
      ob.SYSTEM=system_table.objects.get(id=id)
          ob.process="sd"
          ob.save()
          return render(request,"Staff_module/monitor.html")

    def restart(request):
          id=request.session['sid']
          ob=command_table()
      ob.SYSTEM=system_table.objects.get(id=id)
          ob.process="rs"
          ob.save()
          return render(request,"Staff_module/monitor.html")

    def Screenshot(request):
          id=request.session['sid']
          ob=command_table()
      ob.SYSTEM=system_table.objects.get(id=id)
          ob.process="sc"
          ob.save()
         return redirect("/myapp/viewScreenshot/")

    def background_process(request):
      id=request.session['sid']
          ob=command_table()
      ob.SYSTEM=system_table.objects.get(id=id)
          ob.process="bgp"
          ob.save()
          return redirect("/myapp/viewprocess/")

    def viewScreenshot(request):
          id=request.session['sid']
      ob=screenshot_table.objects.filter(SYSTEM__id=id).order_by("-id")
          return render(request,"Staff_module/detailed view.html",{"data":ob})


    def delect_sc(request,id):
      screenshot_table.objects.get(id=id).delete()
          return redirect('/myapp/viewScreenshot/')

    def viewprocess(request):
          id=request.session['sid']
      ob=process_table.objects.filter(SYSTEM__id=id).order_by("-id")
          return render(request,"Staff_module/kill.html",{"data":ob})

    def kill_pro(request,id,pr):
           ob = command_table()
           ob.SYSTEM = system_table.objects.get(id=id)
           ob.process = pr
           ob.save()
           return redirect("/myapp/viewprocess/")

    def processs(request):
          path = request.GET["p"]
          result = command_table.objects.filter(SYSTEM__id=path)
          res = "#".join([item.process for item in result])

      command_table.objects.filter(SYSTEM__id=path).delete()
        return HttpResponse(res)

    def upf(request):
          print(request.POST)
          print(request.FILES)

         file = request.FILES.get("file")
         name = request.POST.get("name")
           if not file or not name:
           return HttpResponse("missing file or name", status=400)

           # Force save into media/screenshots/
           screenshots_dir = os.path.join(settings.MEDIA_ROOT, "screenshots")
           os.makedirs(screenshots_dir, exist_ok=True)

           fs = FileSystemStorage(location=screenshots_dir)
           filename = fs.save(name, file)

           print("Saved file:", filename)
           return HttpResponse("ok")

    def up(request):
          sc = request.GET.get("sc")
          cp = request.GET.get("cp")
          id = request.GET.get("id")

           ob = screenshot_table()
           ob.SYSTEM = system_table.objects.get(id=id)

           # Save relative paths for FileField
           ob.screenshot = f"screenshots/{sc}"
           ob.campic = f"screenshots/{cp}"

           ob.status = 'pending'
           ob.date=datetime.now().today()
           ob.save()

           return HttpResponse("ok")



  def insprocess(request):
        lis = ['System Idle Process', 'System', 'Registry', 'smss.exe', 'wininit.exe', 'services.exe',
'lsass.exe', 'wsc_proxy.exe', 'Memory Compression', 'igfxCUIService.exe', 'AvastSvc.exe',
'aswToolsSvc.exe', 'dasHost.exe', 'spoolsv.exe', 'IntelCpHDCPSvc.exe', 'novapdfs.exe',
'SecurityHealthService.exe']
        sid = request.GET["p"]
        pr = request.GET["pr"]

        if pr not in lis:
       process_table.objects.filter(SYSTEM__id=sid, process=pr).delete()
     # Process.objects.create(sid=sid, process=pr)
     ob=process_table()
       ob.SYSTEM=system_table.objects.get(id=sid)
     ob.process=pr
           ob.save()
           return HttpResponse("ok")
           return HttpResponse("ok")




    def update_pass(request):
         id=8
         ob=User.objects.get(id=id)
      ob.password=make_password("lab")
         ob.save()
         return HttpResponse("ok")








    ##############################################

    @login_required(login_url='/myapp/')
    def view_lab(request):
          ob=labassistant_table.objects.all()
          return render(request,"Staff_module/staff_view_lab.html",{"data":ob})


    @login_required(login_url='/myapp/login_get/')
    def view_system(request,id):
          request.session['sid']=id
      ob=system_table.objects.filter(LAB_ASSISTANT__id=id)
          for i in ob:
         obb=systemTo_student_table.objects.filter(SYSTEM__id=i.id).order_by("-id")
       if len(obb)==0:
          i.st="na"
       else:
          i.st=obb[0].STUDENT.fname
          return render(request,"Staff_module/staff_view_system.html",{"data":ob})



    def flutter_change_password(request):
          if request.method == "POST":
       old_password = request.POST.get("current_password")
       new_password = request.POST.get("new_password")
           lid = request.POST.get("lid")

           try:
           user = User.objects.get(id=lid)
         except User.DoesNotExist:
           return JsonResponse({'status': 'invalid_user'})

           if user.check_password(old_password):
           user.set_password(new_password)
           user.save()
           return JsonResponse({'status': 'ok'})
         else:
           return JsonResponse({'status': 'wrong_password'})


    def student_view_profile(request):
          lid = request.POST['lid']

           a = student_table.objects.get(LOGIN__id=lid)

           return JsonResponse({
           'status': 'ok',
           'Fname': a.fname,
           'Course': a.COURSE.coursename,
           'Semester': a.semester,
           'Gender': a.gender,
           'Dob': a.dob,
           'Place': a.place,
           'Pin': a.pin,
           'Post': a.post,
           'Phone': a.phone,
           'Email': a.email,
           'Photo': request.build_absolute_uri(a.photo.url) if a.photo else ""
           })
