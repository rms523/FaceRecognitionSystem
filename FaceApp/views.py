from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from deepface import DeepFace
import Dashboard
from django.conf import settings
import os
import math
from Dashboard import helper

def processImage(request, imagesavepath, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))
    # result = DeepFace.verify("C:\\Users\\machina\\Pictures\\Camera Roll\\Rahul1.jpg", "C:\\Users\\machina\\Pictures\\Camera Roll\\Rahul2.jpg")
    # print (result['verified'])
    # print(imgsavepath)
    if request.method == "POST":
        # missing person info
        userimagepath = Dashboard.views.upload(request, fileinput='fileinput1')

        if Dashboard.views.connection.is_connected():
            cursor = Dashboard.views.connection.cursor()
            query = "select guardian_email from missing_person_info where " + \
                    "identifier=%s and account_email='%s'" % (user_id, request.user.username)

            Dashboard.views.log(query)
            cursor.execute(query)
            result = cursor.fetchall()
            Dashboard.views.connection.commit()
            guardian_email = result[0][0]
            print (guardian_email)


        print(settings.MEDIA_ROOT)
        print(imagesavepath)
        print(userimagepath)
        imagesavepath = imagesavepath.replace('/media', '').replace('/', '\\')
        userimagepath = userimagepath.replace('/media', '').replace('/', '\\')
        # imagesavepath = os.path.join(settings.MEDIA_ROOT, imagesavepath.replace('/media', '').replace('/', '\\'))
        # userimagepath = os.path.join(settings.MEDIA_ROOT, userimagepath.replace('/media', '').replace('/', '\\'))
        imagesavepath = settings.MEDIA_ROOT + imagesavepath
        userimagepath = settings.MEDIA_ROOT + userimagepath
        print(imagesavepath)
        print(userimagepath)
        try:
            result = DeepFace.verify(imagesavepath, userimagepath)
        except Exception as e:
            print(str(e))
            print("Print Something went wrong. Please try again")
            next = request.POST.get('next', '/')
            request.session['error'] = 'Something went wrong. Please try again'
            request.session['no_match'] = True
            request.session['is_found'] = False
            request.session.modified = True
            return HttpResponseRedirect(next)

        threshold_value = 0.14
        observed_value = result['distance']
        print("observed value is %f" % observed_value)
        if result['verified'] and observed_value < threshold_value:
            print("Person Image is matched.")
            print(result)
            Dashboard.views.update_person_missing_status(request, user_id)
            next = request.POST.get('next', '/')
            request.session['error'] = ''
            request.session['no_match'] = False
            request.session['is_found'] = True
            request.session.modified = True

            # person was found , so send the email
            helper.send_notification(guardian_email)

            account_email = request.user.username
            # for updating the chart
            if Dashboard.views.connection.is_connected():
                # for generating dashboard image

                cursor = Dashboard.views.connection.cursor()
                query = "select is_found from missing_person_info where " + \
                        "account_email='%s'" % account_email

                print(query)
                cursor.execute(query)
                result = cursor.fetchall()
                Dashboard.views.connection.commit()

                print("adding user result: ")
                print(result)
                # count the number of missing and found person
                missing_count = 0
                found_count = 0
                for status in result:
                    if status[0] == 1:
                        found_count = found_count + 1
                    if status[0] == 0:
                        missing_count = missing_count + 1

                save_path = os.path.join(settings.MEDIA_ROOT, request.user.username)
                save_path = save_path + '.png'
                helper.get_chart([missing_count, found_count], save_path)

                print(save_path)


            return HttpResponseRedirect(next)

        else:
            print("Not matched.")
            print(result)
            next = request.POST.get('next', '/')
            request.session['error'] = ''
            request.session['no_match'] = True
            request.session['is_found'] = False
            request.session.modified = True
            return HttpResponseRedirect(next)

        print(result)

    return redirect('Dashboard:view_info', user_id=user_id)


def webStream(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))
    db_path = os.path.join(settings.MEDIA_ROOT, 'database')
    DeepFace.stream(
        db_path=db_path)  # , model_name="VGG-Face")
    return render(request, 'Dashboard/index.html')
